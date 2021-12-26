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
import pathlib


@dataclasses.dataclass
class Attachment(object):
    filename: str
    content: bytes
    charset: str = None
    content_type: str = None

    @classmethod
    def load_filename(self,
                      filename: str,
                      content_type='application/octet-stream') -> 'Attachment':
        """
        Load an attachment from a file

        :param filename: filename to load data from
        :param content_type: attachment content type
        :return:
        """
        with open(filename, 'rb') as file:
            content = file.read()
        return Attachment(filename=pathlib.Path(filename).name,
                          content=content,
                          content_type=content_type)
