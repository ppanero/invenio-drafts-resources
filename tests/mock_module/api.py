"""Example of a record draft API."""

from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.systemfields import IndexField

from invenio_drafts_resources.records.api import Draft as DraftBase
from invenio_drafts_resources.records.api import Record as RecordBase

from .models import DraftMetadata, RecordMetadata


class Record(RecordBase):
    """Example record API."""

    # Configuration
    model_cls = RecordMetadata

    # System fields
    schema = ConstantField(
        '$schema', 'http://localhost/schemas/records/record-v1.0.0.json')

    index = IndexField(
        'draftsresources-records-record-v1.0.0',
        search_alias='draftsresources-records'
    )


class Draft(DraftBase):
    """Example record API."""

    # Configuration
    model_cls = DraftMetadata

    # System fields
    schema = ConstantField(
        '$schema', 'http://localhost/schemas/records/record-v1.0.0.json')

    index = IndexField(
        'draftsresources-drafts-draft-v1.0.0',
        search_alias='draftsresources-drafts'
    )
