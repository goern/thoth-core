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

import os
import time
import logging

from typing import List

import daiquiri

from github import Github

import openshift.client
from kubernetes.client.rest import ApiException

DEBUG = bool(os.getenv('DEBUG', False))

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('utils')

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


def getOpenPullRequests() -> List:
    """This will get a list of open Pull Requests for all repositories of the Thoth-Station organisation"""
    SESHETA_GITHUB_ACCESS_TOKEN = os.getenv(
        'SESHETA_GITHUB_ACCESS_TOKEN', None)

    if not SESHETA_GITHUB_ACCESS_TOKEN:
        logger.error(
            'Github Token not provided via environment variable SESHETA_GITHUB_ACCESS_TOKEN')
        return None

    github = Github(SESHETA_GITHUB_ACCESS_TOKEN)

    prs = []

    for pr in github.search_issues(
            'is:open is:pr archived:false user:thoth-station '):
        logger.debug(pr)

        prs.append({
            'id': pr.id,
            'number': pr.number,
            'title': pr.title,
            'created_at': pr.created_at,
            'user_login': pr.user.login,
            'repository': pr.repository.name,
            'state': pr.state
        })

    return prs


def getBuildConfigForPullRequest(component: str, number: int) -> dict:
    SESHETA_OPENSHIFT_ACCESS_TOKEN = os.getenv(
        'SESHETA_OPENSHIFT_ACCESS_TOKEN', None)
    THOTH_NAMESPACE = os.getenv(
        'THOTH_NAMESPACE', 'thoth-test-core')

    if not SESHETA_OPENSHIFT_ACCESS_TOKEN:
        logger.error(
            'OpenShift Token not provided via environment variable SESHETA_OPENSHIFT_ACCESS_TOKEN')
        return None

    configuration = openshift.client.Configuration()
    configuration.api_key['authorization'] = SESHETA_OPENSHIFT_ACCESS_TOKEN
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.host = 'https://upshift.engineering.redhat.com'
    configuration.verify_ssl = False

    api_instance = openshift.client.BuildOpenshiftIoV1Api(
        openshift.client.ApiClient(configuration))

    logger.debug(api_instance)

    try:
        api_response = api_instance.list_namespaced_build(THOTH_NAMESPACE)
        print(api_response)
    except ApiException as e:
        logger.error(
            "Exception when calling BuildOpenshiftIoV1Api->list_namespaced_build: %s\n" % e)


if __name__ == '__main__':
    getBuildConfigForPullRequest('user-api', 101)
