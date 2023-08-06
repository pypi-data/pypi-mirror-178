from __future__ import annotations

import base64
import functools
import itertools
import os
import typing as t
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import pyqtgraph as pg
import torch
from PIL import Image
from pyqtgraph.Qt import QtCore
from qtextras import (
    OptionsDict,
    ParameterContainer,
    ParameterEditor,
    RunOptions,
    bindInteractorOptions as bind,
    fns,
    widgets,
)
from scipy import stats
from sklearn.cluster import DBSCAN, FeatureAgglomeration, KMeans, MeanShift

from gemovi.common.constants import get_device
from gemovi.common.utils import (
    pad_image_to_size,
    read_image_folder,
    tensor_to_np,
    to_pil_image,
)
from gemovi.viz.preview import PreviewItemsMixin

if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab, ModelTab
    from gemovi.viz.vae import VAEEncoderTab

T = t.TypeVar("T")

device = get_device(1)


def _mkspec(typ: str = None, **opts):
    out = opts.copy()
    if typ is not None:
        out["type"] = typ
    return out


_colormap_spec = _mkspec("popuplineeditor", limits=fns.listAllPgColormaps())


@dataclass
class TooltipData:
    name: str = None
    label: str = None
    image_data: bytes | t.Any = None
    image_read_func: t.Callable[[t.Any], Image.Image] = to_pil_image

    def __str__(self):
        label_str = f"Label: {self.label}<br/>" if self.label else ""
        name_str = self.name or "<None>"
        html = (
            f'<div style="text-align:center">'
            f"Name: {name_str}<br/>"
            f"{label_str}"
            f"</div>"
        )
        if self.image_data is not None:
            img = self.image_data_to_b64().decode()
            html += f'<img src="data:image/png;base64,{img}"/>'
        return html

    def image_data_to_b64(self, size: int | tuple = 64):
        image_data = self.image_data
        if image_data is None or isinstance(image_data, bytes):
            # Already converted / doesn't exist, nothing to replace
            return image_data
        # Lazy evaluation in all other cases
        image_data = self.image_read_func(image_data)
        image_data = pad_image_to_size(image_data, size)
        buff = BytesIO()
        image_data.save(buff, format="jpeg", quality=80)
        image_bytes = base64.b64encode(buff.getvalue())
        self.image_data = image_bytes
        return image_bytes


class PopoutImageTargetItem(pg.TargetItem):
    default_image_size = np.array([128, 128])

    def __init__(self, image=None, name=None, sample_index: int = None):
        self.default_label_opts = dict(anchor=(0.5, 1.25), offset=(0, 0))
        super().__init__(label=name, labelOpts=self.default_label_opts)
        self.image_item = pg.ImageItem(image)
        self.image_item.setParentItem(self)
        self.sample_index = sample_index

    def boundingRect(self):
        return super().boundingRect().united(self.image_item.boundingRect())

    def set_name(self, name):
        self.setLabel(name, labelOpts=self.default_label_opts)

    def set_image(self, image, image_size=None):
        img = self.image_item
        if image_size is None:
            image_size = self.default_image_size
        img.setImage(image, rect=(*img.pos(), *(image_size * self.pixelSize())))


class TabPlugin:
    name: str | None = None

    def __init__(self, tab: ModelTab):
        if self.name is None:
            self.name = fns.nameFormatter(self.__class__.__name__.replace("Plugin", ""))
        self.tab = tab

    def register_functions(self, editor: ParameterEditor):
        ...


class GenerativeTabPlugin(TabPlugin):
    tab: GenerativeTab

    def register_item(self, item: T, hide=False) -> T:
        self.tab.plot_widget.addItem(item)
        if hide:
            item.hide()
        return item


class GenerativeEncoderTabPlugin(GenerativeTabPlugin):
    tab: t.Any


