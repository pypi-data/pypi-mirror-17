# Copyright (c) 2014 Rackspace, Inc.
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

import abc

import six

from poppy.manager.base import controller


@six.add_metaclass(abc.ABCMeta)
class SSLCertificateController(controller.ManagerControllerBase):
    """SSL certificate controller base class."""

    def __init__(self, manager):
        super(SSLCertificateController, self).__init__(manager)

    @abc.abstractmethod
    def create_ssl_certificate(self, project_id, cert_obj):
        """Create ssl certificate.

       :param project_id
       :param cert_obj
       :raises: NotImplementedError
       """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_ssl_certificate(self, project_id, domain_name, cert_type):
        """Delete ssl certificate.

        :param project_id
        :param domain_name
        :param cert_type
       :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_certs_info_by_domain(self, domain_name, project_id):
        """Get ssl certificate by domain.

        :param domain_name:
        :param project_id:
       :raises: NotImplementedError
        """
        raise NotImplementedError
