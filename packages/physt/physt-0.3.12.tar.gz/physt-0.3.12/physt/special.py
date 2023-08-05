from __future__ import absolute_import
from .histogram_base import HistogramBase
from .histogram_nd import HistogramND
from .histogram1d import Histogram1D
from . import binnings, histogram_nd
import numpy as np


class PolarHistogram(HistogramND):
    """Polar histogram data.

    This is a special case of a 2D histogram with transformed coordinates.
    """
    def __init__(self, binnings, frequencies=None, **kwargs):
        if not "axis_names" in kwargs:
            kwargs["axis_names"] = ("r", "phi")
        if "dim" in kwargs:
            kwargs.pop("dim")
        super(PolarHistogram, self).__init__(2, binnings=binnings, frequencies=frequencies, **kwargs)

    @property
    def bin_sizes(self):
        sizes = self.get_bin_right_edges(0) ** 2 - self.get_bin_left_edges(0) ** 2
        sizes = np.outer(sizes, self.get_bin_widths(1))
        return sizes

    def projection(self, axis_name, **kwargs):
        if isinstance(axis_name, int):
            ax = axis_name
        elif axis_name == self.axis_names[0]:
            ax = 0
        elif axis_name == self.axis_names[1]:
            ax = 1
        else:
            raise RuntimeError("Unknown axis: {0}".format(axis_name))
        klass = (RadialHistogram, AzimuthalHistogram)[ax]
        return HistogramND.projection(self, ax, type=klass, **kwargs)

    def find_bin(self, value, axis=None, radial_coords=False):
        if radial_coords:
            r, phi = value
            # TODO: phi modulo
        else:
            r = np.hypot(value[1], value[0])
            phi = np.arctan2(value[1], value[0])
        return HistogramND.find_bin(self, (r, phi))
    #
    # def fill(self, value, weight=1, radial_coords=False):
    #     # TODO: Adapt to "transform"???
    #     ixbin = self.find_bin(value, radial_coords=radial_coords)
    #     if ixbin is None and self.keep_missed:
    #         self._missed += weight
    #     else:
    #         self._frequencies[ixbin] += weight
    #         self._errors2[ixbin] += weight ** 2
    #     return ixbin
    #
    # def fill_n(self, values, weights=None, dropna=True, radial_coords=False):
    #     HistogramBase.fill_n(self, values=values, weights=weights, dropna=dropna,
    #                          radial_coords=radial_coords)


class RadialHistogram(Histogram1D):
    """Projection of polar histogram to 1D with respect to radius.

    This is a special case of a 1D histogram with transformed coordinates.
    """
    @property
    def bin_sizes(self):
        return self.bin_right_edges ** 2 - self.bin_left_edges ** 2

    def fill_n(self, values, weights=None, dropna=True):
        # TODO: Implement?
        raise NotImplementedError("Radial histogram is not (yet) modifiable")

    def fill(self, value, weight=1):
        # TODO: Implement?
        raise NotImplementedError("Radial histogram is not (yet) modifiable")


class AzimuthalHistogram(Histogram1D):
    """Projection of polar histogram to 1D with respect to phi.

    This is a special case of a 1D histogram with transformed coordinates.
    """
    # TODO: What about fill(_n)? Should it be 1D or 2D?
    # TODO: Add special plotting (polar bar, polar ring)
    def fill_n(self, values, weights=None, dropna=True):
        raise NotImplementedError("Azimuthal histogram is not (yet) modifiable")

    def fill(self, value, weight=1):
        raise NotImplementedError("Azimuthal histogram is not (yet) modifiable")


class SphericalHistogram(HistogramND):
    def __init__(self, bins, frequencies=None, **kwargs):
        if not "axis_names" in kwargs:
            kwargs["axis_names"] = ("r", "theta", "phi")
        kwargs.pop("dim", False)
        super(SphericalHistogram, self).__init__(3, bins=bins, frequencies=frequencies, **kwargs)

    def find_bin(self, value, axis=None, spherical_coords=False):
        if spherical_coords:
            r, theta, phi = value
        else:
            x, y, z = value
            r = np.sqrt(x ** 2, y ** 2, z ** 2)
            theta = np.arccos(z / r)
            phi = np.arctan2(x, y)
        return HistogramND.find_bin(self, (r, theta, phi))



def polar_histogram(xdata, ydata, radial_bins="human", phi_bins=16, *args, **kwargs):
    rdata = np.hypot(ydata, xdata)
    phidata = np.arctan2(ydata, xdata)
    data = np.concatenate([rdata[:, np.newaxis], phidata[:, np.newaxis]], axis=1)
    dropna = kwargs.pop("dropna", False)
    if isinstance(phi_bins, int):
        phi_range = (-np.pi, np.pi)
        if "phi_range" in "kwargs":
            phi_range = kwargs["phi_range"]
        elif "range" in "kwargs":
            phi_range = kwargs["range"][1]
        phi_range = list(phi_range) + [phi_bins + 1]
        phi_bins = np.linspace(*phi_range)

    if dropna:
        data = data[~np.isnan(data).any(axis=1)]
    bin_schemas = binnings.calculate_bins_nd(data, [radial_bins, phi_bins], *args, check_nan=not dropna, **kwargs)

    # Prepare remaining data
    weights = kwargs.pop("weights", None)
    frequencies, errors2, missed = histogram_nd.calculate_frequencies(data, ndim=2,
                                                                  binnings=bin_schemas,
                                                                  weights=weights)
    return PolarHistogram(binnings=bin_schemas, frequencies=frequencies, errors2=errors2, missed=missed)
