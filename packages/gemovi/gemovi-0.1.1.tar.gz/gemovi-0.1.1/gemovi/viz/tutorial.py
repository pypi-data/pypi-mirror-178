from __future__ import annotations

import copy
import typing as t
from pathlib import Path

import pandas as pd
from pyqtgraph.Qt import QtCore, QtWidgets
from qtextras import ParameterEditor, bindInteractorOptions as bind, fns
from skimage import io
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from gemovi.vae.train import main as train_main

if t.TYPE_CHECKING:
    from gemovi.viz import ModelWindow


class WelcomePage(QtWidgets.QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome to the tutorial")
        self.setSubTitle(
            "This wizard will guide you through the basic features of the visualization "
            "package. "
        )


class TutorialPage(QtWidgets.QWizardPage):
    folder: str | Path = None
    sig_folder_changed = QtCore.Signal(object)

    def __init__(
        self,
        long_message: str = None,
        title: str = None,
        register_set_folder: bool = True,
    ):
        super().__init__()
        if title:
            self.setTitle(title)
        label = None
        if long_message:
            label = QtWidgets.QLabel(long_message)
            label.setWordWrap(True)

        self.editor = ParameterEditor()
        if register_set_folder:
            self.set_folder_proc = self.editor.registerFunction(self.set_folder)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        if label:
            layout.addWidget(label)
        layout.addWidget(self.editor.tree)
        self.setLayout(layout)

    @bind(folder=dict(type="file"))
    def set_folder(self, folder: str | Path = "./gemovi-workspace"):
        folder = Path(folder).resolve()
        if folder == self.folder:
            return
        self.folder = folder
        self.sig_folder_changed.emit(folder)


class LoadDataPage(TutorialPage):
    def __init__(self, gemovi_window: ModelWindow = None):
        msg = (
            "<qt>Skip this page if you already have weights from a trained model. "
            "Otherwise, this page will create data suitable for training a model from "
            "scikit-learn's digits dataset. Note that in practice, a much larger "
            "dataset (e.g., Yann Lecun's 'digit' dataset) yields a more accurate "
            "model.\n\nIf you already have a dataset of images, skip the `prepare data` "
            "option and just run `prepare config`. <strong>Note!</strong> If you do "
            "this, be sure to changethe `data_path` option in the config to your "
            "specified image folder.</qt>"
        )
        super().__init__(msg, title="Prepare data")
        self.gemovi_window = gemovi_window
        for function in self.prepare_data, self.prepare_config:
            self.editor.registerFunction(function)

    @bind(test_size=dict(step=0.1, limits=[0.01, 0.99]))
    def prepare_data(self, random_state=42, test_size=0.1):
        if self.folder is None:
            raise ValueError("Please specify a folder first by running `set folder`.")
        # Load the digits dataset
        digits = load_digits()
        X = digits.data
        y = digits.target

        # Make classic train/test splits
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        for folder_name, images in zip(["data_train", "data_test"], [X_train, X_test]):
            out_folder = self.folder / folder_name
            out_folder.mkdir(exist_ok=True, parents=True)
            for ii, image in enumerate(images):
                image = image.reshape((8, 8))
                image = (image - image.min()) / (image.max() - image.min())
                image = (image * 255).astype("uint8")
                io.imsave(out_folder / f"{ii}.png", image)
            for file, data in zip(["labels_train", "labels_test"], [y_train, y_test]):
                df = pd.DataFrame(data.reshape(-1, 1))
                df.columns = ["label"]
                df.to_csv(self.folder / f"{file}.csv", index=False)

    def prepare_config(self, use_gpu=True):
        if self.folder is None:
            raise ValueError("Please specify a folder first by running `set folder`.")
        base_config = copy.deepcopy(self.gemovi_window.parameter_info)

        data_params = base_config["data_params"]
        trainer_params = base_config["trainer_params"]

        data_params["data_path"] = str(self.folder / "data_train")
        data_params["num_workers"] = 1
        if not use_gpu:
            del trainer_params["accelerator"]
            del trainer_params["devices"]
        trainer_params["max_epochs"] = 5
        trainer_params["model_name"] = self.gemovi_window.model_cls.__name__
        trainer_params["log_dir"] = str(self.folder / trainer_params["log_dir"])

        fns.saveToFile(base_config, self.folder / "config.yaml")


class ModelTrainerPage(TutorialPage):
    def __init__(self):
        msg = (
            "Skip this page if you already have weights from a trained model. "
            "Otherwise, this page trains a model from the data generated on the "
            "previous page."
        )
        super().__init__(msg, title="Train a model")
        self.editor.registerFunction(self.train_model)

    def train_model(self):
        if not self.folder:
            raise ValueError("Please specify a folder first by running `set folder`.")
        if not self.folder.joinpath("config.yaml").exists():
            raise ValueError(
                "No config file found; please run the previous page's"
                " `prepare config` function first."
            )

        QtWidgets.QMessageBox.information(
            self,
            "Training",
            "About to train model; close this dialog, then check the terminal for "
            "progress.",
        )
        train_main(self.folder / "config.yaml")


class FinishedPage(TutorialPage):
    def __init__(self, gemovi_window: ModelWindow = None):
        msg = (
            "Congratulations! You have a model that should be directly importable by "
            "the visualization package. Open the `settings` menu and load the best "
            "model weights from the training results folder. If you trained a model "
            "using the previous page, these should be under "
            "`gemovi-workspace/lightning_logs/version_0/checkpoints/`. "
        )
        super().__init__(msg, title="Finished!")
        self.gemovi_window = gemovi_window

        self.editor.registerFunction(self.open_settings)

    def open_settings(self):
        self.gemovi_window.raise_settings_window()


class GettingStartedWizard(QtWidgets.QWizard):
    def __init__(self, parent: ModelWindow):
        super().__init__(parent)
        btn = self.WizardButton
        button_layout = [
            btn.Stretch,
            btn.BackButton,
            btn.CancelButton,
            btn.NextButton,
            btn.FinishButton,
        ]
        self.setButtonLayout(button_layout)
        self.addPage(WelcomePage())
        tutorial_pages = [
            LoadDataPage(parent),
            ModelTrainerPage(),
            FinishedPage(parent),
        ]
        for page in tutorial_pages:
            self.addPage(page)
            page.editor.tree.setMinimumHeight(
                page.editor.tree.sizeHint().height() * 1.25
            )
            for connect_page in tutorial_pages:
                if page is connect_page:
                    continue
                page.sig_folder_changed.connect(connect_page.set_folder)
        self.setWindowTitle("Tutorial")
