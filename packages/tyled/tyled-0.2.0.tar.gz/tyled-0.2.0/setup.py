# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyled',
 'tyled.command',
 'tyled.tileset',
 'tyled.tileset.atlas',
 'tyled.tileset.collection',
 'tyled.tileset.orthogonal']

package_data = \
{'': ['*'],
 'tyled.tileset': ['atlas/templates/*',
                   'collection/templates/*',
                   'orthogonal/templates/*',
                   'templates/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'pillow>=9.3.0,<10.0.0',
 'rectpack>=0.2.2,<0.3.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['tyled = tyled.command:cli']}

setup_kwargs = {
    'name': 'tyled',
    'version': '0.2.0',
    'description': '',
    'long_description': "# Tyled :butterfly:\n\nCLI utility for generating [Tiled](https://www.mapeditor.org/) Tilesets\n\n:notebook: [Documentation](https://tyled.readthedocs.io/en/latest/)\n\n:package: [Package](https://pypi.org/project/tyled/)\n\n## Installation\n\n### From PyPI\n\n#### TLDR - do this at your own risk\n\n        pip install tyled\n\n#### Recommended - pipX\n\nIf you don't already have it installed go to https://pypi.org/project/pipx/ for instructions\n\n        pipx install tyled\n\n\n### From GitHub\n\nClone the repository\n\n        git clone https://github.com/kfields/tyled.git\n        \nNavigate to the new directory which contains the repository\n\n        cd tyled\n\nCreate a Python 3 virtual environment called `env`\n\n        python3 -m venv env\n        \nActivate the environment\n\n        source env/bin/activate\n        \nInstall required packages\n\n        pip install -r requirements.txt\n\n## Commands\n\n### Bake\n\n        tyled bake mytileset.toml [--save/--no-save][--show/--no-show][--rotation/--no-rotation]\n\n#### Options\n\nDefault options are --save, --no-show, --no-rotation\n\n## Projects\n\nTyled Projects are defined using TOML files.\n\nAll Projects must at least have a name and type\n\n```toml\nname = 'mytileset'\ntype = 'collection'\n```\n\n### Options\n\nOptions may be defined within the project file.  Any options defined here will override the command line options\n\n```toml\n[options]\nrotation = true\n```\n\n## Tilesets\n\nTyled currently supports three different kinds of Tilesets:\n\n### Collection Tileset\n\nA Collection Tileset is composed of tiles with images stored in separate files\n\n```toml\nname = 'mytileset'\ntype = 'collection'\n\nfirstgid = 1\nsource = 'sticker-knight/map'\n```\n\nThis example will generate mytileset.tsx in the current working directory\n\n### Orthogonal Tileset\n\nAn Orthogonal Tileset is composed of tiles that have the same dimensions in one image file\n\n```toml\nname = 'mytileset'\ntype = 'orthogonal'\n\nfirstgid = 1\nsource = 'platformer/tiles'\ntilewidth = 128\ntileheight = 128\nspacing = 0\nmargin = 0\ncolumns = 12\n```\n\nThis example will generate mytileset.tsx and mytileset.png in the current working directory\n\n### Atlas Tileset\n\nAn Atlas Tileset is composed of tiles that do not have the same dimensions in one image file\n\n```toml\nname = 'mytileset'\ntype = 'atlas'\n\nfirstgid = 0\nsource = 'sticker-knight/map'\nwidth = 1024\nheight = 1024\nspacing = 0\nmargin = 0\n```\n\nThis example will generate mytileset.tsx and mytileset.png in the current working directory\n",
    'author': 'Kurtis Fields',
    'author_email': 'kurtisfields@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
