#!/usr/bin/env python
# pylint: disable=W0622,E0611
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015 Leandro Toledo de Souza <leandrotoeldodesouza@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

"""This module contains a object that represents a Telegram InputFile"""

try:
    from email.generator import _make_boundary as choose_boundary
    from urllib.request import urlopen
    from io import BufferedReader as file
except ImportError:
    from mimetools import choose_boundary
    from urllib2 import urlopen
import mimetypes
import os
import sys
import imghdr

from telegram import TelegramError

DEFAULT_MIME_TYPE = 'application/octet-stream'
USER_AGENT = 'Python Telegram Bot' \
             ' (https://github.com/leandrotoledo/python-telegram-bot)'


class InputFile(object):
    """This object represents a Telegram InputFile."""

    def __init__(self,
                 data):
        self.data = data
        self.boundary = choose_boundary()

        if 'audio' in data:
            self.input_name = 'audio'
            self.input_file = data.pop('audio')
        if 'document' in data:
            self.input_name = 'document'
            self.input_file = data.pop('document')
        if 'photo' in data:
            self.input_name = 'photo'
            self.input_file = data.pop('photo')
        if 'sticker' in data:
            self.input_name = 'sticker'
            self.input_file = data.pop('sticker')
        if 'video' in data:
            self.input_name = 'video'
            self.input_file = data.pop('video')
        if 'voice' in data:
            self.input_name = 'voice'
            self.input_file = data.pop('voice')
        if 'certificate' in data:
            self.input_name = 'certificate'
            self.input_file = data.pop('certificate')

        if isinstance(self.input_file, file):
            self.input_file_content = self.input_file.read()
            if 'filename' in data:
                self.filename = self.data.pop('filename')
            else:
                self.filename = os.path.basename(self.input_file.name)
            self.mimetype = mimetypes.guess_type(self.filename)[0] or \
                DEFAULT_MIME_TYPE

        if 'http' in self.input_file:
            self.input_file_content = urlopen(self.input_file).read()
            self.mimetype = InputFile.is_image(self.input_file_content)
            self.filename = self.mimetype.replace('/', '.')

    @property
    def headers(self):
        """
        Returns:
            str:
        """
        return {'User-agent': USER_AGENT,
                'Content-type': self.content_type}

    @property
    def content_type(self):
        """
        Returns:
            str:
        """
        return 'multipart/form-data; boundary=%s' % self.boundary

    def to_form(self):
        """
        Returns:
            str:
        """
        form = []
        form_boundary = '--' + self.boundary

        # Add data fields
        for name, value in self.data.items():
            form.extend([
                form_boundary,
                'Content-Disposition: form-data; name="%s"' % name,
                '',
                str(value)
            ])

        # Add input_file to upload
        form.extend([
            form_boundary,
            'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                self.input_name, self.filename
                ),
            'Content-Type: %s' % self.mimetype,
            '',
            self.input_file_content
        ])

        form.append('--' + self.boundary + '--')
        form.append('')

        return InputFile._parse(form)

    @staticmethod
    def _parse(form):
        """
        Returns:
            str:
        """
        if sys.version_info > (3,):
            # on Python 3 form needs to be byte encoded
            encoded_form = []
            for item in form:
                try:
                    encoded_form.append(item.encode())
                except AttributeError:
                    encoded_form.append(item)

            return b'\r\n'.join(encoded_form)
        return '\r\n'.join(form)

    @staticmethod
    def is_image(stream):
        """Check if the content file is an image by analyzing its headers.

        Args:
            stream (str): A str representing the content of a file.

        Returns:
            str: The str mimetype of an image.
        """
        image = imghdr.what(None, stream)
        if image:
            return 'image/%s' % image

        raise TelegramError('Could not parse file content')

    @staticmethod
    def is_inputfile(data):
        """Check if the request is a file request.

        Args:
            data (str): A dict of (str, unicode) key/value pairs

        Returns:
            bool
        """
        if data:
            file_types = ['audio', 'document', 'photo', 'sticker', 'video',
                          'voice', 'certificate']
            file_type = [i for i in list(data.keys()) if i in file_types]

            if file_type:
                file_content = data[file_type[0]]

                if file_type[0] == 'photo' or file_type[0] == 'document':
                    return isinstance(file_content, file) or \
                        str(file_content).startswith('http')

                return isinstance(file_content, file)

        return False
