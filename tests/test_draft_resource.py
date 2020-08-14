# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Drafts Resources module to create REST APIs"""

import json
import time

import pytest
from sqlalchemy.orm.exc import NoResultFound

from invenio_drafts_resources.resources import DraftActionResource, \
    DraftActionResourceConfig, DraftResource, DraftResourceConfig, \
    DraftVersionResource, DraftVersionResourceConfig

HEADERS = {"content-type": "application/json", "accept": "application/json"}


def _assert_single_item_response(response):
    """Assert the fields present on a single item response."""
    response_fields = response.json.keys()
    fields_to_check = ['pid', 'metadata', 'created', 'updated', 'links']

    for field in fields_to_check:
        assert field in response_fields


def _create_and_publish(client, input_record):
    """Create a draft and publish it."""
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
    _assert_single_item_response(response)

    return recid


def test_create_new_record_draft(client, input_draft):
    """Test draft creation of a non-existing record."""
    response = client.post(
        "/records", data=json.dumps(input_draft), headers=HEADERS
    )

    assert response.status_code == 201
    _assert_single_item_response(response)


def test_create_publish_new_record_draft(client, input_record):
    """Test draft publication of a non-existing record.

    It has to first create said draft.
    """
    recid = _create_and_publish(client, input_record)

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

    _assert_single_item_response(response)


def test_create_publish_record_new_revision(client, input_record,
                                            fake_identity):
    """Test draft creation of an existing record and publish it."""
    recid = _create_and_publish(client, input_record)

    # FIXME: Allow ES to clean deleted documents.
    # Flush is not the same. Default collection time is 1 minute.
    time.sleep(70)

    # Create new draft of said record
    orig_title = input_record['title']
    input_record['title'] = "Edited title"
    response = client.post(
        "/records/{}/draft".format(recid),
        data=json.dumps(input_record),
        headers=HEADERS
    )

    assert response.status_code == 201
    _assert_single_item_response(response)
    assert response.json['metadata']['title'] == input_record['title']
    assert response.json['revision'] == 0

    # Check the actual record was not modified
    response = client.get(
        "/records/{}".format(recid),
        headers=HEADERS
    )

    assert response.status_code == 200
    _assert_single_item_response(response)
    assert response.json['metadata']['title'] == orig_title

    # Publish it to check the increment in reversion
    response = client.post(
        "/records/{}/draft/actions/publish".format(recid), headers=HEADERS
    )

    assert response.status_code == 202
    _assert_single_item_response(response)

    assert response.json['metadata']['recid'] == recid
    assert response.json['revision'] == 1
    assert response.json['metadata']['title'] == input_record['title']

    # Check it was actually edited
    response = client.get(
        "/records/{}".format(recid),
        headers=HEADERS
    )
    assert response.json['metadata']['title'] == input_record['title']


def test_create_publish_record_new_version(client, input_record,
                                           fake_identity):
    """Creates a new version of a record.

    Publishes the draft to obtain 2 versions of a record.
    """
    recid = _create_and_publish(client, input_record)

    # Create new draft of said record
    response = client.post(
        "/records/{}/versions".format(recid),
        headers=HEADERS
    )

    assert response.status_code == 201
    _assert_single_item_response(response)
    assert response.json['revision'] == 0
    recid_2 = response.json['metadata']['recid']

    # Publish it to check the increment in version
    response = client.post(
        "/records/{}/draft/actions/publish".format(recid_2), headers=HEADERS
    )

    assert response.status_code == 202
    _assert_single_item_response(response)

    assert response.json['metadata']['recid'] == recid_2 != recid
    assert response.json['revision'] == 0


def test_action_not_configured(client, fake_identity):
    """Tests a non configured action call."""
    # NOTE: recid can be dummy since it won't reach pass the resource view
    response = client.post(
        "/records/1234-abcd/draft/actions/non-configured", headers=HEADERS
    )

    assert response.status_code == 404
    assert response.json['message'] == \
        'Action non-configured not configured.'


def test_command_not_implemented(client, fake_identity):
    """Tests a configured action without implemented function."""
    # NOTE: recid can be dummy since it won't reach pass the resource view
    response = client.post(
        "/records/1234-abcd/draft/actions/command", headers=HEADERS
    )

    assert response.status_code == 500
    assert response.json['message'] == \
        'Command not_implemented not implemented.'
