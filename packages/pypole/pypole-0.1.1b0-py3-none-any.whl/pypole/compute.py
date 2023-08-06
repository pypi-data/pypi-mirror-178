import logging

import numba
import numpy as np
from numpy.typing import NDArray

LOG = logging.getLogger(__name__)

from pypole import NDArray64

_EPSILON = 1e-50


def dipolarity_param(data_map: NDArray64, fitted_map: NDArray64) -> np.float64:
    """Calculate the dipolarity parameter of a magnetic dipole field.

    The dipolarity parameter (DP) is defined as the ratio of the rms of the
    residual (fitted_map - map) to the rms of the data map.
    DP was first introduced by [1]_.

    Args:
      data_map: magnetic field map
      fitted_map: fitted magnetic field map

    Returns:
      float: dipolarity parameter of the magnetic dipole field

    References
    ----------
    .. [1] Fu, Roger R., Eduardo A. Lima, Michael W. R. Volk, and Raisa Trubko.
    “High-Sensitivity Moment Magnetometry With the Quantum Diamond Microscope.”
    Geochemistry, Geophysics, Geosystems 21, no. 8 (2020): e2020GC009147. https://doi.org/10/ghfpqv.
    """
    residual: NDArray64 = fitted_map - data_map
    return 1 - (rms(residual) / rms(data_map))


def rms(b_map: NDArray64) -> np.float64:
    """Calculate the root mean square of a map.

    Args:
      b_map: Map to calculate the RMS of

    Returns:
        float: RMS of the map
    """
    return np.sqrt(np.mean(np.square(b_map))).astype(np.float64)


def upward_continue(
    b_map: NDArray64, distance: float, pixel_size: float, oversample: int = 2
) -> NDArray64:
    """Upward continues a map.

    This function calculates a new map that is the upward continuation of the initial map by a given distance.
    In other words, it returns a new map that looks as if it was measured at a different distance from the sample.

    Args:
      map: The map to be continued
      distance: The distance to upward continue the map in m
      pixel_size: The size of the pixel in the map in m
      oversample: The oversampling factor to use (Default value = 2)

    Returns:
        The upward continued map
    """
    ypix, xpix = b_map.shape
    new_x, new_y = xpix * oversample, ypix * oversample

    # Calculate the new pixel size
    b_map = pad_map(b_map)

    # these freq. coordinates match the fft algorithm
    x_steps = np.concatenate([np.arange(0, new_x / 2, 1), np.arange(-new_x / 2, 0, 1)])
    fx = x_steps / pixel_size / new_x
    y_steps = np.concatenate([np.arange(0, new_y / 2, 1), np.arange(-new_y / 2, 0, 1)])
    fy = y_steps / pixel_size / new_y

    fgrid_x, fgrid_y = np.meshgrid(fx + _EPSILON, fy + _EPSILON)

    kx = 2 * np.pi * fgrid_x
    ky = 2 * np.pi * fgrid_y
    k = np.sqrt(kx**2 + ky**2)

    # Calculate the filter frequency response associated with the x component
    x_filter = np.exp(-distance * k)

    # Compute FFT of the field map
    fft_map = np.fft.fft2(b_map, s=(new_y, new_x))

    # Calculate single component
    b_out = np.fft.ifft2(fft_map * x_filter)
    LOG.debug("Upward continued map by %s m", distance)

    # Crop matrices to get rid of zero padding
    return b_out[ypix : 2 * ypix, xpix : 2 * xpix].real


def pad_map(b_map: NDArray64, oversample: int = 2) -> NDArray64:
    """Pads a map with zeros.

    Args:
      map: The map to be padded

    Returns:
        The padded map
    """
    pad_size = np.array(
        ((b_map.shape[0], b_map.shape[0]), (b_map.shape[1], b_map.shape[1]))
    )
    pad_size *= oversample - 1

    return np.pad(b_map, pad_width=pad_size, mode="constant", constant_values=0)
