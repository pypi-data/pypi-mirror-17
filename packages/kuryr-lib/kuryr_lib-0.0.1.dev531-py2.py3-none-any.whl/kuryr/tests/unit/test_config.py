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

from kuryr.tests.unit import base


class ConfigurationTest(base.TestCase):

    def test_defaults(self):

        self.assertEqual('http://127.0.0.1:9696',
                         cfg.CONF.neutron_client.neutron_uri)

        self.assertEqual('kuryr',
                         cfg.CONF.neutron_client.default_subnetpool_v4)

        self.assertEqual('kuryr6',
                         cfg.CONF.neutron_client.default_subnetpool_v6)

        self.assertEqual('http://127.0.0.1:35357/v2.0',
                         cfg.CONF.keystone_client.auth_uri)
