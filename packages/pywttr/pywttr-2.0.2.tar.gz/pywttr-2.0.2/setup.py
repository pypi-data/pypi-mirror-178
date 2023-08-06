# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywttr']

package_data = \
{'': ['*']}

install_requires = \
['pywttr-models>=1.0,<2.0', 'requests>=2.28,<3.0']

setup_kwargs = {
    'name': 'pywttr',
    'version': '2.0.2',
    'description': 'Wrapper for wttr.in API',
    'long_description': '# pywttr\n\n[![CI](https://github.com/monosans/pywttr/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/monosans/pywttr/actions/workflows/ci.yml)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/monosans/pywttr/main.svg)](https://results.pre-commit.ci/latest/github/monosans/pywttr/main)\n[![codecov](https://codecov.io/gh/monosans/pywttr/branch/main/graph/badge.svg)](https://codecov.io/gh/monosans/pywttr)\n\nWrapper for [wttr.in](https://wttr.in) weather forecast API.\n\nAsynchronous version [here](https://github.com/monosans/aiopywttr).\n\n## Installation\n\n```bash\npython -m pip install pywttr\n```\n\n## Example\n\nThis example prints the average temperature in New York today.\n\n```python\nfrom pywttr import Wttr\n\nwttr = Wttr("New York")\nforecast = wttr.en()\nprint(forecast.weather[0].avgtemp_c)\n```\n\nOther languages may also be used instead of `en`. For a complete list of supported languages, follow the code completion in your IDE.\n\n## Documentation\n\nThere is no documentation, just follow the code completion in your IDE.\n\nFor an example of type annotations, see `pywttr-models` [README.md](https://github.com/monosans/pywttr-models#usage-for-type-annotation).\n\n## Recommended IDEs\n\n- [Visual Studio Code](https://code.visualstudio.com) (with [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python))\n- [PyCharm](https://jetbrains.com/pycharm)\n\n## License\n\n[MIT](https://github.com/monosans/pywttr/blob/main/LICENSE)\n',
    'author': 'monosans',
    'author_email': 'hsyqixco@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/monosans/pywttr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
