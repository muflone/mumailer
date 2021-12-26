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

from mumailer import Connection, Message, Recipient

from command_line_arguments import (ENCRYPTION_PROTOCOLS,
                                    get_command_line_options)


options = get_command_line_options()

message = Message(sender=Recipient(name='Muflone Ovinis',
                                   address='muflone@muflone.com'),
                  to=[Recipient(address='webreg@muflone.com')],
                  subject='Testing with SSL',
                  body='<html><body><h1>Hello world!</h1></body></html>',
                  use_html=True)

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
