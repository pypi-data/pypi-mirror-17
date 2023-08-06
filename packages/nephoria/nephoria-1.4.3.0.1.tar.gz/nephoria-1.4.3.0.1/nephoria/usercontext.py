#!/usr/bin/python
# -*- coding: utf-8 -*-
# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2011, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from logging import INFO, DEBUG
from boto3.session import Session
from cloud_utils.log_utils.eulogger import Eulogger
from cloud_utils.log_utils import get_traceback, red
from cloud_admin.access.autocreds import AutoCreds
from nephoria.aws.iam.iamops import IAMops
from nephoria.aws.s3.s3ops import S3ops
from nephoria.aws.ec2.ec2ops import EC2ops
from nephoria.aws.ec2.b3_ec2ops import B3_EC2ops
from nephoria.aws.elb.elbops import ELBops
from nephoria.aws.sts.stsops import STSops
from nephoria.aws.sqs.sqsops import SQSops
from nephoria.aws.cloudformation.cfnops import CFNops
from nephoria.aws.cloudwatch.cwops import CWops
from nephoria.aws.autoscaling.asops import ASops
from nephoria import __DEFAULT_API_VERSION__

class UserContext(AutoCreds):

    # This map is used for ops connection class lookups...
    CLASS_MAP = {IAMops.__name__: 'iam',
                 S3ops.__name__: 's3',
                 EC2ops.__name__: 'ec2',
                 ELBops.__name__: 'elb',
                 STSops.__name__: 'sts',
                 SQSops.__name__: 'sqs',
                 CWops.__name__: 'cloudwatch',
                 CFNops.__name__: 'cloudformation',
                 ASops.__name__: 'autoscaling',
                 B3_EC2ops.__name__: 'b3_ec2ops'}

    def __init__(self,  aws_access_key=None, aws_secret_key=None, aws_account_name=None,
                 aws_user_name=None, port=8773, credpath=None, string=None, region=None,
                 machine=None, keysdir=None, logger=None, service_connection=None,
                 eucarc=None, existing_certs=False, boto_debug=0, https=True, api_version=None,
                 log_level=None):
        if log_level is None:
            if service_connection:
                log_level = service_connection.log.stdout_level
            else:
                log_level = DEBUG
        super(UserContext, self).__init__(aws_access_key=aws_access_key,
                                          aws_secret_key=aws_secret_key,
                                          aws_account_name=aws_account_name,
                                          aws_user_name=aws_user_name,
                                          service_port=port, region_domain=region,
                                          credpath=credpath, string=string,
                                          machine=machine, keysdir=keysdir,
                                          logger=logger, log_level=log_level,
                                          existing_certs=existing_certs,
                                          service_connection=service_connection,
                                          https=https, auto_create=False)
        self._user_info = {}
        self._session = None
        self._connections = {}
        self.region = region
        self.api_version = api_version or __DEFAULT_API_VERSION__

        # Logging setup
        if not logger:
            logger = Eulogger(str(self), stdout_level=log_level)
        self.log = logger
        self.log.debug = self.log.debug
        self.critical = self.log.critical
        self.info = self.log.info
        if eucarc:
            for key, value in eucarc.__dict__.iteritems():
                setattr(self, key, value)
        elif not (aws_access_key and aws_secret_key and self.serviceconnection):
            try:
                self.auto_find_credentials(assume_admin=False)
            except ValueError as VE:
                self.log.error('Failed to auto create user credentials and service paths:"{0}"'
                               .format(VE))
        if service_connection:
            self.update_attrs_from_cloud_services()
        self._test_resources = {}
        self._connection_kwargs = {'eucarc': self, 
                                   'connection_debug': boto_debug,
                                   'user_context': self,
                                   'region': region,
                                   'api_version': self.api_version,
                                   'log_level': log_level}
        self.log.identifier = str(self)
        self.log.debug('Successfully created User Context')

    ##########################################################################################
    #   User/Account Properties, Attributes, Methods, etc..
    ##########################################################################################

    def __repr__(self):
        account_name = ""
        user_name = ""
        account_id = ""
        try:
            account_name = self.account_name or ""
            user_name = self.user_name or ""
            account_id = self.account_id or ""
            if not (account_name or user_name or account_id) and self.access_key:
                account_id = "KEYID:{0}".format(self.access_key)
            if account_name:
                account_name = ":{0}".format(account_name)
            if user_name:
                user_name = ":{0}".format(user_name)

        except:
            pass
        return "{0}:{1}:{2}:{3}".format(self.__class__.__name__, account_id,
                                      account_name, user_name)

    @property
    def test_resources(self):
        resource_dict = {}
        for key, value in self._connections.iteritems():
            resource_dict[key] = getattr(value, 'test_resources', {})
        return resource_dict

    @property
    def user_info(self):
        if not self._user_info:
            if self.iam:
                if self.account_name == 'eucalyptus' and self.user_name == 'admin':
                    delegate_account = self.account_id
                else:
                    delegate_account = None
                self._user_info = self.iam.get_user_info(delegate_account=delegate_account)
        return self._user_info

    @property
    def user_name(self):
        if not self._user_name:
            self._user_name = self.user_info.get('user_name', None)
        return self._user_name

    @property
    def user_id(self):
        return self.user_info.get('user_id', None)

    @property
    def account_name(self):
        if not self._account_name:
            if self.iam:
                account = self.iam.get_account(account_name=self._account_name)
                self._account_name = account.get('account_name', None)
        return self._account_name

    @property
    def account_id(self):
        if not self._account_id:
            if self.iam:
                account = self.iam.get_account(account_name=self._account_name)
                self._account_id = account.get('account_id', None)
        return self._account_id

    ##########################################################################################
    #   BASE CONNECTION INFO
    ##########################################################################################

    @property
    def session(self):
        if not self._session:
            self._session = Session(aws_access_key_id=self.aws_access_key,
                                    aws_secret_access_key=self.aws_secret_key,
                                    region_name=self.region)
        return self._session

    @session.setter
    def session(self, newsession):
        if newsession is None:
            self._session = newsession
            return
        if isinstance(newsession, Session):
            self._session = newsession
            return
        raise TypeError('Unsupported type for Session, got: "{0}/{1}"'
                        .format(newsession, type(newsession)))




    ##########################################################################################
    #   CLOUD SERVICE CONNECTIONS
    ##########################################################################################

    @property
    def b3_ec2(self):
        ops_class = B3_EC2ops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            self._connections[name] = ops_class(**self._connection_kwargs)
        return self._connections.get(name, None)

    @property
    def iam(self):
        ops_class = IAMops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                   'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)

    @property
    def s3(self):
        ops_class = S3ops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                   'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)

    @property
    def ec2(self):
        ops_class = EC2ops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                   'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)

    @property
    def elb(self):
        ops_class = ELBops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                   'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)

    @property
    def sts(self):
        ops_class = STSops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                   'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)

    @property
    def sqs(self):
        ops_class = SQSops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                       'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)

    @property
    def autoscaling(self):
        ops_class = ASops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                   'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)

    @property
    def cloudwatch(self):
        ops_class = CWops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                   'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)

    @property
    def cloudformation(self):
        ops_class = CFNops
        name = self.CLASS_MAP[ops_class.__name__]
        if not self._connections.get(name, None):
            if getattr(self, ops_class.EUCARC_URL_NAME, None):
                try:
                    self._connections[name] = ops_class(**self._connection_kwargs)
                except Exception as CE:
                    self.log.error(red('{0}\nFailed to created "{1}" interface.\n'
                                   'Connection kwargs:\n{2}\nError:{3}'
                                       .format(get_traceback(),
                                               ops_class.__name__,
                                               self._connection_kwargs,
                                               CE)))
        return self._connections.get(name, None)