class ImageFilledROI(QtCore.QObject):
    sig_image_positions_changed = QtCore.Signal()

    def __init__(self, plot_widget: pg.PlotWidget):
        super().__init__()
        self.plot_widget = plot_widget
        self.roi = self._make_rect_roi()
        self.image_items: list[pg.ImageItem] = []
        self.spacing = (0, 0)
        self._region_change_approximate_n_samples = 0

    def _make_rect_roi(self):
        roi = pg.RectROI((0, 0), (3, 3), pen="k")
        self.plot_widget.addItem(roi)
        roi.setZValue(11)
        while roi.getHandles():
            roi.removeHandle(0)
        # Add abundance of handles on all sides
        for handle_x, handle_y in itertools.product(*[[0, 0.5, 1]] * 2):
            if handle_x == handle_y == 0.5:
                continue
            roi.addScaleHandle([handle_x, handle_y], [1 - handle_x, 1 - handle_y])
        return roi

    def hide(self):
        self.roi.hide()
        for item in self.image_items:
            item.hide()

    def show(self):
        self.roi.show()
        for item in self.image_items:
            item.show()

    def ensure_n_image_items(self, n_items: int):
        while len(self.image_items) > n_items:
            self.plot_widget.removeItem(self.image_items.pop())

        while 0 <= len(self.image_items) < n_items:
            img_item = pg.ImageItem()
            self.plot_widget.addItem(img_item)
            img_item.setZValue(0)
            self.image_items.append(img_item)

    def get_image_items(self, approximate_n_samples: int, return_spacing=False):
        roi = self.roi
        grid_x, grid_y = self.rect_to_grid(
            roi.pos(), roi.size(), approximate_n_samples - 1
        )
        if grid_x.shape[0] <= 1 or grid_x.shape[1] <= 1:
            return
        spacing = (grid_x[0, 1] - grid_x[0, 0], grid_y[1, 0] - grid_y[0, 0])
        grid_x = grid_x.ravel()
        grid_y = grid_y.ravel()

        self.ensure_n_image_items(grid_x.size)
        self.spacing = spacing

        for img_item, grid_pt in zip(
            self.image_items, np.column_stack((grid_x, grid_y))
        ):
            img_item.setPos(*grid_pt)

        if return_spacing:
            return self.image_items, spacing
        return self.image_items

    def set_image_data(self, image_data: t.Sequence[np.ndarray]):
        for img_item, img_data in zip(self.image_items, image_data):
            img_item.setImage(img_data, rect=(0, 0, *self.spacing))

    @staticmethod
    def rect_to_grid(
        top_left_xy: t.Sequence, width_height: np.ndarray, n_samples: int
    ) -> np.ndarray:
        """
        Uniformly fill a rect with approximate_n_samples

        Solve the system of equations:

        * nx * ny = approximate_n_samples
        * x spacing = width / nx
        * y spacing = height / ny
        * x spacing = y spacing

        -> nx = approximate_n_samples * sqrt(width / (height * approximate_n_samples))
        -> ny = sqrt(approximate_n_samples * height / width)
        """
        if n_samples < 1:
            return np.mgrid[0:0, 0:0]
        nx = n_samples * np.sqrt(width_height[0] / (width_height[1] * n_samples))
        ny = np.sqrt(n_samples * width_height[1] / width_height[0])
        bottom_right_xy = np.array(top_left_xy) + width_height
        grid = np.meshgrid(
            np.arange(top_left_xy[0], bottom_right_xy[0], width_height[0] / nx),
            np.arange(top_left_xy[1], bottom_right_xy[1], width_height[1] / ny),
        )
        return grid

    def change_images_with_roi(self, update_on_changing=True, approximate_n_samples=0):
        signals = [
            self.roi.sigRegionChanged,
            self.roi.sigRegionChangeFinished,
        ]
        for signal in signals:
            pg.disconnect(signal, self.on_region_changed_while_listening)
        connect_idx = 0 if update_on_changing else 1
        signals[connect_idx].connect(self.on_region_changed_while_listening)
        self._region_change_approximate_n_samples = approximate_n_samples
        self.on_region_changed_while_listening()

    def on_region_changed_while_listening(self):
        self.get_image_items(self._region_change_approximate_n_samples)
        self.sig_image_positions_changed.emit()


