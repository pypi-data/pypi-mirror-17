# djpi2

Compute the rotation matrix d(pi/2) used in rotating data expressed in spherical harmonics.

# Usage

call djpi2 (`dj`, `lmax`)

# Parameters

`dj` : output, real\*8, dimension (`lmax`+1, `lmax`+1, `lmax`+1)
:   The rotation matrix dj(pi/2).
	
`lmax` : input, integer
:   The maximum spherical harmonic degree of the spherical harmonic rotation.

# Description

`djpi2` will calculate the rotation matrix `d_{mM}^j (pi/2)` that is used in rotating spherical harmonics in the routines `SHRotateRealCoef` and `SHRotateCoef`.

This routine is based on code originally written by Guy Masters.

# See also

[shrotatecoef](shrotatecoef.html), [shrotaterealcoef](shrotaterealcoef.html)
