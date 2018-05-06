#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   thoth-naming-service
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


class ThothDashboardServiceException(Exception):
    """A base exception for Thoth SrcOps and DevOps Dashboard Service exception hierarchy."""


class ThothDashboardServiceOpenShiftUnavailable(ThothDashboardServiceException):
    """Failure communicating with OpenShift"""

    def __init__(self):
        self.message = "Unable to communicate with OpenShift after successful authentication"


class ThothDashboardServiceMissingAuthToken(ThothDashboardServiceException):
    """A required Auth token has not been provided.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

    def getMessage(self):
        return self.message


class ThothDashboardServiceMissingOpenShiftAuthToken(ThothDashboardServiceMissingAuthToken):
    """The required OpenShift Auth token has not been provided."""

    def __init__(self, env_var_name):
        super(ThothDashboardServiceMissingAuthToken, self).__init__(
            f'The required OpenShift Token has not been provided via environment variable {env_var_name}')
        self.missing_var = env_var_name
        self.message = f'The required OpenShift Token has not been provided via environment variable: {env_var_name}'


class ThothDashboardServiceExpiredOpenShiftAuthToken(ThothDashboardServiceMissingAuthToken):
    """The required OpenShift Auth token has expired."""

    def __init__(self, env_var_name):
        super(ThothDashboardServiceMissingAuthToken, self).__init__(
            f'The required OpenShift Token has expired, please reset environment variable {env_var_name}')
        self.missing_var = env_var_name
        self.message = f'The required OpenShift Token has expired, please reset environment variable {env_var_name}'


class ThothDashboardServiceMissingGitHubAuthToken(ThothDashboardServiceMissingAuthToken):
    """The required GitHub Auth token has not been provided."""

    def __init__(self, env_var_name):
        super(ThothMissingAuthToken, self).__init__(
            f'The required GitHub Token has not been provided via environment variable {env_var_name}')
        self.missing_var = env_var_name
        self.message = f'The required GitHub Token has not been provided via environment variable: {env_var_name}'