class GridDecoderPlugin(GenerativeTabPlugin):
    name = "ROI Decoder"

    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.plot_widget = tab.plot_widget
        tab.sig_samples_selected.connect(self.on_samples_selected)

        tab.register_selection_listener(
            self.grid_decode_selection_listener, enabled=False
        )

        self.image_tiled_roi = ImageFilledROI(tab.plot_widget)
        self.image_tiled_roi.sig_image_positions_changed.connect(
            self.update_decoding_roi_contents
        )
        self.roi = self.image_tiled_roi.roi
        self.roi.hide()
        self._last_selected_index = 0

    def on_samples_selected(self, sample_indexes: list[int]):
        if len(sample_indexes):
            self._last_selected_index = sample_indexes[0]

    def grid_decode_selection_listener(self, sample_indexes: list[int]):
        if len(sample_indexes):
            self.roi_decoding_proc()
        else:
            self.image_tiled_roi.hide()

    @bind(sample_idx=dict(ignore=True))
    def grid_decode_sample(
        self, sample_index: int | None = None, n_samples=50, update_on_changing=True
    ):
        """
        Decode the selected sample and a surrounding grid of points.

        The grid is filled with approximately ``n_samples`` points and spaced
        in proportion to how the rectangular ROI is scaled.

        Parameters
        ----------
        sample_index
            The index of the sample to decode. If None, the last selected sample
            is used.
        n_samples
            The approximate number of samples to decode. The actual number of samples
            may be slightly different to ensure the grid is totally filled.
        update_on_changing
            If ``True``, the decoding will be updated as the ROI is moved or resized.
            Otherwise, the decoding will only be updated when the ROI is released.
        """
        if sample_index is None:
            sample_index = self._last_selected_index
        if sample_index is None:
            self.image_tiled_roi.hide()
            return

        n_samples = max(n_samples, 0)
        self.image_tiled_roi.change_images_with_roi(update_on_changing, n_samples)
        if n_samples <= 0:
            self.image_tiled_roi.hide()
            return

        self.image_tiled_roi.show()
        xformed_xy = tensor_to_np(
            self.get_transformed_sample_index(flatten=True, xy_dims_only=True)
        )
        roi_size = np.array(self.roi.size())
        new_roi_pos = xformed_xy - roi_size / 2
        self.roi.setPos(new_roi_pos)

    def get_transformed_sample_index(self, flatten=False, xy_dims_only=False):
        sample_idx = self._last_selected_index
        decoded = self.tab.get_transformed_samples([sample_idx])
        if xy_dims_only:
            decoded = decoded[:, [self.tab.xdim, self.tab.ydim]]
        if flatten:
            decoded = decoded[0]
        return decoded

    def update_decoding_roi_contents(self):
        if not self.roi.isVisible():
            return
        items = self.image_tiled_roi.image_items
        xformed = (
            self.get_transformed_sample_index().broadcast_to(len(items), -1).clone()
        )
        positions = torch.tensor(
            np.row_stack([item.pos() for item in items]), dtype=xformed.dtype
        )
        xformed[:, self.tab.xdim] = positions[:, 0]
        xformed[:, self.tab.ydim] = positions[:, 1]
        samples = self.tab.dim_tformer.inverse_transform(xformed).type_as(
            self.tab.samples
        )
        pred = self.tab.forward(samples)
        pred_imgs = tensor_to_np(pred).transpose((0, 2, 3, 1))
        self.image_tiled_roi.set_image_data(pred_imgs)

    def register_functions(self, editor: ParameterEditor):
        self.roi_decoding_proc = editor.registerFunction(self.grid_decode_sample)


