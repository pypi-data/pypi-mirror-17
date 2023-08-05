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

import sys

from osc_lib.command import command
from osc_lib import utils as osc_utils
from oslo_log import log as logging

from saharaclient.osc.v1 import utils

DATA_SOURCE_FIELDS = ['name', 'id', 'type', 'url', 'description', 'is_public',
                      'is_protected']
DATA_SOURCE_CHOICES = ["swift", "hdfs", "maprfs", "manila"]


class CreateDataSource(command.ShowOne):
    """Creates data source"""

    log = logging.getLogger(__name__ + ".CreateDataSource")

    def get_parser(self, prog_name):
        parser = super(CreateDataSource, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            metavar="<name>",
            help="Name of the data source",
        )
        parser.add_argument(
            '--type',
            metavar="<type>",
            choices=DATA_SOURCE_CHOICES,
            help="Type of the data source (%s) "
                 "[REQUIRED]" % ', '.join(DATA_SOURCE_CHOICES),
            required=True
        )
        parser.add_argument(
            '--url',
            metavar="<url>",
            help="Url for the data source [REQUIRED]",
            required=True
        )
        parser.add_argument(
            '--username',
            metavar="<username>",
            help="Username for accessing the data source url"
        )
        parser.add_argument(
            '--password',
            metavar="<password>",
            help="Password for accessing the data source url"
        )
        parser.add_argument(
            '--description',
            metavar="<description>",
            help="Description of the data source"
        )
        parser.add_argument(
            '--public',
            action='store_true',
            default=False,
            help='Make the data source public',
        )
        parser.add_argument(
            '--protected',
            action='store_true',
            default=False,
            help='Make the data source protected',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.data_processing

        description = parsed_args.description or ''
        data = client.data_sources.create(
            name=parsed_args.name, description=description,
            data_source_type=parsed_args.type, url=parsed_args.url,
            credential_user=parsed_args.username,
            credential_pass=parsed_args.password,
            is_public=parsed_args.public,
            is_protected=parsed_args.protected).to_dict()

        data = utils.prepare_data(data, DATA_SOURCE_FIELDS)

        return self.dict2columns(data)


class ListDataSources(command.Lister):
    """Lists data sources"""

    log = logging.getLogger(__name__ + ".ListDataSources")

    def get_parser(self, prog_name):
        parser = super(ListDataSources, self).get_parser(prog_name)
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help='List additional fields in output',
        )
        parser.add_argument(
            '--type',
            metavar="<type>",
            choices=DATA_SOURCE_CHOICES,
            help="List data sources of specific type "
                 "(%s)" % ', '.join(DATA_SOURCE_CHOICES)
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.data_processing
        search_opts = {'type': parsed_args.type} if parsed_args.type else {}

        data = client.data_sources.list(search_opts=search_opts)

        if parsed_args.long:
            columns = DATA_SOURCE_FIELDS
            column_headers = utils.prepare_column_headers(columns)

        else:
            columns = ('name', 'id', 'type')
            column_headers = utils.prepare_column_headers(columns)

        return (
            column_headers,
            (osc_utils.get_item_properties(
                s,
                columns
            ) for s in data)
        )


class ShowDataSource(command.ShowOne):
    """Display data source details"""

    log = logging.getLogger(__name__ + ".ShowDataSource")

    def get_parser(self, prog_name):
        parser = super(ShowDataSource, self).get_parser(prog_name)
        parser.add_argument(
            "data_source",
            metavar="<data-source>",
            help="Name or id of the data source to display",
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.data_processing

        data = utils.get_resource(
            client.data_sources, parsed_args.data_source).to_dict()
        data = utils.prepare_data(data, DATA_SOURCE_FIELDS)

        return self.dict2columns(data)


class DeleteDataSource(command.Command):
    """Delete data source"""

    log = logging.getLogger(__name__ + ".DeleteDataSource")

    def get_parser(self, prog_name):
        parser = super(DeleteDataSource, self).get_parser(prog_name)
        parser.add_argument(
            "data_source",
            metavar="<data-source>",
            nargs="+",
            help="Name(s) or id(s) of the data source(s) to delete",
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.data_processing
        for ds in parsed_args.data_source:
            data_source_id = utils.get_resource_id(
                client.data_sources, ds)
            client.data_sources.delete(data_source_id)
            sys.stdout.write(
                'Data Source "{ds}" has been removed '
                'successfully.\n'.format(ds=ds))


class UpdateDataSource(command.ShowOne):
    """Update data source"""

    log = logging.getLogger(__name__ + ".UpdateDataSource")

    def get_parser(self, prog_name):
        parser = super(UpdateDataSource, self).get_parser(prog_name)
        parser.add_argument(
            'data_source',
            metavar="<data-source>",
            help="Name or id of the data source",
        )
        parser.add_argument(
            '--name',
            metavar="<name>",
            help="New name of the data source",
        )
        parser.add_argument(
            '--type',
            metavar="<type>",
            choices=DATA_SOURCE_CHOICES,
            help="Type of the data source "
                 "(%s)" % ', '.join(DATA_SOURCE_CHOICES)
        )
        parser.add_argument(
            '--url',
            metavar="<url>",
            help="Url for the data source"
        )
        parser.add_argument(
            '--username',
            metavar="<username>",
            help="Username for accessing the data source url"
        )
        parser.add_argument(
            '--password',
            metavar="<password>",
            help="Password for accessing the data source url"
        )
        parser.add_argument(
            '--description',
            metavar="<description>",
            help="Description of the data source"
        )
        public = parser.add_mutually_exclusive_group()
        public.add_argument(
            '--public',
            action='store_true',
            dest='is_public',
            help='Make the data source public (Visible from other tenants)',
        )
        public.add_argument(
            '--private',
            action='store_false',
            dest='is_public',
            help='Make the data source private (Visible only from this '
                 'tenant)',
        )
        protected = parser.add_mutually_exclusive_group()
        protected.add_argument(
            '--protected',
            action='store_true',
            dest='is_protected',
            help='Make the data source protected',
        )
        protected.add_argument(
            '--unprotected',
            action='store_false',
            dest='is_protected',
            help='Make the data source unprotected',
        )
        parser.set_defaults(is_public=None, is_protected=None)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.data_processing

        credentials = {}
        if parsed_args.username:
            credentials['user'] = parsed_args.username
        if parsed_args.password:
            credentials['password'] = parsed_args.password
        if not credentials:
            credentials = None

        update_fields = utils.create_dict_from_kwargs(
            name=parsed_args.name,
            description=parsed_args.description,
            type=parsed_args.type, url=parsed_args.url,
            credentials=credentials,
            is_public=parsed_args.is_public,
            is_protected=parsed_args.is_protected)

        ds_id = utils.get_resource_id(
            client.data_sources, parsed_args.data_source)
        data = client.data_sources.update(ds_id, update_fields).data_source
        data = utils.prepare_data(data, DATA_SOURCE_FIELDS)

        return self.dict2columns(data)
