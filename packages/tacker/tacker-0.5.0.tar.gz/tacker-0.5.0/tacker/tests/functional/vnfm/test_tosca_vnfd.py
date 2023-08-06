# Copyright 2016 Brocade Communications System, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg
import yaml

from tacker.plugins.common import constants as evt_constants
from tacker.tests.functional import base
from tacker.tests.utils import read_file

CONF = cfg.CONF


class VnfdTestCreate(base.BaseTackerTest):
    def _test_create_list_delete_tosca_vnfd(self, tosca_vnfd_file):
        input_yaml = read_file(tosca_vnfd_file)
        tosca_dict = yaml.safe_load(input_yaml)
        vnfd_name = 'sample-tosca-vnfd'
        tosca_arg = {'vnfd': {'name': vnfd_name,
                              'attributes': {'vnfd': tosca_dict}}}
        vnfd_instance = self.client.create_vnfd(body=tosca_arg)
        self.assertIsNotNone(vnfd_instance)

        vnfds = self.client.list_vnfds().get('vnfds')
        self.assertIsNotNone(vnfds, "List of vnfds are Empty after Creation")

        vnfd_id = vnfd_instance['vnfd']['id']
        self.verify_vnfd_events(
            vnfd_id, evt_constants.RES_EVT_CREATE,
            vnfd_instance['vnfd'][evt_constants.RES_EVT_CREATED_FLD])

        try:
            self.client.delete_vnfd(vnfd_id)
        except Exception:
            assert False, "vnfd Delete failed"
        self.verify_vnfd_events(vnfd_id, evt_constants.RES_EVT_DELETE)

    def test_tosca_vnfd(self):
        self._test_create_list_delete_tosca_vnfd('sample-tosca-vnfd.yaml')

    def test_tosca_large_vnfd(self):
        self._test_create_list_delete_tosca_vnfd(
            'sample-tosca-vnfd-large-template.yaml')
