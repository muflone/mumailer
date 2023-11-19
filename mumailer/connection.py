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

import smtplib
import ssl
from typing import Optional

from .encryption import ENCRYPTION_PROTOCOLS
from .message import Message


class Connection(object):
    def __init__(self,
                 server: str,
                 port: int = 25,
                 username: str = None,
                 password: str = None):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.context = None
        self._use_ssl = False
        self._use_tls = False

    def set_encryption(self,
                       encryption: Optional[str],
                       ciphers: Optional[str] = '') -> None:
        """
        Set the encryption protocol and ciphers

        :param encryption: encryption method from ENCRYPTION_PROTOCOLS
        :param ciphers: encryption ciphers for the selected protocol
        """
        self._use_ssl = encryption.startswith('SSL') if encryption else False
        self._use_tls = encryption.startswith('TLS') if encryption else False
        if protocol := ENCRYPTION_PROTOCOLS.get(encryption):
            self.context = ssl.SSLContext(protocol=protocol)
            if ciphers:
                self.context.set_ciphers(ciphers)

    def connect(self,
                timeout: int = 30) -> None:
        """
        Connect to the SMTP server

        :param timeout: timeout in seconds before aborting the connection
        """
        if not self._use_ssl:
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
        if self._use_tls:
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
        self.connection.send_message(msg=message._to_email_message())
