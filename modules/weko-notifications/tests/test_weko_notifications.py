# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 National Institute of Informatics.
#
# WEKO-Notifications is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from __future__ import absolute_import, print_function

from flask import Flask

from weko_notifications import WekoNotifications


def test_version():
    """Test version import."""
    from weko_notifications import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = WekoNotifications(app)
    assert 'weko-notifications' in app.extensions

    app = Flask('testapp')
    ext = WekoNotifications()
    assert 'weko-notifications' not in app.extensions
    ext.init_app(app)
    assert 'weko-notifications' in app.extensions

def test_no_after_request_when_notifications_disabled():
    app = Flask('testapp')
    app.config['WEKO_NOTIFICATIONS'] = False
    ext = WekoNotifications(app)
    # Ensure blueprint_ui is not registered
    assert "weko_notifications.ui" not in app.blueprints
    # Ensure after_request is not registered
    assert not any(
        hasattr(f, '__name__') and f.__name__ == "inbox_link"
        for f in app.after_request_funcs.get(None, [])
    )

# .tox/c1/bin/pytest --cov=weko_notifications tests/test_weko_notifications.py::test_inbox_link_after_request_branch_coverage -v -vv -s --cov-branch --cov-report=term --cov-report=html --basetemp=/code/modules/weko-notifications/.tox/c1/tmp --full-trace
def test_inbox_link_after_request_branches():
    from flask import Flask, Response
    from flask_menu import Menu
    from weko_notifications.ext import WekoNotifications

    # endpoint != "weko_theme.index" and HEAD
    app1 = Flask("testapp1")
    Menu(app1)
    app1.config["WEKO_NOTIFICATIONS"] = True
    app1.config["THEME_SITEURL"] = "http://localhost"
    WekoNotifications(app1)
    @app1.route("/notindex", methods=["HEAD"], endpoint="notindex")
    def notindex():
        return Response("", status=200)
    with app1.test_client() as client:
        resp = client.head("/notindex")
        assert "Link" not in resp.headers

    # endpoint == "weko_theme.index" and GET
    app2 = Flask("testapp2")
    Menu(app2)
    app2.config["WEKO_NOTIFICATIONS"] = True
    app2.config["THEME_SITEURL"] = "http://localhost"
    WekoNotifications(app2)
    @app2.route("/get", methods=["GET"], endpoint="weko_theme.index")
    def get_index():
        return Response("ok", status=200)
    with app2.test_client() as client:
        resp = client.get("/get")
        assert "Link" not in resp.headers

    # endpoint == "weko_theme.index" and HEAD
    app3 = Flask("testapp3")
    Menu(app3)
    app3.config["WEKO_NOTIFICATIONS"] = True
    app3.config["THEME_SITEURL"] = "http://localhost"
    WekoNotifications(app3)
    @app3.route("/head", methods=["HEAD"], endpoint="weko_theme.index")
    def head_index():
        return Response("", status=200)
    with app3.test_client() as client:
        resp = client.head("/head")
        assert "Link" in resp.headers
        assert 'rel="http://www.w3.org/ns/ldp#inbox"' in resp.headers["Link"]