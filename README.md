# MuMailer

[![Travis CI Build Status](https://img.shields.io/travis/com/muflone/mumailer/master.svg)](https://www.travis-ci.com/github/muflone/mumailer)
[![CircleCI Build Status](https://img.shields.io/circleci/project/github/muflone/mumailer/master.svg)](https://circleci.com/gh/muflone/mumailer)
[![PyPI - Version](https://img.shields.io/pypi/v/MuMailer.svg)](https://pypi.org/project/MuMailer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/MuMailer.svg)](https://pypi.org/project/MuMailer/)

**Description:** Simple mailer agent using SMTP

**Copyright:** 2021-2023 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/mumailer

**Documentation:** http://www.muflone.com/mumailer/

# Description

MuMailer is a simple mail transfer agent (MTA) to send email messages
from Python or from command line arguments, using multiple profiles to
configure arguments.

Please see below and the **samples** folder for some usage examples.

# System Requirements

* Python 3.x
* PyYAML 6.x (https://pypi.org/project/PyYAML/)

# Basic usage

To use MuMailer from Python you have to instance a **Connection** and a
**Message** objects and then execute the send method on the connection
object passing the message object.

The Connection object refers to the SMTP server connection and it will require
the SMTP server data (server, port, username, password, encryption).

The Message object will contain the information needed to send a single message
(sender, recipients, subject, body, attachments).

For sender, reply-to, to, cc and bcc arguments you need to pass some
Recipient objects with an email address and optionally a name (pass None if you
don't want to specify the recipient name).

See the following example:

```python
from mumailer import Connection, Message, Recipient

message = Message(sender=Recipient('Muflone', 'muflone@example.com'),
                  to=[Recipient('Foo', 'foo@example.com')],
                  cc=[Recipient('Bar', 'bar@example.com')],
                  subject='Test e-mail',
                  body='<html><body><h1>Hello world!</h1></body></html>',
                  use_html=True)
connection = Connection(server='localhost',
                        port=587,
                        username='<username>',
                        password='<smtp password>')
connection.connect()
connection.send(message)
connection.disconnect()
```

The previous code will prepare a message from *Muflone* and will send the
message to *Foo*, adding *Bar* to the CC (carbon copy) list, using the subject
*Test e-mail* with the HTML body **Hello world!**.

The SMTP connection will be established to the localhost server on the TCP port
587 (the server must be running) using username and password authentication.
The SMTP data will be encrypted using the TLS protocol.

## Adding attachments

A Message object can have one or more attachments being sent along with the
message body.

To add an attachment to the Message object you have to instance an
**Attachment** object from which you can set its content (as binary data) or
load it from a file.

The class method load_filename will return an Attachment object with the file
content.

```python
from mumailer import Attachment

pdf_attachment = Attachment.load_filename(filename='myfile.pdf',
                                          content_type='application/pdf')
message.add_attachment(pdf_attachment)

txt_attachment = Attachment.load_filename(filename='document.txt',
                                          content_type='text/plain')
message.add_attachment(txt_attachment)
```

## Adding custom headers

Custom headers can be added to the message by passing one or more Header objects
to the `headers` argument or by adding each header to the headers list.

```python
from mumailer import Header

header = Header(name='X-Mailer',
                value='MuMailer')
message.add_header(header)

header = Header.parse(header='X-Spam=0')
message.add_header(header)
```

## SMTP Profiles

The SMTP settings can also be got from a profile file like the following:

```yaml
SMTP:
  SERVER: <SMTP server>
  PORT: 465
  USERNAME: <username>
  PASSWORD: <password>
  TIMEOUT: 30
  ENCRYPTION: TLSv1_2
  CIPHERS:
```

And instance the **ProfileSmtp** object:

```python
from mumailer import Connection, ProfileSmtp

profile_smtp = ProfileSmtp(filename='profile-smtp.yaml')

connection = Connection(server=profile_smtp.server,
                        port=profile_smtp.port,
                        username=profile_smtp.username,
                        password=profile_smtp.password)
```

## Message Profiles

Message profiles files can be used to set up the options for the message to be
sent, saving in a profile file the sender, the recipients, subject, attachments
list and others options.

```yaml
MESSAGE:
  SENDER: Muflone muflone@example.com
  TO:
    - Foo foo@example.com
  CC:
    - Bar bar@example.com
  SUBJECT: Test e-mail
  BODY: <html><body><h1>Hello world!</h1></body></html>
  HTML: true
  ATTACHMENTS:
    - README.md
    - LICENSE
  CONTENT_TYPES:
    - text/plain
    - application/octet-stream
- HEADERS:
    - X-Mailer=MuMailer
    - X-MuMailer-Profile=message.yaml
```

And instance the **ProfileMessage** object:

```python
from mumailer import Header, Message, ProfileMessage, Recipient

profile_message = ProfileMessage(filename='profile-message.yaml')

message = Message(sender=Recipient.parse(profile_message.sender),
                  reply_to=Recipient.parse(profile_message.reply_to),
                  to=Recipient.parse_as_list(profile_message.to),
                  cc=Recipient.parse_as_list(profile_message.cc),
                  bcc=Recipient.parse_as_list(profile_message.bcc),
                  subject=profile_message.subject,
                  body=profile_message.body,
                  use_html=profile_message.use_html,
                  headers=Header.parse_as_list(profile_message.headers))
```
