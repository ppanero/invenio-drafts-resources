# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Drafts Resources module to create REST APIs."""

from flask import g
from flask_resources import CollectionResource, SingletonResource
from flask_resources.context import resource_requestctx

from ..errors import ActionNotConfigured, CommandNotImplemented
from ..services import RecordDraftService
from .draft_config import DraftActionResourceConfig, DraftResourceConfig, \
    DraftVersionResourceConfig


class DraftResource(SingletonResource):
    """Draft resource."""

    default_config = DraftResourceConfig

    def __init__(self, service=None, *args, **kwargs):
        """Constructor."""
        super(DraftResource, self).__init__(*args, **kwargs)
        self.service = service or RecordDraftService()

    def read(self):
        """Read an item."""
        identity = g.identity
        id_ = resource_requestctx.route["pid_value"]

        return self.service.read_draft(id_, identity), 200

    def create(self):
        """Create an item."""
        data = resource_requestctx.request_content
        identity = g.identity
        id_ = resource_requestctx.route["pid_value"]

        return self.service.edit(id_, data, identity), 201

    def update(self):
        """Update an item."""
        # TODO: IMPLEMENT ME!
        return self.service.update(), 200

    def delete(self):
        """Delete an item."""
        # TODO: IMPLEMENT ME!
        return self.service.delete(), 200


class DraftVersionResource(CollectionResource):
    """Draft version resource."""

    default_config = DraftVersionResourceConfig

    def __init__(self, service=None, *args, **kwargs):
        """Constructor."""
        super(DraftVersionResource, self).__init__(*args, **kwargs)
        self.service = service or RecordDraftService()

    def search(self):
        """Perform a search over the items."""
        # TODO: IMPLEMENT ME!
        return self.service.search()

    def create(self):
        """Create an item."""
        identity = g.identity
        id_ = resource_requestctx.route["pid_value"]

        return self.service.new_version(id_, identity), 201


class DraftActionResource(SingletonResource):
    """Draft action resource."""

    default_config = DraftActionResourceConfig

    def __init__(self, service=None, *args, **kwargs):
        """Constructor."""
        super(DraftActionResource, self).__init__(*args, **kwargs)
        self.service = service or RecordDraftService()

    def create(self):
        """Any POST business logic."""
        action = resource_requestctx.route["action"]
        try:
            cmd_name = self.config.action_commands[action]
            cmd_func = getattr(self.service, command)
        except KeyError:
            raise ActionNotConfigured(action=action)
        except NameError:
            raise CommandNotImplemented(cmd_name)

        # NOTE: Due to the route we assume the commands only need
        # id_ and identity
        identity = g.identity
        id_ = resource_requestctx.route["pid_value"]

        return cmd_func(id_, identity), 202
