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

import smtplib
import ssl

from .message import Message


class Connection(object):
    def __init__(self,
                 server: str,
                 port: int = 25,
                 username: str = None,
                 password: str = None,
                 use_tls: bool = False,
                 use_ssl: bool = False):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        self.connection = None
        self.context = None

    def set_encryption(self,
                       protocol: ssl._SSLMethod,
                       ciphers: str = '') -> None:
        """
        Set the encryption protocol and ciphers

        :param protocol: encryption protocol
        :param ciphers: encryption ciphers for the selected protocol
        """
        self.context = ssl.SSLContext(protocol=protocol)
        if ciphers:
            self.context.set_ciphers(ciphers)

    def connect(self,
                timeout: int = 30) -> None:
        """
        Connect to the SMTP server

        :param timeout: timeout in seconds before aborting the connection
        """
        if not self.use_ssl:
            # Use plain text
            self.connection = smtplib.SMTP(host=self.server,
                                           port=self.port,
                                           timeout=timeout)
        else:
            # Use SSL
            self.connection = smtplib.SMTP_SSL(host=self.server,
                                               port=self.port,
                                               timeout=timeout,
                                               context=self.context)
        if self.use_tls:
            # Use TLS
            self.connection.starttls(context=self.context)
        if self.username:
            # Authenticate with user and password
            self.connection.login(user=self.username,
                                  password=self.password)

    def disconnect(self) -> None:
        """
        Disconnect from the SMTP server
        """
        self.connection.quit()

    def noop(self) -> None:
        """
        Command to not execute anything, only used to keep alive the connection
        """
        self.connection.noop()

    def send(self,
             message: Message) -> None:
        """
        Send message to the server

        :param message: Message object to send
        """
        self.connection.send_message(msg=message.to_email_message())
