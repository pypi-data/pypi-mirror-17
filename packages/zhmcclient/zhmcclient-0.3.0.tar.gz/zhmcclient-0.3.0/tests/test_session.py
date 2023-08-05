# Copyright 2016 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Unit tests for _session module.
"""

from __future__ import absolute_import

import unittest
import requests
import requests_mock

from zhmcclient._session import Session


class SessionTests(unittest.TestCase):
    """
    Test the ``Session`` class.
    """

    # TODO: Test Session.get() in all variations (including errors)
    # TODO: Test Session.post() in all variations (including errors)
    # TODO: Test Session.delete() in all variations (including errors)

    @staticmethod
    def mock_server_1(m):
        """
        Set up the mocked responses for a simple HMC server that supports
        logon and logoff.
        """
        m.register_uri('POST', '/api/sessions',
                       json={'api-session': 'fake-session-id'},
                       headers={'X-Request-Id': 'fake-request-id'})
        m.register_uri('DELETE', '/api/sessions/this-session',
                       headers={'X-Request-Id': 'fake-request-id'},
                       status_code=204)

    def test_init(self):
        """Test initialization of Session object."""

        session = Session('fake-host', 'fake-user', 'fake-pw')

        self.assertEqual(session.host, 'fake-host')
        self.assertEqual(session.userid, 'fake-user')
        self.assertEqual(session._password, 'fake-pw')
        base_url = 'https://' + session.host + ':6794'
        self.assertEqual(session.base_url, base_url)
        self.assertTrue('Content-type' in session.headers)
        self.assertTrue('Accept' in session.headers)
        self.assertEqual(len(session.headers), 2)
        self.assertIsNone(session.session_id)
        self.assertTrue('X-API-Session' not in session.headers)
        self.assertIsNone(session.session)

    @requests_mock.mock()
    def test_logon_logoff(self, m):
        """Test logon and logoff; this uses post() and delete()."""

        self.mock_server_1(m)

        session = Session('fake-host', 'fake-user', 'fake-pw')

        self.assertIsNone(session.session_id)
        self.assertTrue('X-API-Session' not in session.headers)
        self.assertIsNone(session.session)

        logged_on = session.is_logon()

        self.assertFalse(logged_on)

        session.logon()

        self.assertEqual(session.session_id, 'fake-session-id')
        self.assertTrue('X-API-Session' in session.headers)
        self.assertTrue(isinstance(session.session, requests.Session))

        logged_on = session.is_logon()

        self.assertTrue(logged_on)

        session.logoff()

        self.assertIsNone(session.session_id)
        self.assertTrue('X-API-Session' not in session.headers)
        self.assertIsNone(session.session)

        logged_on = session.is_logon()

        self.assertFalse(logged_on)

    @staticmethod
    def test_delete_completed_job_status():
        """
        This tests the 'Delete Completed Job Status' operation.
        """
        session = Session('fake-host', 'fake-user', 'fake-id')
        with requests_mock.mock() as m:
            # Because logon is deferred until needed, we perform it
            # explicitly in order to keep mocking in the actual test simple.
            m.post('/api/sessions', json={'api-session': 'fake-session-id'})
            session.logon()
        job_uri = "/api/jobs/d9a3788e-683a-11e6-817c-00215e676926"
        with requests_mock.mock() as m:
            result = {}
            m.delete(job_uri, json=result)
            session.delete_completed_job_status(job_uri)

        with requests_mock.mock() as m:
            m.delete('/api/sessions/this-session', status_code=204)
            session.logoff()

    @staticmethod
    def test_query_job_status():
        """
        This tests the 'Query Job Status' operation.
        """
        session = Session('fake-host', 'fake-user', 'fake-id')
        with requests_mock.mock() as m:
            # Because logon is deferred until needed, we perform it
            # explicitly in order to keep mocking in the actual test simple.
            m.post('/api/sessions', json={'api-session': 'fake-session-id'})
            session.logon()
        job_uri = "/api/jobs/d9a3788e-683a-11e6-817c-00215e676926"
        with requests_mock.mock() as m:
            result = {
                "job-reason-code": 0,
                "job-status-code": 204,
                "status": "complete"
            }
            m.get(job_uri, json=result)
            session.query_job_status(job_uri)

        with requests_mock.mock() as m:
            m.delete('/api/sessions/this-session', status_code=204)
            session.logoff()
