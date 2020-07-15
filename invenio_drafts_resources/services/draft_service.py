# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Draft Service."""

from invenio_records_resources.resource_unit import IdentifiedRecord
from invenio_records_resources.services import RecordService, \
    RecordServiceConfig

from ..resource_unit import IdentifiedDraft
from .permissions import DraftPermissionPolicy


class DraftServiceConfig(RecordServiceConfig):
    """Draft Service configuration."""

    # Service configuration
    permission_policy_cls = DraftPermissionPolicy
    resource_unit_cls = IdentifiedDraft

    # RecordService configuration
    # TODO: FILL ME!

    # DraftService configuration
    # TODO: FILL ME!
    draft_of_resource_unit_cls = IdentifiedRecord


class DraftService(RecordService):
    """Draft Service interface."""

    default_config = DraftServiceConfig

    # High-level API
    def read(self, id_, identity):
        """Retrieve a draft."""
        # TODO: IMPLEMENT ME!
        # High likelihood that we can just rely on RecordService here
        # and simply configure DraftServiceConfig appropriately
        return self.resource_unit_cls()

    def search(self, querystring, identity, pagination=None, *args, **kwargs):
        """Search for drafts matching the querystring."""
        # TODO: IMPLEMENT ME!
        # High likelihood that we can just rely on RecordService here
        # and simply configure DraftServiceConfig appropriately
        return self.resource_list_cls()

    def create(self, data, identity):
        """Create a draft."""
        # TODO: IMPLEMENT ME!
        return self.resource_unit_cls()

    def delete(self, id_, identity):
        """Delete a draft from database and search indexes."""
        # TODO: IMPLEMENT ME!
        # High likelihood that we can just rely on RecordService here
        # and simply configure DraftServiceConfig appropriately
        return self.resource_unit_cls()

    def update(self, id_, data, identity):
        """Replace a draft."""
        # TODO: IMPLEMENT ME!
        # High likelihood that we can just rely on RecordService here
        # and simply configure DraftServiceConfig appropriately
        return self.resource_unit_cls()

    def publish(self, id_, identity):
        """Publish a draft."""
        # TODO: IMPLEMENT ME!
        return self.draft_of_resource_unit_cls()
