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

import ssl


ENCRYPTION_PROTOCOLS = {
    '': None,
    'SSLv23': ssl.PROTOCOL_SSLv23,
    'TLS_CLIENT': ssl.PROTOCOL_TLS_CLIENT,
    'TLS_SERVER': ssl.PROTOCOL_TLS_SERVER,
    'TLS': ssl.PROTOCOL_TLS,
    'TLSv1': ssl.PROTOCOL_TLSv1,
    'TLSv1_1': ssl.PROTOCOL_TLSv1_1,
    'TLSv1_2': ssl.PROTOCOL_TLSv1_2,
}
