# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typing_aliases']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.3.0']

setup_kwargs = {
    'name': 'typing-aliases',
    'version': '1.0.0',
    'description': 'Various type aliases.',
    'long_description': '# `typing-aliases`\n\n[![License][License Badge]][License]\n[![Version][Version Badge]][Package]\n[![Downloads][Downloads Badge]][Package]\n[![Discord][Discord Badge]][Discord]\n\n[![Documentation][Documentation Badge]][Documentation]\n[![Check][Check Badge]][Actions]\n[![Test][Test Badge]][Actions]\n[![Coverage][Coverage Badge]][Coverage]\n\n> *Various type aliases.*\n\n## Installing\n\n**Python 3.7 or above is required.**\n\n### pip\n\nInstalling the library with `pip` is quite simple:\n\n```console\n$ pip install typing-aliases\n```\n\nAlternatively, the library can be installed from source:\n\n```console\n$ git clone https://github.com/nekitdev/typing-aliases.git\n$ cd typing-aliases\n$ python -m pip install .\n```\n\n### poetry\n\nYou can add `typing-aliases` as a dependency with the following command:\n\n```console\n$ poetry add typing-aliases\n```\n\nOr by directly specifying it in the configuration like so:\n\n```toml\n[tool.poetry.dependencies]\ntyping-aliases = "^1.0.0"\n```\n\nAlternatively, you can add it directly from the source:\n\n```toml\n[tool.poetry.dependencies.typing-aliases]\ngit = "https://github.com/nekitdev/typing-aliases.git"\n```\n\n## Documentation\n\nYou can find the documentation [here][Documentation].\n\n## Support\n\nIf you need support with the library, you can send an [email][Email]\nor refer to the official [Discord server][Discord].\n\n## Changelog\n\nYou can find the changelog [here][Changelog].\n\n## Security Policy\n\nYou can find the Security Policy of `typing-aliases` [here][Security].\n\n## Contributing\n\nIf you are interested in contributing to `typing-aliases`, make sure to take a look at the\n[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].\n\n## License\n\n`typing-aliases` is licensed under the MIT License terms. See [License][License] for details.\n\n[Email]: mailto:support@nekit.dev\n\n[Discord]: https://nekit.dev/discord\n\n[Actions]: https://github.com/nekitdev/typing-aliases/actions\n\n[Changelog]: https://github.com/nekitdev/typing-aliases/blob/main/CHANGELOG.md\n[Code of Conduct]: https://github.com/nekitdev/typing-aliases/blob/main/CODE_OF_CONDUCT.md\n[Contributing Guide]: https://github.com/nekitdev/typing-aliases/blob/main/CONTRIBUTING.md\n[Security]: https://github.com/nekitdev/typing-aliases/blob/main/SECURITY.md\n\n[License]: https://github.com/nekitdev/typing-aliases/blob/main/LICENSE\n\n[Package]: https://pypi.org/project/typing-aliases\n[Coverage]: https://codecov.io/gh/nekitdev/typing-aliases\n[Documentation]: https://nekitdev.github.io/typing-aliases\n\n[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2\n[License Badge]: https://img.shields.io/pypi/l/typing-aliases\n[Version Badge]: https://img.shields.io/pypi/v/typing-aliases\n[Downloads Badge]: https://img.shields.io/pypi/dm/typing-aliases\n\n[Documentation Badge]: https://github.com/nekitdev/typing-aliases/workflows/docs/badge.svg\n[Check Badge]: https://github.com/nekitdev/typing-aliases/workflows/check/badge.svg\n[Test Badge]: https://github.com/nekitdev/typing-aliases/workflows/test/badge.svg\n[Coverage Badge]: https://codecov.io/gh/nekitdev/typing-aliases/branch/main/graph/badge.svg\n',
    'author': 'nekitdev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nekitdev/typing-aliases',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
