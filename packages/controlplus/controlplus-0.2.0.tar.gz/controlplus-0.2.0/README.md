# controlplus

A package for analysis and design of Control Systems in python by Dr. Ahsen Tahir.

## Installation

```bash
$ pip install controlplus
```

## Usage

from controlplus.controlplus import find_rlocus, compensated_pole_from_ts, zero_compensator_tf, draw_overlay_rlocus

import control
import matplotlib.pyplot as plt




Forward path transfer function:

s = control.TransferFunction.s;
G = 1 / (s * (s + 4) * (s + 6))

Consider second order approximation:

damp_ratio = 0.504

Draw root locus with overlaying damping ratio lines with intersecting points/poles:

plt.figure(figsize=(8,6));
draw_overlay_rlocus(G, damp_ratio);
plt.show()

Desired settling time:

new_ts = 1.11

Find compensator pole for PD controller:

desired = compensated_pole_from_ts(new_ts, damp_ratio)

Get polynomial for zero compensator:

Gc = zero_compensator_tf(desired, G)

Final transfer function:

final_G = Gc * G

Find poles and respective gains for intersection of damping ratio line and root locus:

find_rlocus(G, damp_ratio)

Draw root locus with overlaying damping ratio lines with intersecting points/poles:

plt.figure(figsize=(8,6));
draw_overlay_rlocus(final_G, damp_ratio);
plt.show()

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`controlplus` was created by Dr. Ahsen Tahir. It is licensed under the terms of the GNU General Public License v3.0 license.

## Credits

`controlplus` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/).
