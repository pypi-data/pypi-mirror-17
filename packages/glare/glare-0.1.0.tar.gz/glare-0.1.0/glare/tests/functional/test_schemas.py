# Copyright 2016 OpenStack Foundation
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

import jsonschema

from oslo_serialization import jsonutils
import requests

from glare.common import utils
from glare.tests import functional

fixture_base_props = {
    u'activated_at': {
        u'description': u'Datetime when artifact has became active.',
        u'filter_ops': [u'eq',
                        u'neq',
                        u'in',
                        u'gt',
                        u'gte',
                        u'lt',
                        u'lte'],
        u'format': u'date-time',
        u'readOnly': True,
        u'required_on_activate': False,
        u'sortable': True,
        u'type': [u'string',
                  u'null']},
    u'created_at': {
        u'description': u'Datetime when artifact has been created.',
        u'filter_ops': [u'eq',
                        u'neq',
                        u'in',
                        u'gt',
                        u'gte',
                        u'lt',
                        u'lte'],
        u'format': u'date-time',
        u'readOnly': True,
        u'sortable': True,
        u'type': u'string'},
    u'description': {u'default': u'',
                     u'description': u'Artifact description.',
                     u'filter_ops': [u'eq',
                                     u'neq',
                                     u'in'],
                     u'maxLength': 4096,
                     u'mutable': True,
                     u'required_on_activate': False,
                     u'type': [u'string',
                               u'null']},
    u'icon': {u'additionalProperties': False,
              u'description': u'Artifact icon.',
              u'filter_ops': [],
              u'properties': {u'md5': {u'type': [u'string', u'null']},
                              u'sha1': {u'type': [u'string', u'null']},
                              u'sha256': {u'type': [u'string', u'null']},
                              u'content_type': {u'type': u'string'},
                              u'external': {u'type': u'boolean'},
                              u'size': {u'type': [u'number',
                                                  u'null']},
                              u'status': {u'enum': [u'saving',
                                                    u'active',
                                                    u'pending_delete'],
                                          u'type': u'string'}},
              u'required': [u'size',
                            u'md5', u'sha1', u'sha256',
                            u'external',
                            u'status',
                            u'content_type'],
              u'required_on_activate': False,
              u'type': [u'object',
                        u'null']},
    u'id': {u'description': u'Artifact UUID.',
            u'filter_ops': [u'eq',
                            u'neq',
                            u'in'],
            u'maxLength': 255,
            u'pattern': u'^([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}'
                        u'-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}$',
            u'readOnly': True,
            u'sortable': True,
            u'type': u'string'},
    u'license': {u'description': u'Artifact license type.',
                 u'filter_ops': [u'eq',
                                 u'neq',
                                 u'in'],
                 u'maxLength': 255,
                 u'required_on_activate': False,
                 u'type': [u'string',
                           u'null']},
    u'license_url': {u'description': u'URL to artifact license.',
                     u'filter_ops': [u'eq',
                                     u'neq',
                                     u'in'],
                     u'maxLength': 255,
                     u'required_on_activate': False,
                     u'type': [u'string',
                               u'null']},
    u'metadata': {u'additionalProperties': {u'type': u'string'},
                  u'default': {},
                  u'description': u'Key-value dict with useful information '
                                  u'about an artifact.',
                  u'filter_ops': [u'eq',
                                  u'neq'],
                  u'maxProperties': 255,
                  u'required_on_activate': False,
                  u'type': [u'object',
                            u'null']},
    u'name': {u'description': u'Artifact Name.',
              u'filter_ops': [u'eq',
                              u'neq',
                              u'in'],
              u'maxLength': 255,
              u'required_on_activate': False,
              u'sortable': True,
              u'type': u'string'},
    u'owner': {u'description': u'ID of user/tenant who uploaded artifact.',
               u'filter_ops': [u'eq',
                               u'neq',
                               u'in'],
               u'maxLength': 255,
               u'readOnly': True,
               u'required_on_activate': False,
               u'sortable': True,
               u'type': u'string'},
    u'provided_by': {u'additionalProperties': False,
                     u'description': u'Info about artifact authors.',
                     u'filter_ops': [u'eq',
                                     u'neq',
                                     u'in'],
                     u'maxProperties': 255,
                     u'properties': {u'company': {u'type': u'string'},
                                     u'href': {u'type': u'string'},
                                     u'name': {u'type': u'string'}},
                     u'required_on_activate': False,
                     u'type': [u'object',
                               u'null']},
    u'release': {u'default': [],
                 u'description': u'Target Openstack release for artifact. It '
                                 u'is usually the same when artifact was '
                                 u'uploaded.',
                 u'filter_ops': [u'eq',
                                 u'neq',
                                 u'in'],
                 u'items': {u'type': u'string'},
                 u'maxItems': 255,
                 u'required_on_activate': False,
                 u'type': [u'array',
                           u'null'],
                 u'unique': True},
    u'status': {u'default': u'drafted',
                u'description': u'Artifact status.',
                u'enum': [u'drafted',
                          u'active',
                          u'deactivated',
                          u'deleted'],
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'sortable': True,
                u'type': u'string'},
    u'supported_by': {u'additionalProperties': {u'type': u'string'},
                      u'description': u'Info about persons who responsible '
                                      u'for artifact support',
                      u'filter_ops': [u'eq',
                                      u'neq',
                                      u'in'],
                      u'maxProperties': 255,
                      u'required': [u'name'],
                      u'required_on_activate': False,
                      u'type': [u'object',
                                u'null']},
    u'tags': {u'default': [],
              u'description': u'List of tags added to Artifact.',
              u'filter_ops': [u'eq',
                              u'neq',
                              u'in'],
              u'items': {u'type': u'string'},
              u'maxItems': 255,
              u'mutable': True,
              u'required_on_activate': False,
              u'type': [u'array',
                        u'null']},
    u'updated_at': {
        u'description': u'Datetime when artifact has been updated last time.',
        u'filter_ops': [u'eq',
                        u'neq',
                        u'in',
                        u'gt',
                        u'gte',
                        u'lt',
                        u'lte'],
        u'format': u'date-time',
        u'readOnly': True,
        u'sortable': True,
        u'type': u'string'},
    u'version': {u'default': u'0.0.0',
                 u'description': u'Artifact version(semver).',
                 u'filter_ops': [u'eq',
                                 u'neq',
                                 u'in',
                                 u'gt',
                                 u'gte',
                                 u'lt',
                                 u'lte'],
                 u'pattern': u'/^([0-9]+)\\.([0-9]+)\\.([0-9]+)(?:-'
                             u'([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?'
                             u'(?:\\+[0-9A-Za-z-]+)?$/',
                 u'required_on_activate': False,
                 u'sortable': True,
                 u'type': u'string'},
    u'visibility': {u'default': u'private',
                    u'description': u'Artifact visibility that defines if '
                                    u'artifact can be available to other '
                                    u'users.',
                    u'filter_ops': [u'eq'],
                    u'maxLength': 255,
                    u'sortable': True,
                    u'type': u'string'}
}

