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

import argparse
from typing import Optional

from mumailer import ENCRYPTION_PROTOCOLS, Recipient


def recipient_type(option) -> Recipient:
    """
    Validate recipient type option

    :param option: recipient string in the form "Name address" or "address"
    :return: recipient string if the option is valid or raise ArgumentTypeError
    """
    recipient = Recipient.parse(option)
    if '@' not in recipient.address:
        raise argparse.ArgumentTypeError(f'Invalid recipient {option}')
    return option


def get_attachment_content_type(content_types: list[str],
                                index: int) -> Optional[str]:
    """
    Get the content type for attachments

    If the content_types list is empty returns no content type
    If the content_types list has a single value use that for every attachment
    else use the matching content_type for the attachment index

    :param content_types: list of content types
    :param index: content type index to lookup
    :return: matching content type with the previous rules
    """
    if content_types:
        if len(content_types) == 1:
            # Use the same content type for every attachment
            result = content_types[0]
        else:
            # Use the value from the content types list
            result = content_types[index]
    else:
        # No explicit content type
        result = None
    return result


def get_command_line_options() -> argparse.Namespace:
    """
    Parse command line arguments

    :return: argparse.Namespace object with the command line options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--server',
                        required=True,
                        type=str,
                        help='SMTP server address')
    parser.add_argument('--port',
                        required=True,
                        type=int,
                        help='SMTP server port number')
    parser.add_argument('--username',
                        required=False,
                        type=str,
                        help='SMTP authentication username')
    parser.add_argument('--password',
                        required=False,
                        type=str,
                        help='SMTP authentication username')

    group = parser.add_argument_group('recipients')
    group.add_argument('--sender',
                       required=True,
                       type=recipient_type,
                       help='Sender name and address')
    group.add_argument('--reply_to',
                       required=False,
                       type=recipient_type,
                       help='Reply-to name and address')
    group.add_argument('--to',
                       required=False,
                       type=recipient_type,
                       default=[],
                       nargs=argparse.ZERO_OR_MORE,
                       help='Message recipient name and address')
    group.add_argument('--cc',
                       required=False,
                       type=recipient_type,
                       default=[],
                       nargs=argparse.ZERO_OR_MORE,
                       help='Message recipient name and address for CC')
    group.add_argument('--bcc',
                       required=False,
                       type=recipient_type,
                       default=[],
                       nargs=argparse.ZERO_OR_MORE,
                       help='Message recipient name and address for BCC')

    group = parser.add_argument_group('message')
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

    group = parser.add_argument_group('encryption')
    group.add_argument('--encryption',
                       required=False,
                       type=str,
                       choices=ENCRYPTION_PROTOCOLS.keys(),
                       help='encrypion protocol')
    group.add_argument('--ciphers',
                       required=False,
                       type=str,
                       help='encryption ciphers')
    options = parser.parse_args()
    # Check the content_type arguments
    # It must be one of the following:
    # - zero values = no content type
    # - one value = uses the same content type for every attachment
    # - more values = each attachment has its content type, the two lists must
    #                 have the same length
    if (options.content_type and
            len(options.content_type) not in (1, len(options.attachment))):
        raise argparse.ArgumentTypeError('Content type arguments must be 1 or '
                                         'in the same number for attachments')
    return options
