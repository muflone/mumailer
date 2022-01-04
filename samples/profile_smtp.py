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
                      CommandLineOptions,
                      Connection,
                      Message,
                      ProfileSmtp,
                      Recipient)


if __name__ == '__main__':
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
            content_type=command_line.get_attachment_content_type(
                index=index)))

    profile_smtp = ProfileSmtp(filename=options.profile_smtp)
    mailer = Connection(server=options.server or profile_smtp.server,
                        port=options.port or profile_smtp.port,
                        username=options.username or profile_smtp.username,
                        password=options.password or profile_smtp.password,
                        use_tls=profile_smtp.use_tls,
                        use_ssl=profile_smtp.use_ssl)
    if encryption := ENCRYPTION_PROTOCOLS.get(options.encryption or
                                              profile_smtp.encryption):
        mailer.set_encryption(protocol=encryption,
                              ciphers=options.ciphers or profile_smtp.ciphers)
    mailer.connect()
    mailer.send(message)
    mailer.disconnect()
