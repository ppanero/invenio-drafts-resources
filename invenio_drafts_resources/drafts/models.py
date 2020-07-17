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
from invenio_records.models import Timestamp
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy_utils.types import JSONType, UUIDType


class DraftMetadataBase(Timestamp):
    """Represent a base class for draft metadata.

    The DraftMetadata object  contains a `created` and  a `updated`
    properties that are automatically updated.
    """

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

    id = db.Column(
        UUIDType,
        primary_key=True,
        default=uuid.uuid4,
    )
    """Draft identifier, it is the same than the record it is draft of."""

    fork_version_id = db.Column(db.Integer)
    """Version id of the record it is draft of."""

    version_id = db.Column(db.Integer, nullable=False)
    """Used by SQLAlchemy for optimistic concurrency control."""

    status = db.Column(db.String(255), default="draft", nullable=False)
    """Status for workflow management."""

    expiry_date = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        default=datetime.utcnow,
        nullable=True
    )
    """Specifies when the it expires. If `NULL` the draft does not expire."""

    json = db.Column(
        db.JSON().with_variant(
            postgresql.JSONB(none_as_null=True),
            'postgresql',
        ).with_variant(
            JSONType(),
            'sqlite',
        ).with_variant(
            JSONType(),
            'mysql',
        ),
        default=lambda: dict(),
        nullable=True
    )
    """Store metadata in JSON format.
    When you create a new `Record the `json field value should never be
    `NULL`. Default value is an empty dict. `NULL` value means that the
    record metadata has been deleted.
    """

    __mapper_args__ = {
        'version_id_col': version_id
    }
