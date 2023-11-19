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

from types import SimpleNamespace
from typing import Union

from mumailer import (Attachment,
                      CommandLineOptions,
                      Connection,
                      Header,
                      Message,
                      ProfileMessage,
                      ProfileSmtp,
                      Recipient)


def choose_option(profile: Union[ProfileSmtp, ProfileMessage],
                  cmdline: CommandLineOptions,
                  options: Union[str, tuple[str]]) -> Union[None, str, int]:
    """
    Get option from both a ProfileSmtp or command-line

    :param profile: ProfileSmtp or ProfileMessage object
    :param cmdline: CommandLineOptions object
    :param options: option names in profile and cmdline object
    :return: matching option value
    """
    if isinstance(options, (tuple, list)):
        cmdline_option = options[0]
        profile_option = options[1]
    else:
        cmdline_option = options
        profile_option = options
    value = getattr(cmdline.options, cmdline_option)
    if profile and value in (None, []):
        value = getattr(profile, profile_option)
    return value


def merge_options(cmdline: CommandLineOptions) -> SimpleNamespace:
    result = {}
    # Get available options from both command line and SMTP profile
    profile = (ProfileSmtp(filename=cmdline.options.profile_smtp)
               if cmdline.options.profile_smtp
               else None)
    for option in ('server', 'port', 'username', 'password',
                   'encryption', 'ciphers'):
        result[option] = choose_option(profile=profile,
                                       cmdline=cmdline,
                                       options=option)
    # Get available options from both command line and Message profile
    profile = (ProfileMessage(filename=cmdline.options.profile_message)
               if cmdline.options.profile_message
               else None)
    for option in ('sender', 'to', 'cc', 'bcc', 'reply_to',
                   'subject', 'body', 'body_file'):
        result[option] = choose_option(profile=profile,
                                       cmdline=cmdline,
                                       options=option)
    # Options with different names
    for option in (('html', 'use_html'),
                   ('attachment', 'attachments'),
                   ('content_type', 'content_types'),
                   ('header', 'headers')):
        result[option[1]] = choose_option(profile=profile,
                                          cmdline=cmdline,
                                          options=option)
    return SimpleNamespace(**result)


def main():
    # Get command-line options
    command_line = CommandLineOptions()
    command_line.add_smtp_arguments()
    command_line.add_encryption_arguments()
    command_line.add_recipients_arguments()
    command_line.add_message_arguments()
    command_line.parse_options()
    options = merge_options(cmdline=command_line)
    # Get message body from body_file or body options
    if options.body_file:
        with open(options.body_file, 'r') as file:
            body = file.read()
    else:
        body = options.body
    message = Message(
        sender=Recipient.parse(options.sender),
        reply_to=Recipient.parse(options.reply_to),
        to=Recipient.parse_as_list(options.to),
        cc=Recipient.parse_as_list(options.cc),
        bcc=Recipient.parse_as_list(options.bcc),
        subject=options.subject,
        body=body,
        use_html=options.use_html,
        headers=Header.parse_as_list(options.headers)
    )
    # Add attachments
    for index, attachment_file in enumerate(options.attachments):
        content_type = (options.content_type[0]
                        if len(options.content_types) == 1
                        else options.content_types[index])
        message.add_attachment(Attachment.load_filename(
            filename=attachment_file,
            content_type=content_type))
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
