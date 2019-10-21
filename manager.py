#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import (Migrate, MigrateCommand)

import settings
import apps
from apps import create_app


def main():
    main_app = create_app()
    manager = Manager(main_app)
    Migrate(main_app, apps.db)
    manager.add_command('db', MigrateCommand)
    manager.run()


if __name__ == '__main__':
    main()