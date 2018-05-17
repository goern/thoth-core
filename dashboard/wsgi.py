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

import daiquiri

from flask import Flask, Response, jsonify, request, render_template
from flask.helpers import make_response

from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import Counter, Histogram
from prometheus_client import core, generate_latest

import utils
import exceptions

__version__ = '0.1.0'
__description__ = 'Thoth: SrcOps and DevOps Dashboard'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', 'local')


DEBUG = bool(os.getenv('DEBUG', False))

FLASK_REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Flask Request Latency',
                                  ['method', 'endpoint'])
FLASK_REQUEST_COUNT = Counter('flask_request_count', 'Flask Request Count',
                              ['method', 'endpoint', 'http_status'])

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('dashboard_service')

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


def before_request():
    request.start_time = time.time()


def after_request(response):
    request_latency = time.time() - request.start_time
    FLASK_REQUEST_LATENCY.labels(
        request.method, request.path).observe(request_latency)
    FLASK_REQUEST_COUNT.labels(
        request.method, request.path, response.status_code).inc()

    return response


application = Flask(__name__)
application.logger.setLevel(logging.DEBUG)

application.before_request(before_request)
application.after_request(after_request)


@application.route('/readiness')
def api_readiness():
    return jsonify({
        'name': __description__,
        'version': f'v{__version__}+{__git_commit_id__}'
    }), 200, {'ContentType': 'application/json'}


@application.route('/liveness')
def api_liveness():
    return jsonify({
        'name': __description__,
        'version': f'v{__version__}+{__git_commit_id__}'
    }), 200, {'ContentType': 'application/json'}


@application.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/pullrequests')
def getPullRequests():
    include_closed = request.args.get('includeClosed')

    if include_closed is None:
        include_closed = False

    logger.debug(f'requesting closed and open pull requests: {include_closed}')

    try:
        open_prs = utils.getPullRequests(include_closed)

        return jsonify(open_prs)

    except exceptions.ThothDashboardServiceMissingAuthToken as e:
        logger.error(e)

        resp = jsonify({'error': e.message})
        resp.headers['Retry-After'] = '180'
        return resp, 503


@application.route('/pullrequests/<int:number>')
def getPullRequestByNumber(number: int):
    try:
        prs = utils.getPullRequestByNumber(number)

        return jsonify(prs)

    except exceptions.ThothDashboardServiceMissingAuthToken as e:
        logger.error(e)

        resp = jsonify({'error': e.message})
        resp.headers['Retry-After'] = '180'
        return resp, 503


@application.route('/imageStreamTags')
def getImageStreamsTags():
    try:
        ist = utils.getImageStreamTags()

        return jsonify(ist)

    except exceptions.ThothDashboardServiceMissingAuthToken as e:
        logger.error(e)

        resp = jsonify({'error': e.message})
        resp.headers['Retry-After'] = '180'
        return resp, 503

    except exceptions.ThothDashboardServiceOpenShiftUnavailable as e:
        logger.error(e.message)

        return jsonify({'error': e.message}), 500


@application.route('/imageStreamTags/<sha>')
def getImageStreamsTagsBySha(sha):
    try:
        tag = utils.getImageStreamTagBySha(sha)

        return jsonify(tag)

    except exceptions.ThothDashboardServiceMissingAuthToken as e:
        logger.error(e)

        resp = jsonify({'error': e.message})
        resp.headers['Retry-After'] = '180'
        return resp, 503

    except exceptions.ThothDashboardServiceOpenShiftUnavailable as e:
        logger.error(e.message)

        return jsonify({'error': e.message}), 500


@application.route('/containers/<deploymentconfig>')
def getContainersByDeploymentConfig(deploymentconfig):
    try:
        pods = utils.getContainersByDeploymentConfig(deploymentconfig)

        return jsonify(pods)

    except exceptions.ThothDashboardServiceMissingAuthToken as e:
        logger.error(e)

        resp = jsonify({'error': e.message})
        resp.headers['Retry-After'] = '180'
        return resp, 503

    except exceptions.ThothDashboardServiceOpenShiftUnavailable as e:
        logger.error(e.message)

        return jsonify({'error': e.message}), 500


@application.route('/builds')
def getBuilds():
    try:
        builds = utils.getBuildByOutputImageSha(
            'sha256:5d44cc5e7fb741b126fc3910c0a06884413232e2ea84cf3cb4257327b226c4b1')

        return jsonify(builds)

    except exceptions.ThothDashboardServiceMissingAuthToken as e:
        logger.error(e)

        resp = jsonify({'error': e.message})
        resp.headers['Retry-After'] = '180'
        return resp, 503

    except exceptions.ThothDashboardServiceOpenShiftUnavailable as e:
        logger.error(e.message)

        return jsonify({'error': e.message}), 500


@application.route('/deploymentStatus/<deploymentconfig>')
def getStatusByDeploymentConfig(deploymentconfig):
    try:
        pods = utils.getContainersByDeploymentConfig(deploymentconfig)

        # FIXME there might be more than one pod!
        ist = utils.getImageStreamTagBySha(pods[0]['pod']['image']['sha'])
        pods[0]['pod']['image']['tag'] = ist

        # add the source reference
        pods[0]['source'] = {}

        return jsonify(pods)

    except exceptions.ThothDashboardServiceMissingAuthToken as e:
        logger.error(e)

        resp = jsonify({'error': e.message})
        resp.headers['Retry-After'] = '180'
        return resp, 503

    except exceptions.ThothDashboardServiceOpenShiftUnavailable as e:
        logger.error(e.message)

        return jsonify({'error': e.message}), 500


if __name__ == "__main__":
    logger.info(
        f'Thoth SrcOps and DevOps Dashboard Service v{__version__}+{__git_commit_id__}')

    application.run(host='0.0.0.0', port=8080, debug=DEBUG)
