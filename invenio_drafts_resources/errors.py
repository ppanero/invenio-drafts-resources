# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Errors."""

from flask_resources.errors import HTTPJSONException


class ActionNotConfigured(HTTPJSONException):
    """Action not configured error."""

    code = 404
    description = "Not found. Action not configured."

    def __init__(self, action=None, **kwargs):
        """Constructor."""
        super(ActionNotConfigured, self).__init__(**kwargs)
        if action:
            self.description = f"Action {action} not configured."


class CommandNotImplemented(HTTPJSONException):
    """Command not implemented error."""

    code = 500
    description = "Command not implemented."

    def __init__(self, cmd_name=None, **kwargs):
        """Constructor."""
        super(CommandNotImplemented, self).__init__(**kwargs)
        if cmd_name:
            self.description = f"Command {cmd_name} not implemented."
