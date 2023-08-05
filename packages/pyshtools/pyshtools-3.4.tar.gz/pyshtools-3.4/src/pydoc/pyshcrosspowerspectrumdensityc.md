# SHCrossPowerSpectrumDensityC

Compute the cross-power spectral density of two complex functions.

# Usage

`cspectrum` = pyshtools.SHCrossPowerSpectrumDensityC (`cilm1`, `cilm2`, [`lmax`])

# Returns

`cspectrum` : complex, dimension (`lmax`+1)
:   The cross-power spectral density of the two complex functions.

# Parameters

`cilm1` : complex, dimension (2, `lmaxin1`+1, `lmaxin1`+1)
:   The complex spherical harmonics of the first complex function.

`cilm2` : complex, dimension (2, `lmaxin2`+1, `lmaxin2`+1)
:   The complex spherical harmonics of the first complex function.

`lmax` : optional, integer, default = min(`lmaxin1`, `lmaxin2`)
:   The maximum spherical harmonic degree of the cross power spectral density. This must be less than or equal to the minimum of `lmaxin1` and `lmaxin2`.

# Description

`SHCrossPowerSpectrumDensityC` will calculate the cross-power spectral density of two complex functions expressed in complex spherical harmonics. For a given spherical harmonic degree `l`, this is calculated as:

`cspectrum(l) = Sum_{i=0}^1 Sum_{m=0}^l cilm1[i, l, m] * conjg[cilm2[i, l, m]] / (2l + 1)`.

# See also

[shpowerlc](pyshpowerlc.html), [shpowerdensitylc](pyshpowerdensitylc.html), [shcrosspowerlc](pyshcrosspowerlc.html), [shcrosspowerdensitylc](pyshcrosspowerdensitylc.html), [shpowerspectrumc](pyshpowerspectrumc.html), [shpowerspectrumdensityc](pyshpowerspectrumdensityc.html), [shcrosspowerspectrumc](pyshcrosspowerspectrumc.html)
