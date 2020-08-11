# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs."""

import json

import pytz
from flask_resources.serializers import SerializerMixin
from invenio_records_resources.serializers import RecordJSONSerializer


class DraftJSONSerializer(RecordJSONSerializer):
    """Drafts JSON serializer implementation."""

    def __init__(self, schema=None):
        """Constructor."""
        self.schema = schema

    def _process_draft(self, draft_unit, *args, **kwargs):
        pid = draft_unit.id
        draft = draft_unit.record  # FIXME: refactor to unit
        draft_dict = dict(
            pid=pid,
            metadata=draft.dumps(),
            revision=draft.revision_id,
            created=(
                pytz.utc.localize(draft.created).isoformat()
                if draft.created and not draft.created.tzinfo
                else None
            ),
            updated=(
                pytz.utc.localize(draft.updated).isoformat()
                if draft.updated and not draft.updated.tzinfo
                else None
            ),
            expiry=(
                pytz.utc.localize(draft.expiry_date).isoformat()
                if draft.expiry_date and not draft.expiry_date.tzinfo
                else None
            ),
            links=dict()  # TODO: Implement me. See issue #19
        )

        # TODO: Shall we includ fork_version_id and record_pid in
        # the serialization?
        return draft_dict

    def serialize_object(self, obj, response_ctx=None, *args, **kwargs):
        """Dump the object into a json string."""
        if obj:  # e.g. delete op has no return body
            return json.dumps(self._process_draft(obj))
        else:
            return ""

    def serialize_object_list(
        self, obj_list, response_ctx=None, *args, **kwargs
    ):
        """Not implemented.

        Drafts are only serialized and returned back as individual objects.
        """
        raise NotImplementedError()
