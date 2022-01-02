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

import pathlib

from mumailer import Attachment, Connection, Message, Recipient

from command_line_arguments import (ENCRYPTION_PROTOCOLS,
                                    get_command_line_options)


if __name__ == '__main__':
    options = get_command_line_options()

    message = Message(sender=Recipient.parse(options.sender),
                      reply_to=Recipient.parse(options.reply_to),
                      to=[Recipient.parse(option) for option in options.to],
                      cc=[Recipient.parse(option) for option in options.cc],
                      bcc=[Recipient.parse(option) for option in options.bcc],
                      subject=options.subject,
                      body=options.body,
                      use_html=options.html)
    message.add_attachment(Attachment.load_filename(
        filename=pathlib.Path(__file__).parent.parent / 'README.md',
        content_type='text/plain'))
    message.add_attachment(Attachment.load_filename(
        filename=pathlib.Path(__file__).parent.parent / 'LICENSE'))

    mailer = Connection(server=options.server,
                        port=options.port,
                        username=options.username,
                        password=options.password,
                        use_tls=False,
                        use_ssl=True)
    if encryption_protocol := ENCRYPTION_PROTOCOLS.get(options.encryption):
        mailer.set_encryption(protocol=encryption_protocol,
                              ciphers=options.ciphers)
    mailer.connect()
    mailer.send(message)
    mailer.disconnect()
