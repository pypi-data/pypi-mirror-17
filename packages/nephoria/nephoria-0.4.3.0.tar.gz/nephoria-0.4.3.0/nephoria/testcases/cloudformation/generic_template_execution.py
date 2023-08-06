#!/usr/bin/env python
import re
from boto.exception import BotoServerError

from nephoria.testcase_utils.cli_test_runner import CliTestRunner
from nephoria.testcase_utils.cli_test_runner import SkipTestException
from nephoria.testcontroller import TestController
import copy
import time
import random
import os.path


class GenericTemplateRun(CliTestRunner):

    _CLI_DESCRIPTION = ("Test given Cloudformation template"
                        " against Eucalyptus Cloudformation. "
                        "This script utilizes the following "
                        "Cloudformation API calls: "
                        "CreateStack, DeleteStack, DescribeStacks, "
                        "and ValidateTemplate."
                        )
    _DEFAULT_CLI_ARGS = copy.copy(CliTestRunner._DEFAULT_CLI_ARGS)

    _DEFAULT_CLI_ARGS['template_file'] = {
        'args': ['--template-file'],
        'kwargs': {'dest': 'template_file',
                   'help': 'file location containing JSON template',
                   'default': None}}

    _DEFAULT_CLI_ARGS['template_params'] = {
        'args': ['--template-parameters'],
        'kwargs': {
                   'dest': 'template_params',
                   'help': ("key=value parameters to use with "
                            "stack's template. Multiple parameters "
                            "should be space-delimited."),
                   'nargs': '?',
                   'default': None}}

    _DEFAULT_CLI_ARGS['stack_name'] = {
        'args': ['--stack-name'],
        'kwargs': {'dest': 'stack_name',
                   'help': 'Name of Cloudformation Stack Deployment',
                   'default': None}}

    _DEFAULT_CLI_ARGS['disable_rollback'] = {
        'args': ['--disable-rollback'],
        'kwargs': {'dest': 'disable_rollback',
                   'help': ("Set to True to disable rollback of "
                            "the stack if stack creation failed. "
                            "Default is False."),
                   'action': 'store_true'}}

    _DEFAULT_CLI_ARGS['timeout_min'] = {
        'args': ['--timeout-in-min'],
        'kwargs': {'dest': 'timeout',
                   'help': ("The amount of time that can pass before the "
                            "stack status becomes CREATE_FAILED; if "
                            "DisableRollback is not set or is set to "
                            "False, the stack will be rolled back."),
                   'type': int,
                   'default': '1'}}

    _DEFAULT_CLI_ARGS['capabilities'] = {
        'args': ['--capabilities'],
        'kwargs': {'dest': 'capabilities',
                   'help': ("The list of capabilities that you want to allow "
                            "in the stack. If your template contains certain "
                            "resources, you must specify the CAPABILITY_IAM "
                            "value for this parameter; otherwise, this action "
                            "returns an InsufficientCapabilities error. The "
                            "following resources require you to specify the "
                            "capabilities parameter: "
                            "`AWS::CloudFormation::Stack`_,"
                            " `AWS::IAM::AccessKey`_, "
                            "`AWS::IAM::Group`_, "
                            "`AWS::IAM::InstanceProfile`_, "
                            "`AWS::IAM::Policy`_, "
                            "`AWS::IAM::Role`_, "
                            "`AWS::IAM::User`_, and "
                            "`AWS::IAM::UserToGroupAddition`_."),
                   'choices': ['CAPABILITY_IAM'],
                   'default': None}}

    _DEFAULT_CLI_ARGS['on_failure'] = {
        'args': ['--on-failure'],
        'kwargs': {'dest': 'on_failure',
                   'help': ("Determines what action will be taken if stack "
                            "creation fails. This must be one of: "
                            "DO_NOTHING, ROLLBACK, or DELETE."),
                   'choices': ['DO_NOTHING', 'ROLLBACK', 'DELETE'],
                   'default': 'ROLLBACK'}}

    @property
    def tc(self):
        tc = getattr(self, '__tc', None)
        if not tc:
            tc = TestController(self.args.clc,
                                password=self.args.password,
                                clouduser_name=self.args.test_user,
                                clouduser_account=self.args.test_account,
                                log_level=self.args.log_level)
            setattr(self, '__tc', tc)
        return tc

    @property
    def user(self):
        user = getattr(self, '__user', None)
        if not user:
            try:
                user = self.tc.get_user_by_name(
                                    aws_account_name=self.args.test_account,
                                    aws_user_name=self.args.test_user)
            except:
                user = self.tc.create_user_using_cloudadmin(
                                    aws_account_name=self.args.test_account,
                                    aws_user_name=self.args.test_user)
            setattr(self, '__user', user)
        return user

    @property
    def stack_name(self):
        """
        Make sure stack name is set.  If stack name not passed,
        generate stack name.
        """
        stack_name = getattr(self, '__stack_name', None)
        if (
               self.args.stack_name and
               not stack_name
           ):
            stack_name = self.args.stack_name
        elif not stack_name:
            stack_name = "nephoria-stack-" + str(int(time.time()))

        setattr(self, '__stack_name', stack_name)
        return stack_name

    @property
    def on_failure(self):
        """
        Check to see if --disable-rollback is set to true.
        If so, set --on-failure to None.
        """
        if self.args.disable_rollback is True:
            on_failure = None
        else:
            on_failure = self.args.on_failure
        return on_failure

    @property
    def disable_rollback(self):
        """
        Check to see if --disable-rollback is set to true.
        If so, set to value appropriately
        """
        if self.args.disable_rollback is True:
            disable_rollback = self.args.disable_rollback
        else:
            disable_rollback = None
        return disable_rollback

    def test_validate_template(self):
        """
        Test Coverage:
            - validate provided template
        """
        self.log.debug("Validating Cloudformation Template.")
        """
        Confirm the following:
            - if --template-file is used.
            - if --template-file is used, confirm file exists.
        """
        if self.args.template_file is None:
            raise ValueError("Please pass template-file.")
        elif (
               self.args.template_file and
               os.path.exists(self.args.template_file) is False
           ):
            raise ValueError("File passed for template-file does not exist.")
        else:
            temp = open(self.args.template_file)
            temp_body = temp.read()
            temp.close()
            try:
                self.tc.user.cloudformation.validate_template(
                                                   template_body=temp_body)
                self.log.debug("Template is valid.")
            except BotoServerError as e:
                self.log.error("Error validating template: " + e.error_message)
                raise e

    def test_stack_deployment(self):
        self.log.debug("Deploy Cloudformation Stack")
        """
        If template parameter(s), store them in a list
        """
        parameters = []
        if self.args.template_params:
            for param in self.args.template_params.split():
                try:
                    k, v = param.split("=")
                    parameters.append((k, v))
                except ValueError as e:
                    self.log.error("Parameter not in key=value format")
                    raise e
        else:
            self.log.debug("No parameters passed.")
        """
        If capabilities, store in a list
        Currently, only CAPABILITY_IAM should be in the list
        """
        if self.args.capabilities:
            capabilities = self.args.capabilities.split()
        else:
            capabilities = None

        """
        Make sure timeout is set to minutes.
        Timeout will be used for stack creation.
        """
        timeout = int(time.time()) + 60*int(self.args.timeout)
        """
        Create custom tags to associate test
        with resource(s)
        """
        nephoria_job_id = self.stack_name + str(time.time())
        tags = {
                "Purpose": "nephoria test resource",
                "Test Script": "generic_template_execution.py",
                "Nephoria Job ID": nephoria_job_id
               }
        """
        Create stack passing supported arguments.
        Stack information should be returned from create_stack
        """
        temp = open(self.args.template_file)
        temp_body = temp.read()
        temp.close()
        try:
            resp = self.tc.user.cloudformation.create_stack(
                               self.stack_name,
                               template_body=temp_body,
                               parameters=parameters,
                               disable_rollback=self.disable_rollback,
                               capabilities=capabilities,
                               tags=tags,
                               on_failure=self.on_failure)
        except BotoServerError as e:
            self.log.error("Failed to create stack")
            raise e

        while True:
            """
            Confirm stack completed within timeout period
            by using describe_stack leverging
            decorrelated jitter exponential backoff for each
            request. If stack failed to create, raise error
            """
            stacks = self.tc.user.cloudformation.describe_stacks(
                                   resp.stack_name)
            events_list = stacks[0].describe_events()
            events = '\n'.join(map(str, events_list[len(events_list)::-1]))
            if stacks[0].stack_status == 'CREATE_COMPLETE':
                outputs_list = stacks[0].outputs
                outputs = '\n'.join(map(str,
                                        outputs_list[len(outputs_list)::-1]))
                self.log.debug("Stack deployment complete.")
                self.log.debug("\nStack events:\n" + events)
                self.log.debug("\nStack outputs:\n" + outputs)
                break
            elif stacks[0].stack_status == 'CREATE_FAILED':
                self.log.error("Stack deployment failed: " +
                               str(stacks[0].stack_status_reason))
                self.log.error("Stack events:\n" + events)
                raise RuntimeError("Stack deployment failed: " +
                                   str(stacks[0].stack_status_reason))
            elif int(time.time()) > timeout:
                self.log.error("Stack deployment failed "
                               "to complete in provided stack "
                               "timeout: " + str(self.args.timeout) +
                               " min.")
                self.log.error("Stack events:\n" + events)
                raise RuntimeError("Stack failed to deploy "
                                   "within timeout: " +
                                   str(self.args.timeout) +
                                   " min.")
            sleep_time = min(int(timeout),
                             random.uniform(2, 2*3))
            self.log.debug("Sleep " + str(sleep_time) +
                           " seconds before next request..")
            time.sleep(sleep_time)

    def clean_method(self):
        """
        Check to see if there are any stacks.
        If so, delete the stacks
        """
        stack_id = self.stack_name
        stacks = self.tc.user.cloudformation.describe_stacks(stack_id)
        if stacks:
            for stack in stacks:
                if (
                       self.on_failure == 'DELETE' or
                       self.on_failure == 'ROLLBACK'
                   ):
                        self.log.debug("Deleting the following stack: " +
                                       str(stack.stack_name))
                        try:
                            self.tc.user.cloudformation.delete_stack(
                                                        stack.stack_name)
                        except BotoServerError as e:
                            self.log.error("Failed to delete stack")
                            raise e
                else:
                    self.log.debug("Stack and resources not deleted.")
                    pass

if __name__ == "__main__":
    test = GenericTemplateRun()
    result = test.run()
    exit(result)
