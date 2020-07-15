# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Draft File Service."""

from invenio_records_resources.services import FileMetadataService, \
    FileMetadataServiceConfig


class DraftFileMetadataServiceConfig(FileMetadataServiceConfig):
    """Draft File Metadata Service configuration."""

    # TODO: FILL ME!
    pass


class DraftFileMetadataService(FileMetadataService):
    """Draft File Metadata Service."""

    default_config = DraftFileMetadataServiceConfig

    # High-level API
    def search(self, querystring, identity, pagination=None, *args, **kwargs):
        """Search for drafts matching the querystring."""
        # TODO: IMPLEMENT ME!
        # High likelihood that we can just rely on RecordService here
        # and simply configure DraftServiceConfig appropriately
        return self.resource_list_cls()

    def create(self, data, identity, *args, **kwargs):
        """Create a draft."""
        # TODO: IMPLEMENT ME!
        return self.resource_unit_cls()

    def update_all(self, data, identity, *args, **kwargs):
        """Delete an item."""
        # TODO: IMPLEMENT ME!
        return self.resource_list_cls()

    def delete_all(self, data, identity, *args, **kwargs):
        """Delete an item."""
        # TODO: IMPLEMENT ME!
        return self.resource_list_cls()

    def read(self, id_, identity, *args, **kwargs):
        """Read an item."""
        # TODO: IMPLEMENT ME!
        return self.resource_unit_cls()

    def update(self, id_, data, identity, *args, **kwargs):
        """Replace a draft."""
        # TODO: IMPLEMENT ME!
        return self.resource_unit_cls()

    def delete(self, id_, identity, *args, **kwargs):
        """Delete an item."""
        # TODO: IMPLEMENT ME!
        return self.resource_unit_cls()
