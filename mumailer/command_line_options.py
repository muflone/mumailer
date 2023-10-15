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

import argparse
import pathlib
from typing import Optional

from .constants import APP_NAME, APP_VERSION, APP_DESCRIPTION
from .encryption import ENCRYPTION_PROTOCOLS
from .header import Header
from .recipient import Recipient


class CommandLineOptions(object):
    """
    Parse command line arguments
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=f'{APP_NAME}',
                                              description=APP_DESCRIPTION)
        self.parser.add_argument('-V',
                                 '--version',
                                 action='version',
                                 version=f'{APP_NAME} v{APP_VERSION}')

    def _recipient_type(self, option: str) -> Recipient:
        """
        Validate recipient type option

        :param option: recipient string in the form "Name address" or "address"
        :return: recipient string if the option is valid or raise
                 ArgumentTypeError
        """
        recipient = Recipient.parse(option)
        if '@' not in recipient.address:
            raise argparse.ArgumentTypeError(f'Invalid recipient {option}')
        return option

    def _header_type(self, option: str) -> Header:
        """
        Validate header type option

        :param option: header string in the form "Name=address"
        :return: header string if the option is valid or raise
                 ArgumentTypeError
        """
        header = Header.parse(option)
        if not header:
            raise argparse.ArgumentTypeError(f'Invalid header {option}')
        return option

    def add_group(self, name: str) -> argparse._ArgumentGroup:
        """
        Add a command-line options group

        :param name: name for the new group
        :return: _ArgumentGroup object with the new command-line options group
        """
        return self.parser.add_argument_group(name)

    def add_smtp_arguments(self) -> None:
        """
        Add SMTP command-line options
        """
        group = self.add_group('SMTP options')
        group.add_argument('--profile-smtp',
                           required=False,
                           type=str,
                           help='profile file with SMTP settings')
        group.add_argument('--server',
                           required=False,
                           type=str,
                           help='SMTP server address')
        group.add_argument('--port',
                           required=False,
                           type=int,
                           help='SMTP server port number')
        group.add_argument('--username',
                           required=False,
                           type=str,
                           help='SMTP authentication username')
        group.add_argument('--password',
                           required=False,
                           type=str,
                           help='SMTP authentication username')

    def add_encryption_arguments(self) -> None:
        """
        Add SMTP encryption command-line options
        """
        group = self.add_group('encryption')
        group.add_argument('--encryption',
                           required=False,
                           type=str,
                           choices=ENCRYPTION_PROTOCOLS.keys(),
                           help='encryption protocol')
        group.add_argument('--ciphers',
                           required=False,
                           type=str,
                           help='encryption ciphers')

    def add_recipients_arguments(self) -> None:
        """
        Add recipients command-line options
        """
        group = self.add_group('recipients')
        group.add_argument('--sender',
                           required=False,
                           type=self._recipient_type,
                           help='Sender name and address')
        group.add_argument('--reply_to',
                           required=False,
                           type=self._recipient_type,
                           help='Reply-to name and address')
        group.add_argument('--to',
                           required=False,
                           type=self._recipient_type,
                           default=[],
                           nargs=argparse.ZERO_OR_MORE,
                           help='Message recipient name and address')
        group.add_argument('--cc',
                           required=False,
                           type=self._recipient_type,
                           default=[],
                           nargs=argparse.ZERO_OR_MORE,
                           help='Message recipient name and address for CC')
        group.add_argument('--bcc',
                           required=False,
                           type=self._recipient_type,
                           default=[],
                           nargs=argparse.ZERO_OR_MORE,
                           help='Message recipient name and address for BCC')

    def add_message_arguments(self) -> None:
        """
        Add recipients command-line options
        """
        group = self.add_group('message')
        group.add_argument('--profile-message',
                           required=False,
                           type=str,
                           help='profile file with message settings')
        group.add_argument('--subject',
                           required=False,
                           type=str,
                           help='Message subject')
        group.add_argument('--body',
                           required=False,
                           type=str,
                           help='Message body')
        group.add_argument('--body-file',
                           required=False,
                           type=str,
                           help='Get message body from the specified file')
        group.add_argument('--html',
                           required=False,
                           action='store_true',
                           default=False,
                           help='Format message body as HTML')
        group.add_argument('--attachment',
                           required=False,
                           type=str,
                           default=[],
                           nargs=argparse.ZERO_OR_MORE,
                           help='File to attach to the message')
        group.add_argument('--content-type',
                           required=False,
                           type=str,
                           default=[],
                           nargs=argparse.ZERO_OR_MORE,
                           help='Content type list for attachments')
        group.add_argument('--header',
                           required=False,
                           type=str,
                           default=[],
                           nargs=argparse.ZERO_OR_MORE,
                           help='Additional header for the message')

    def parse_options(self) -> argparse.Namespace:
        """
        Parse command-line options

        :return: command-line options
        """
        self.options = self.parser.parse_args()
        # Check for missing options
        if not any(vars(self.options).values()):
            self.parser.print_help()
            self.parser.exit(1)
        # Check if profile-smtp or server/port arguments options are set
        if not self.options.profile_smtp and not all([self.options.server,
                                                      self.options.port]):
            raise argparse.ArgumentTypeError('Missing profile-smtp or '
                                             'server+port options')
        # Check if profile-message or sender argument option is set
        if not self.options.profile_message and not self.options.sender:
            raise argparse.ArgumentTypeError('Missing profile-message or '
                                             'sender option')
        # Check if the profile-smtp file exists
        if (self.options.profile_smtp and
                not pathlib.Path(self.options.profile_smtp).is_file()):
            raise argparse.ArgumentTypeError('The profile-smtp specified '
                                             'does not exist')
        # Check if the profile-message file exists
        if (self.options.profile_message and
                not pathlib.Path(self.options.profile_message).is_file()):
            raise argparse.ArgumentTypeError('The profile-message specified '
                                             'does not exist')

        # Check the content_type arguments
        # It must be one of the following:
        # - zero values = no content type
        # - one value = uses the same content type for every attachment
        # - more values = each attachment has its content type, the two lists
        #                 must have the same length
        if (self.options.content_type and len(self.options.content_type) not in
                (1, len(self.options.attachment))):
            raise argparse.ArgumentTypeError('Content type arguments must '
                                             'be 1 or in the same number for '
                                             'attachments')
        return self.options

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
        if self.options.content_type:
            if len(self.options.content_type) == 1:
                # Use the same content type for every attachment
                result = self.options.content_type[0]
            else:
                # Use the value from the content types list
                result = self.options.content_type[index]
        else:
            # No explicit content type
            result = None
        return result
