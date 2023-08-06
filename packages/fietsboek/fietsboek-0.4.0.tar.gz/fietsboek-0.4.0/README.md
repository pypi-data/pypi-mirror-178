Fietsboek
=========

Fietsboek is a self-hostable sharing site for GPX track recordings with social
features. The goal is to have an application like [MyTourbook][MyTourbook] that
runs as a web-service and allows sharing and discovering of new tracks.

Note that Fietsboek is early in development and a hobby project, as such many
features are still lacking.

[MyTourbook]: https://mytourbook.sourceforge.io/mytourbook/

Installation
------------

Setup instructions are in the documentation. You can either build it locally
using [Sphinx](https://www.sphinx-doc.org/), or view the generated version
online: https://kingdread.de/fietsboek/

Development
-----------

- Setup the environment:

      virtualenv .venv
      .venv/bin/pip install -e '.[testing]'

- Adjust `development.ini` to your needs
- Initialize the database:

      .venv/bin/alembic -c development.ini updgrade head
- Serve the code:

      .venv/bin/pserve development.ini --reload

- Hack away!

License
-------

    Fietsboek, the GPX web sharing project
    Copyright (C) 2022 Daniel Schadt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

