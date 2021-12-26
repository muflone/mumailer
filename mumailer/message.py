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
import datetime
import email.message
import email.utils
from typing import Optional

from .attachment import Attachment
from .recipient import Recipient


@dataclasses.dataclass
class Message(object):
    sender: Recipient
    subject: str
    body: str
    to: Optional[list[Recipient]] = None
    cc: Optional[list[Recipient]] = None
    bcc: Optional[list[Recipient]] = None
    reply_to: Optional[Recipient] = None
    use_html: bool = False
    date: Optional[datetime.datetime] = None
    attachments: Optional[list[Attachment]] = dataclasses.field(
        default_factory=lambda: [])

    def to_email_message(self) -> email.message.EmailMessage:
        """
        Create a new EmailMessage object with the fields from attributes

        :return: EmailMessage with the fields set
        """
        message = email.message.EmailMessage()
        message['From'] = str(self.sender)
        if self.reply_to:
            message['Reply-To'] = str(self.reply_to)
        if self.to:
            message['To'] = ', '.join(map(str, self.to))
        if self.cc:
            message['Cc'] = ', '.join(map(str, self.cc))
        if self.bcc:
            message['Bcc'] = ', '.join(map(str, self.bcc))
        message['Subject'] = self.subject
        message['Date'] = email.utils.formatdate(timeval=self.date)
        message.set_content(self.body,
                            subtype='html' if self.use_html else 'plain')
        if self.attachments:
            # Add attachments
            for attachment in self.attachments:
                maintype, subtype = attachment.content_type.split('/', 1)
                message.add_attachment(obj=attachment.content,
                                       maintype=maintype,
                                       subtype=subtype,
                                       filename=attachment.filename)
        return message

    def add_attachment(self,
                       attachment: Attachment) -> None:
        """
        Add a new Attachment object to the attachments list

        :param attachment: Attachment object to append
        """
        self.attachments.append(attachment)
