##
#     Project: MuMailer
# Description: Simple mailer agent using SMTP
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021 Fabio Castelli
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

from .yaml_profile import YamlProfile


class ProfileSmtp(YamlProfile):
    SECTION = 'SMTP'
    OPTION_SERVER = 'SERVER'
    OPTION_PORT = 'PORT'
    OPTION_USERNAME = 'USERNAME'
    OPTION_PASSWORD = 'PASSWORD'
    OPTION_USE_TLS = 'TLS'
    OPTION_USE_SSL = 'SSL'
    OPTION_TIMEOUT = 'TIMEOUT'
    OPTION_ENCRYPTION = 'ENCRYPTION'
    OPTION_CIPHERS = 'CIPHERS'

    def __init__(self, filename: str):
        super().__init__(filename)
        self.section_name = self.SECTION
        # Get options from profile file
        self.server = self.get_option(option=self.OPTION_SERVER)
        self.port = self.get_option(option=self.OPTION_PORT,
                                    default=25)
        self.username = self.get_option(option=self.OPTION_USERNAME)
        self.password = self.get_option(option=self.OPTION_PASSWORD)
        self.use_tls = self.get_option(option=self.OPTION_USE_TLS,
                                       default=False)
        self.use_ssl = self.get_option(option=self.OPTION_USE_SSL,
                                       default=False)
        self.encryption = self.get_option(option=self.OPTION_ENCRYPTION)
        self.ciphers = self.get_option(option=self.OPTION_CIPHERS)