enabled_artifact_types = (
    u'sample_artifact', u'images', u'heat_templates',
    u'heat_environments', u'tosca_templates', u'murano_packages')


def generate_type_props(props):
    props.update(fixture_base_props)
    return props


fixtures = {
    u'sample_artifact': {
        u'name': u'sample_artifact',
        u'properties': generate_type_props({
            u'blob': {u'additionalProperties': False,
                      u'description': u'I am Blob',
                      u'filter_ops': [],
                      u'mutable': True,
                      u'properties': {
                          u'md5': {u'type': [u'string', u'null']},
                          u'sha1': {u'type': [u'string', u'null']},
                          u'sha256': {u'type': [u'string', u'null']},
                          u'content_type': {
                              u'type': u'string'},
                          u'external': {
                              u'type': u'boolean'},
                          u'size': {u'type': [
                              u'number',
                              u'null']},
                          u'status': {
                              u'enum': [
                                  u'saving',
                                  u'active',
                                  u'pending_delete'],
                              u'type': u'string'}},
                      u'required': [u'size',
                                    u'md5', u'sha1', u'sha256',
                                    u'external',
                                    u'status',
                                    u'content_type'],
                      u'required_on_activate': False,
                      u'type': [u'object',
                                u'null']},
            u'bool1': {u'default': False,
                       u'filter_ops': [u'eq'],
                       u'required_on_activate': False,
                       u'type': [u'string',
                                 u'null']},
            u'bool2': {u'default': False,
                       u'filter_ops': [u'eq'],
                       u'required_on_activate': False,
                       u'type': [u'string',
                                 u'null']},
            u'dependency1': {u'filter_ops': [u'eq',
                                             u'neq',
                                             u'in'],
                             u'required_on_activate': False,
                             u'type': [u'string',
                                       u'null']},
            u'dependency2': {u'filter_ops': [u'eq',
                                             u'neq',
                                             u'in'],
                             u'required_on_activate': False,
                             u'type': [u'string',
                                       u'null']},
            u'dict_of_blobs': {
                u'additionalProperties': {
                    u'additionalProperties': False,
                    u'properties': {
                        u'md5': {u'type': [u'string', u'null']},
                        u'sha1': {u'type': [u'string', u'null']},
                        u'sha256': {u'type': [u'string', u'null']},
                        u'content_type': {
                            u'type': u'string'},
                        u'external': {
                            u'type': u'boolean'},
                        u'size': {
                            u'type': [
                                u'number',
                                u'null']},
                        u'status': {
                            u'enum': [
                                u'saving',
                                u'active',
                                u'pending_delete'],
                            u'type': u'string'}},
                    u'required': [u'size',
                                  u'md5', u'sha1', u'sha256',
                                  u'external',
                                  u'status',
                                  u'content_type'],
                    u'type': [u'object',
                              u'null']},
                u'default': {},
                u'filter_ops': [],
                u'maxProperties': 255,
                u'required_on_activate': False,
                u'type': [u'object',
                          u'null']},
            u'dict_of_int': {
                u'additionalProperties': {
                    u'type': u'string'},
                u'default': {},
                u'filter_ops': [u'eq'],
                u'maxProperties': 255,
                u'required_on_activate': False,
                u'type': [u'object',
                          u'null']},
            u'dict_of_str': {
                u'additionalProperties': {
                    u'type': u'string'},
                u'default': {},
                u'filter_ops': [u'eq'],
                u'maxProperties': 255,
                u'required_on_activate': False,
                u'type': [u'object',
                          u'null']},
            u'dict_validators': {
                u'additionalProperties': False,
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxProperties': 3,
                u'properties': {
                    u'abc': {u'type': [u'string',
                                       u'null']},
                    u'def': {u'type': [u'string',
                                       u'null']},
                    u'ghi': {u'type': [u'string',
                                       u'null']},
                    u'jkl': {u'type': [u'string',
                                       u'null']}},
                u'required_on_activate': False,
                u'type': [u'object',
                          u'null']},
            u'float1': {u'filter_ops': [u'eq',
                                        u'neq',
                                        u'in',
                                        u'gt',
                                        u'gte',
                                        u'lt',
                                        u'lte'],
                        u'required_on_activate': False,
                        u'sortable': True,
                        u'type': [u'number',
                                  u'null']},
            u'float2': {u'filter_ops': [u'eq',
                                        u'neq',
                                        u'in',
                                        u'gt',
                                        u'gte',
                                        u'lt',
                                        u'lte'],
                        u'required_on_activate': False,
                        u'sortable': True,
                        u'type': [u'number',
                                  u'null']},
            u'int1': {u'filter_ops': [u'eq',
                                      u'neq',
                                      u'in',
                                      u'gt',
                                      u'gte',
                                      u'lt',
                                      u'lte'],
                      u'required_on_activate': False,
                      u'sortable': True,
                      u'type': [u'integer',
                                u'null']},
            u'int2': {u'filter_ops': [u'eq',
                                      u'neq',
                                      u'in',
                                      u'gt',
                                      u'gte',
                                      u'lt',
                                      u'lte'],
                      u'required_on_activate': False,
                      u'sortable': True,
                      u'type': [u'integer',
                                u'null']},
            u'int_validators': {u'filter_ops': [u'eq',
                                                u'neq',
                                                u'in',
                                                u'gt',
                                                u'gte',
                                                u'lt',
                                                u'lte'],
                                u'maximum': 20,
                                u'minumum': 10,
                                u'required_on_activate': False,
                                u'type': [u'integer',
                                          u'null']},
            u'list_of_int': {u'default': [],
                             u'filter_ops': [u'eq'],
                             u'items': {
                                 u'type': u'string'},
                             u'maxItems': 255,
                             u'required_on_activate': False,
                             u'type': [u'array',
                                       u'null']},
            u'list_of_str': {u'default': [],
                             u'filter_ops': [u'eq'],
                             u'items': {
                                 u'type': u'string'},
                             u'maxItems': 255,
                             u'required_on_activate': False,
                             u'type': [u'array',
                                       u'null']},
            u'list_validators': {u'default': [],
                                 u'filter_ops': [
                                     u'eq',
                                     u'neq',
                                     u'in'],
                                 u'items': {
                                     u'type': u'string'},
                                 u'maxItems': 3,
                                 u'required_on_activate': False,
                                 u'type': [u'array',
                                           u'null'],
                                 u'unique': True},
            u'small_blob': {u'additionalProperties': False,
                            u'filter_ops': [],
                            u'mutable': True,
                            u'properties': {
                                u'md5': {u'type': [u'string', u'null']},
                                u'sha1': {u'type': [u'string', u'null']},
                                u'sha256': {u'type': [u'string', u'null']},
                                u'content_type': {
                                    u'type': u'string'},
                                u'external': {
                                    u'type': u'boolean'},
                                u'size': {
                                    u'type': [
                                        u'number',
                                        u'null']},
                                u'status': {
                                    u'enum': [
                                        u'saving',
                                        u'active',
                                        u'pending_delete'],
                                    u'type': u'string'}},
                            u'required': [u'size',
                                          u'md5', u'sha1', u'sha256',
                                          u'external',
                                          u'status',
                                          u'content_type'],
                            u'required_on_activate': False,
                            u'type': [u'object',
                                      u'null']},
            u'str1': {u'filter_ops': [u'eq',
                                      u'neq',
                                      u'in',
                                      u'gt',
                                      u'gte',
                                      u'lt',
                                      u'lte'],
                      u'maxLength': 255,
                      u'required_on_activate': False,
                      u'sortable': True,
                      u'type': [u'string',
                                u'null']},
            u'string_mutable': {u'filter_ops': [u'eq',
                                                u'neq',
                                                u'in',
                                                u'gt',
                                                u'gte',
                                                u'lt',
                                                u'lte'],
                                u'maxLength': 255,
                                u'mutable': True,
                                u'required_on_activate': False,
                                u'type': [u'string',
                                          u'null']},
            u'string_required': {
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in',
                                u'gt',
                                u'gte',
                                u'lt',
                                u'lte'],
                u'maxLength': 255,
                u'type': [u'string',
                          u'null']},
            u'string_validators': {
                u'enum': [u'aa',
                          u'bb',
                          u'ccccccccccc',
                          None],
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in',
                                u'gt',
                                u'gte',
                                u'lt',
                                u'lte'],
                u'maxLength': 10,
                u'required_on_activate': False,
                u'type': [u'string',
                          u'null']},
            u'system_attribute': {u'default': u'default',
                                  u'filter_ops': [u'eq',
                                                  u'neq',
                                                  u'in'],
                                  u'maxLength': 255,
                                  u'readOnly': True,
                                  u'sortable': True,
                                  u'type': [u'string',
                                            u'null']}
        }),
        u'required': [u'name'],
        u'title': u'Artifact type sample_artifact of version 1.0',
        u'type': u'object'},
    u'tosca_templates': {
        u'name': u'tosca_templates',
        u'properties': generate_type_props({
            u'template': {
                u'additionalProperties': False,
                u'description': u'TOSCA template body.',
                u'filter_ops': [],
                u'properties': {
                    u'md5': {u'type': [u'string', u'null']},
                    u'sha1': {u'type': [u'string', u'null']},
                    u'sha256': {u'type': [u'string', u'null']},
                    u'content_type': {
                        u'type': u'string'},
                    u'external': {u'type': u'boolean'},
                    u'size': {u'type': [u'number',
                                        u'null']},
                    u'status': {u'enum': [u'saving',
                                          u'active',
                                          u'pending_delete'],
                                u'type': u'string'}},
                u'required': [u'size',
                              u'md5', u'sha1', u'sha256',
                              u'external',
                              u'status',
                              u'content_type'],
                u'type': [u'object',
                          u'null']},
            u'template_format': {u'description': u'TOSCA template format.',
                                 u'filter_ops': [u'eq',
                                                 u'neq',
                                                 u'in'],
                                 u'maxLength': 255,
                                 u'type': [u'string',
                                           u'null']},
        }),
        u'required': [u'name'],
        u'title': u'Artifact type tosca_templates of version 1.0',
        u'type': u'object'},
    u'murano_packages': {
        u'name': u'murano_packages',
        u'properties': generate_type_props({
            u'categories': {
                u'default': [],
                u'description': u'List of categories specified for '
                                u'the package.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'items': {u'type': u'string'},
                u'maxItems': 255,
                u'mutable': True,
                u'type': [u'array',
                          u'null']},
            u'class_definitions': {
                u'default': [],
                u'description': u'List of class definitions '
                                u'in the package.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'items': {u'type': u'string'},
                u'maxItems': 255,
                u'type': [u'array',
                          u'null'],
                u'unique': True},
            u'dependencies': {
                u'default': [],
                u'description': u'List of package dependencies for '
                                u'this package.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'items': {u'type': u'string'},
                u'maxItems': 255,
                u'required_on_activate': False,
                u'type': [u'array',
                          u'null']},
            u'display_name': {
                u'description': u'Package name in human-readable format.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'mutable': True,
                u'type': [u'string',
                          u'null']},
            u'inherits': {
                u'additionalProperties': {u'type': u'string'},
                u'default': {},
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxProperties': 255,
                u'type': [u'object',
                          u'null']},
            u'keywords': {u'default': [],
                          u'filter_ops': [u'eq',
                                          u'neq',
                                          u'in'],
                          u'items': {u'type': u'string'},
                          u'maxItems': 255,
                          u'mutable': True,
                          u'type': [u'array',
                                    u'null']},
            u'package': {
                u'additionalProperties': False,
                u'description': u'Murano Package binary.',
                u'filter_ops': [],
                u'properties': {u'md5': {u'type': [u'string', u'null']},
                                u'sha1': {u'type': [u'string', u'null']},
                                u'sha256': {u'type': [u'string', u'null']},
                                u'content_type': {u'type': u'string'},
                                u'external': {u'type': u'boolean'},
                                u'size': {u'type': [u'number',
                                                    u'null']},
                                u'status': {u'enum': [u'saving',
                                                      u'active',
                                                      u'pending_delete'],
                                            u'type': u'string'}},
                u'required': [u'size',
                              u'md5', u'sha1', u'sha256',
                              u'external',
                              u'status',
                              u'content_type'],
                u'required_on_activate': False,
                u'type': [u'object',
                          u'null']},
            u'type': {
                u'default': u'Application',
                u'description': u'Package type.',
                u'enum': [u'Application',
                          u'Library',
                          None],
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'type': [u'string',
                          u'null']}
        }),
        u'required': [u'name'],
        u'title': u'Artifact type murano_packages of version 1.0',
        u'type': u'object'},
    u'images': {
        u'name': u'images',
        u'properties': generate_type_props({
            u'architecture': {
                u'description': u'Operating system architecture as specified '
                                u'in http://docs.openstack.org/trunk/'
                                u'openstack-compute/admin/content/adding-'
                                u'images.html',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'required_on_activate': False,
                u'type': [u'string',
                          u'null']},
            u'cloud_user': {u'description': u'Default cloud user.',
                            u'filter_ops': [u'eq',
                                            u'neq',
                                            u'in'],
                            u'maxLength': 255,
                            u'required_on_activate': False,
                            u'type': [u'string', u'null']},
            u'container_format': {u'description': u'Image container format.',
                                  u'enum': [u'ami',
                                            u'ari',
                                            u'aki',
                                            u'bare',
                                            u'ovf',
                                            u'ova',
                                            u'docker',
                                            None],
                                  u'filter_ops': [u'eq',
                                                  u'neq',
                                                  u'in'],
                                  u'maxLength': 255,
                                  u'type': [u'string',
                                            u'null']},

            u'disk_format': {u'description': u'Image disk format.',
                             u'enum': [u'ami',
                                       u'ari',
                                       u'aki',
                                       u'vhd',
                                       u'vhdx',
                                       u'vmdk',
                                       u'raw',
                                       u'qcow2',
                                       u'vdi',
                                       u'iso',
                                       None],
                             u'filter_ops': [u'eq',
                                             u'neq',
                                             u'in'],
                             u'maxLength': 255,
                             u'type': [u'string', u'null']},
            u'image': {u'additionalProperties': False,
                       u'description': u'Image binary.',
                       u'filter_ops': [],
                       u'properties': {
                           u'md5': {u'type': [u'string', u'null']},
                           u'sha1': {u'type': [u'string', u'null']},
                           u'sha256': {u'type': [u'string', u'null']},
                           u'content_type': {u'type': u'string'},
                           u'external': {u'type': u'boolean'},
                           u'size': {u'type': [u'number',
                                               u'null']},
                           u'status': {u'enum': [u'saving',
                                                 u'active',
                                                 u'pending_delete'],
                                       u'type': u'string'}},
                       u'required': [u'size',
                                     u'md5', u'sha1', u'sha256',
                                     u'external',
                                     u'status',
                                     u'content_type'],
                       u'required_on_activate': False,
                       u'type': [u'object', u'null']},
            u'image_indirect_url': {
                u'description': u'URL where image is available for users by '
                                u'accepting EULA or some other form. It is '
                                u'used when it is not possible to upload '
                                u'image directly to Glare. F.e. some Windows '
                                u'cloud images requires EULA acceptance '
                                u'before download.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'required_on_activate': False,
                u'type': [u'string', u'null']},
            u'instance_uuid': {
                u'description': u'Metadata which can be used to record which '
                                u'instance this image is associated with. '
                                u'(Informational only, does not create an '
                                u'instance snapshot.)',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'required_on_activate': False,
                u'type': [u'string',
                          u'null']},
            u'kernel_id': {
                u'description': u'ID of image stored in Glare that should be '
                                u'used as the kernel when booting an '
                                u'AMI-style image.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'pattern': u'^([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-'
                            u'([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-'
                            u'([0-9a-fA-F]){12}$',
                u'required_on_activate': False,
                u'type': [u'string', u'null']},
            u'min_disk': {
                u'description': u'Minimal disk space required to boot image.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'minumum': 0,
                u'required_on_activate': False,
                u'type': [u'integer', u'null']},
            u'min_ram': {
                u'description': u'Minimal RAM required to boot image.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'minumum': 0,
                u'required_on_activate': False,
                u'type': [u'integer', u'null']},
            u'os_distro': {
                u'description': u'Common name of operating system distribution'
                                u' as specified in http://docs.openstack.org/'
                                u'trunk/openstack-compute/admin/content/'
                                u'adding-images.html',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'required_on_activate': False,
                u'type': [u'string', u'null']},
            u'os_version': {
                u'description': u'Operating system version as specified by the'
                                u' distributor',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'required_on_activate': False,
                u'type': [u'string', u'null']},
            u'ramdisk_id': {
                u'description': u'ID of image stored in Glare that should be '
                                u'used as the ramdisk when booting an '
                                u'AMI-style image.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxLength': 255,
                u'pattern': u'^([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F])'
                            u'{4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}$',
                u'required_on_activate': False,
                u'type': [u'string', u'null']}}),
        u'required': [u'name'],
        u'title': u'Artifact type images of version 1.0',
        u'type': u'object'},
    u'heat_templates': {
        u'name': u'heat_templates',
        u'properties': generate_type_props({
            u'default_envs': {
                u'additionalProperties': {u'type': u'string'},
                u'default': {},
                u'description': u'Default environments that can '
                                u'be applied to the template if no '
                                u'environments specified by user.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxProperties': 255,
                u'mutable': True,
                u'type': [u'object',
                          u'null']},
            u'environments': {
                u'additionalProperties': {u'type': u'string'},
                u'default': {},
                u'description': u'References to Heat Environments '
                                u'that can be used with current '
                                u'template.',
                u'filter_ops': [u'eq',
                                u'neq',
                                u'in'],
                u'maxProperties': 255,
                u'mutable': True,
                u'type': [u'object',
                          u'null']},
            u'nested_templates': {
                u'additionalProperties':
                    {u'additionalProperties': False,
                     u'properties': {
                         u'md5': {u'type': [u'string', u'null']},
                         u'sha1': {u'type': [u'string', u'null']},
                         u'sha256': {u'type': [u'string', u'null']},
                         u'content_type': {
                             u'type': u'string'},
                         u'external': {u'type': u'boolean'},
                         u'size': {u'type': [u'number',
                                             u'null']},
                         u'status': {u'enum': [u'saving',
                                               u'active',
                                               u'pending_delete'],
                                     u'type': u'string'}},
                     u'required': [u'size',
                                   u'md5', u'sha1', u'sha256',
                                   u'external',
                                   u'status',
                                   u'content_type'],
                     u'type': [u'object',
                               u'null']},
                u'default': {},
                u'description': u'Dict of nested templates where key is the '
                                u'name  of template and value is nested '
                                u'template body.',
                u'filter_ops': [],
                u'maxProperties': 255,
                u'type': [u'object',
                          u'null']},
            u'template': {
                u'additionalProperties': False,
                u'description': u'Heat template body.',
                u'filter_ops': [],
                u'properties': {
                    u'md5': {u'type': [u'string', u'null']},
                    u'sha1': {u'type': [u'string', u'null']},
                    u'sha256': {u'type': [u'string', u'null']},
                    u'content_type': {
                        u'type': u'string'},
                    u'external': {u'type': u'boolean'},
                    u'size': {u'type': [u'number',
                                        u'null']},
                    u'status': {u'enum': [u'saving',
                                          u'active',
                                          u'pending_delete'],
                                u'type': u'string'}},
                u'required': [u'size',
                              u'md5', u'sha1', u'sha256',
                              u'external',
                              u'status',
                              u'content_type'],
                u'type': [u'object',
                          u'null']},

        }),
        u'required': [u'name'],
        u'title': u'Artifact type heat_templates of version 1.0',
        u'type': u'object'},
    u'heat_environments': {
        u'name': u'heat_environments',
        u'properties': generate_type_props({
            u'environment': {
                u'additionalProperties': False,
                u'description': u'Heat Environment text body.',
                u'filter_ops': [],
                u'properties': {u'md5': {u'type': [u'string', u'null']},
                                u'sha1': {u'type': [u'string', u'null']},
                                u'sha256': {u'type': [u'string', u'null']},
                                u'content_type': {u'type': u'string'},
                                u'external': {u'type': u'boolean'},
                                u'size': {u'type': [u'number',
                                                    u'null']},
                                u'status': {u'enum': [u'saving',
                                                      u'active',
                                                      u'pending_delete'],
                                            u'type': u'string'}},
                u'required': [u'size',
                              u'md5', u'sha1', u'sha256',
                              u'external',
                              u'status',
                              u'content_type'],
                u'type': [u'object',
                          u'null']},

        }),
        u'required': [u'name'],
        u'title': u'Artifact type heat_environments of version 1.0',
        u'type': u'object'}
}


class TestSchemas(functional.FunctionalTest):

    def setUp(self):
        super(TestSchemas, self).setUp()
        self.glare_server.deployment_flavor = 'noauth'

        self.glare_server.enabled_artifact_types = ','.join(
            enabled_artifact_types)
        self.glare_server.custom_artifact_types_modules = (
            'glare.tests.functional.sample_artifact')
        self.start_servers(**self.__dict__.copy())

    def tearDown(self):
        self.stop_servers()
        self._reset_database(self.glare_server.sql_connection)
        super(TestSchemas, self).tearDown()

    def _url(self, path):
        return 'http://127.0.0.1:%d%s' % (self.glare_port, path)

    def _check_artifact_method(self, url, status=200):
        headers = {
            'X-Identity-Status': 'Confirmed',
        }
        response = requests.get(self._url(url), headers=headers)
        self.assertEqual(status, response.status_code, response.text)
        if status >= 400:
            return response.text
        if ("application/json" in response.headers["content-type"] or
                "application/schema+json" in response.headers["content-type"]):
            return jsonutils.loads(response.text)
        return response.text

    def get(self, url, status=200, headers=None):
        return self._check_artifact_method(url, status=status)

    def test_schemas(self):

        # Get list schemas of artifacts
        result = self.get(url='/schemas')
        self.assertEqual(fixtures, result['schemas'], utils.DictDiffer(
            result['schemas'], fixtures))

        # Get schemas for specific artifact type
        for at in enabled_artifact_types:
            result = self.get(url='/schemas/%s' % at)
            self.assertEqual(fixtures[at], result['schemas'][at],
                             utils.DictDiffer(
                                 result['schemas'][at]['properties'],
                                 fixtures[at]['properties']))

        # Get schema of sample_artifact
        result = self.get(url='/schemas/sample_artifact')
        self.assertEqual(fixtures['sample_artifact'],
                         result['schemas']['sample_artifact'],
                         utils.DictDiffer(
                             result['schemas']['sample_artifact'][
                                 'properties'],
                             fixtures['sample_artifact']['properties']))

        # Validation of schemas
        result = self.get(url='/schemas')['schemas']
        for artifact_type, schema in result.items():
            jsonschema.Draft4Validator.check_schema(schema)