class ScatterplotPlugin(GenerativeTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.scatterplot = self.register_item(
            pg.ScatterPlotItem(brush=None, pen="w", hoverable=True, tip=None)
        )
        self.scatterplot_properties = ParameterContainer()
        self.colormap = pg.colormap.get("plasma")

        def toggle_scatterplot():
            self.scatterplot.setVisible(not self.scatterplot.isVisible())

        self.tab.menu.addAction("Toggle Scatterplot Visible", toggle_scatterplot)
        for signal in tab.sig_samples_changed, tab.sig_transformer_changed:
            signal.connect(self.on_samples_or_transformer_changed)

        self.scatterplot.sigHovered.connect(self.on_scatter_hover)
        self.scatterplot.sigClicked.connect(self.on_scatter_click)

    def on_samples_or_transformer_changed(self):
        self.plot_samples()

    def plot_samples(self):
        def img_getter(idx: int):
            info = self.tab.samples_info
            if info.image_files and info.image_files[idx]:
                image = info.image_files[idx]
            else:
                image = self.tab.forward(self.tab.samples[idx].unsqueeze(0))[0]
            return to_pil_image(image)

        user_data = [
            TooltipData(name=f"Sample {ii}", image_data=ii, image_read_func=img_getter)
            for ii in range(self.tab.samples.shape[0])
        ]
        tformed = tensor_to_np(self.tab.get_transformed_samples())
        brushes = None
        if self.tab.samples_info.numeric_labels is not None:
            brushes = self.colormap.map(self.tab.samples_info.numeric_labels)

        props = self.scatterplot_properties
        self.scatterplot.setData(
            tformed[:, self.tab.xdim],
            tformed[:, self.tab.ydim],
            data=user_data,
            brush=brushes,
            pen=props["pen"],
            pxMode=props["pixel_mode"],
            size=props["size"],
        )

    def on_scatter_hover(self, item, points, _evt):
        if not len(points):
            item.setToolTip(None)
            return
        tooltip: TooltipData = points[0].data()
        if tooltip.label is None:
            numeric_lbl = self.tab.numeric_labels[points[0].index()]
            tooltip.label = self.tab.samples_info.number_label_map[numeric_lbl]
        item.setToolTip(str(tooltip))

    def on_scatter_click(self, _item, points, _evt):
        indexes = [p.index() for p in points]
        self.tab.update_selected_samples(indexes)

    @bind(colormap=_colormap_spec, pen=_mkspec("pen"))
    def update_scatterplot_properties(
        self, colormap="plasma", pen="w", size=15.0, pixel_mode=True  # noqa
    ):
        self.colormap = fns.getAnyPgColormap(colormap, forceExist=True)
        # Properties are captured by `self.scatterplot_properties`, so no need
        # to do anything here other than set colormap and replot. Noqa above to avoid
        # unused argument warning.
        self.plot_samples()

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(
            self.update_scatterplot_properties,
            runOptions=RunOptions.ON_CHANGED,
            container=self.scatterplot_properties,
        )


class PerturbationPlugin(GenerativeTabPlugin):
    mapping_granularity = 0.05

    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.gaus_overlay_item = self.register_item(pg.ImageItem())
        self.gaus_overlay_item.setZValue(-10)
        self.gaus_overlay_item.setOpacity(0.75)
        self.gaus_overlay_item.setColorMap("viridis")
        self.create_uniform_map()

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.create_uniform_map)
        editor.registerFunction(self.create_perturbation_map)
        editor.registerFunction(
            self.update_overlay_properties, runOptions=RunOptions.ON_CHANGED
        )

    @bind(granularity=_mkspec("float", limits=(0.01, 0.5)), colormap=_colormap_spec)
    def update_overlay_properties(self, granularity=0.05, colormap="viridis"):
        """
        Parameters
        ----------
        granularity
            When creating perturbation maps, this is the granularity of the mapping,
            i.e., how much resolution should be applied when samplng points in the
            latent space. The lower the value, the higher the resolution, but the
            longer it will take to create the map.
        colormap
            The colormap to use for the perturbation map image
        """
        self.mapping_granularity = granularity
        self.gaus_overlay_item.setColorMap(colormap)

    def create_perturbation_map(self, n_samples=100, standard_deviations=3):
        """
        Creates a map of how strongly minor changes in the currently viewed dimensions
        affect the generated image.

        Parameters
        ----------
        n_samples
            Number of samples to use for each point in the map
        standard_deviations
            How many standard deviations to use for the gaussian perturbation
        """
        samples = (
            torch.rand(n_samples, self.tab.get_num_latent_dims(), device=device)
            * standard_deviations
            - standard_deviations / 2
        )
        base_pred = self.tab.forward(samples).detach()
        check_space = torch.linspace(
            -1, 1, int(1 / self.mapping_granularity), device=device
        )
        dy, dx = torch.meshgrid(check_space, check_space, indexing="ij")
        dx_vec = dx.reshape(-1)
        dy_vec = dy.reshape(-1)
        map_xy = np.arange(
            -standard_deviations, standard_deviations, self.mapping_granularity
        )
        out_map = np.zeros((len(map_xy), len(map_xy)), dtype=np.float32)
        for ii, sample in enumerate(samples):
            # TODO: Tile somehow to get shapes broadcastable without inplace update
            batch = sample.unsqueeze(0).expand(dx_vec.size(0), *sample.shape)
            # Clone for in-place operations
            batch = batch.clone()
            batch[:, self.tab.xdim] += dx_vec
            batch[:, self.tab.ydim] += dy_vec
            pred = self.tab.forward(batch).detach()
            ref = base_pred[ii]
            diff = torch.abs(pred - ref).view(len(dx_vec), -1).mean(dim=1).cpu().numpy()
            # Find out which output locations should be updated
            xy_batch = (
                batch[:, [self.tab.xdim, self.tab.ydim]].cpu().numpy().reshape(-1, 2)
            )
            x_idxs = np.searchsorted(map_xy, xy_batch[:, 0])
            y_idxs = np.searchsorted(map_xy, xy_batch[:, 1])
            # f = interpolate.interp2d(xy_batch[:, 0], xy_batch[:, 1], diff, kind="cubic")
            x_interp = np.interp(map_xy[x_idxs], xy_batch[:, 0], diff)
            y_interp = np.interp(map_xy[y_idxs], xy_batch[:, 1], diff)
            out_map[y_idxs, x_idxs] += (x_interp + y_interp) / 2
        self.gaus_overlay_item.setImage(
            out_map,
            rect=(
                -standard_deviations,
                -standard_deviations,
                standard_deviations * 2,
                standard_deviations * 2,
            ),
        )

    def create_uniform_map(self, standard_deviations=5):
        """
        Displays a simple 0-mean, unit-variance gaussian distribution over the latent
        space. This is useful to visually calibrate where samples lie relative to
        the expected latent space distribution.

        Parameters
        ----------
        standard_deviations
            How many standard deviations to show in the displayed image
        """
        # Shorten name for brevity below
        std_devs = standard_deviations
        gran = self.mapping_granularity
        yy, xx = np.mgrid[-std_devs:std_devs:gran, -std_devs:std_devs:gran]
        gaus_data = stats.norm.pdf(yy) * stats.norm.pdf(xx)
        self.gaus_overlay_item.setImage(
            gaus_data,
            rect=(-std_devs, -std_devs, std_devs * 2, std_devs * 2),
        )


