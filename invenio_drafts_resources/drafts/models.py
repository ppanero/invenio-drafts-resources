# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft Models API."""

import uuid
from datetime import datetime

from invenio_db import db
from invenio_records.models import RecordMetadataBase
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy_utils.types import JSONType, UUIDType


class DraftMetadataBase(RecordMetadataBase):
    """Represent a base class for draft metadata."""

    fork_version_id = db.Column(db.Integer)
    """Version id of the record it is draft of."""

    expiry_date = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        default=datetime.utcnow,
        nullable=True
    )
    """Specifies when the draft expires. If `NULL` the draft doesn't expire."""
