# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 National Institute of Informatics.
#
# WEKO-Notifications is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

import pytest
from unittest.mock import patch
from marshmallow import ValidationError

from weko_notifications.config import COAR_NOTIFY_CONTEXT
from weko_notifications.notifications import Notification, ActivityType

# .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace

# class TestNotifications:
# .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
class TestNotifications:
    # def __init__(self):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test__init__ -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test__init__(self):
        notification = Notification()
        assert notification.activity_type == None
        assert notification.origin == {}
        assert notification.target == {}
        assert notification.object == {}
        assert notification.actor == {}
        assert notification.context == {}
        assert notification.in_reply_to == None
        assert notification.payload == {}
        assert notification._is_validated == False

    # def body(self):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_current_body -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_current_body(self, json_notifications):
        after_approval = json_notifications["after_approval"]
        notification = Notification()
        notification.payload["id"] = after_approval["id"]
        notification.activity_type = after_approval["type"]
        notification.origin = after_approval["origin"]
        notification.target = after_approval["target"]
        notification.object = after_approval["object"]
        notification.actor = after_approval["actor"]
        notification.context = after_approval["context"]
        notification.in_reply_to = after_approval["inReplyTo"]

        assert notification.current_body == after_approval

    # def __str__(self):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test__str__ -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test__str__(self, json_notifications):
        after_approval = json_notifications["after_approval"]
        notification = Notification()
        notification.payload["id"] = after_approval["id"]
        notification.activity_type = after_approval["type"]
        notification.origin = after_approval["origin"]
        notification.target = after_approval["target"]
        notification.object = after_approval["object"]
        notification.actor = after_approval["actor"]
        notification.context = after_approval["context"]
        notification.in_reply_to = after_approval["inReplyTo"]

        result = str(notification)
        assert result == str(notification.current_body)
        assert len(result) == len(str(after_approval))

        assert str(after_approval["id"]) in result

    # def __eq__(self, other):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test__eq__ -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test__eq__(self, json_notifications):
        after_approval = json_notifications["after_approval"]
        offer_approval = json_notifications["offer_approval"]
        notification = Notification().load(after_approval)
        notification2 = Notification().load(after_approval)
        notification3 = Notification().load(offer_approval)

        assert notification == notification2
        assert notification != notification3

    # def create(self):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_create -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_create(self, json_notifications):
        after_approval = json_notifications["after_approval"]
        notification = Notification()
        notification.payload["id"] = after_approval["id"]
        notification.activity_type = after_approval["type"]
        notification.origin = after_approval["origin"]
        notification.target = after_approval["target"]
        notification.object = after_approval["object"]
        notification.actor = after_approval["actor"]
        notification.context = after_approval["context"]
        notification.in_reply_to = after_approval["inReplyTo"]

        notification.create()

        assert notification.payload.pop("updated") is not None
        assert notification.payload == after_approval
        assert notification._is_validated == True

    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_validate_success -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_validate_success(self):
        notification = Notification()
        notification.activity_type = ["Announce"]
        notification.origin = {
            "id": "urn:uuid:123e4567-e89b-12d3-a456-426614174001",
            "type": "Service",
            "inbox": "https://example.org/inbox"
        }
        notification.target = {
            "id": "urn:uuid:123e4567-e89b-12d3-a456-426614174002",
            "type": "Service",
            "inbox": "https://example.org/inbox2"
        }
        notification.object = {
            "id": "urn:uuid:123e4567-e89b-12d3-a456-426614174003"
        }
        notification.actor = {
            "id": "urn:uuid:123e4567-e89b-12d3-a456-426614174004",
            "type": "Person",
            "name": "Test Actor"
        }
        notification.context = {
            "id": "urn:uuid:123e4567-e89b-12d3-a456-426614174005"
        }
        notification.in_reply_to = None
        notification.payload["id"] = "urn:uuid:123e4567-e89b-12d3-a456-426614174000"
        notification.payload["@context"] = [
            "https://www.w3.org/ns/activitystreams",
            "https://purl.org/coar/notify"
        ]
        result = notification.validate()
        assert result is notification
        assert notification._is_validated is True

    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_send -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    @pytest.mark.parametrize("patch_send,client_type,expected_exception,expected_result", [
        (True, "valid", None, "dummy_id"),
        (False, "invalid", TypeError, None),
    ])
    def test_send(self, patch_send, client_type, expected_exception, expected_result):
        from weko_notifications.client import NotificationClient
        notification = Notification()
        if client_type == "valid":
            client = NotificationClient(inbox="https://example.org/inbox")
            if patch_send:
                client.send = lambda n: "dummy_id"
        else:
            client = object()
        if expected_exception:
            with pytest.raises(expected_exception):
                notification.send(client)
        else:
            result = notification.send(client)
            assert result == expected_result
    
    # def load(self, payload):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_load -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_load(self, json_notifications):
        after_approval = json_notifications["after_approval"]
        notification = Notification().load(after_approval)

        assert notification.payload.pop("updated") is not None
        assert notification.payload == after_approval
        assert notification._is_validated == True

    # def create_item_registared(cls, target_id, actor_id, object_id, **kwargs):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_create_item_registared -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_create_item_registared(self, app, json_notifications):
        after_registration = json_notifications["after_registration"]
        after_registration.pop("id")

        notification = Notification.create_item_registered(
            target_id=3,
            actor_id=3,
            object_id=2000001,
            object_name="A new record",
            actor_name="Alex",
            ietf_cite_as="https://doi.org/10.34477/0002000001"
        )

        assert notification.payload.pop("id") is not None
        assert notification.payload.pop("updated") is not None
        assert notification.payload["@context"] == COAR_NOTIFY_CONTEXT
        assert notification.activity_type == ActivityType.ANNOUNCE_INGEST.value
        assert notification.payload == after_registration
        assert notification._is_validated == True

    # def create_request_approval(cls, target_id, object_id, actor_id, context_id, **kwargs):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_create_request_approval -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_create_request_approval(self, app, json_notifications):
        offer_approval = json_notifications["offer_approval"]
        offer_approval.pop("id")

        notification = Notification.create_request_approval(
            target_id=1,
            actor_id=3,
            object_id=2000001,
            object_name="A new record",
            context_id="A-20250306-00001",
            actor_name="Alex"
        )

        assert notification.payload.pop("id") is not None
        assert notification.payload.pop("updated") is not None
        assert notification.payload["@context"] == COAR_NOTIFY_CONTEXT
        assert notification.activity_type == ActivityType.OFFER_ENDORSE.value
        assert notification.payload == offer_approval
        assert notification._is_validated == True

    # def create_item_approved(cls, target_id, object_id, actor_id, context_id, **kwargs):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_create_item_approved -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_create_item_approved(self, app, json_notifications):
        after_approval = json_notifications["after_approval"]
        after_approval.pop("id")
        after_approval.pop("inReplyTo")

        notification = Notification.create_item_approved(
            target_id=3,
            actor_id=1,
            object_id=2000001,
            object_name="A new record",
            context_id="A-20250306-00001",
            actor_name="Admin",
            ietf_cite_as="https://doi.org/10.34477/0002000001"
        )

        assert notification.payload.pop("id") is not None
        assert notification.payload.pop("updated") is not None
        assert notification.payload["@context"] == COAR_NOTIFY_CONTEXT
        assert notification.activity_type == ActivityType.ANNOUNCE_ENDORSE.value
        assert notification.payload == after_approval
        assert notification._is_validated == True

    # def create_item_rejected(cls, target_id, object_id, actor_id, context_id, **kwargs):
    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_create_item_rejected -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_create_item_rejected(self, app, json_notifications):
        after_rejection = json_notifications["after_rejection"]
        after_rejection.pop("id")
        after_rejection.pop("inReplyTo")

        notification = Notification.create_item_rejected(
            target_id=3,
            actor_id=1,
            object_id=2000001,
            object_name="A new record",
            context_id="A-20250306-00001",
            actor_name="Admin"
        )

        assert notification.payload.pop("id") is not None
        assert notification.payload.pop("updated") is not None
        assert notification.payload["@context"] == COAR_NOTIFY_CONTEXT
        assert notification.activity_type == ActivityType.ACKNOWLEDGE_AND_REJECT.value
        assert notification.payload == after_rejection
        assert notification._is_validated == True

    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_create_request_delete_approval -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_create_request_delete_approval(self, app):
        notification = Notification.create_request_delete_approval(
            target_id=1,
            object_id=2000001,
            actor_id=2,
            context_id=123,
            object_name="Test Object",
            actor_name="Test Actor"
        )
        assert notification.payload["type"] == ActivityType.OFFER_ENDORSE.deletion_value
        assert notification._is_validated is True

    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_create_item_delete_approved -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_create_item_delete_approved(self, app):
        notification = Notification.create_item_delete_approved(
            target_id=1,
            object_id=2000001,
            actor_id=2,
            context_id=123,
            object_name="Test Object",
            ietf_cite_as="https://doi.org/10.1234/0002000001",
            actor_name="Test Actor"
        )
        assert notification.payload["type"] == ActivityType.ANNOUNCE_ENDORSE.deletion_value
        assert notification._is_validated is True

    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_create_item_delete_rejected -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
    def test_create_item_delete_rejected(self, app):
        notification = Notification.create_item_delete_rejected(
            target_id=1,
            object_id=2000001,
            actor_id=2,
            context_id=123,
            object_name="Test Object",
            ietf_cite_as="https://doi.org/10.1234/0002000001",
            actor_name="Test Actor"
        )
        assert notification.payload["type"] == ActivityType.ACKNOWLEDGE_AND_REJECT.deletion_value
        assert notification._is_validated is True

    # .tox/c1/bin/pytest --cov=weko_notifications tests/test_notifications.py::TestNotifications::test_set_all_in_reply_to_direct -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace    
    def test_set_all_in_reply_to_direct(self, app):
        notification = Notification()
        import weko_notifications.notifications as notifications_mod
        notifications_mod.url_for = lambda endpoint, **kwargs: f"https://example.org/{endpoint}"
        notifications_mod.inbox_url = lambda **kwargs: "https://example.org/inbox"
        notifications_mod.user_uri = lambda user_id, **kwargs: f"https://example.org/user/{user_id}"

        notification.create = lambda: notification
        notification.set_type = lambda x: None
        notification.set_origin = lambda **kwargs: None
        notification.set_target = lambda **kwargs: None
        notification.set_object = lambda **kwargs: None
        notification.set_actor = lambda **kwargs: None
        notification.set_context = lambda **kwargs: None

        notification.set_all(
            activity_type=["Announce"],
            target_id=1,
            object_id=2,
            actor_id=3,
            in_reply_to="urn:uuid:direct-test"
        )
        assert notification.in_reply_to == "urn:uuid:direct-test"