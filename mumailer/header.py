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

import dataclasses


@dataclasses.dataclass
class Header(object):
    name: str
    value: str

    def __str__(self):
        """
        Format the header in email format (name: value)

        :return: header formatted value
        """
        return (f'{self.name}: {self.value}')

    @staticmethod
    def parse(header: str) -> 'Header':
        """
        Parse a header in a Header object

        :param data: option in the form name=value
        :return: Header object
        """
        if header is None:
            result = None
        else:
            if '=' in header:
                name, value = header.split(sep='=',
                                           maxsplit=1)
                result = Header(name=name,
                                value=value)
            else:
                result = None
        return result

    @staticmethod
    def parse_as_list(headers: list[str]) -> list['Header']:
        """
        Parse a list of headers as a Headers list

        :param headers: list to extract headers
        :return: Headers list object
        """
        return list(map(Header.parse, headers))
