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

from msrest.serialization import Model


class HttpAuthentication(Model):
    """HttpAuthentication.

    :param type: Gets or sets the http authentication type. Possible values
     include: 'NotSpecified', 'ClientCertificate', 'ActiveDirectoryOAuth',
     'Basic'
    :type type: str or :class:`HttpAuthenticationType
     <azure.mgmt.scheduler.models.HttpAuthenticationType>`
    """ 

    _attribute_map = {
        'type': {'key': 'type', 'type': 'HttpAuthenticationType'},
    }

    def __init__(self, type=None):
        self.type = type