class PopoutPlugin(GenerativeTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.popout_target = self.register_item(PopoutImageTargetItem(), hide=True)

        self.global_popouts: list[PopoutImageTargetItem] = []

        ti = self.popout_target
        ti.setZValue(100)

        self.tab.register_selection_listener(self.popout_selection_listener)
        self.popout_target.sigPositionChanged.connect(self.on_target_move)

    def popout_selection_listener(self, sample_indexes: list[int]):
        if not len(sample_indexes):
            self.popout_target.hide()
            self.popout_target.sample_index = None
            self.clear_popout_samples()
            return
        self.popout_target.sample_index = sample_indexes[0]
        self.popout_target.show()
        xformed = self.tab.get_transformed_samples(sample_indexes[0])
        self.popout_target.setPos(xformed[self.tab.xdim], xformed[self.tab.ydim])

    def on_target_move(self, target: PopoutImageTargetItem):
        sample_index = target.sample_index
        if sample_index is None:
            return
        samples = self.tab.samples
        x, y = target.pos()
        xformed = self.tab.get_transformed_samples([sample_index])
        xformed[0, self.tab.xdim] = x
        xformed[0, self.tab.ydim] = y

        selected_sample = self.tab.dim_tformer.inverse_transform(xformed).type_as(
            samples
        )
        pred = self.tab.forward(selected_sample)
        pred_imgs = tensor_to_np(pred).transpose((0, 2, 3, 1))
        target.set_image(pred_imgs[0])
        target.set_name(str(sample_index))

    def ensure_n_popouts(self, n_popouts: int):
        while len(self.global_popouts) > n_popouts:
            self.tab.plot_widget.removeItem(self.global_popouts.pop())

        while len(self.global_popouts) < n_popouts:
            new_popout = self.register_item(PopoutImageTargetItem(), hide=True)
            new_popout.setZValue(100)
            new_popout.sigPositionChanged.connect(self.on_target_move)
            self.global_popouts.append(new_popout)

    def popout_selected_samples(self, sample_indexes: list[int], image_size=None):
        self.ensure_n_popouts(len(sample_indexes))
        for sample_index, popout in zip(sample_indexes, self.global_popouts):
            xformed = self.tab.get_transformed_samples(sample_index)
            popout.setPos(xformed[self.tab.xdim], xformed[self.tab.ydim])
            popout.sample_index = sample_index
            if image_size is not None:
                popout.default_image_size = image_size
            self.on_target_move(popout)
            popout.show()

    @bind(n_samples=dict(limits=[0, None]), image_size=dict(limits=[2, None]))
    def popout_random_samples(self, n_samples=15, image_size=64):
        """
        Display image popups of random samples from the latent space

        Parameters
        ----------
        n_samples
            Number of samples to display
        image_size
            Size of the displayed images in screen pixels
        """
        samples = self.tab.samples
        if samples is None or not len(samples):
            return
        n_samples = min(n_samples, len(samples))
        n_samples = max(n_samples, 0)
        sample_indexes = np.random.choice(len(samples), n_samples, replace=False)
        self.popout_selected_samples(
            sample_indexes, np.array([image_size] * 2, dtype=np.int32)
        )

    def clear_popout_samples(self):
        self.ensure_n_popouts(0)

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.popout_random_samples)


class SampleMetadataPlugin(GenerativeTabPlugin):
    name_clusterer_map = dict(
        kmeans=KMeans, agg=FeatureAgglomeration, dbscan=DBSCAN, meanshift=MeanShift
    )

    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        tab.sig_model_changed.connect(self.on_model_changed)

    def on_model_changed(self):
        self.get_samples_from_latent_space()

    @bind(
        cluster_method=_mkspec("list", limits=list(name_clusterer_map)),
        cluster_kwargs=_mkspec("text"),
    )
    def label_samples_from_clustering(
        self,
        cluster_method="kmeans",
        cluster_kwargs: str | dict = None,
    ):
        """
        Fits a scikit-learn clustering algorithm to the latent space of the current model
        and labels the samples with the cluster labels.

        Parameters
        ----------
        cluster_method
            Clustering method to use. It is fit on the latent space of the samples,
            including any dimension transforms that have been applied. The output
            of ``fit_predict`` is used to label the samples.
        cluster_kwargs
            Keyword arguments to pass to the clustering method. If a string, it is
            evaluated as a dictionary literal. Multiple keywords can be comma-separated,
            e.g. ``"n_clusters=10, n_init=10"``.
        """
        samples_info = self.tab.samples_info
        if samples_info.samples is None:
            return
        if cluster_kwargs is None:
            cluster_kwargs = {}
        elif isinstance(cluster_kwargs, str):
            cluster_str = f"dict({cluster_kwargs})"
            cluster_kwargs = eval(cluster_str)

        clusterer = self.name_clusterer_map[cluster_method](**cluster_kwargs)
        transformed = self.tab.dim_tformer.transform(samples_info.samples)
        labels = clusterer.fit_predict(tensor_to_np(transformed))
        mapper = OptionsDict("Clusterer")
        numeric, mapping = mapper.toNumeric(labels, rescale=True, returnMapping=True)
        samples_info.number_label_map = mapping
        samples_info.numeric_labels = numeric

        self.tab.sig_samples_changed.emit()

    def get_samples_from_latent_space(self, n_samples=25):
        """
        Reset the sample latents to a random set of samples from the model

        Parameters
        ----------
        n_samples
            Number of samples to use
        """
        if n_samples <= 0:
            n_samples = None
        self.tab.samples_info.samples = self.tab.get_random_latent_samples(n_samples)
        self.tab.samples_info.unset_labels()
        self.tab.sig_samples_changed.emit()

    @bind(file=dict(type="file", fileMode="AnyFile", acceptMode="AcceptSave"))
    def save_samples(self, file="./sample_info.pt"):
        """
        Save the samples and their metadata (label, numeric->label map, etc.) to a file.

        Uses ``torch.save`` behind the scenes, so the file can be loaded with
        ``torch.load``.

        Parameters
        ----------
        file
            The file to save to, typically using the .pt extension
        """
        torch.save(self.tab.samples_info.state_dict(), file)

    @bind(file=dict(type="file"))
    def load_samples(self, file="./sample_info.pt"):
        """
        Loads a file saved by :meth:`save_samples`

        Parameters
        ----------
        file
            The file to load
        """
        self.tab.samples_info.load_state_dict(torch.load(file))
        self.tab.sig_samples_changed.emit()

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.get_samples_from_latent_space)
        editor.registerFunction(self.label_samples_from_clustering)
        editor.registerFunction(self.save_samples)
        editor.registerFunction(self.load_samples)


