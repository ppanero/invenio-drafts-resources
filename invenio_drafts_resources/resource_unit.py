# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resource Unit."""


class IdentifiedDraft:
    """Resource unit representing pid + Draft data clump."""

    def __init__(self, pid=None, draft=None):
        """Initialize the draft state."""
        self.id = pid.pid_value
        self.pids = [pid]
        self.draft = draft
