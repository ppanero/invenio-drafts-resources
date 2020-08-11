# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Drafts Resources module to create REST APIs"""

import pytest
from invenio_pidstore.models import PIDStatus
from sqlalchemy.orm.exc import NoResultFound


def test_create_draft_of_new_record(app, draft_service, input_draft,
                                    fake_identity):
    """Test draft creation of a non-existing record."""
    # Needs `app` context because of invenio_access/permissions.py#166
    identified_draft = draft_service.create(
        data=input_draft, identity=fake_identity
    )

    assert identified_draft.id

    for key, value in input_draft.items():
        assert identified_draft.record[key] == value

    # Check for pid and parent pid
    assert identified_draft.record['recid']
    assert identified_draft.record['conceptrecid']


def test_create_draft_of_existing_record(app, draft_service, record_service,
                                         input_record, fake_identity):
    """Test draft creation of an existing record."""
    # FIXME: Since there are no files changes creation of a new draft of a
    # record is always a new revision (next test)
    # Needs `app` context because of invenio_access/permissions.py#166
    # Create new record
    # identified_record = record_service.create(
    #     data=input_record, identity=fake_identity
    # )

    # recid = identified_record.id
    # assert recid
    # assert identified_record.record.revision_id == 0

    # for key, value in input_record.items():
    #     assert identified_record.record[key] == value

    # # Create new draft of said record
    # orig_title = input_record['title']
    # input_record['title'] = "Edited title"
    # identified_draft = draft_service.create(
    #     data=input_record,
    #     identity=fake_identity,
    #     id_=recid
    # )

    # # Diff id and rev is 0, it is a new version not revision
    # assert identified_draft.id != recid
    # assert identified_draft.record.revision_id == 0

    # for key, value in input_record.items():
    #     assert identified_draft.record[key] == value

    # # Check the actual record was not modified
    # identified_record = draft_service.read(id_=recid, identity=fake_identity)

    # assert identified_record.record['title'] == orig_title


def test_create_a_new_record_revision(app, draft_service, record_service,
                                      input_record, fake_identity):
    """Test draft creation of an existing record."""
    # Needs `app` context because of invenio_access/permissions.py#166
    # Create new record
    identified_record = record_service.create(
        data=input_record, identity=fake_identity
    )

    recid = identified_record.id
    assert recid
    assert identified_record.record.revision_id == 0

    for key, value in input_record.items():
        assert identified_record.record[key] == value

    # Create new draft of said record
    orig_title = input_record['title']
    input_record['title'] = "Edited title"
    identified_draft = draft_service.edit(
        data=input_record,
        identity=fake_identity,
        id_=recid
    )

    # Diff revision: same pid and rev+1
    assert identified_draft.id == recid
    assert identified_draft.record.revision_id == 1

    for key, value in input_record.items():
        assert identified_draft.record[key] == value

    # Check the actual record was not modified
    identified_record = draft_service.read(id_=recid, identity=fake_identity)

    assert identified_record.record['title'] == orig_title


def test_publish_draft_of_new_record(app, draft_service, input_record,
                                     fake_identity):
    """Test draft publication of a non-existing record.

    It has to first create said draft.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    # Crate the draft
    identified_draft = draft_service.create(
        data=input_record, identity=fake_identity
    )
    assert identified_draft.id
    for pid in identified_draft.pids:
        assert pid.status == PIDStatus.RESERVED

    for key, value in input_record.items():
        assert identified_draft.record[key] == value

    # Publish it
    identified_record = draft_service.publish(
        id_=identified_draft.id, identity=fake_identity
    )

    assert identified_record.id
    for pid in identified_record.pids:
        assert pid.status == PIDStatus.REGISTERED

    for key, value in input_record.items():
        assert identified_record.record[key] == value

    # Check draft deletion
    # TODO: Remove import when exception is properly handled
    with pytest.raises(NoResultFound):
        identified_draft = draft_service.read_draft(
            identified_draft.id, identity=fake_identity
        )

    # Test record exists
    identified_record = draft_service.read(
        identified_record.id, identity=fake_identity
    )

    assert identified_record.id
    for pid in identified_record.pids:
        assert pid.status == PIDStatus.REGISTERED

    for key, value in input_record.items():
        assert identified_record.record[key] == value


def test_create_new_version_of_record(app, draft_service, input_record,
                                      fake_identity):
    """Creates a new version of a record.

    Publishes the draft to obtain 2 versions of a record.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    # Cannot create with record service due to the lack of versioning
    # Crate the draft
    identified_draft_1 = draft_service.create(
        data=input_record, identity=fake_identity
    )
    assert identified_draft_1.id
    for pid in identified_draft_1.pids:
        assert pid.status == PIDStatus.RESERVED

    assert identified_draft_1.record.revision_id == 0

    # Publish it
    identified_record_1 = draft_service.publish(
        id_=identified_draft_1.id, identity=fake_identity
    )

    assert identified_record_1.id
    for pid in identified_record_1.pids:
        assert pid.status == PIDStatus.REGISTERED

    assert identified_record_1.record.revision_id == 0

    # Create new version
    identified_draft_2 = draft_service.new_version(
        id_=identified_record_1.id, identity=fake_identity
    )

    assert identified_draft_2.id != identified_record_1.id
    for pid in identified_draft_2.pids:
        assert pid.status == PIDStatus.RESERVED

    assert identified_draft_2.record.revision_id == 0

    # Publish it
    identified_record_2 = draft_service.publish(
        id_=identified_draft_2.id, identity=fake_identity
    )

    assert identified_record_2.id
    for pid in identified_record_2.pids:
        assert pid.status == PIDStatus.REGISTERED

    assert identified_record_2.record.revision_id == 0

    assert identified_record_1.record['conceptrecid'] == \
        identified_record_2.record['conceptrecid']
