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

from mumailer import (ENCRYPTION_PROTOCOLS,
                      Attachment,
                      Connection,
                      Message,
                      Recipient)

from command_line_arguments import (get_attachment_content_type,
                                    get_command_line_options)


if __name__ == '__main__':
    options = get_command_line_options()

    # Get message body from body_file or body options
    if options.body_file:
        with open(options.body_file, 'r') as file:
            body = file.read()
    else:
        body = options.body
    message = Message(sender=Recipient.parse(options.sender),
                      reply_to=Recipient.parse(options.reply_to),
                      to=[Recipient.parse(option) for option in options.to],
                      cc=[Recipient.parse(option) for option in options.cc],
                      bcc=[Recipient.parse(option) for option in options.bcc],
                      subject=options.subject,
                      body=body,
                      use_html=options.html)
    # Add attachments
    for index, attachment_file in enumerate(options.attachment):
        message.add_attachment(Attachment.load_filename(
            filename=attachment_file,
            content_type=get_attachment_content_type(
                content_types=options.content_type,
                index=index)))

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
