# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.

import copy
import logging

from cinderclient import exceptions as cinder_exceptions
from novaclient import exceptions as nova_exceptions

from cloudferry.lib.base.action import action
from cloudferry.lib.utils import proxy_client
from cloudferry.lib.utils import utils

LOG = logging.getLogger(__name__)


class AttachVolumesCompute(action.Action):

    def run(self, info, **kwargs):
        info = copy.deepcopy(info)
        compute_res = self.cloud.resources[utils.COMPUTE_RESOURCE]
        storage_res = self.cloud.resources[utils.STORAGE_RESOURCE]
        for instance in info[utils.INSTANCES_TYPE].itervalues():
            if not instance[utils.META_INFO].get(utils.VOLUME_BODY):
                continue
            for vol in instance[utils.META_INFO][utils.VOLUME_BODY]:
                volume = vol['volume']
                volume_id = volume['id']
                status = None
                with proxy_client.expect_exception(cinder_exceptions.NotFound):
                    try:
                        status = storage_res.get_status(volume_id)
                    except cinder_exceptions.NotFound:
                        dst_volume = storage_res.get_migrated_volume(volume_id)
                        if dst_volume:
                            volume_id = dst_volume.id
                            status = dst_volume.status

                if status == 'available':
                    nova_client = compute_res.nova_client
                    inst = instance['instance']
                    try:
                        nova_client.volumes.create_server_volume(
                            inst['id'], volume_id, volume['device'])
                        timeout = self.cfg.migrate.storage_backend_timeout
                        storage_res.try_wait_for_status(volume_id,
                                                        storage_res.get_status,
                                                        'in-use',
                                                        timeout=timeout)
                    except (cinder_exceptions.ClientException,
                            nova_exceptions.ClientException) as e:
                        msg = ("Failed attaching volume %s to instance %s: "
                               "%s. Skipping")
                        LOG.warning(msg, volume_id, inst['id'], e.message)
        return {}
