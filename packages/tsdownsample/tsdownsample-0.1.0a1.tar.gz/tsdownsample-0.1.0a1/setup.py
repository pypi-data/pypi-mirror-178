# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsdownsample']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21', 'pandas>=1.3']

setup_kwargs = {
    'name': 'tsdownsample',
    'version': '0.1.0a1',
    'description': 'Time series downsampling in rust',
    'long_description': '# tsdownsample\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/tsdownsample.svg)](https://pypi.org/project/tsdownsample/)\n[![support-version](https://img.shields.io/pypi/pyversions/tsdownsample)](https://img.shields.io/pypi/pyversions/tsdownsample)\n[![Downloads](https://pepy.tech/badge/tsdownsample)](https://pepy.tech/project/tsdownsample)\n<!-- [![Testing](https://github.com/predict-idlab/tsflex/actions/workflows/test.yml/badge.svg)](https://github.com/predict-idlab/tsflex/actions/workflows/test.yml) -->\n\n**📈 Time series downsampling** algorithms for visualization\n\n## Features ✨\n\n* **Fast**: written in rust with pyo3 bindings  \n  - leverages optimized [argminmax](https://github.com/jvdd/argminmax) - which is SIMD accelerated with runtime feature detection\n  - scales linearly with the number of data points\n  - scales multi-threaded with rayon (rust)\n* **Efficient**: memory efficient\n  - works on views of the data (no copies)\n  - no intermediate data structures are created\n* **Flexible**: works on any type of data\n    - supported datatypes are `f16`, `f32`, `f64`, `i16`, `i32`, `i64`, `u16`, `u32`, `u64`  \n    *!! 🚀 `f16` [argminmax](https://github.com/jvdd/argminmax) is 200-300x faster than numpy*\n* **Easy to use**: simple API\n\n## Install\n\n> ❗🚨❗ This package is currently under development - no stable release yet ❗🚨❗\n\n\n```bash\npip install tsdownsample\n```\n\n## Usage\n\n```python\nimport tsdownsample as tsds\nimport pandas as pd; import numpy as np\n\n# Create a time series\ny = np.random.randn(10_000_000)\ns = pd.Series(y)\n\n# Downsample to 1000 points\ns_ds = tsds.minmaxlttb(s, n_out=1000)\n```\n\n---\n\n<p align="center">\n👤 <i>Jeroen Van Der Donckt</i>\n</p>',
    'author': 'Jeroen Van Der Donckt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/predict-idlab/tsdownsample',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}
from setup import *
build(setup_kwargs)

setup(**setup_kwargs)
