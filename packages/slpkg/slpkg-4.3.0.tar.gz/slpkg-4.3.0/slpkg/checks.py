#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.blacklist import Blacklist


@dataclass
class Check:
    ''' Some checks before proceed. '''
    log_packages: str = Configs.log_packages
    sbo_repo_tag: str = Configs.sbo_repo_tag
    db_path: str = Configs.db_path
    database_name: str = Configs.database
    etc_path: str = Configs.etc_path

    def exists(self, slackbuilds: list):
        ''' Checking if the slackbuild exists in the repository. '''
        packages = []

        for sbo in slackbuilds:
            if not SBoQueries(sbo).slackbuild():
                packages.append(sbo)

        if packages:
            raise SystemExit(f'\nPackages {", ".join(packages)} '
                             'does not exists.\n')

    def unsupported(self, slackbuilds: list):
        ''' Checking for unsupported slackbuilds. '''
        for sbo in slackbuilds:
            sources = SBoQueries(sbo).sources()

            if 'UNSUPPORTED' in sources:
                raise SystemExit(f'\nPackage {sbo} unsupported by arch.\n')

    def installed(self, slackbuilds: list):
        ''' Checking for installed packages. '''

        for package in os.listdir(self.log_packages):
            for sbo in slackbuilds:

                if sbo + '-' in package and self.sbo_repo_tag in package:
                    return

        raise SystemExit('\nNot found installed packages.\n')

    def blacklist(self, slackbuilds: list):
        ''' Checking if the packages are blacklisted. '''
        packages = []
        black = Blacklist()

        for package in black.get():
            if package in slackbuilds:
                packages.append(package)

        if packages:
            raise SystemExit(
                f'\nThe packages \'{", ".join(packages)}\' is blacklisted.\n'
                f'Please edit the blacklist.yml file in {self.etc_path} '
                'folder.\n')

    def database(self):
        ''' Checking for empty table '''
        db = f'{self.db_path}/{self.database_name}'
        if not SBoQueries('').names() or not os.path.isfile(db):
            raise SystemExit('\nYou need to update the package lists first.\n'
                             'Please run slpkg update.\n')