class FileSampleOptionsPlugin(SampleMetadataPlugin):
    # Ensure name is same as parent
    name = "Sample Metadata"

    tab: VAEEncoderTab

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.get_samples_from_folder)
        editor.registerFunction(self.label_samples_from_file)
        super().register_functions(editor)

    @bind(file=dict(type="file", value=""))
    def label_samples_from_file(self, file, label_column=""):
        """
        Label the samples with the values in a CSV file.

        Parameters
        ----------
        file
            Csv with at least ``label_column`` (see below) present
        label_column
            Column in ``file`` to use as label. If not present in the file or not
            provided, the function returns without doing anything. Depending on
            the data type of the column:
              - If numeric/bool-like, the values are normalized to 0->1 and used
                as labels.
              - If string-like, the values are mapped to numeric labels based on their
                order of appearance and used as above.
        """
        info = self.tab.samples_info
        df = pd.read_csv(file)
        if len(df) != len(info.samples) or label_column not in df:
            return
        labels = df[label_column]
        valid_label_mask = labels.notna()
        param = OptionsDict(label_column, "")
        numeric, mapping = param.toNumeric(
            labels[valid_label_mask], rescale=True, returnMapping=True
        )
        if not valid_label_mask.all():
            # Need to resize `numeric` to match data + add `nan` to the map
            new_numeric = np.full(len(labels), np.nan)
            new_numeric[valid_label_mask] = numeric
            mapping[np.nan] = None
            numeric = new_numeric
        info.number_label_map = mapping
        info.numeric_labels = numeric

        self.tab.sig_samples_changed.emit()

    @bind(source=_mkspec("file", fileMode="Directory"))
    def get_samples_from_folder(
        self,
        source: str | Path | list | torch.Tensor = "",
        batch_size=32,
        max_num_samples=1_000,
    ):
        """
        Generates latent samples by encoding each image in a folder.

        Parameters
        ----------
        source
            Folder of images. If blank, random latent samples are used instead
        batch_size
            Batch size to read images. Useful when dealing with large amounts of data.
        max_num_samples
            Upper bound on randomly selected samples from the source.
        """
        if not os.path.exists(source):
            return
        samples, names = read_image_folder(source)
        if not samples:
            return
        if max_num_samples < len(samples):
            keep_idxs = np.random.choice(len(samples), max_num_samples, replace=False)
            samples = [samples[i] for i in keep_idxs]
            names = [names[i] for i in keep_idxs]
        mu_all, std_all = [], []
        for batch_start in range(0, len(samples), batch_size):
            batch = samples[batch_start : batch_start + batch_size]
            batch = torch.cat(
                [self.tab.image_as_normed_tensor(im) for im in batch], dim=0
            )
            mu, std = self.tab.forward_encoder(batch)
            mu = mu.view(-1, mu.shape[1])
            std = std.view(-1, std.shape[1])
            mu_all.append(mu)
            std_all.append(std)
        mu_all = torch.cat(mu_all, dim=0)

        info = self.tab.samples_info
        info.unset_labels()
        info.samples = mu_all
        info.image_files = [os.path.join(source, name) for name in names]
        self.tab.sig_samples_changed.emit()


