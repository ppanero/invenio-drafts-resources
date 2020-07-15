# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Draft Service."""

from .draft_service import DraftService, DraftServiceConfig


class DraftVersionServiceConfig(DraftServiceConfig):
    """Draft Version Service configuration."""

    # Service configuration
    # TODO: FILL ME!

    # RecordService configuration
    # TODO: FILL ME!

    # DraftVersionService configuration
    # TODO: FILL ME!


class DraftVersionService(DraftService):
    """Draft Service interface."""

    default_config = DraftVersionServiceConfig

    # High-level API
    def search(self, querystring, identity, pagination=None, *args, **kwargs):
        """Search for drafts matching the querystring."""
        # TODO: IMPLEMENT ME!
        return self.resource_list_cls()

    def create(self, data, identity):
        """Create a draft."""
        # TODO: IMPLEMENT ME!
        return self.resource_unit_cls()
