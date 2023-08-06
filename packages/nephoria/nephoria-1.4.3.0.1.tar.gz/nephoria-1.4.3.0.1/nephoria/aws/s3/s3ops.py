# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2014, Eucalyptus Systems, Inc.
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
# Author: vic.iglesias@eucalyptus.com

from boto.s3.bucket import Bucket
from boto.s3.prefix import Prefix

import os
import hashlib
from boto.s3.connection import OrdinaryCallingFormat, S3Connection
from boto.s3.key import Key
from boto.s3.acl import ACL, Grant
from boto.exception import S3ResponseError
from boto.s3.deletemarker import DeleteMarker
import boto.s3
from nephoria.baseops.botobaseops import BotoBaseOps


class S3opsException(Exception):
    """Exception raised for errors that occur when running S3 operations.

    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        print self.msg


class S3ops(BotoBaseOps):
    s3_groups = {
             "all_users":"http://acs.amazonaws.com/groups/global/AllUsers",
             "authenticated_users":"http://acs.amazonaws.com/groups/global/AuthenticatedUsers",
             "log_delivery":"http://acs.amazonaws.com/groups/s3/LogDelivery"
             }
    EUCARC_URL_NAME = 's3_url'
    SERVICE_PREFIX = 's3'
    CONNECTION_CLASS = S3Connection

    def setup(self):
        self.connection.calling_format = OrdinaryCallingFormat()
        super(S3ops, self).setup()

    def setup_resource_trackers(self):
        """
        Setup keys in the test_resources hash in order to track artifacts created
        """
        #todo add/define clean methods here...
        self.test_resources_clean_methods["keys"] = None
        self.test_resources_clean_methods["buckets"] = None

        for resource_name in self.test_resources_clean_methods.iterkeys():
            self.test_resources[resource_name] = []

    def get_bucket(self, bucket_name):
        """
        Bring balance in the force.
        Basically this method just returns the output using boto connection,
        but may be in future it will do something meaningful.
        This wrapper ensures that tester can continue using nephoria APIs.
        :param bucket_name:
        :return:
        """
        return self.connection.get_bucket(bucket_name)

    def create_bucket(self, bucket_name, location=None):
        """
        Test Coverages:
            - Create a bucket.
            - Ensures bucket exists by calling boto s3.lookup

        bucket_name The name of the Bucket
        """

        # TODO create_bucket move to boto3

        bucket = self.get_bucket_by_name(bucket_name)
        if bucket:
            self.log.debug("Bucket '(%s)' already exists" % bucket_name)
        else:
            try:
                if location:
                    bucket = self.connection.create_bucket(bucket_name, location=location)
                else:
                    bucket = self.connection.create_bucket(bucket_name)
            except self.connection.provider.storage_create_error, e:
                raise S3opsException("Bucket '(%s)' is owned by another user" % bucket_name )

            if not self.get_bucket_by_name(bucket.name):
                raise S3opsException("Bucket could not be found after creation")

        self.test_resources["buckets"].append(bucket)
        self.log.debug("Created bucket: " + bucket_name)
        return bucket
    
    def delete_bucket(self, bucket):
        """
        Test Coverage:
            - Deletes a bucket.
            - Checks if bucket still exists.

        bucket_name The name of the Bucket
        """
        if not isinstance(bucket, Bucket):
            try:
                bucket = self.connection.get_bucket(bucket)
            except:
                raise S3opsException("Bucket '(%s)' not found." % bucket)

        bucket_name = bucket.name
        try:
            bucket.delete()
        except self.connection.provider.storage_create_error, e:
                raise S3opsException('Bucket (%s) is owned by another user' % bucket_name)

        # Check if the bucket still exists
        if self.get_bucket_by_name(bucket_name):
            raise S3opsException('Bucket (%s) still exists after delete operation' % bucket_name )
        self.log.debug("Bucket %s is deleted successfully." % bucket_name)

    def delete_all_buckets(self):
        '''
        Deletes all buckets.
        Returns: list of all buckets, which should be an empty list.
        '''
        buckets = self.get_all_bucket_names()
        l = len(buckets)
        if l > 1:
            for i in range(l):
                self.clear_bucket(buckets[i])
            for i in range(l):
                try:
                    self.delete_bucket(buckets[i])
                except S3opsException:
                    pass
        elif l == 1:
            self.clear_bucket(buckets[0])
            try:
                self.delete_bucket(buckets[0])
            except S3opsException:
                pass

        return self.connection.get_all_buckets()

    def get_all_bucket_names(self):
        """
        Returns: list of all bucket names
        """
        buckets = self.connection.get_all_buckets()
        l = len(buckets)
        if l > 0:
            for i in range(l):
                buckets[i] = str(buckets[i].name)
        return buckets


    def get_bucket_by_name(self, bucket_name):
        """
        Lookup a bucket by name, if it does not exist raise an exception
        """
        bucket = self.connection.lookup(bucket_name)
        if bucket:
            return bucket
        else:
            return None
    
    def upload_object(self, bucket_name, key_name, path_to_file=None, contents=None):
        """
        Write the contents of a local file to walrus
        bucket_name   The name of the walrus Bucket.
        key_name      The name of the object containing the data in walrus.
        path_to_file  Fully qualified path to local file.
        """
        bucket = self.get_bucket_by_name(bucket_name)
        if bucket == None:
            raise S3opsException("Could not find bucket " + bucket_name + " to upload file")
        # Get a new, blank Key object from the bucket.  This Key object only
        # exists locally until we actually store data in it.
        key = bucket.new_key(key_name)
        if key == None:
            raise RuntimeError( "Unable to create key " + key_name  )
        if path_to_file is None:
            if contents is None:
                contents = os.urandom(1024)
            key.set_contents_from_string(contents)
        else:
            key.set_contents_from_filename(path_to_file)
        self.log.debug("Uploaded key: " + str(key_name) + " to bucket:" + str(bucket_name))
        self.test_resources["keys"].append(key)
        return key
    
    def get_objects_by_prefix(self, bucket_name, prefix):
        """
        Get keys in the specified bucket that match the prefix if no prefix is passed all objects are returned
        as a result set.
        If only 1 key matches it will be returned as a Key object. 
        """
        bucket = self.get_bucket_by_name(bucket_name)
        keys = bucket.get_all_keys(prefix=prefix)
        if len(keys) < 1:
            self.log.warn("Unable to find any keys with prefix " + prefix + " in " + str(bucket) )
        if len(keys) == 2:
            return keys[0]
        return keys
        
    def delete_object(self, object):
        bucket = object.bucket
        name = object.name
        object.delete()
        try:
            self.connection.get_bucket(bucket).get_key(name)
            raise S3opsException("Walrus object " + name + " in bucket "  +  bucket.name  + " still exists after delete")
        except Exception, e:
            return
        
    def clear_bucket(self, bucket_name=None):
        """Deletes the contents of the bucket specified and the bucket itself
            THIS WILL DELETE EVERYTHING!
           bucket       bucket name to clear
        """
        try:
            bucket = self.connection.get_bucket(bucket_name=bucket_name)
        except S3ResponseError as e:
            self.log.debug('No bucket' + bucket_name + ' found: ' + e.message)
            raise Exception('Not found')
        
        try:
            self.log.debug( "Getting bucket listing for " + bucket.name )
            self.log.debug(  "Iterating throught the bucket" )
            key_list = bucket.list()        
            self.log.debug(  "Starting loop" )
            for k in key_list:
                if isinstance(k, Prefix):
                    self.log.debug(  "Skipping prefix" )
                    continue
                self.log.debug(  "Deleting key: " + k.name )
                bucket.delete_key(k)
            bucket.delete()
        except S3ResponseError as e:
            self.log.debug(  "Exception caught doing bucket cleanup." + e.message )
            #Todo: need to make this work with Walrus's non-S3-compliant error codes
            if e.status == 409:
                #Do version cleanup
                self.log.debug(  "Cleaning up versioning artifacts" )
                try:
                    keys = bucket.get_all_versions()
                    for k in keys:
                        if isinstance(k, Key):
                            self.log.debug(  "Got version: " + k.name + "--" + k.version_id + "-- Delete marker? " + str(k.delete_marker) )
                            self.log.debug(  "Deleting key: " + k.name )
                            bucket.delete_key(key_name=k.name,version_id=k.version_id)
                        elif isinstance(k, DeleteMarker):
                            self.log.debug(  "Got marker: " + k.name + "--" + k.version_id + "--" + str(k.is_latest) )
                            self.log.debug(  "Deleting delete marker" )
                            bucket.delete_key(key_name=k.name,version_id=k.version_id)
                    self.log.debug(  "Deleting bucket " + bucket.name )
                    bucket.delete()
                except Exception as e:
                    self.log.debug(  "Exception deleting versioning artifacts: " + e.message )
            else:
                self.log.debug('Got ' + e.message + ' and status ' + str(e.status))
                    
    def clear_keys_with_prefix(self, bucket, prefix):
        try :
            listing = self.connection.get_all_buckets()
            for bucket in listing:
                if bucket.name.startswith(prefix):
                    self.log.debug("Getting bucket listing for " + bucket.name)
                    key_list = bucket.list()
                    for k in key_list:
                        if isinstance(k, boto.s3.prefix.Prefix):
                            self.log.debug("Skipping prefix")
                            continue
                        self.log.debug("Deleting key: " + k.name)
                        bucket.delete_key(k)
                    bucket.delete()
                else:
                    self.log.debug("skipping bucket: " + bucket.name)
        except S3ResponseError as e:
            raise S3opsException("Exception caught doing bucket cleanup.")

    def get_canned_acl(self, canned_acl=None, bucket_owner_id=None, bucket_owner_display_name=None):
        """
        Returns an acl object that can be applied to a bucket or key. It is intended to be used to verify
        results that the service returns. To set a canned-acl you can simply set it on the bucket directly without
        this method.
        
        bucket_owner_id         Account id of the owner of the bucket. Required
        canned_acl       Canned acl to implement. Required. 
                         Options: ['private','public-read', 'public-read-write', 'authenticated-read',  'log-delivery-write', 'bucket-owner-full-control', 'bucket-owner-full-control']
        bucket_owner_display_name  Required. The account display name for the bucket owner, so that the correct permission can be generated fully
        """
        if bucket_owner_id == None or canned_acl == None or bucket_owner_display_name == None :
            raise S3opsException( "No user_id or canned_acl passed to get_canned_acl()" )
        
        built_acl = ACL()
        built_acl.add_user_grant(permission='FULL_CONTROL',user_id=bucket_owner_id, display_name=bucket_owner_display_name)
        
        if canned_acl == "public-read":
            built_acl.add_grant(Grant(permission="READ",type='Group',uri=self.s3_groups["all_users"]))        
        elif canned_acl == "public-read-write":
            built_acl.add_grant(Grant(permission="READ",type='Group',uri=self.s3_groups["all_users"]))
            built_acl.add_grant(Grant(permission="WRITE",type='Group',uri=self.s3_groups["all_users"]))                
        elif canned_acl == "authenticated-read":
            built_acl.add_grant(Grant(permission="READ",type='Group',uri=self.s3_groups["authenticated_users"]))        
        elif canned_acl == "log-delivery-write":
            built_acl.add_grant(Grant(permission="WRITE",type='Group',uri=self.s3_groups["log_delivery"]))        
        elif canned_acl == "bucket-owner-read":
            if bucket_owner_id is None:
                raise Exception("No bucket_owner_id passed when trying to create bucket-owner-read canned acl ")
            built_acl.add_grant(Grant(permission="READ",id=bucket_owner_id))
        elif canned_acl == "bucket-owner-full-control":
            if bucket_owner_id is None:
                raise Exception("No bucket_owner_id passed when trying to create bucket-owner-full-control canned acl ")
            built_acl.add_grant(Grant(permission="FULL_CONTROL",id=bucket_owner_id))
        return built_acl
    
    def check_acl_equivalence(self, acl1=None, acl2=None):
        '''
        Checks if acl1 = acl2 based on comparison of the set of grants irrespective of order.
        One limitation is that each grant's xml string deserialization must be the same to be
        considered equivalent. This has implications for the grant displayname in particular.
        For example, an ACL with an unknown account specified will not generally have a
        display-name associated with the account id, so the comparison may fail in that case even
        though the ids and permissions are identical.
        
        Returns None if there is an input problem such as one or more inputs are None
        
        acl1    An ACL object from boto.s3.acl
        acl2    An ACL object from boto.s3.acl
        '''
        if acl1 == None or acl2 == None:
            return None
        
        acl1grants = set()
        acl2grants = set()
        
        #calculate the symmetric-difference of the two sets of grants
        for val in acl1.grants:
            acl1grants.add(val.to_xml())
        
        for val in acl2.grants:
            acl2grants.add(val.to_xml())        
            
        return not len(acl1grants.symmetric_difference(acl2grants)) > 0

    def check_md5(self, eTag=None, data=None):
        hasher = hashlib.md5()
        hasher.update(data)
        data_hash = "\"" + hasher.hexdigest() + "\""
        if data_hash != eTag:
            raise Exception( "Hash/eTag mismatch: \nhash = " + data_hash + "\neTag= " + eTag)
