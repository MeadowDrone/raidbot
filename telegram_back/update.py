#!/usr/bin/env python
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

"""This module contains a object that represents a Telegram Update"""

from telegram import Message, TelegramObject


class Update(TelegramObject):
    """This object represents a Telegram Update.

    Attributes:
        update_id (int):
        message (:class:`telegram.Message`):

    Args:
        update_id (int):
        **kwargs: Arbitrary keyword arguments.

    Keyword Args:
        message (Optional[:class:`telegram.Message`]):
    """
    def __init__(self,
                 update_id,
                 **kwargs):
        # Required
        self.update_id = int(update_id)
        # Optionals
        self.message = kwargs.get('message')

    @staticmethod
    def de_json(data):
        """
        Args:
            data (str):

        Returns:
            telegram.Update:
        """
        if not data:
            return None

        data['message'] = Message.de_json(data['message'])

        return Update(**data)
