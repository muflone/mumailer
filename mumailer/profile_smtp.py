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

import configparser

SECTION_SMTP = 'SMTP'
OPTION_SMTP_SERVER = 'SERVER'
OPTION_SMTP_PORT = 'PORT'
OPTION_SMTP_USERNAME = 'USERNAME'
OPTION_SMTP_PASSWORD = 'PASSWORD'
OPTION_SMTP_USE_TLS = 'TLS'
OPTION_SMTP_USE_SSL = 'SSL'
OPTION_SMTP_TIMEOUT = 'TIMEOUT'
OPTION_SMTP_ENCRYPTION = 'ENCRYPTION'
OPTION_SMTP_CIPHERS = 'CIPHERS'


class ProfileSmtp(object):
    def __init__(self, filename: str):
        self.config = configparser.RawConfigParser()
        self.config.optionxform = str
        self.config.read(filenames=filename)
        # Get options from profile file
        self.server = self.get_option(option=OPTION_SMTP_SERVER)
        self.port = int(self.get_option(option=OPTION_SMTP_PORT,
                                        default=25))
        self.username = self.get_option(option=OPTION_SMTP_USERNAME)
        self.password = self.get_option(option=OPTION_SMTP_PASSWORD)
        self.use_tls = bool(int(self.get_option(option=OPTION_SMTP_USE_TLS,
                                                default='0')))
        self.use_ssl = bool(int(self.get_option(option=OPTION_SMTP_USE_SSL,
                                                default='0')))
        self.encryption = self.get_option(option=OPTION_SMTP_ENCRYPTION)
        self.ciphers = self.get_option(option=OPTION_SMTP_CIPHERS)

    def get_option(self, option: str, default: str = None) -> str:
        """
        Get an option value from the profile with the section SMTP

        :param option: name for the option to get data
        :param default: default value if the option is not found
        :return: option value
        """
        return self.config.get(section=SECTION_SMTP,
                               option=option,
                               fallback=default)
