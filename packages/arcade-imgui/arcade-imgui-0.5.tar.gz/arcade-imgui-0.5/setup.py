# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcade_imgui']

package_data = \
{'': ['*']}

install_requires = \
['arcade>=2.6,<2.8', 'imgui>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'arcade-imgui',
    'version': '0.5',
    'description': 'IMGUI integration for Python Arcade',
    'long_description': '# Arcade ImGui\n\n[The Python Arcade Library](https://arcade.academy/) + [pyimgui](https://github.com/swistakm/pyimgui) = :heart:\n\n:package: [Package](https://pypi.org/project/arcade-imgui/)\n\n## Prerequisite\n\nGet [Poetry](https://python-poetry.org/)\n\n## Clone\n\n```bash\ngit clone https://github.com/kfields/arcade-imgui.git\ncd arcade-imgui\npoetry shell\npoetry install\n```\n\n## Run an example\n```bash\ncd examples\npython basic.py\n```\n\n## Run the Demo\n```bash\ncd imdemo\npoetry install\npython imdemo\n```\n\n## Run the ImFlo Demo\n```bash\ncd imflo\npoetry install\npython imflo\n```',
    'author': 'Kurtis Fields',
    'author_email': 'kurtisfields@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kfields/arcade-imgui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
