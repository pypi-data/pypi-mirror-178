# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['controlplus']

package_data = \
{'': ['*']}

install_requires = \
['control>=0.9.2', 'matplotlib>=3.6.2', 'numpy>=1.23.5']

setup_kwargs = {
    'name': 'controlplus',
    'version': '0.2.0',
    'description': 'A package for analysis and design of Control Systems in python.',
    'long_description': '# controlplus\n\nA package for analysis and design of Control Systems in python by Dr. Ahsen Tahir.\n\n## Installation\n\n```bash\n$ pip install controlplus\n```\n\n## Usage\n\nfrom controlplus.controlplus import find_rlocus, compensated_pole_from_ts, zero_compensator_tf, draw_overlay_rlocus\n\nimport control\nimport matplotlib.pyplot as plt\n\n\n\n\nForward path transfer function:\n\ns = control.TransferFunction.s;\nG = 1 / (s * (s + 4) * (s + 6))\n\nConsider second order approximation:\n\ndamp_ratio = 0.504\n\nDraw root locus with overlaying damping ratio lines with intersecting points/poles:\n\nplt.figure(figsize=(8,6));\ndraw_overlay_rlocus(G, damp_ratio);\nplt.show()\n\nDesired settling time:\n\nnew_ts = 1.11\n\nFind compensator pole for PD controller:\n\ndesired = compensated_pole_from_ts(new_ts, damp_ratio)\n\nGet polynomial for zero compensator:\n\nGc = zero_compensator_tf(desired, G)\n\nFinal transfer function:\n\nfinal_G = Gc * G\n\nFind poles and respective gains for intersection of damping ratio line and root locus:\n\nfind_rlocus(G, damp_ratio)\n\nDraw root locus with overlaying damping ratio lines with intersecting points/poles:\n\nplt.figure(figsize=(8,6));\ndraw_overlay_rlocus(final_G, damp_ratio);\nplt.show()\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`controlplus` was created by Dr. Ahsen Tahir. It is licensed under the terms of the GNU General Public License v3.0 license.\n\n## Credits\n\n`controlplus` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/).\n',
    'author': 'Dr. Ahsen Tahir',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://controlplus.readthedocs.io/en/latest/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
