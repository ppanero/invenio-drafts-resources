# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft Services."""

from .draft_file_metadata_service import DraftFileMetadataService, \
    DraftFileMetadataServiceConfig
from .draft_file_service import DraftFileService, DraftFileServiceConfig
from .draft_service import DraftService, DraftServiceConfig
from .draft_version_service import DraftVersionService, \
    DraftVersionServiceConfig

__all__ = (
    "DraftFileMetadataService",
    "DraftFileMetadataServiceConfig",
    "DraftFileService",
    "DraftFileServiceConfig",
    "DraftService",
    "DraftServiceConfig",
    "DraftVersionService",
    "DraftVersionServiceConfig"
)
