# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Drafts permissions."""

from invenio_records_permissions.generators import AnyUser
from invenio_records_permissions.policies.records import RecordPermissionPolicy


class DraftPermissionPolicy(RecordPermissionPolicy):
    """Custom permission policy."""

    # FIXME: Revist this along the development
    # Default create should be "authenticated"?
    can_create = [AnyUser()]
