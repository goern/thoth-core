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

from urllib.parse import urlparse

import daiquiri

from github import Github

import openshift.client
import kubernetes.client
from kubernetes.client.rest import ApiException

import exceptions


DEBUG = bool(os.getenv('DEBUG', False))
THOTH_NAMESPACE = 'thoth-test-core'

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('utils')

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


def getPullRequests(include_closed: bool) -> List:
    """This will get a list of Pull Requests for all repositories of the Thoth-Station organisation"""
    SESHETA_GITHUB_ACCESS_TOKEN = os.getenv(
        'SESHETA_GITHUB_ACCESS_TOKEN', None)

    if not SESHETA_GITHUB_ACCESS_TOKEN:
        raise exceptions.ThothDashboardServiceMissingGitHubAuthToken(
            "SESHETA_GITHUB_ACCESS_TOKEN")

    query = 'is:open is:pr archived:false user:thoth-station '
    if include_closed:
        query = 'is:open is:closed is:pr archived:false user:thoth-station '

    github = Github(SESHETA_GITHUB_ACCESS_TOKEN)

    prs = []

    for pr in github.search_issues(query):
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


def getPullRequestByNumber(number: int) -> List:
    logger.debug(f'looking for Pull Request number {number}')

    SESHETA_GITHUB_ACCESS_TOKEN = os.getenv(
        'SESHETA_GITHUB_ACCESS_TOKEN', None)

    if not SESHETA_GITHUB_ACCESS_TOKEN:
        raise exceptions.ThothDashboardServiceMissingGitHubAuthToken(
            "SESHETA_GITHUB_ACCESS_TOKEN")

    query = 'is:pr archived:false user:thoth-station 101 '

    github = Github(SESHETA_GITHUB_ACCESS_TOKEN)

    prs = []

    for pr in github.search_issues(query):
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


def getImageStreamTags() -> List:
    api_instance = openshift.client.ImageOpenshiftIoV1Api(
        openshift.client.ApiClient(_getOpenShiftConfiguration()))

    ist = []

    try:
        api_response = api_instance.list_namespaced_image_stream(
            THOTH_NAMESPACE)

        for imagestream in api_response.items:
            try:
                for tag in imagestream.status.tags:
                    oldest_generation = 0

                    for image in tag.items:
                        if image.generation > oldest_generation:
                            oldest_generation = image.generation
                            sha = image.image

                    logger.debug(
                        f"ImageStream: {imagestream.metadata.name}, Tag: {tag.tag}, Sha: {sha}")

                    ist.append({
                        'name': imagestream.metadata.name,
                        'tag': tag.tag,
                        'sha': sha
                    })
            except TypeError as e:
                logger.error(
                    f"While analysing {imagestream.metadata.name}: {e}")
                continue

    except ApiException as e:
        logger.error(
            "Exception when calling BuildOpenshiftIoV1Api->list_namespaced_build: %s" % e)
    except ValueError as e:
        logger.error(
            "Exception when calling BuildOpenshiftIoV1Api->list_namespaced_build: %s" % e)

        raise exceptions.ThothDashboardServiceOpenShiftUnavailable()

    return ist


def getImageStreamTagBySha(sha) -> str:
    """ yes, we assume that the sha is unique within the namespace"""

    api_instance = openshift.client.ImageOpenshiftIoV1Api(
        openshift.client.ApiClient(_getOpenShiftConfiguration()))

    ist = getImageStreamTags()

    for tag in ist:
        if sha == tag['sha']:
            return tag['tag']

    return None


def getContainersByDeploymentConfig(deploymentconfig) -> List:
    api_instance = kubernetes.client.CoreV1Api(
        openshift.client.ApiClient(_getOpenShiftConfiguration()))

    pods = []

    try:
        api_response = api_instance.list_namespaced_pod(
            THOTH_NAMESPACE, label_selector=f"deploymentconfig={deploymentconfig}")

        for pod in api_response.items:
            for container in pod.spec.containers:
                logger.debug(f"{pod.metadata.name} {container.image}")

                reg, _img, sha = _splitFullRefImage(container.image)
                ns, img = _splitImage(_img)

                pods.append({
                    'pod_name': pod.metadata.name,
                    'image': {
                        'fullRef': container.image,
                        'registry': reg,
                        'namespace': ns,
                        'image': img,
                        'sha': sha
                    },
                    'name': container.name
                })

    except ApiException as e:
        logger.error(
            "Exception when calling CoreV1Api->list_namespaced_pod: %s" % e)

        if e.reason == 'Unauthorized':
            raise exceptions.ThothDashboardServiceExpiredOpenShiftAuthToken(
                'SESHETA_OPENSHIFT_ACCESS_TOKEN')
    except ValueError as e:
        logger.error(
            "Exception when calling CoreV1Api->list_namespaced_pod: %s" % e)

        raise exceptions.ThothDashboardServiceOpenShiftUnavailable()

    return pods


def _getOpenShiftConfiguration() -> openshift.client.Configuration:
    SESHETA_OPENSHIFT_ACCESS_TOKEN = os.getenv(
        'SESHETA_OPENSHIFT_ACCESS_TOKEN', None)
    THOTH_NAMESPACE = os.getenv(
        'THOTH_NAMESPACE', 'thoth-test-core')

    if not SESHETA_OPENSHIFT_ACCESS_TOKEN:
        raise exceptions.ThothDashboardServiceMissingOpenShiftAuthToken(
            "SESHETA_OPENSHIFT_ACCESS_TOKEN")

    configuration = openshift.client.Configuration()
    configuration.api_key['authorization'] = SESHETA_OPENSHIFT_ACCESS_TOKEN
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.host = 'https://upshift.engineering.redhat.com'
    configuration.verify_ssl = False

    return configuration


def _splitFullRefImage(image: str) -> List:
    if not image.startswith('docker://'):
        image = 'docker://' + image

    # let's splite the image URL and esp the sha
    o = urlparse(image)
    image, sha = o.path.split('@')

    logger.debug(o, image, sha)

    return o.netloc, image, sha


def _splitImage(image: str) -> List:
    s = image.split('/')

    return s[1], s[2]
