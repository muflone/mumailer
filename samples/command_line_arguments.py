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
import ssl

from mumailer.recipient import Recipient

ENCRYPTION_PROTOCOLS = {
    'SSLv23': ssl.PROTOCOL_SSLv23,
    'TLS_CLIENT': ssl.PROTOCOL_TLS_CLIENT,
    'TLS_SERVER': ssl.PROTOCOL_TLS_SERVER,
    'TLSv1': ssl.PROTOCOL_TLSv1,
    'TLSv1_1': ssl.PROTOCOL_TLSv1_1,
    'TLSv1_2': ssl.PROTOCOL_TLSv1_2,
}


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
    return parser.parse_args()
