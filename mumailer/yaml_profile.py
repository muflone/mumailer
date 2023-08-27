##
#     Project: MuMailer
# Description: Simple mailer agent using SMTP
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2023 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from typing import Any

import yaml


class YamlProfile(object):
    def __init__(self, filename: str):
        self.section_name = ''
        with open(filename, 'r') as file:
            self.config = yaml.load(stream=file,
                                    Loader=yaml.Loader)

    def get_option(self, option: str, default: Any = None) -> Any:
        """
        Get an option value from the profile with the section in
        `self.section_name`

        :param option: name for the option to get data
        :param default: default value if the option is not found
        :return: option value
        """
        return self.config[self.section_name].get(option,
                                                  default)
