# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Draft Service."""

from invenio_db import db
from invenio_records_resources.services import MarshmallowDataValidator, \
    RecordService, RecordServiceConfig
from werkzeug.utils import cached_property

from ..resource_units import IdentifiedRecordDraft
from .permissions import DraftPermissionPolicy
from .schemas import DraftMetadataSchemaJSONV1


class RecordDraftServiceConfig(RecordServiceConfig):
    """Draft Service configuration."""

    # Service configuration
    permission_policy_cls = DraftPermissionPolicy

    # RecordService configuration
    resource_unit_cls = IdentifiedRecordDraft

    # DraftService configuration.
    # WHY: We want to force user input choice here.
    draft_cls = None
    draft_data_validator = MarshmallowDataValidator(
        schema=DraftMetadataSchemaJSONV1
    )


class RecordDraftService(RecordService):
    """Draft Service interface."""

    default_config = RecordDraftServiceConfig

    @cached_property
    def draft_data_validator(self):
        """Returns an instance of the draft data validator."""
        return self.config.draft_data_validator

    @cached_property
    def draft_resolver(self):
        """Factory for creating a draft resolver instance."""
        return self.config.resolver_cls(
            pid_type=self.config.resolver_pid_type,
            getter=self.config.draft_cls.get_record,
            registered_only=False
        )

    def resolve_draft(self, id_):
        """Resolve a persistent identifier to a record draft."""
        return self.draft_resolver.resolve(id_)

    # High-level API
    # Inherits record read, search, create, delete and update

    def create(self, data, identity):
        """Create a draft for a new record.

        It does not eagerly create the associated record.
        """
        self.require_permission(identity, "create")
        validated_data = self.draft_data_validator.validate(data)
        draft = self.config.draft_cls.create(validated_data)
        # Create PID (New) associated to the draft UUID
        pid = self.minter(
            record_uuid=draft.id,
            data=draft,
            with_obj_type=None
        )

        db.session.commit()  # Persist DB
        if self.indexer:
            self.indexer.index(draft)

        return self.config.resource_unit_cls(pid=pid, record=draft)

    def edit(self, id_, data, identity):
        """Create a draft for an existing record.

        :param id_: record PID value.
        """
        pid, record = self.resolve(id_)
        # FIXME: How to check permission on the record?
        self.require_permission(identity, "create")
        validated_data = self.draft_data_validator.validate(data)
        draft = self.config.draft_cls.create(validated_data, record)
        db.session.commit()  # Persist DB
        if self.indexer:
            self.indexer.index(draft)

        return self.config.resource_unit_cls(pid=pid, record=draft)

    def publish(self, id_, identity):
        """Publish a draft."""
        # TODO: IMPLEMENT ME!
        return self.config.draft_of_resource_unit_cls()
