# Copyright (c) 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from osc_lib.tests import utils as osc_utils

from saharaclient.api import job_executions as api_je
from saharaclient.osc.v1 import jobs as osc_je
from saharaclient.tests.unit.osc.v1 import fakes

JOB_EXECUTION_INFO = {
    "is_public": False,
    "id": "je_id",
    "interface": [],
    "is_protected": False,
    "input_id": 'input_id',
    "output_id": 'output_id',
    "job_id": "job_id",
    "cluster_id": 'cluster_id',
    "start_time": "start",
    "end_time": "end",
    "engine_job_id": "engine_job_id",
    "info": {
        "status": 'SUCCEEDED'
    },
    "job_configs": {
        "configs": {
            "config1": "1",
            "config2": "2"
        },
        "args": [
            "arg1",
            "arg2"
        ],
        "params": {
            "param2": "value2",
            "param1": "value1"
        }
    }
}


class TestJobs(fakes.TestDataProcessing):
    def setUp(self):
        super(TestJobs, self).setUp()
        self.je_mock = self.app.client_manager.data_processing.job_executions
        self.je_mock.reset_mock()


class TestExecuteJob(TestJobs):
    # TODO(apavlov): check for execution with --interface, --configs, --json
    def setUp(self):
        super(TestExecuteJob, self).setUp()
        self.je_mock.create.return_value = api_je.JobExecution(
            None, JOB_EXECUTION_INFO)
        self.ds_mock = self.app.client_manager.data_processing.data_sources
        self.ds_mock.find_unique.return_value = mock.Mock(id='ds_id')
        self.c_mock = self.app.client_manager.data_processing.clusters
        self.c_mock.find_unique.return_value = mock.Mock(id='cluster_id')
        self.jt_mock = self.app.client_manager.data_processing.jobs
        self.jt_mock.find_unique.return_value = mock.Mock(id='job_id')
        self.ds_mock.reset_mock()
        self.c_mock.reset_mock()
        self.jt_mock.reset_mock()

        # Command to test
        self.cmd = osc_je.ExecuteJob(self.app, None)

    def test_job_execute_minimum_options(self):
        arglist = ['--job-template', 'job-template', '--cluster', 'cluster']
        verifylist = [('job_template', 'job-template'), ('cluster', 'cluster')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.je_mock.create.assert_called_once_with(
            cluster_id='cluster_id', configs={}, input_id='ds_id',
            interface=None, is_protected=False, is_public=False,
            job_id='job_id', output_id='ds_id')

    def test_job_execute_all_options(self):
        arglist = ['--job-template', 'job-template', '--cluster', 'cluster',
                   '--input', 'input', '--output', 'output', '--params',
                   'param1:value1', 'param2:value2', '--args', 'arg1', 'arg2',
                   '--configs', 'config1:1', 'config2:2', '--public',
                   '--protected']

        verifylist = [('job_template', 'job-template'), ('cluster', 'cluster'),
                      ('input', 'input'), ('output', 'output'),
                      ('params', ['param1:value1', 'param2:value2']),
                      ('args', ['arg1', 'arg2']),
                      ('configs', ['config1:1', 'config2:2']),
                      ('public', True),
                      ('protected', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.je_mock.create.assert_called_once_with(
            cluster_id='cluster_id',
            configs={'configs': {'config1': '1', 'config2': '2'},
                     'args': ['arg1', 'arg2'],
                     'params': {'param2': 'value2', 'param1': 'value1'}},
            input_id='ds_id', interface=None, is_protected=True,
            is_public=True, job_id='job_id', output_id='ds_id')

        # Check that columns are correct
        expected_columns = ('Cluster id', 'End time', 'Engine job id', 'Id',
                            'Input id', 'Is protected', 'Is public',
                            'Job template id', 'Output id', 'Start time',
                            'Status')
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = ('cluster_id', 'end', 'engine_job_id', 'je_id',
                         'input_id', False, False, 'job_id', 'output_id',
                         'start', 'SUCCEEDED')
        self.assertEqual(expected_data, data)


class TestListJobs(TestJobs):
    def setUp(self):
        super(TestListJobs, self).setUp()
        self.je_mock.list.return_value = [api_je.JobExecution(
            None, JOB_EXECUTION_INFO)]

        # Command to test
        self.cmd = osc_je.ListJobs(self.app, None)

    def test_jobs_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        expected_columns = ['Id', 'Cluster id', 'Job id', 'Status']
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = [('je_id', 'cluster_id', 'job_id', 'SUCCEEDED')]
        self.assertEqual(expected_data, list(data))

    def test_jobs_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        expected_columns = ['Id', 'Cluster id', 'Job id', 'Status',
                            'Start time', 'End time']
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = [('je_id', 'cluster_id', 'job_id', 'SUCCEEDED',
                          'start', 'end')]
        self.assertEqual(expected_data, list(data))

    def test_jobs_list_extra_search_opts(self):
        arglist = ['--status', 'succeeded']
        verifylist = [('status', 'succeeded')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        expected_columns = ['Id', 'Cluster id', 'Job id', 'Status']
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = [('je_id', 'cluster_id', 'job_id', 'SUCCEEDED')]
        self.assertEqual(expected_data, list(data))


class TestShowJob(TestJobs):
    def setUp(self):
        super(TestShowJob, self).setUp()
        self.je_mock.get.return_value = api_je.JobExecution(
            None, JOB_EXECUTION_INFO)

        # Command to test
        self.cmd = osc_je.ShowJob(self.app, None)

    def test_job_show(self):
        arglist = ['job_id']
        verifylist = [('job', 'job_id')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.je_mock.get.assert_called_once_with('job_id')

        # Check that columns are correct
        expected_columns = ('Cluster id', 'End time', 'Engine job id', 'Id',
                            'Input id', 'Is protected', 'Is public',
                            'Job template id', 'Output id', 'Start time',
                            'Status')
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = ('cluster_id', 'end', 'engine_job_id', 'je_id',
                         'input_id', False, False, 'job_id', 'output_id',
                         'start', 'SUCCEEDED')
        self.assertEqual(expected_data, data)


class TestDeleteJob(TestJobs):
    def setUp(self):
        super(TestDeleteJob, self).setUp()
        self.je_mock.get.return_value = api_je.JobExecution(
            None, JOB_EXECUTION_INFO)

        # Command to test
        self.cmd = osc_je.DeleteJob(self.app, None)

    def test_job_delete(self):
        arglist = ['job_id']
        verifylist = [('job', ['job_id'])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.je_mock.delete.assert_called_once_with('job_id')


class TestUpdateJob(TestJobs):
    def setUp(self):
        super(TestUpdateJob, self).setUp()
        self.je_mock.get.return_value = api_je.JobExecution(
            None, JOB_EXECUTION_INFO)
        self.je_mock.update.return_value = mock.Mock(
            job_execution=JOB_EXECUTION_INFO.copy())

        # Command to test
        self.cmd = osc_je.UpdateJob(self.app, None)

    def test_job_update_no_options(self):
        arglist = []
        verifylist = []

        self.assertRaises(osc_utils.ParserException, self.check_parser,
                          self.cmd, arglist, verifylist)

    def test_job_update_nothing_updated(self):
        arglist = ['job_id']

        verifylist = [('job', 'job_id')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.je_mock.update.assert_called_once_with('job_id')

    def test_job_update_public_protected(self):
        arglist = ['job_id', '--public', '--protected']

        verifylist = [('job', 'job_id'), ('is_public', True),
                      ('is_protected', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.je_mock.update.assert_called_once_with(
            'job_id', is_protected=True, is_public=True)

        # Check that columns are correct
        expected_columns = ('Cluster id', 'End time', 'Engine job id', 'Id',
                            'Input id', 'Is protected', 'Is public',
                            'Job template id', 'Output id', 'Start time',
                            'Status')
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = ('cluster_id', 'end', 'engine_job_id', 'je_id',
                         'input_id', False, False, 'job_id', 'output_id',
                         'start', 'SUCCEEDED')
        self.assertEqual(expected_data, data)

    def test_job_update_private_unprotected(self):
        arglist = ['job_id', '--private', '--unprotected']

        verifylist = [('job', 'job_id'), ('is_public', False),
                      ('is_protected', False)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.je_mock.update.assert_called_once_with(
            'job_id', is_protected=False, is_public=False)
