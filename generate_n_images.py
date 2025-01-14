# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Minimal script for generating an image using pre-trained StyleGAN generator."""

import os
import pickle
import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import config
import sys

def main():
    # Initialize TensorFlow.
    tflib.init_tf()

    # To this
    url = os.path.abspath(sys.argv[1])
    with open(url, 'rb') as f:
        _G, _D, Gs = pickle.load(f)

        # _G = Instantaneous snapshot of the generator. Mainly useful for resuming a previous training run.
        # _D = Instantaneous snapshot of the discriminator. Mainly useful for resuming a previous training run.
        # Gs = Long-term average of the generator. Yields higher-quality results than the instantaneous snapshot.

    # Print network details.
    Gs.print_layers()

    for x in range(0, int(sys.argv[2])):
        # Pick latent vector.
        rnd = np.random.RandomState(x)
        latents = rnd.randn(1, Gs.input_shape[1])

        fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True, output_transform=fmt)

        os.makedirs(config.result_dir, exist_ok=True)
        png_filename = os.path.join(config.result_dir + '/generated',  str(x).zfill(4) + '.png')
        PIL.Image.fromarray(images[0], 'RGB').save(png_filename)

if __name__ == "__main__":
    main()
