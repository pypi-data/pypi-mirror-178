# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['id_translation',
 'id_translation.dio',
 'id_translation.fetching',
 'id_translation.offline']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1', 'rics==1.0.0', 'sqlalchemy>=1.0.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1']}

setup_kwargs = {
    'name': 'id-translation',
    'version': '0.1.0',
    'description': 'Convert IDs into human-readable labels.',
    'long_description': '<div align="center">\n  <img src="https://github.com/rsundqvist/rics/raw/master/docs/logo-text.png"><br>\n</div>\n\n-----------------\n\n# Convert IDs to human-readable labels. <!-- omit in toc -->\n[![PyPI - Version](https://img.shields.io/pypi/v/id-translation.svg)](https://pypi.python.org/pypi/id-translation)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/id-translation.svg)](https://pypi.python.org/pypi/id-translation)\n[![Tests](https://github.com/rsundqvist/id-translation/workflows/tests/badge.svg)](https://github.com/rsundqvist/id-translation/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/rsundqvist/id-translation/branch/main/graph/badge.svg)](https://codecov.io/gh/rsundqvist/id-translation)\n[![Read the Docs](https://readthedocs.org/projects/id-translation/badge/)](https://id-translation.readthedocs.io/)\n[![PyPI - License](https://img.shields.io/pypi/l/id-translation.svg)](https://pypi.python.org/pypi/id-translation)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n## What is it?\n\nA package suite for translating integer IDs typically found in databases. Translation is highly configurable and tested\nfor multiple different SQL dialects and schema naming paradigms. This is configurable using TOML, allowing power users\nto specify shared configurations that "just work" for regular users. See the example snippet below.\n\n```python\nfrom id_translation import Translator\n\ndef get_singleton() -> Translator:\n  """Returns pre-built Translator instance."""\n  return Translator.load_persistent_instance(\n    "/company/translation/config.toml",\n    extra_fetchers=["/company/translation/customer-database-config.toml"],\n    # Singleton is updated by a CRON job; regular users don\'t have write access.\n    max_age=None,  # None = never update\n  )\n```\n_A function to create [Translator][translate] instances that "just work"._\n\n## Highlighted Features\n\n- A highly configurable translation [format] strings.\n- Powerful automated [Name-to-source][n2s-mapping] and format [placeholder][pm-mapping] mapping, backed by the \n  [RiCS](https://rics.readthedocs.io/) library.\n- Prebuilt fetchers for [SQL][sql-fetcher] and [file-system][pandas-fetcher] sources.\n- Configure using [TOML][translator-config].\n- Support for [persistent] instances stored on disk.\n\n[translate]: https://id-translation.readthedocs.io/en/latest/_autosummary/id_translation.html#id_translation.Translator.translate\n[format]: https://id-translation.readthedocs.io/en/latest/_autosummary/id_translation.offline.html#id_translation.offline.Format\n[n2s-mapping]: https://id-translation.readthedocs.io/en/latest/documentation/translation-primer.html#name-to-source-mapping\n[pm-mapping]: https://id-translation.readthedocs.io/en/latest/documentation/translation-primer.html#placeholder-mapping\n[persistent]: https://id-translation.readthedocs.io/en/latest/_autosummary/id_translation.html#id_translation.Translator.load_persistent_instance\n[sql-fetcher]: https://id-translation.readthedocs.io/en/latest/_autosummary/id_translation.fetching.html#id_translation.fetching.SqlFetcher\n[pandas-fetcher]: https://id-translation.readthedocs.io/en/latest/_autosummary/id_translation.fetching.html#id_translation.fetching.PandasFetcher\n[translator-config]: https://id-translation.readthedocs.io/en/latest/documentation/translator-config.html\n\n\n## Installation\nThe package is published through the [Python Package Index (PyPI)]. Source code\nis available on GitHub: https://github.com/rsundqvist/id-translation\n\n```sh\npip install -U id-translation\n```\n\nThis is the preferred method to install ``id-translation``, as it will always install the\nmost recent stable release.\n\nIf you don\'t have [pip] installed, this [Python installation guide] can guide\nyou through the process.\n\n## License\n[MIT](LICENSE.md)\n\n## Documentation\nHosted on Read the Docs: https://id-translation.readthedocs.io\n\n## Contributing\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. To get \nstarted, see the [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).\n\n[Python Package Index (PyPI)]: https://pypi.org/project/id-translation\n[pip]: https://pip.pypa.io\n[Python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/\n',
    'author': 'Richard Sundqvist',
    'author_email': 'richard.sundqvist@live.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rsundqvist/id-translation',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
