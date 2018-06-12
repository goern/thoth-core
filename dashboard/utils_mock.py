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

"""Thoth: SrcOps and DevOps Dashboard - these are mocked up data/methods"""

import os
import time
import logging
import json

from typing import List

from urllib.parse import urlparse

import daiquiri

import utils
import exceptions


DEBUG = bool(os.getenv('DEBUG', False))

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('utils')

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


def getPullRequests(include_closed: bool) -> List:
    result = []

    with open('fixtures/pullrequests.json') as infile:
        data = json.load(infile)

    if include_closed:
        return data

    for pr in data:
        if pr['state'] == 'open':
            result.append(pr)

    return result


def getPullRequestByNumber(number: int) -> List:
    prs = getPullRequests(True)

    for pr in prs:
        if pr['number'] == number:
            return pr

    return None


def getBuildByOutputImageSha(sha: str) -> List:

    return []


def getImageStreamTags() -> List:
    with open('fixtures/imageStreamTags.json') as infile:
        data = json.load(infile)

    return data


def getImageStreamTagBySha(sha) -> str:
    result = []
    ists = getImageStreamTags()

    for ist in ists:
        if ist['sha'] == sha:
            result.append(ist)

    return result


def getContainersByDeploymentConfig(deploymentconfig) -> List:
    result = []
    pods = []

    with open('fixtures/pods.json') as infile:
        data = json.load(infile)

    for pod in data['items']:
        for container in pod['spec']['containers']:
            logger.debug(container['image'])
            reg, _img, sha = utils._splitFullRefImage(container['image'])
            ns, img = utils._splitImage(_img)

            if 'deploymentconfig' in pod['metadata']['labels'].keys():
                if pod['metadata']['labels']['deploymentconfig'] == deploymentconfig:
                    pods.append({
                        'deployment': {
                            'name': pod['metadata']['name'],
                            'image': {
                                'fullRef': container['image'],
                                'registry': reg,
                                'namespace': ns,
                                'image': img,
                                'sha': sha
                            },
                            'containerName': container['name'],
                            'imageStreamTags': getImageStreamTagBySha(sha),
                            'pullRequest': getPullRequestByNumber(101)
                        }
                    })

    return pods
