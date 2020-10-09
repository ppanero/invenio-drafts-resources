# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Data access layer tests."""

import pytest
from invenio_search import current_search_client
from jsonschema import ValidationError
from mock_module.api import Draft


#
# Smoke tests
#
def test_record_empty(app, db):
    """Test record creation."""
    # Empty record creation works, and injects a schema.
    record = Draft.create({})
    db.session.commit()
    assert record.schema

    # JSONSchema validation works.
    pytest.raises(
        ValidationError,
        Draft.create,
        {'metadata': {'title': 1}}
    )


def test_record_via_field(app, db):
    """Record creation via field."""
    record = Draft.create({}, metadata={'title': 'test'})
    assert record.metadata == {'title': 'test'}


def test_record_indexing(app, db, es, example_record, indexer):
    """Test indexing of a record."""
    # Index document in ES
    assert indexer.index(example_record)['result'] == 'created'

    # Retrieve document from ES
    data = current_search_client.get(
        'draftsresources-drafts-draft-v1.0.0',
        id=example_record.id,
        doc_type='_doc'
    )

    # Loads the ES data and compare
    record = Draft.loads(data['_source'])
    assert record == example_record
    assert record.id == example_record.id
    assert record.revision_id == example_record.revision_id
    assert record.created == example_record.created
    assert record.updated == example_record.updated
    assert record.expires_at == example_record.expires_at

    # Check system fields
    record.metadata == example_record['metadata']


def test_record_delete_reindex(app, db, es, example_record, example_data,
                               indexer):
    """Test reindexing of a deleted record."""
    record = example_record

    # Index record
    assert indexer.index(record)['result'] == 'created'

    # Delete record.
    record.delete()
    db.session.commit()
    assert indexer.delete(record)['result'] == 'deleted'

    # Update record and reindex (this will cause troubles unless proper
    # optimistic concurrency control is used).
    record.undelete()
    record.commit()
    db.session.commit()
    assert indexer.index(record)['result'] == 'created'
