# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from .http_authentication import HttpAuthentication


class ClientCertAuthentication(HttpAuthentication):
    """ClientCertAuthentication.

    :param type: Gets or sets the http authentication type. Possible values
     include: 'NotSpecified', 'ClientCertificate', 'ActiveDirectoryOAuth',
     'Basic'
    :type type: str or :class:`HttpAuthenticationType
     <azure.mgmt.scheduler.models.HttpAuthenticationType>`
    :param password: Gets or sets the password.
    :type password: str
    :param pfx: Gets or sets the pfx.
    :type pfx: str
    :param certificate_thumbprint: Gets or sets the certificate thumbprint.
    :type certificate_thumbprint: str
    :param certificate_expiration_date: Gets or sets the certificate
     expiration date.
    :type certificate_expiration_date: datetime
    :param certificate_subject_name: Gets or sets the certificate subject
     name.
    :type certificate_subject_name: str
    """ 

    _attribute_map = {
        'type': {'key': 'type', 'type': 'HttpAuthenticationType'},
        'password': {'key': 'password', 'type': 'str'},
        'pfx': {'key': 'pfx', 'type': 'str'},
        'certificate_thumbprint': {'key': 'certificateThumbprint', 'type': 'str'},
        'certificate_expiration_date': {'key': 'certificateExpirationDate', 'type': 'iso-8601'},
        'certificate_subject_name': {'key': 'certificateSubjectName', 'type': 'str'},
    }

    def __init__(self, type=None, password=None, pfx=None, certificate_thumbprint=None, certificate_expiration_date=None, certificate_subject_name=None):
        super(ClientCertAuthentication, self).__init__(type=type)
        self.password = password
        self.pfx = pfx
        self.certificate_thumbprint = certificate_thumbprint
        self.certificate_expiration_date = certificate_expiration_date
        self.certificate_subject_name = certificate_subject_name
