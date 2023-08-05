#  (c) Copyright 2015 Hewlett Packard Enterprise Development LP
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

DIRECTORY = '/tmp/'
TEST_CLI_CONFIG = '/tmp/cli.conf'
CLI_CONFIG = '/etc/cinderdiags/cli.conf'
NOVA_PACKAGES = [
    ('sysfsutils',  '2.1'),
    ('sg3-utils || sg3_utils', '1.3'),
]
CINDER_PACKAGES = [
    ('python-3parclient', '4.2.0'),
    ('sysfsutils',  '2.1'),
    ('sg3-utils || sg3_utils', '1.3'),
]
HPE3PAR_DRIVERS = [
    'hpe_3par_iscsi.HPE3PARISCSIDriver',
    'hpe_3par_fc.HPE3PARFCDriver'
]
