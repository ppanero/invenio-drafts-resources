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
from flask_resources.resources import ResourceConfig
from invenio_records_resources.responses import RecordResponse
from invenio_records_resources.schemas import RecordSchemaJSONV1
from invenio_records_resources.serializers import RecordJSONSerializer

from ..serializers import DraftJSONSerializer
from ..services import DraftVersionService, RecordDraftService
from ..services.schemas import DraftSchemaJSONV1


class DraftResourceConfig(ResourceConfig):
    """Draft resource config."""

    list_route = "/records/<pid_value>/draft"
    response_handlers = {
        "application/json": RecordResponse(
            DraftJSONSerializer(schema=DraftSchemaJSONV1)
        )
    }


class DraftResource(SingletonResource):
    """Draft resource."""

    default_config = DraftResourceConfig

    def __init__(self, service=None, *args, **kwargs):
        """Constructor."""
        super(DraftResource, self).__init__(*args, **kwargs)
        self.service = service or RecordDraftService()

    def read(self, *args, **kwargs):
        """Read an item."""
        identity = g.identity
        id_ = resource_requestctx.route["pid_value"]

        return self.service.read_draft(id_, identity), 200

    def create(self, *args, **kwargs):
        """Create an item."""
        data = resource_requestctx.request_content
        identity = g.identity
        id_ = resource_requestctx.route["pid_value"]

        return self.service.edit(id_, data, identity), 201

    def update(self, *args, **kwargs):
        """Update an item."""
        # TODO: IMPLEMENT ME!
        return self.service.update(), 200

    def delete(self, *args, **kwargs):
        """Delete an item."""
        # TODO: IMPLEMENT ME!
        return self.service.delete(), 200


class DraftVersionResourceConfig(ResourceConfig):
    """Draft resource config."""

    list_route = "/records/<pid_value>/versions"


class DraftVersionResource(CollectionResource):
    """Draft version resource."""

    default_config = DraftVersionResourceConfig

    def __init__(self, service=None, *args, **kwargs):
        """Constructor."""
        super(DraftVersionResource, self).__init__(*args, **kwargs)
        self.service = service or DraftVersionService()

    def search(self, *args, **kwargs):
        """Perform a search over the items."""
        # TODO: IMPLEMENT ME!
        return self.service.search()

    def create(self, *args, **kwargs):
        """Create an item."""
        identity = g.identity
        id_ = resource_requestctx.route["pid_value"]

        return self.service.version(id_, identity), 201


class DraftActionResourceConfig(ResourceConfig):
    """Draft action resource config."""

    list_route = "/records/<pid_value>/draft/actions/<action>"
    response_handlers = {
        "application/json": RecordResponse(
            RecordJSONSerializer(schema=RecordSchemaJSONV1)
        )
    }


class DraftActionResource(SingletonResource):
    """Draft action resource."""

    default_config = DraftActionResourceConfig

    def __init__(self, service=None, *args, **kwargs):
        """Constructor."""
        super(DraftActionResource, self).__init__(*args, **kwargs)
        self.service = service or RecordDraftService()

    def create(self, *args, **kwargs):
        """Any POST business logic."""
        if resource_requestctx.route["action"] == "publish":
            identity = g.identity
            id_ = resource_requestctx.route["pid_value"]
            return self.service.publish(id_, identity), 202
        return {}, 202
