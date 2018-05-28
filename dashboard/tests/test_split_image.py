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

"""Thoth: SrcOps and DevOps Dashboard"""

import pytest
from hamcrest import *
import unittest

import utils


@pytest.fixture
def images():
    return [
        'repository/image',
        'repository/image:tag',
        'host/repository/image:tag',
        'docker://host/repository/image:tag'
        'image:tag@sha256:checksum',
        'repository/image:tag@sha256:checksum'
    ]


def test_splitImage(images):
    assert len(images) == 5

    for image in images:
        image, sha = utils._splitImage(image)

        assert_that(image, is_(not_none()))
        assert_that(image, ends_with('image'))
