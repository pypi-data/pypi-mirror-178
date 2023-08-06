from __future__ import annotations

from typing import Type

import numpy as np
import torch
from torch import nn, optim
from torch.nn import functional as F
from torchvision import models as tvmodels

from gemovi.common.utils import ParamDict, load_trainer_state_dict


def conv_transpose_bn(
    in_planes: int,
    out_planes: int,
    stride: int = 1,
    groups: int = 1,
    padding: int = 1,
    kernel_size=4,
    relu=False,
) -> nn.Sequential:
    """kxk (default 4x4) transposed convolution with padding and batch norm"""
    seq = nn.Sequential(
        nn.ConvTranspose2d(
            in_planes,
            out_planes,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            groups=groups,
            bias=False,
        ),
        nn.BatchNorm2d(out_planes),
    )
    if relu:
        seq.add_module(str(len(seq)), nn.ReLU(True))
    return seq


class ResNetUpsampleBlock(nn.Module):
    """
    Reimplementation of ResNet BasicBlock but with ConvTranspose2d instead of Conv2d
    to make the image bigger at each stage.
    """

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv_bn1_relu = conv_transpose_bn(
            in_channels, out_channels, stride, relu=True
        )
        self.conv_bn2 = conv_transpose_bn(out_channels, out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.upsampler = conv_transpose_bn(
            in_channels, out_channels, relu=False, stride=stride
        )

    def forward(self, x):
        identity = x
        out = self.conv_bn1_relu(x)
        out = self.conv_bn2(out)
        if identity.shape == out.shape:
            identity = self.upsampler(identity)
        out += identity
        out = self.relu(out)
        return out


class Discriminator(nn.Module):
    def __init__(self, num_filters, num_image_channels):
        super().__init__()

        self.main = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(num_image_channels, num_filters, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf) x 32 x 32
            nn.Conv2d(num_filters, num_filters * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(num_filters * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*2) x 16 x 16
            nn.Conv2d(num_filters * 2, num_filters * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(num_filters * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*4) x 8 x 8
            nn.Conv2d(num_filters * 4, num_filters * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(num_filters * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*8) x 4 x 4
            nn.Conv2d(num_filters * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid(),
        )

    def forward(self, input):
        return self.main(input)


class ResnetDiscriminator(nn.Module):
    def __init__(self, num_filters, num_image_channels):
        super().__init__()
        self.resnet = tvmodels.resnet18(pretrained=True)
        for param in self.resnet.parameters():
            param.requires_grad = False
        # Resetting last layer will enable grads, so no need to do it manually
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, 1)

    def forward(self, input):
        return self.resnet(input)


class Generator(nn.Module):
    def __init__(self, num_latent_dims, num_filters, num_image_channels):
        super().__init__()
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(num_latent_dims, num_filters * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(num_filters * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(num_filters * 8, num_filters * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(num_filters * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d(num_filters * 4, num_filters * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(num_filters * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d(num_filters * 2, num_filters, 4, 2, 1, bias=False),
            nn.BatchNorm2d(num_filters),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d(num_filters, num_image_channels, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. (nc) x 64 x 64
        )

    def forward(self, input):
        return self.main(input)


class ResnetGenerator(nn.Module):
    def __init__(self, num_latent_dims, num_filters, num_image_channels, *image_wh):
        super().__init__()

        if len(image_wh) == 1:
            image_wh = (image_wh[0], image_wh[0])

        self.base_width = 64
        self.preconv = conv_transpose_bn(num_latent_dims, num_filters * 8)
        self.block1 = ResNetUpsampleBlock(num_filters * 8, num_filters * 4, stride=2)
        self.block2 = ResNetUpsampleBlock(num_filters * 4, num_filters * 2, stride=2)
        self.block3 = ResNetUpsampleBlock(num_filters * 2, num_filters, stride=2)
        self.block4 = conv_transpose_bn(
            num_filters, num_image_channels, kernel_size=3, relu=True
        )
        self.activation = nn.Tanh()

    def forward(self, input):
        out = self.preconv(input)
        # FIXME: Dimensions are of course wrong
        out = self.block1(out)
        out = self.block2(out)
        out = self.block3(out)
        out = self.block4(out)
        out = self.activation(out)
        return out


class Encoder(Discriminator):
    def __init__(self, num_filters, num_image_channels, num_latent_dims, *image_wh):
        super().__init__(num_filters, num_image_channels)

        if len(image_wh) == 1:
            image_wh = (image_wh[0], image_wh[0])
        image_size = (num_image_channels, *image_wh)
        num_in_features = np.prod(self.main(torch.rand(1, *image_size)).shape)
        self.main[-1] = nn.Linear(num_in_features, num_latent_dims)


class ResnetEncoder(ResnetDiscriminator):
    # Use same init signature as Encoder for compatibility
    def __init__(self, num_filters, num_image_channels, num_latent_dims, *image_wh):
        super().__init__(num_filters, num_image_channels)
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, num_latent_dims)


class DCGAN(nn.Module):
    real_label = 1.0
    fake_label = 0.0

    manage_gradients = True

    def __init__(
        self,
        num_latent_dims=128,
        num_generator_filters=64,
        num_discrim_filters=64,
        num_image_channels=3,
        image_size=64,
        learn_rate=0.0002,
        beta1=0.5,
        beta2=0.999,
        discriminator_cls=Discriminator,
        generator_cls=Generator,
        encoder_cls: Type[Encoder] = None,
        initial_weights_file: str = None,
    ):
        super().__init__()
        self.opts = ParamDict(locals())
        for kk in list(self.opts):
            if kk == "self" or "cls" in kk:
                self.opts.pop(kk)

        generator = generator_cls(
            num_latent_dims, num_generator_filters, num_image_channels
        )
        discriminator = discriminator_cls(num_discrim_filters, num_image_channels)
        encoder = None
        if encoder_cls is not None:
            encoder = encoder_cls(
                num_discrim_filters, num_image_channels, num_latent_dims, image_size
            )

        self.generator = generator
        self.discriminator = discriminator
        self.encoder = encoder

        # Apply the weights_init function to randomly initialize all weights
        # to mean=0, stdev=0.02 as per the DCGAN paper.
        for model in self.children():
            model.apply(self._weights_init)
        if initial_weights_file:
            state = load_trainer_state_dict(
                torch.load(initial_weights_file), strict=False
            )
            self.load_state_dict(state)

        self.configure_optimizers()

        # Initialize BCELoss function
        self.criterion = F.binary_cross_entropy

    def configure_optimizers(self):
        betas = self.opts.beta1, self.opts.beta2
        optimizers = []
        for model in self.children():
            cur_optim = optim.Adam(
                model.parameters(), lr=self.opts.learn_rate, betas=betas
            )
            optimizers.append(cur_optim)
        # "None" only applies when no encoder is used
        optimizers.append(None)
        self.gen_optim, self.discrim_optim, self.encoder_optim = optimizers[:3]
        return optimizers[:3]

    def resolve_batch_and_noise(self, batch):
        if not isinstance(batch, torch.Tensor):
            batch, _ = batch
        b_size = batch.size(0)
        noise = torch.randn(
            b_size, self.opts.num_latent_dims, 1, 1, device=batch.device
        )
        return batch, noise

    def training_step(self, batch, optimizer_idx):
        batch, noise = self.resolve_batch_and_noise(batch)
        return self.train_step_for_idx(optimizer_idx)(batch, noise)

    def loss_for_idx(self, idx):
        return ["err_g", "err_d", "err_e"][idx]

    def train_step_for_idx(self, idx):
        return [
            self.gen_train_step,
            self.discrim_train_step,
            self.encoder_train_step,
        ][idx]

    def _maybe_update_gradients(self, optimizer, loss):
        if self.manage_gradients:
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    def discrim_train_step(self, batch, noise):
        """Update D network: maximize log(D(x)) + log(1 - D(G(z)))"""
        # Forward pass real batch through D
        discrim_on_real = self.discriminator(batch).view(-1)
        label = torch.full_like(discrim_on_real, self.real_label)
        # Calculate loss on all-real batch
        err_d_real = self.criterion(discrim_on_real, label)

        # Train with all-fake batch
        # Generate fake image batch with G
        fake = self.generator(noise).detach()
        label = torch.full_like(discrim_on_real, self.fake_label)
        # Classify all fake batch with D
        discrim_on_fake = self.discriminator(fake).view(-1)
        # Calculate D's loss on the all-fake batch
        err_d_fake = self.criterion(discrim_on_fake, label)
        # Compute error of D as sum over the fake and the real batches
        err_d = (err_d_real + err_d_fake) / 2

        self._maybe_update_gradients(self.discrim_optim, err_d)

        d_g_z1 = discrim_on_fake.mean()
        d_x = discrim_on_real.mean()
        log = dict(err_d=err_d, d_g_z1=d_g_z1, d_x=d_x)
        return log

    def gen_train_step(self, batch, noise):
        """Update G network: maximize log(D(G(z)))"""

        fake = self.generator(noise)

        # Since we just updated D, perform another forward pass of all-fake batch through D
        output = self.discriminator(fake).view(-1)
        label = torch.full_like(output, self.real_label)
        # Calculate G's loss based on this output
        err_g = self.criterion(output, label)
        d_g_z2 = output.mean()
        log_dict = dict(d_g_z2=d_g_z2, err_g=err_g)

        self._maybe_update_gradients(self.gen_optim, err_g)

        return log_dict

    def encoder_train_step(self, batch, noise):
        if not self.encoder:
            return dict()
        fake = self.generator(noise).detach()
        encoded = self.encoder(fake).view(noise.shape)
        err_e = F.mse_loss(encoded, noise)
        self._maybe_update_gradients(self.encoder_optim, err_e)

        log = dict(err_e=err_e)
        return log

    # custom weights initialization called on netG and netD
    @staticmethod
    def _weights_init(model):
        classname = model.__class__.__name__
        if classname.find("Conv") != -1:
            nn.init.normal_(model.weight.data, 0.0, 0.02)
        elif classname.find("BatchNorm") != -1:
            nn.init.normal_(model.weight.data, 1.0, 0.02)
            nn.init.constant_(model.bias.data, 0)

    def likelihood_is_real(self, images: torch.Tensor):
        return self.discriminator(images).view(-1)
