# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask_principal import Identity
from invenio_access import any_user
from invenio_app.factory import create_api
from invenio_db import db
from invenio_records.api import Record
from invenio_records.models import RecordMetadataBase
from invenio_records_permissions.generators import AnyUser
from invenio_records_permissions.policies.records import RecordPermissionPolicy
from invenio_records_resources.resources import RecordResource
from invenio_search import RecordsSearch

from invenio_drafts_resources.drafts import DraftBase, DraftMetadataBase
from invenio_drafts_resources.resources import DraftActionResource, \
    DraftActionResourceConfig, DraftResource, DraftVersionResource
from invenio_drafts_resources.services import RecordDraftService, \
    RecordDraftServiceConfig
from invenio_drafts_resources.services.pid_manager import PIDManager, \
    PIDManagerConfig


class AnyUserPermissionPolicy(RecordPermissionPolicy):
    """Custom permission policy."""

    can_list = [AnyUser()]
    can_create = [AnyUser()]
    can_read = [AnyUser()]
    can_update = [AnyUser()]
    can_delete = [AnyUser()]
    can_read_files = [AnyUser()]
    can_update_files = [AnyUser()]
    can_publish = [AnyUser()]


class CustomDraftMetadata(db.Model, DraftMetadataBase):
    """Represent a custom draft metadata."""

    __tablename__ = 'custom_drafts_metadata'


class CustomDraft(DraftBase):
    """Custom draft API."""

    model_cls = CustomDraftMetadata


class CustomRecordMetadata(db.Model, RecordMetadataBase):
    """Represent a custom draft metadata."""

    __tablename__ = 'custom_record_metadata'


class CustomRecord(Record):
    """Custom draft API."""

    model_cls = CustomRecordMetadata


class TestSearch(RecordsSearch):
    """Test record search."""

    class Meta:
        """Test configuration."""

        index = "records"


class CustomPIDManagerConfig(PIDManagerConfig):
    """Custom pid manager config."""

    draft_cls = CustomDraft
    record_cls = CustomRecord


class CustomRecordDraftServiceConfig(RecordDraftServiceConfig):
    """Custom draft service config."""

    draft_route = "/records/<pid_value>/draft"
    draft_action_route = "/records/<pid_value>/draft/actions/<action>"
    draft_cls = CustomDraft
    record_cls = CustomRecord
    search_cls = TestSearch
    permission_policy_cls = AnyUserPermissionPolicy
    pid_manager = PIDManager(config=CustomPIDManagerConfig)


@pytest.fixture(scope='module')
def app_config(app_config):
    """Override pytest-invenio app_config fixture.

    For test purposes we need to enforce some configuration variables before
    endpoints are created.
    invenio-records-rest is imported from invenio-records-permissions, so
    we need to disable its default endpoint, until we are completely
    decoupled from invenio-records-rest. Issue:
    https://github.com/inveniosoftware/invenio-records-permissions/issues/51
    """
    app_config["RECORDS_REST_ENDPOINTS"] = {}
    app_config["RECORDS_UI_ENDPOINTS"] = {
        "recid": {
            "route": "/records/<pid_value>"
        }
    }
    app_config["INDEXER_DEFAULT_DOC_TYPE"] = "testrecord"
    app_config["INDEXER_DEFAULT_INDEX"] = TestSearch.Meta.index
    app_config["SEARCH_MAPPINGS"] = ['drafts', 'records']
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="module")
def base_app(base_app):
    """Base application factory fixture."""
    search = base_app.extensions["invenio-search"]
    search.register_mappings(TestSearch.Meta.index, 'mock_module.mappings')
    search.register_mappings('drafts', 'mock_module.mappings')
    yield base_app


def _draft_service():
    """Create a draft service."""
    return RecordDraftService(config=CustomRecordDraftServiceConfig)


class CustomDraftActionResourceConfig(DraftActionResourceConfig):
    """Draft action resource config."""

    action_commands = {
        "publish": "publish",
        "command": "not_implemented"
    }


@pytest.fixture(scope="module")
def app(app):
    """Application factory fixture."""
    with app.app_context():
        record_bp = RecordResource(
            service=_draft_service()
        ).as_blueprint("record_resource")
        draft_bp = DraftResource(
            service=_draft_service()
        ).as_blueprint("draft_resource")
        draft_action_bp = DraftActionResource(
            service=_draft_service(),
            config=CustomDraftActionResourceConfig
        ).as_blueprint("draft_action_resource")
        draft_version_bp = DraftVersionResource(
            service=_draft_service()
        ).as_blueprint("draft_version_resource")

        app.register_blueprint(record_bp)
        app.register_blueprint(draft_bp)
        app.register_blueprint(draft_action_bp)
        app.register_blueprint(draft_version_bp)
        yield app


@pytest.fixture(scope="module")
def draft_service(app):
    """Draft service factory fixture.

    Depends on app fixture, because you need an app context
    to use a service.
    """
    return _draft_service()


@pytest.fixture(scope="module")
def record_service(app):
    """Record service factory fixture.

    Depends on app fixture, because you need an app context
    to use a service.
    """
    return _record_service()


@pytest.fixture(scope="function")
def input_draft():
    """Minimal draft data as dict coming from the external world."""
    return {
        "_access": {"metadata_restricted": False, "files_restricted": False},
        "_owners": [1],
        "_created_by": 1,
        "title": "A Romans story",
    }


@pytest.fixture(scope="function")
def input_record():
    """Minimal record data as dict coming from the external world."""
    return {
        "_access": {"metadata_restricted": False, "files_restricted": False},
        "_owners": [1],
        "_created_by": 1,
        "title": "A Romans story",
        "description": "A looong description full of lorem ipsums"
    }


@pytest.fixture(scope="function")
def fake_identity():
    """Fake identity providing `any_user` system role."""
    identity = Identity(1)
    identity.provides.add(any_user)

    return identity
