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

from typing import Optional

from .yaml_profile import YamlProfile


class ProfileMessage(YamlProfile):
    SECTION = 'MESSAGE'
    SENDER = 'SENDER'
    TO = 'TO'
    CC = 'CC'
    BCC = 'BCC'
    REPLY_TO = 'REPLY_TO'
    SUBJECT = 'SUBJECT'
    BODY = 'BODY'
    BODY_FILE = 'BODY_FILE'
    USE_HTML = 'HTML'
    DATE = 'DATE'
    ATTACHMENTS = 'ATTACHMENTS'
    CONTENT_TYPES = 'CONTENT_TYPES'
    HEADERS = 'HEADERS'

    def __init__(self, filename: str):
        super().__init__(filename)
        self.section_name = self.SECTION
        # Get options from profile file
        self.sender = self.get_option(option=self.SENDER)
        self.to = self.get_option(option=self.TO,
                                  default=[])
        self.cc = self.get_option(option=self.CC,
                                  default=[])
        self.bcc = self.get_option(option=self.BCC,
                                   default=[])
        self.reply_to = self.get_option(option=self.REPLY_TO)
        self.subject = self.get_option(option=self.SUBJECT)
        self.body = self.get_option(option=self.BODY)
        self.body_file = self.get_option(option=self.BODY_FILE)
        self.use_html = self.get_option(option=self.USE_HTML,
                                        default=False)
        self.date = self.get_option(option=self.DATE)
        self.attachments = self.get_option(option=self.ATTACHMENTS,
                                           default=[])
        self.content_types = self.get_option(option=self.CONTENT_TYPES,
                                             default=[])
        self.headers = self.get_option(option=self.HEADERS,
                                       default=[])

    def get_content_type(self, index: int) -> Optional[str]:
        """
        Get the content type for attachments

        If the content_types list is empty returns no content type
        If the content_types list has a single value use that for every
        attachment else use the matching content_type for the attachment index

        :param content_types: list of content types
        :param index: content type index to lookup
        :return: matching content type with the previous rules
        """
        if self.content_types:
            if len(self.content_types) == 1:
                # Use the same content type for every attachment
                result = self.content_types[0]
            else:
                # Use the value from the content types list
                result = self.content_types[index]
        else:
            # No explicit content type
            result = None
        return result
