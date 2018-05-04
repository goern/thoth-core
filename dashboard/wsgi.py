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

from flask import Flask, Response, jsonify, request
from flask.helpers import make_response

from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import Counter, Histogram
from prometheus_client import core, generate_latest

import utils

__version__ = '0.1.0'
__description__ = 'Thoth: SrcOps and DevOps Dashboard'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', 'local')


DEBUG = bool(os.getenv('DEBUG', False))

FLASK_REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Flask Request Latency',
                                  ['method', 'endpoint'])
FLASK_REQUEST_COUNT = Counter('flask_request_count', 'Flask Request Count',
                              ['method', 'endpoint', 'http_status'])

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('ops-dashboard')

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
def getOpenPullRequests():
    open_prs = utils.getOpenPullRequests()

    return jsonify(open_prs)


if __name__ == "__main__":
    logger.info(
        f'Thoth Naming Service v{__version__}+{__git_commit_id__}')
    application.run(host='0.0.0.0', port=8080, debug=DEBUG)
