# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fietsboek',
 'fietsboek.alembic',
 'fietsboek.alembic.versions',
 'fietsboek.models',
 'fietsboek.scripts',
 'fietsboek.updater',
 'fietsboek.updater.scripts',
 'fietsboek.views']

package_data = \
{'': ['*'],
 'fietsboek': ['locale/*',
               'locale/de/LC_MESSAGES/*',
               'locale/de/html/*',
               'locale/en/LC_MESSAGES/*',
               'locale/en/html/*',
               'static/*',
               'static/GM_Utils/*',
               'static/GM_Utils/Icons/*',
               'static/GM_Utils/leaflet/*',
               'static/GM_Utils/leaflet/images/*',
               'static/fonts/*',
               'templates/*']}

install_requires = \
['Babel>=2.11,<3.0',
 'Click>=8.1,<9.0',
 'SQLAlchemy>=1.4,<2.0',
 'alembic>=1.8,<2.0',
 'bleach>=5,<6',
 'cryptography>=38,<39',
 'gpxpy>=1.5,<2.0',
 'importlib_metadata>=5.0.0,<6.0.0',
 'importlib_resources>=5.10,<6.0',
 'markdown>=3.4,<4.0',
 'pyramid>=2,<3',
 'pyramid_debugtoolbar>=4.9,<5.0',
 'pyramid_jinja2>=2.10,<3.0',
 'pyramid_retry>=2.1,<3.0',
 'pyramid_tm>=2.5,<3.0',
 'redis>=4.3.4,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'transaction>=3,<4',
 'waitress>=2.1,<3.0',
 'zope.sqlalchemy>=1.6,<2.0']

extras_require = \
{'testing': ['WebTest>=3,<4', 'pytest>=7.2,<8.0', 'pytest-cov']}

entry_points = \
{'console_scripts': ['fietsctl = fietsboek.scripts.fietsctl:main',
                     'fietsupdate = fietsboek.updater.cli:cli'],
 'paste.app_factory': ['main = fietsboek:main']}

setup_kwargs = {
    'name': 'fietsboek',
    'version': '0.4.0',
    'description': 'GPX file sharing website',
    'long_description': "Fietsboek\n=========\n\nFietsboek is a self-hostable sharing site for GPX track recordings with social\nfeatures. The goal is to have an application like [MyTourbook][MyTourbook] that\nruns as a web-service and allows sharing and discovering of new tracks.\n\nNote that Fietsboek is early in development and a hobby project, as such many\nfeatures are still lacking.\n\n[MyTourbook]: https://mytourbook.sourceforge.io/mytourbook/\n\nInstallation\n------------\n\nSetup instructions are in the documentation. You can either build it locally\nusing [Sphinx](https://www.sphinx-doc.org/), or view the generated version\nonline: https://kingdread.de/fietsboek/\n\nDevelopment\n-----------\n\n- Setup the environment:\n\n      virtualenv .venv\n      .venv/bin/pip install -e '.[testing]'\n\n- Adjust `development.ini` to your needs\n- Initialize the database:\n\n      .venv/bin/alembic -c development.ini updgrade head\n- Serve the code:\n\n      .venv/bin/pserve development.ini --reload\n\n- Hack away!\n\nLicense\n-------\n\n    Fietsboek, the GPX web sharing project\n    Copyright (C) 2022 Daniel Schadt\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU Affero General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU Affero General Public License for more details.\n\n    You should have received a copy of the GNU Affero General Public License\n    along with this program.  If not, see <https://www.gnu.org/licenses/>.\n\n",
    'author': 'Daniel Schadt',
    'author_email': 'fietsboek@kingdread.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/dunj3/fietsboek',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
