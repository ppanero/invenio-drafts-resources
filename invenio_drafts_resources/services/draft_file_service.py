# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Draft File Service."""


from invenio_records_resources.services import FileService, FileServiceConfig


class DraftFileServiceConfig(FileServiceConfig):
    """Draft File Service configuration."""

    pass


class DraftFileService(FileService):
    """Draft File Service."""

    default_config = DraftFileServiceConfig

    # High-level API
    def read(self, id_, identity, *args, **kwargs):
        """Retrieve the actual file."""
        # TODO: IMPLEMENT ME!
        # High likelihood that we can just rely on FileService here
        # and simply configure DraftFileServiceConfig appropriately
        return self.resource_unit_cls()
