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

from .profile import Profile

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


class ProfileSmtp(Profile):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.section_name = SECTION_SMTP
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