class EncoderROIPlugin(GenerativeEncoderTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.encoded_roi = self.register_item(
            pg.CircleROI((0, 0), radius=0.1, pen="r", movable=False), hide=True
        )

        while self.encoded_roi.handles:
            self.encoded_roi.removeHandle(0)

        # Not featureful enough yet to be worth exposing
        # tab.register_selection_listener(self.encode_sample_listener, enabled=False)

    def encode_sample_listener(self, sample_indexes: list[int]):
        if (
            not len(sample_indexes)
            or (image := self.tab.get_index_as_image(sample_indexes[0])) is None
        ):
            self.encoded_roi.hide()
            return
        self.encoded_roi.show()
        input_image = self.tab.image_as_normed_tensor(image)
        xdim, ydim = self.tab.xdim, self.tab.ydim

        mu, std = self.tab.forward_encoder(input_image)
        mu_xform = self.tab.dim_tformer.transform(mu).view(-1)
        std_xform = self.tab.dim_tformer.transform(std).view(-1)
        self.encoded_roi.setSize(tuple(tensor_to_np(std_xform[[xdim, ydim]])))
        new_pos = tensor_to_np(mu_xform[[xdim, ydim]])
        self.encoded_roi.setPos(pg.Point(*new_pos) - self.encoded_roi.size() / 2)


class ReencodingPlugin(GenerativeEncoderTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.plot_widget = tab.plot_widget
        self.arrow_items: list[pg.ArrowItem] = []
        self.arrow_properties = ParameterContainer()
        self.reencoding_properties = ParameterContainer()
        self.window_handle = None
        self.n_encodings = 10

        tab.register_selection_listener(self.reencoding_trail_listener, enabled=False)

    def multiple_encode(self):
        """
        Opens a dialog allowing the user to reencode the selected samples multiple times
        and observe trends in differential error
        """
        if not (image := self.tab.get_index_as_image()):
            return
        image_tensor = self.tab.image_as_normed_tensor(image)

        layout = pg.GraphicsLayout()
        view = pg.GraphicsView()
        view.setCentralItem(layout)

        ref_vb = layout.addViewBox(row=0, col=0, lockAspect=True)
        ref_img = pg.ImageItem(np.array(image))
        ref_vb.addItem(ref_img)

        encoded_vb = layout.addViewBox(row=0, col=1, lockAspect=True)
        encoded_img = pg.ImageItem(ref_img.image)
        encoded_vb.addItem(encoded_img)
        err_plot = layout.addPlot(row=1, col=0, colspan=2)
        err_curve = pg.PlotCurveItem(pen="r", width=3)
        err_plot.addItem(err_curve)

        @functools.lru_cache(maxsize=30)
        def cached_encode(n=0):
            diffs = []
            if n <= 0:
                return diffs, image_tensor
            diffs, prev_image = cached_encode(n - 1)
            mu, _ = self.tab.forward_encoder(prev_image)
            next_image = self.tab.forward(mu)
            diffs = diffs.copy()
            diffs.append(torch.abs(next_image - prev_image).sum().item())
            return diffs, next_image

        def encode_decode(n=0):
            """
            Encodes and decodes the image n times, plotting the error at each step

            Parameters
            ----------
            n
                Number of times to encode and decode the image
            """
            diffs, encoded_tensor = cached_encode(n)
            image_np = tensor_to_np(encoded_tensor[0]).transpose((1, 2, 0))
            encoded_img.setImage(image_np)
            err_curve.setData(np.arange(n), diffs)
            err_plot.autoRange()

        editor = ParameterEditor()
        editor.registerFunction(encode_decode, runOptions=RunOptions.ON_CHANGED)

        window = widgets.EasyWidget.buildWidget([view, editor], "H", useSplitter=True)
        window.show()
        window.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.window_handle = window

    def ensure_n_arrows(self, n: int):
        while len(self.arrow_items) > n:
            self.plot_widget.removeItem(self.arrow_items.pop())

        while len(self.arrow_items) < n:
            self.arrow_items.append(self.register_item(pg.ArrowItem(), hide=True))

    def reencoding_trail_listener(self, sample_indexes: list[int]):
        if len(sample_indexes):
            sample_indexes = [sample_indexes[0]]
        self.make_reencoding_arrow_trail(
            **self.reencoding_properties, sample_indexes=sample_indexes
        )

    def make_reencoding_arrow_trail(
        self, sample_indexes: list[int], n_encodings: int, batch_size=16
    ):
        """
        Creates a trail of arrows showing the path of a sample as it is progressively
        encoded and decoded

        Parameters
        ----------
        sample_indexes
            Indexes of the samples to encode/decode
        n_encodings
            Number of times to encode/decode the sample
        batch_size
            When many samples are specified, pytorch can run out of error attempting
            to get all encoding trails at once. This parameter controls how many
            samples are encoded at once, but has no impact on the final output other
            than computing efficiency.
        """
        samples = self.tab.samples
        if samples is None or n_encodings <= 0 or not len(sample_indexes):
            self.ensure_n_arrows(0)
            return
        samples = samples[sample_indexes]

        batch_size = min(batch_size, len(samples))

        all_trail_locations = np.empty(
            (len(samples), n_encodings + 1, 2), dtype=np.float32
        )
        for batch_start in range(0, len(samples), batch_size):
            batch = samples[batch_start : batch_start + batch_size]
            batch_end = batch_start + len(batch)
            for ii in range(n_encodings):
                cur_locations = self.tab.dim_tformer.transform(batch)[
                    :, [self.tab.xdim, self.tab.ydim]
                ]
                all_trail_locations[batch_start:batch_end, ii] = tensor_to_np(
                    cur_locations
                )
                images = self.tab.forward(batch)
                batch, _ = self.tab.forward_encoder(images)
            # Add last batch
            cur_locations = self.tab.dim_tformer.transform(batch)[
                :, [self.tab.xdim, self.tab.ydim]
            ]
            all_trail_locations[batch_start:batch_end, -1] = tensor_to_np(cur_locations)

        # Diff is approximate_n_samples x n_encodings x 2
        diffs = np.diff(all_trail_locations, axis=1)
        # Make arrow items pointing in diff direction, length proportional to diff
        angles = np.arctan2(diffs[:, :, 1], diffs[:, :, 0])
        # 0 degrees points left in arrow item, but we want it to point right
        angles = 180 + np.rad2deg(angles)
        lengths = np.linalg.norm(diffs, axis=2)
        arrow_items = [
            pg.ArrowItem(
                pos=pos,
                angle=angle,
                tailLen=length - 0.05,
                pxMode=False,
                headLen=0.05,
                tailWidth=0.01,
                **self.arrow_properties,
            )
            for pos, angle, length in zip(
                all_trail_locations[:, 1:, :].reshape(-1, 2),
                angles.ravel(),
                lengths.ravel(),
            )
        ]
        for old_arrow in self.arrow_items:
            self.plot_widget.removeItem(old_arrow)
        self.arrow_items = arrow_items
        for arrow in arrow_items:
            self.plot_widget.addItem(arrow)
        return all_trail_locations

    @bind(brush=_mkspec("color"), pen=_mkspec("pen"))
    def update_arrow_properties(self, brush="b", pen="w"):
        """
        Change the appearance of reencoding arrows

        Parameters
        ----------
        brush
            Arrow brush color
        pen
            Arrow pen color
        """
        for arrow in self.arrow_items:
            arrow.setBrush(pg.mkBrush(brush))
            arrow.setPen(pg.mkPen(pen))

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.multiple_encode)
        editor.registerFunction(
            self.random_sample_reencoding_trails, container=self.reencoding_properties
        )
        self.reencoding_properties.pop("n_samples")
        editor.registerFunction(
            self.update_arrow_properties,
            runOptions=RunOptions.ON_CHANGED,
            container=self.arrow_properties,
        )

    def random_sample_reencoding_trails(self, n_encodings=10, n_samples=100):
        """
        Create reencoding trails for a random sample of the data

        Parameters
        ----------
        n_encodings
            Number of times to encode/decode the sample
        n_samples
            Number of samples to encode/decode
        """
        if self.tab.samples is None:
            return
        n_samples = min(n_samples, len(self.tab.samples))
        n_samples = max(0, n_samples)
        sample_indexes = np.random.choice(
            len(self.tab.samples), n_samples, replace=False
        )
        self.make_reencoding_arrow_trail(
            n_encodings=n_encodings, sample_indexes=sample_indexes
        )


class PredictionPlugin(TabPlugin):
    def __init__(self, tab: ModelTab):
        super().__init__(tab)
        self.window_handle = None

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.predict_on_samples)

    @bind(image_or_path=_mkspec("file", fileMode="Directory"))
    def predict_on_samples(self, image_or_path=""):
        """
        Discriminator prediction of how likely each sample is to be real. Each image
        is displayed along with its confidence in a gridded window.

        Parameters
        ----------
        image_or_path
            Path to a directory of images on which to run the prediction,
            or a single numpy image
        """
        if isinstance(image_or_path, np.ndarray):
            images = [Image.fromarray(image_or_path)]
            names = ["Confidence"]
        elif isinstance(image_or_path, (str, Path)):
            images, names = read_image_folder(image_or_path)
        else:
            raise ValueError(f"Invalid image or path type: {type(image_or_path)}")

        img_as_batch = torch.cat(
            [self.tab.image_as_normed_tensor(image) for image in images]
        )
        confidences = (
            self.tab.model.discriminator(img_as_batch)
            .view(-1)
            .detach()
            .cpu()
            .numpy()
            .round(2)
        )
        num_rows = int(np.sqrt(len(images)))
        num_cols = int(np.ceil(len(images) / num_rows))
        images_np = [tensor_to_np(im).transpose((1, 2, 0)) for im in img_as_batch]
        preview = PreviewItemsMixin()
        out_widget = preview.preview_widget
        preview.make_previews(num_rows, num_cols)
        preview.update_previews(images_np, confidences, names, show_labels=True)
        out_widget.show()
        out_widget.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.window_handle = out_widget
