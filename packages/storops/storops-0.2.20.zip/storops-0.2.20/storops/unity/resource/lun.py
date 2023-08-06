# Copyright (c) 2015 EMC Corporation.
# All Rights Reserved.
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

from __future__ import unicode_literals

import logging

from storops.unity.resource import UnityResource, UnityResourceList
import storops.unity.resource.pool
from storops.unity.enums import TieringPolicyEnum, NodeEnum, HostLUNAccessEnum
from storops.unity.resource.storage_resource import UnityStorageResource
from storops.exception import UnityResourceNotFoundError
from storops.unity.resource.sp import UnityStorageProcessor

__author__ = 'Jay Xu'

log = logging.getLogger(__name__)


class UnityLun(UnityResource):
    @classmethod
    def create(cls, cli, name, pool, size, sp=None, host_access=None,
               is_thin=None, description=None, iolimit_policy=None,
               is_repl_dst=None, tiering_policy=None, snap_schedule=None):
        pool_clz = storops.unity.resource.pool.UnityPool
        pool = pool_clz.get(cli, pool)

        req_body = cls._compose_lun_parameter(
            cli, name=name, pool=pool, size=size, sp=sp, is_thin=is_thin,
            host_access=host_access, description=description,
            iolimit_policy=iolimit_policy, is_repl_dst=is_repl_dst,
            tiering_policy=tiering_policy, snap_schedule=snap_schedule)
        resp = cli.type_action(UnityStorageResource().resource_class,
                               'createLun', **req_body)
        resp.raise_if_err()
        sr = UnityStorageResource(_id=resp.resource_id, cli=cli)
        return sr.luns[0]

    @staticmethod
    def _compose_lun_parameter(cli, **kwargs):
        sp = kwargs.get('sp')
        if isinstance(sp, UnityStorageProcessor):
            sp_node = sp.to_node_enum()
        else:
            sp_node = None

        TieringPolicyEnum.verify(kwargs.get('tiering_policy'))
        NodeEnum.verify(sp_node)

        # TODO:iolimit_policy and snap_schedule
        req_body = cli.make_body(
            name=kwargs.get('name'),
            description=kwargs.get('description'),
            replicationParameters=cli.make_body(
                isReplicationDestination=kwargs.get('is_repl_dst')
            ),
            lunParameters=cli.make_body(
                isThinEnabled=kwargs.get('is_thin'),
                size=kwargs.get('size'),
                pool=kwargs.get('pool'),
                defaultNode=sp_node,
                fastVPParameters=cli.make_body(
                    tieringPolicy=kwargs.get('tiering_policy')),
            )
        )

        # Empty host access can be used to wipe the host_access
        if 'lunParameters' not in req_body:
            req_body['lunParameters'] = {}
        req_body['lunParameters']['hostAccess'] = cli.make_body(
            kwargs.get('host_access'), allow_empty=True)

        return req_body

    def modify(self, name=None, size=None, host_access=None,
               description=None, is_thin=None, sp=None, iolimit_policy=None,
               is_repl_dst=None, tiering_policy=None, snap_schedule=None):

        req_body = self._compose_lun_parameter(
            self._cli, name=None, pool=None, size=size, sp=sp,
            host_access=host_access, is_thin=is_thin, description=description,
            iolimit_policy=iolimit_policy, is_repl_dst=is_repl_dst,
            tiering_policy=tiering_policy, snap_schedule=snap_schedule
        )
        resp = self._cli.action(UnityStorageResource().resource_class,
                                self.get_id(), 'modifyLun', **req_body)
        resp.raise_if_err()
        return resp

    def delete(self, async=False, force_snap_delete=False,
               force_vvol_delete=False):
        sr = self.storage_resource
        if not self.existed or sr is None:
            raise UnityResourceNotFoundError(
                'cannot find lun {}.'.format(self.get_id()))
        resp = self._cli.delete(sr.resource_class, self.get_id(),
                                forceSnapDeletion=force_snap_delete,
                                forceVvolDeletion=force_vvol_delete,
                                async=async)
        resp.raise_if_err()
        return resp

    def attach_to(self, host, access_mask=HostLUNAccessEnum.PRODUCTION):
        host_access = [{'host': host, 'accessMask': access_mask}]
        # If this lun has been attached to other host, don't overwrite it.
        if self.host_access:
            host_access += [{'host': item.host,
                            'accessMask': item.access_mask} for item
                            in self.host_access if host.id != item.host.id]

        resp = self.modify(host_access=host_access)
        resp.raise_if_err()
        return resp

    def detach_from(self, host):
        if self.host_access is None or not host:
            return None

        new_access = [{
            'host': item.host,
            'accessMask': item.access_mask} for item
                in self.host_access if host.id != item.host.id]
        resp = self.modify(host_access=new_access)
        resp.raise_if_err()
        return resp


class UnityLunList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityLun
