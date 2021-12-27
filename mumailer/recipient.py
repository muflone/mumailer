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

import dataclasses


@dataclasses.dataclass
class Recipient(object):
    name: str = None
    address: str = ''

    def __str__(self):
        """
        Format the recipient in email format ("name" <address>)

        :return: recipient address formatted as a string
        """
        return (f'"{self.name}" <{self.address}>'
                if self.name
                else f'<{self.address}>')

    @classmethod
    def parse(self, address: str) -> 'Recipient':
        """
        Parse an address in a Recipient object
        Can receive both "Name email" or "email" only

        :param address: option to extract recipient address
        :return: Recipient object
        """
        if address is None:
            result = None
        else:
            if ' ' in address:
                name, email = address.rsplit(' ', 1)
            else:
                name = None
                email = address
            result = Recipient(name=name,
                               address=email)
        return result
