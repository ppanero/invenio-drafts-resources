# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Drafts Resources module to create REST APIs"""

import json

import pytest
from sqlalchemy.orm.exc import NoResultFound

from invenio_drafts_resources.resources import DraftActionResource, \
    DraftActionResourceConfig, DraftResource, DraftResourceConfig, \
    DraftVersionResource, DraftVersionResourceConfig

HEADERS = {"content-type": "application/json", "accept": "application/json"}


def test_create_draft_of_new_record(client, input_draft):
    """Test draft creation of a non-existing record."""
    response = client.post(
        "/records", data=json.dumps(input_draft), headers=HEADERS
    )

    assert response.status_code == 201
    response_fields = response.json.keys()
    fields_to_check = ['pid', 'metadata', 'revision',
                       'created', 'updated', 'links']

    for field in fields_to_check:
        assert field in response_fields


def test_create_draft_of_existing_record(client, record_service,
                                         input_record, fake_identity):
    """Test draft creation of an existing record."""
    # Create new record manually since the endpoint it overwritten
    identified_record = record_service.create(
        data=input_record, identity=fake_identity
    )

    recid = identified_record.id
    assert recid

    for key, value in input_record.items():
        assert identified_record.record[key] == value

    # Create new draft of said record
    orig_title = input_record['title']
    input_record['title'] = "Edited title"
    response = client.post(
        "/records/{}/draft".format(recid),
        data=json.dumps(input_record),
        headers=HEADERS
    )

    assert response.status_code == 201
    response_fields = response.json.keys()
    fields_to_check = ['pid', 'metadata', 'revision',
                       'created', 'updated', 'links']

    for field in fields_to_check:
        assert field in response_fields

    assert response.json['metadata']['title'] == input_record['title']

    # Check the actual record was not modified
    response = client.get(
        "/records/{}".format(recid),
        headers=HEADERS
    )

    assert response.status_code == 200
    response_fields = response.json.keys()
    fields_to_check = ['pid', 'metadata', 'revision',
                       'created', 'updated', 'links']

    for field in fields_to_check:
        assert field in response_fields

    assert response.json['metadata']['title'] == orig_title


def test_publish_draft_of_new_record(client, input_record):
    """Test draft publication of a non-existing record.

    It has to first create said draft.
    """
    # Create the draft
    response = client.post(
        "/records", data=json.dumps(input_record), headers=HEADERS
    )

    assert response.status_code == 201
    recid = response.json['pid']

    # Publish it
    response = client.post(
        "/records/{}/draft/actions/publish".format(recid), headers=HEADERS
    )

    assert response.status_code == 202
    response_fields = response.json.keys()
    fields_to_check = ['pid', 'metadata', 'revision',
                       'created', 'updated', 'links']

    for field in fields_to_check:
        assert field in response_fields

    # Check draft deletion
    # TODO: Remove import when exception is properly handled
    with pytest.raises(NoResultFound):
        response = client.get(
            "/records/{}/draft".format(recid),
            headers=HEADERS
        )
    # assert response.status_code == 404

    # Test record exists
    response = client.get("/records/{}".format(recid), headers=HEADERS)

    assert response.status_code == 200

    response_fields = response.json.keys()
    fields_to_check = ['pid', 'metadata', 'revision',
                       'created', 'updated', 'links']

    for field in fields_to_check:
        assert field in response_fields
