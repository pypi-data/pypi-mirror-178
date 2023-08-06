# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_plugin_no_content_hash']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2,<2.0']

entry_points = \
{'poetry.plugin': ['export = '
                   'poetry_plugin_no_content_hash.plugin:NoContentHashPlugin']}

setup_kwargs = {
    'name': 'poetry-plugin-no-content-hash',
    'version': '1.0.0',
    'description': 'Poetry plugin to remove the content hash',
    'long_description': "# Poetry Plugin: No Content Hash\n\nThis package is a plugin that removes the content hash mechanism of Poetry.\n\n## Rationale\n\n- The hash causes conflicts all the time (https://github.com/python-poetry/poetry/issues/496)\n- Rust's Cargo had the same problem for a while (https://github.com/rust-lang/cargo/pull/7070)\n",
    'author': 'Marcel Jackwerth',
    'author_email': 'marceljackwerth@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
