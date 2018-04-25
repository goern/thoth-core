#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   thoth-core
#   Copyright(C) 2018 Christoph Görn
#
#   This program is free software: you can redistribute it and / or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Thoth: Core: End-to-End Tests: Result API feature test steps."""

from http import HTTPStatus

import requests

from behave import given, when, then
from hamcrest import assert_that, equal_to, is_not, not_none


@given('I am using the TEST environement')
def step_impl(context):
    # TODO read this from ENV
    context.endpoint_url = 'http://user-api-thoth-test-core.cloud.upshift.engineering.redhat.com/api/v1'


@given(u'the TEST database is empty')
def step_impl(context):
    payload = {
        'secret': 'secret101'
    }
    r = requests.post(
        f'{context.endpoint_url}/erase-graph', params=payload)

    assert_that(r.status_code, equal_to(HTTPStatus.OK))
