# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orderings']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'orderings',
    'version': '1.0.0',
    'description': 'Ordering enumeration and protocols.',
    'long_description': '# `orderings`\n\n[![License][License Badge]][License]\n[![Version][Version Badge]][Package]\n[![Downloads][Downloads Badge]][Package]\n[![Discord][Discord Badge]][Discord]\n\n[![Documentation][Documentation Badge]][Documentation]\n[![Check][Check Badge]][Actions]\n[![Test][Test Badge]][Actions]\n[![Coverage][Coverage Badge]][Coverage]\n\n> *Ordering enumeration and protocols.*\n\n## Installing\n\n**Python 3.7 or above is required.**\n\n### pip\n\nInstalling the library with `pip` is quite simple:\n\n```console\n$ pip install orderings\n```\n\nAlternatively, the library can be installed from source:\n\n```console\n$ git clone https://github.com/nekitdev/orderings.git\n$ cd orderings\n$ python -m pip install .\n```\n\n### poetry\n\nYou can add `orderings` as a dependency with the following command:\n\n```console\n$ poetry add orderings\n```\n\nOr by directly specifying it in the configuration like so:\n\n```toml\n[tool.poetry.dependencies]\norderings = "^1.0.0"\n```\n\nAlternatively, you can add it directly from the source:\n\n```toml\n[tool.poetry.dependencies.orderings]\ngit = "https://github.com/nekitdev/orderings.git"\n```\n\n## Examples\n\n### Core\n\nThe core of `orderings` is the [`Ordering`][orderings.core.Ordering] enumeration\nand the [`Compare`][orderings.core.Compare] protocol:\n\n```python\nfrom attrs import frozen\nfrom orderings import Compare, Ordering\n\nI = TypeVar("I", bound="Int")\n\n\n@frozen()\nclass Int(Compare):\n    value: int\n\n    def compare(self: I, other: I) -> Ordering:\n        self_value = self.value\n        other_value = other.value\n\n        if self_value < other_value:\n            return Ordering.LESS\n\n        if self_value > other_value:\n            return Ordering.GREATER\n\n        return Ordering.EQUAL\n```\n\n[`Compare`][orderings.core.Compare] implements all ordering operations\n(`==`, `!=`, `<`, `>`, `<=`, `>=`) using the [`compare`][orderings.core.Compare.compare] method.\n\n## Documentation\n\nYou can find the documentation [here][Documentation].\n\n## Support\n\nIf you need support with the library, you can send an [email][Email]\nor refer to the official [Discord server][Discord].\n\n## Changelog\n\nYou can find the changelog [here][Changelog].\n\n## Security Policy\n\nYou can find the Security Policy of `orderings` [here][Security].\n\n## Contributing\n\nIf you are interested in contributing to `orderings`, make sure to take a look at the\n[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].\n\n## License\n\n`orderings` is licensed under the MIT License terms. See [License][License] for details.\n\n[Email]: mailto:support@nekit.dev\n\n[Discord]: https://nekit.dev/discord\n\n[Actions]: https://github.com/nekitdev/orderings/actions\n\n[Changelog]: https://github.com/nekitdev/orderings/blob/main/CHANGELOG.md\n[Code of Conduct]: https://github.com/nekitdev/orderings/blob/main/CODE_OF_CONDUCT.md\n[Contributing Guide]: https://github.com/nekitdev/orderings/blob/main/CONTRIBUTING.md\n[Security]: https://github.com/nekitdev/orderings/blob/main/SECURITY.md\n\n[License]: https://github.com/nekitdev/orderings/blob/main/LICENSE\n\n[Package]: https://pypi.org/project/orderings\n[Coverage]: https://codecov.io/gh/nekitdev/orderings\n[Documentation]: https://nekitdev.github.io/orderings\n\n[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2\n[License Badge]: https://img.shields.io/pypi/l/orderings\n[Version Badge]: https://img.shields.io/pypi/v/orderings\n[Downloads Badge]: https://img.shields.io/pypi/dm/orderings\n\n[Documentation Badge]: https://github.com/nekitdev/orderings/workflows/docs/badge.svg\n[Check Badge]: https://github.com/nekitdev/orderings/workflows/check/badge.svg\n[Test Badge]: https://github.com/nekitdev/orderings/workflows/test/badge.svg\n[Coverage Badge]: https://codecov.io/gh/nekitdev/orderings/branch/main/graph/badge.svg\n\n[orderings.core.Compare]: https://nekitdev.github.io/orderings/reference/core#orderings.core.Compare\n[orderings.core.Compare.compare]: https://nekitdev.github.io/orderings/reference/core#orderings.core.Compare.compare\n[orderings.core.Ordering]: https://nekitdev.github.io/orderings/reference/core#orderings.core.Ordering\n',
    'author': 'nekitdev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nekitdev/orderings',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
