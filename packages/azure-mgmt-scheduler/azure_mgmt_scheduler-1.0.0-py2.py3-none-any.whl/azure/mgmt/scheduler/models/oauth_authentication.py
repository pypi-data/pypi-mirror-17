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


class OAuthAuthentication(HttpAuthentication):
    """OAuthAuthentication.

    :param type: Gets or sets the http authentication type. Possible values
     include: 'NotSpecified', 'ClientCertificate', 'ActiveDirectoryOAuth',
     'Basic'
    :type type: str or :class:`HttpAuthenticationType
     <azure.mgmt.scheduler.models.HttpAuthenticationType>`
    :param secret: Gets or sets the secret.
    :type secret: str
    :param tenant: Gets or sets the tenant.
    :type tenant: str
    :param audience: Gets or sets the audience.
    :type audience: str
    :param client_id: Gets or sets the client identifier.
    :type client_id: str
    """ 

    _attribute_map = {
        'type': {'key': 'type', 'type': 'HttpAuthenticationType'},
        'secret': {'key': 'secret', 'type': 'str'},
        'tenant': {'key': 'tenant', 'type': 'str'},
        'audience': {'key': 'audience', 'type': 'str'},
        'client_id': {'key': 'clientId', 'type': 'str'},
    }

    def __init__(self, type=None, secret=None, tenant=None, audience=None, client_id=None):
        super(OAuthAuthentication, self).__init__(type=type)
        self.secret = secret
        self.tenant = tenant
        self.audience = audience
        self.client_id = client_id
