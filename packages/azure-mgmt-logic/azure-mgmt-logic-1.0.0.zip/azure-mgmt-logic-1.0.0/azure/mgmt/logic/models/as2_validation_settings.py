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


class AS2ValidationSettings(Model):
    """AS2ValidationSettings.

    :param override_message_properties: The value indicating whether to
     override incoming message properties with those in agreement.
    :type override_message_properties: bool
    :param encrypt_message: The value indicating whether the message has to
     be encrypted.
    :type encrypt_message: bool
    :param sign_message: The value indicating whether the message has to be
     signed.
    :type sign_message: bool
    :param compress_message: The value indicating whether the message has to
     be compressed.
    :type compress_message: bool
    :param check_duplicate_message: The value indicating whether to check for
     duplicate message.
    :type check_duplicate_message: bool
    :param interchange_duplicates_validity_days: The number of days to look
     back for duplicate interchange.
    :type interchange_duplicates_validity_days: int
    :param check_certificate_revocation_list_on_send: The value indicating
     whether to check for certificate revocation list on send.
    :type check_certificate_revocation_list_on_send: bool
    :param check_certificate_revocation_list_on_receive: The value indicating
     whether to check for certificate revocation list on receive.
    :type check_certificate_revocation_list_on_receive: bool
    :param encryption_algorithm: The encryption algorithm. Possible values
     include: 'NotSpecified', 'None', 'DES3', 'RC2', 'AES128', 'AES192',
     'AES256'
    :type encryption_algorithm: str or :class:`EncryptionAlgorithm
     <azure.mgmt.logic.models.EncryptionAlgorithm>`
    """ 

    _attribute_map = {
        'override_message_properties': {'key': 'overrideMessageProperties', 'type': 'bool'},
        'encrypt_message': {'key': 'encryptMessage', 'type': 'bool'},
        'sign_message': {'key': 'signMessage', 'type': 'bool'},
        'compress_message': {'key': 'compressMessage', 'type': 'bool'},
        'check_duplicate_message': {'key': 'checkDuplicateMessage', 'type': 'bool'},
        'interchange_duplicates_validity_days': {'key': 'interchangeDuplicatesValidityDays', 'type': 'int'},
        'check_certificate_revocation_list_on_send': {'key': 'checkCertificateRevocationListOnSend', 'type': 'bool'},
        'check_certificate_revocation_list_on_receive': {'key': 'checkCertificateRevocationListOnReceive', 'type': 'bool'},
        'encryption_algorithm': {'key': 'encryptionAlgorithm', 'type': 'EncryptionAlgorithm'},
    }

    def __init__(self, override_message_properties=None, encrypt_message=None, sign_message=None, compress_message=None, check_duplicate_message=None, interchange_duplicates_validity_days=None, check_certificate_revocation_list_on_send=None, check_certificate_revocation_list_on_receive=None, encryption_algorithm=None):
        self.override_message_properties = override_message_properties
        self.encrypt_message = encrypt_message
        self.sign_message = sign_message
        self.compress_message = compress_message
        self.check_duplicate_message = check_duplicate_message
        self.interchange_duplicates_validity_days = interchange_duplicates_validity_days
        self.check_certificate_revocation_list_on_send = check_certificate_revocation_list_on_send
        self.check_certificate_revocation_list_on_receive = check_certificate_revocation_list_on_receive
        self.encryption_algorithm = encryption_algorithm
