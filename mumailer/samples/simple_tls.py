#!/usr/bin/python3
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

from mumailer import (Attachment,
                      CommandLineOptions,
                      Connection,
                      Header,
                      Message,
                      Recipient)


def main():
    # Get command-line options
    command_line = CommandLineOptions()
    command_line.add_smtp_arguments()
    command_line.add_encryption_arguments()
    command_line.add_recipients_arguments()
    command_line.add_message_arguments()
    options = command_line.parse_options()

    # Get message body from body_file or body options
    if options.body_file:
        with open(options.body_file, 'r') as file:
            body = file.read()
    else:
        body = options.body
    message = Message(sender=Recipient.parse(options.sender),
                      reply_to=Recipient.parse(options.reply_to),
                      to=Recipient.parse_as_list(options.to),
                      cc=Recipient.parse_as_list(options.cc),
                      bcc=Recipient.parse_as_list(options.bcc),
                      subject=options.subject,
                      body=body,
                      use_html=options.html,
                      headers=Header.parse_as_list(options.header))
    # Add attachments
    for index, attachment_file in enumerate(options.attachment):
        message.add_attachment(Attachment.load_filename(
            filename=attachment_file,
            content_type=command_line.get_content_type(index=index)))

    mailer = Connection(server=options.server,
                        port=options.port,
                        username=options.username,
                        password=options.password)
    mailer.set_encryption(encryption=options.encryption,
                          ciphers=options.ciphers)
    mailer.connect()
    mailer.send(message)
    mailer.disconnect()


if __name__ == '__main__':
    main()
