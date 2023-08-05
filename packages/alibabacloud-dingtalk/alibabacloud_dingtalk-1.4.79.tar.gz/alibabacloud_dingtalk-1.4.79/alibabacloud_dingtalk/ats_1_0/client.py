# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_dingtalk.ats_1_0 import models as dingtalkats__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        if UtilClient.empty(self._endpoint):
            self._endpoint = 'api.dingtalk.com'

    def add_application_reg_form_template(
        self,
        request: dingtalkats__1__0_models.AddApplicationRegFormTemplateRequest,
    ) -> dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddApplicationRegFormTemplateHeaders()
        return self.add_application_reg_form_template_with_options(request, headers, runtime)

    async def add_application_reg_form_template_async(
        self,
        request: dingtalkats__1__0_models.AddApplicationRegFormTemplateRequest,
    ) -> dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddApplicationRegFormTemplateHeaders()
        return await self.add_application_reg_form_template_with_options_async(request, headers, runtime)

    def add_application_reg_form_template_with_options(
        self,
        request: dingtalkats__1__0_models.AddApplicationRegFormTemplateRequest,
        headers: dingtalkats__1__0_models.AddApplicationRegFormTemplateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.name):
            body['name'] = request.name
        if not UtilClient.is_unset(request.outer_id):
            body['outerId'] = request.outer_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse(),
            self.do_roarequest('AddApplicationRegFormTemplate', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/flows/applicationRegForms/templates', 'json', req, runtime)
        )

    async def add_application_reg_form_template_with_options_async(
        self,
        request: dingtalkats__1__0_models.AddApplicationRegFormTemplateRequest,
        headers: dingtalkats__1__0_models.AddApplicationRegFormTemplateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.name):
            body['name'] = request.name
        if not UtilClient.is_unset(request.outer_id):
            body['outerId'] = request.outer_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse(),
            await self.do_roarequest_async('AddApplicationRegFormTemplate', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/flows/applicationRegForms/templates', 'json', req, runtime)
        )

    def add_file(
        self,
        request: dingtalkats__1__0_models.AddFileRequest,
    ) -> dingtalkats__1__0_models.AddFileResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddFileHeaders()
        return self.add_file_with_options(request, headers, runtime)

    async def add_file_async(
        self,
        request: dingtalkats__1__0_models.AddFileRequest,
    ) -> dingtalkats__1__0_models.AddFileResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddFileHeaders()
        return await self.add_file_with_options_async(request, headers, runtime)

    def add_file_with_options(
        self,
        request: dingtalkats__1__0_models.AddFileRequest,
        headers: dingtalkats__1__0_models.AddFileHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddFileResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.file_name):
            body['fileName'] = request.file_name
        if not UtilClient.is_unset(request.media_id):
            body['mediaId'] = request.media_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddFileResponse(),
            self.do_roarequest('AddFile', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/files', 'json', req, runtime)
        )

    async def add_file_with_options_async(
        self,
        request: dingtalkats__1__0_models.AddFileRequest,
        headers: dingtalkats__1__0_models.AddFileHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddFileResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.file_name):
            body['fileName'] = request.file_name
        if not UtilClient.is_unset(request.media_id):
            body['mediaId'] = request.media_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddFileResponse(),
            await self.do_roarequest_async('AddFile', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/files', 'json', req, runtime)
        )

    def add_user_account(
        self,
        request: dingtalkats__1__0_models.AddUserAccountRequest,
    ) -> dingtalkats__1__0_models.AddUserAccountResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddUserAccountHeaders()
        return self.add_user_account_with_options(request, headers, runtime)

    async def add_user_account_async(
        self,
        request: dingtalkats__1__0_models.AddUserAccountRequest,
    ) -> dingtalkats__1__0_models.AddUserAccountResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddUserAccountHeaders()
        return await self.add_user_account_with_options_async(request, headers, runtime)

    def add_user_account_with_options(
        self,
        request: dingtalkats__1__0_models.AddUserAccountRequest,
        headers: dingtalkats__1__0_models.AddUserAccountHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddUserAccountResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        body = {}
        if not UtilClient.is_unset(request.channel_account_name):
            body['channelAccountName'] = request.channel_account_name
        if not UtilClient.is_unset(request.channel_user_identify):
            body['channelUserIdentify'] = request.channel_user_identify
        if not UtilClient.is_unset(request.phone_number):
            body['phoneNumber'] = request.phone_number
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddUserAccountResponse(),
            self.do_roarequest('AddUserAccount', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/channels/users/accounts', 'json', req, runtime)
        )

    async def add_user_account_with_options_async(
        self,
        request: dingtalkats__1__0_models.AddUserAccountRequest,
        headers: dingtalkats__1__0_models.AddUserAccountHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddUserAccountResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        body = {}
        if not UtilClient.is_unset(request.channel_account_name):
            body['channelAccountName'] = request.channel_account_name
        if not UtilClient.is_unset(request.channel_user_identify):
            body['channelUserIdentify'] = request.channel_user_identify
        if not UtilClient.is_unset(request.phone_number):
            body['phoneNumber'] = request.phone_number
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddUserAccountResponse(),
            await self.do_roarequest_async('AddUserAccount', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/channels/users/accounts', 'json', req, runtime)
        )

    def collect_resume_detail(
        self,
        request: dingtalkats__1__0_models.CollectResumeDetailRequest,
    ) -> dingtalkats__1__0_models.CollectResumeDetailResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.CollectResumeDetailHeaders()
        return self.collect_resume_detail_with_options(request, headers, runtime)

    async def collect_resume_detail_async(
        self,
        request: dingtalkats__1__0_models.CollectResumeDetailRequest,
    ) -> dingtalkats__1__0_models.CollectResumeDetailResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.CollectResumeDetailHeaders()
        return await self.collect_resume_detail_with_options_async(request, headers, runtime)

    def collect_resume_detail_with_options(
        self,
        request: dingtalkats__1__0_models.CollectResumeDetailRequest,
        headers: dingtalkats__1__0_models.CollectResumeDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.CollectResumeDetailResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel_outer_id):
            body['channelOuterId'] = request.channel_outer_id
        if not UtilClient.is_unset(request.channel_talent_id):
            body['channelTalentId'] = request.channel_talent_id
        if not UtilClient.is_unset(request.deliver_job_id):
            body['deliverJobId'] = request.deliver_job_id
        if not UtilClient.is_unset(request.opt_user_id):
            body['optUserId'] = request.opt_user_id
        if not UtilClient.is_unset(request.resume_data):
            body['resumeData'] = request.resume_data
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.CollectResumeDetailResponse(),
            self.do_roarequest('CollectResumeDetail', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/resumes/details', 'json', req, runtime)
        )

    async def collect_resume_detail_with_options_async(
        self,
        request: dingtalkats__1__0_models.CollectResumeDetailRequest,
        headers: dingtalkats__1__0_models.CollectResumeDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.CollectResumeDetailResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel_outer_id):
            body['channelOuterId'] = request.channel_outer_id
        if not UtilClient.is_unset(request.channel_talent_id):
            body['channelTalentId'] = request.channel_talent_id
        if not UtilClient.is_unset(request.deliver_job_id):
            body['deliverJobId'] = request.deliver_job_id
        if not UtilClient.is_unset(request.opt_user_id):
            body['optUserId'] = request.opt_user_id
        if not UtilClient.is_unset(request.resume_data):
            body['resumeData'] = request.resume_data
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.CollectResumeDetailResponse(),
            await self.do_roarequest_async('CollectResumeDetail', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/resumes/details', 'json', req, runtime)
        )

    def confirm_rights(
        self,
        rights_code: str,
        request: dingtalkats__1__0_models.ConfirmRightsRequest,
    ) -> dingtalkats__1__0_models.ConfirmRightsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.ConfirmRightsHeaders()
        return self.confirm_rights_with_options(rights_code, request, headers, runtime)

    async def confirm_rights_async(
        self,
        rights_code: str,
        request: dingtalkats__1__0_models.ConfirmRightsRequest,
    ) -> dingtalkats__1__0_models.ConfirmRightsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.ConfirmRightsHeaders()
        return await self.confirm_rights_with_options_async(rights_code, request, headers, runtime)

    def confirm_rights_with_options(
        self,
        rights_code: str,
        request: dingtalkats__1__0_models.ConfirmRightsRequest,
        headers: dingtalkats__1__0_models.ConfirmRightsHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.ConfirmRightsResponse:
        UtilClient.validate_model(request)
        rights_code = OpenApiUtilClient.get_encode_param(rights_code)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.ConfirmRightsResponse(),
            self.do_roarequest('ConfirmRights', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/rights/{rights_code}/confirm', 'json', req, runtime)
        )

    async def confirm_rights_with_options_async(
        self,
        rights_code: str,
        request: dingtalkats__1__0_models.ConfirmRightsRequest,
        headers: dingtalkats__1__0_models.ConfirmRightsHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.ConfirmRightsResponse:
        UtilClient.validate_model(request)
        rights_code = OpenApiUtilClient.get_encode_param(rights_code)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.ConfirmRightsResponse(),
            await self.do_roarequest_async('ConfirmRights', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/rights/{rights_code}/confirm', 'json', req, runtime)
        )

    def finish_beginner_task(
        self,
        task_code: str,
        request: dingtalkats__1__0_models.FinishBeginnerTaskRequest,
    ) -> dingtalkats__1__0_models.FinishBeginnerTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.FinishBeginnerTaskHeaders()
        return self.finish_beginner_task_with_options(task_code, request, headers, runtime)

    async def finish_beginner_task_async(
        self,
        task_code: str,
        request: dingtalkats__1__0_models.FinishBeginnerTaskRequest,
    ) -> dingtalkats__1__0_models.FinishBeginnerTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.FinishBeginnerTaskHeaders()
        return await self.finish_beginner_task_with_options_async(task_code, request, headers, runtime)

    def finish_beginner_task_with_options(
        self,
        task_code: str,
        request: dingtalkats__1__0_models.FinishBeginnerTaskRequest,
        headers: dingtalkats__1__0_models.FinishBeginnerTaskHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.FinishBeginnerTaskResponse:
        UtilClient.validate_model(request)
        task_code = OpenApiUtilClient.get_encode_param(task_code)
        query = {}
        if not UtilClient.is_unset(request.scope):
            query['scope'] = request.scope
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.FinishBeginnerTaskResponse(),
            self.do_roarequest('FinishBeginnerTask', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/beginnerTasks/{task_code}/finish', 'json', req, runtime)
        )

    async def finish_beginner_task_with_options_async(
        self,
        task_code: str,
        request: dingtalkats__1__0_models.FinishBeginnerTaskRequest,
        headers: dingtalkats__1__0_models.FinishBeginnerTaskHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.FinishBeginnerTaskResponse:
        UtilClient.validate_model(request)
        task_code = OpenApiUtilClient.get_encode_param(task_code)
        query = {}
        if not UtilClient.is_unset(request.scope):
            query['scope'] = request.scope
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.FinishBeginnerTaskResponse(),
            await self.do_roarequest_async('FinishBeginnerTask', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/beginnerTasks/{task_code}/finish', 'json', req, runtime)
        )

    def get_application_reg_form_by_flow_id(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdRequest,
    ) -> dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetApplicationRegFormByFlowIdHeaders()
        return self.get_application_reg_form_by_flow_id_with_options(flow_id, request, headers, runtime)

    async def get_application_reg_form_by_flow_id_async(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdRequest,
    ) -> dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetApplicationRegFormByFlowIdHeaders()
        return await self.get_application_reg_form_by_flow_id_with_options_async(flow_id, request, headers, runtime)

    def get_application_reg_form_by_flow_id_with_options(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdRequest,
        headers: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse:
        UtilClient.validate_model(request)
        flow_id = OpenApiUtilClient.get_encode_param(flow_id)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse(),
            self.do_roarequest('GetApplicationRegFormByFlowId', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/flows/{flow_id}/applicationRegForms', 'json', req, runtime)
        )

    async def get_application_reg_form_by_flow_id_with_options_async(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdRequest,
        headers: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse:
        UtilClient.validate_model(request)
        flow_id = OpenApiUtilClient.get_encode_param(flow_id)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse(),
            await self.do_roarequest_async('GetApplicationRegFormByFlowId', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/flows/{flow_id}/applicationRegForms', 'json', req, runtime)
        )

    def get_candidate_by_phone_number(
        self,
        request: dingtalkats__1__0_models.GetCandidateByPhoneNumberRequest,
    ) -> dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetCandidateByPhoneNumberHeaders()
        return self.get_candidate_by_phone_number_with_options(request, headers, runtime)

    async def get_candidate_by_phone_number_async(
        self,
        request: dingtalkats__1__0_models.GetCandidateByPhoneNumberRequest,
    ) -> dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetCandidateByPhoneNumberHeaders()
        return await self.get_candidate_by_phone_number_with_options_async(request, headers, runtime)

    def get_candidate_by_phone_number_with_options(
        self,
        request: dingtalkats__1__0_models.GetCandidateByPhoneNumberRequest,
        headers: dingtalkats__1__0_models.GetCandidateByPhoneNumberHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.phone_number):
            query['phoneNumber'] = request.phone_number
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse(),
            self.do_roarequest('GetCandidateByPhoneNumber', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/candidates', 'json', req, runtime)
        )

    async def get_candidate_by_phone_number_with_options_async(
        self,
        request: dingtalkats__1__0_models.GetCandidateByPhoneNumberRequest,
        headers: dingtalkats__1__0_models.GetCandidateByPhoneNumberHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.phone_number):
            query['phoneNumber'] = request.phone_number
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse(),
            await self.do_roarequest_async('GetCandidateByPhoneNumber', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/candidates', 'json', req, runtime)
        )

    def get_file_upload_info(
        self,
        request: dingtalkats__1__0_models.GetFileUploadInfoRequest,
    ) -> dingtalkats__1__0_models.GetFileUploadInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetFileUploadInfoHeaders()
        return self.get_file_upload_info_with_options(request, headers, runtime)

    async def get_file_upload_info_async(
        self,
        request: dingtalkats__1__0_models.GetFileUploadInfoRequest,
    ) -> dingtalkats__1__0_models.GetFileUploadInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetFileUploadInfoHeaders()
        return await self.get_file_upload_info_with_options_async(request, headers, runtime)

    def get_file_upload_info_with_options(
        self,
        request: dingtalkats__1__0_models.GetFileUploadInfoRequest,
        headers: dingtalkats__1__0_models.GetFileUploadInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetFileUploadInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.file_name):
            query['fileName'] = request.file_name
        if not UtilClient.is_unset(request.file_size):
            query['fileSize'] = request.file_size
        if not UtilClient.is_unset(request.md_5):
            query['md5'] = request.md_5
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetFileUploadInfoResponse(),
            self.do_roarequest('GetFileUploadInfo', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/files/uploadInfos', 'json', req, runtime)
        )

    async def get_file_upload_info_with_options_async(
        self,
        request: dingtalkats__1__0_models.GetFileUploadInfoRequest,
        headers: dingtalkats__1__0_models.GetFileUploadInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetFileUploadInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.file_name):
            query['fileName'] = request.file_name
        if not UtilClient.is_unset(request.file_size):
            query['fileSize'] = request.file_size
        if not UtilClient.is_unset(request.md_5):
            query['md5'] = request.md_5
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetFileUploadInfoResponse(),
            await self.do_roarequest_async('GetFileUploadInfo', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/files/uploadInfos', 'json', req, runtime)
        )

    def get_flow_id_by_relation_entity_id(
        self,
        request: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdRequest,
    ) -> dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetFlowIdByRelationEntityIdHeaders()
        return self.get_flow_id_by_relation_entity_id_with_options(request, headers, runtime)

    async def get_flow_id_by_relation_entity_id_async(
        self,
        request: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdRequest,
    ) -> dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetFlowIdByRelationEntityIdHeaders()
        return await self.get_flow_id_by_relation_entity_id_with_options_async(request, headers, runtime)

    def get_flow_id_by_relation_entity_id_with_options(
        self,
        request: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdRequest,
        headers: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.relation_entity):
            query['relationEntity'] = request.relation_entity
        if not UtilClient.is_unset(request.relation_entity_id):
            query['relationEntityId'] = request.relation_entity_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse(),
            self.do_roarequest('GetFlowIdByRelationEntityId', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/flows/ids', 'json', req, runtime)
        )

    async def get_flow_id_by_relation_entity_id_with_options_async(
        self,
        request: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdRequest,
        headers: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.relation_entity):
            query['relationEntity'] = request.relation_entity
        if not UtilClient.is_unset(request.relation_entity_id):
            query['relationEntityId'] = request.relation_entity_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse(),
            await self.do_roarequest_async('GetFlowIdByRelationEntityId', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/flows/ids', 'json', req, runtime)
        )

    def get_job_auth(
        self,
        job_id: str,
        request: dingtalkats__1__0_models.GetJobAuthRequest,
    ) -> dingtalkats__1__0_models.GetJobAuthResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetJobAuthHeaders()
        return self.get_job_auth_with_options(job_id, request, headers, runtime)

    async def get_job_auth_async(
        self,
        job_id: str,
        request: dingtalkats__1__0_models.GetJobAuthRequest,
    ) -> dingtalkats__1__0_models.GetJobAuthResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetJobAuthHeaders()
        return await self.get_job_auth_with_options_async(job_id, request, headers, runtime)

    def get_job_auth_with_options(
        self,
        job_id: str,
        request: dingtalkats__1__0_models.GetJobAuthRequest,
        headers: dingtalkats__1__0_models.GetJobAuthHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetJobAuthResponse:
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        query = {}
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetJobAuthResponse(),
            self.do_roarequest('GetJobAuth', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/auths/jobs/{job_id}', 'json', req, runtime)
        )

    async def get_job_auth_with_options_async(
        self,
        job_id: str,
        request: dingtalkats__1__0_models.GetJobAuthRequest,
        headers: dingtalkats__1__0_models.GetJobAuthHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetJobAuthResponse:
        UtilClient.validate_model(request)
        job_id = OpenApiUtilClient.get_encode_param(job_id)
        query = {}
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetJobAuthResponse(),
            await self.do_roarequest_async('GetJobAuth', 'ats_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/ats/auths/jobs/{job_id}', 'json', req, runtime)
        )

    def query_interviews(
        self,
        request: dingtalkats__1__0_models.QueryInterviewsRequest,
    ) -> dingtalkats__1__0_models.QueryInterviewsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.QueryInterviewsHeaders()
        return self.query_interviews_with_options(request, headers, runtime)

    async def query_interviews_async(
        self,
        request: dingtalkats__1__0_models.QueryInterviewsRequest,
    ) -> dingtalkats__1__0_models.QueryInterviewsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.QueryInterviewsHeaders()
        return await self.query_interviews_with_options_async(request, headers, runtime)

    def query_interviews_with_options(
        self,
        request: dingtalkats__1__0_models.QueryInterviewsRequest,
        headers: dingtalkats__1__0_models.QueryInterviewsHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.QueryInterviewsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.next_token):
            query['nextToken'] = request.next_token
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        body = {}
        if not UtilClient.is_unset(request.candidate_id):
            body['candidateId'] = request.candidate_id
        if not UtilClient.is_unset(request.start_time_begin_millis):
            body['startTimeBeginMillis'] = request.start_time_begin_millis
        if not UtilClient.is_unset(request.start_time_end_millis):
            body['startTimeEndMillis'] = request.start_time_end_millis
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.QueryInterviewsResponse(),
            self.do_roarequest('QueryInterviews', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/interviews/query', 'json', req, runtime)
        )

    async def query_interviews_with_options_async(
        self,
        request: dingtalkats__1__0_models.QueryInterviewsRequest,
        headers: dingtalkats__1__0_models.QueryInterviewsHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.QueryInterviewsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.next_token):
            query['nextToken'] = request.next_token
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        body = {}
        if not UtilClient.is_unset(request.candidate_id):
            body['candidateId'] = request.candidate_id
        if not UtilClient.is_unset(request.start_time_begin_millis):
            body['startTimeBeginMillis'] = request.start_time_begin_millis
        if not UtilClient.is_unset(request.start_time_end_millis):
            body['startTimeEndMillis'] = request.start_time_end_millis
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.QueryInterviewsResponse(),
            await self.do_roarequest_async('QueryInterviews', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/interviews/query', 'json', req, runtime)
        )

    def report_message_status(
        self,
        request: dingtalkats__1__0_models.ReportMessageStatusRequest,
    ) -> dingtalkats__1__0_models.ReportMessageStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.ReportMessageStatusHeaders()
        return self.report_message_status_with_options(request, headers, runtime)

    async def report_message_status_async(
        self,
        request: dingtalkats__1__0_models.ReportMessageStatusRequest,
    ) -> dingtalkats__1__0_models.ReportMessageStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.ReportMessageStatusHeaders()
        return await self.report_message_status_with_options_async(request, headers, runtime)

    def report_message_status_with_options(
        self,
        request: dingtalkats__1__0_models.ReportMessageStatusRequest,
        headers: dingtalkats__1__0_models.ReportMessageStatusHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.ReportMessageStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.error_code):
            body['errorCode'] = request.error_code
        if not UtilClient.is_unset(request.error_msg):
            body['errorMsg'] = request.error_msg
        if not UtilClient.is_unset(request.message_id):
            body['messageId'] = request.message_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.ReportMessageStatusResponse(),
            self.do_roarequest('ReportMessageStatus', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/channels/messages/statuses/report', 'json', req, runtime)
        )

    async def report_message_status_with_options_async(
        self,
        request: dingtalkats__1__0_models.ReportMessageStatusRequest,
        headers: dingtalkats__1__0_models.ReportMessageStatusHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.ReportMessageStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.error_code):
            body['errorCode'] = request.error_code
        if not UtilClient.is_unset(request.error_msg):
            body['errorMsg'] = request.error_msg
        if not UtilClient.is_unset(request.message_id):
            body['messageId'] = request.message_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.ReportMessageStatusResponse(),
            await self.do_roarequest_async('ReportMessageStatus', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/channels/messages/statuses/report', 'json', req, runtime)
        )

    def sync_channel_message(
        self,
        request: dingtalkats__1__0_models.SyncChannelMessageRequest,
    ) -> dingtalkats__1__0_models.SyncChannelMessageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.SyncChannelMessageHeaders()
        return self.sync_channel_message_with_options(request, headers, runtime)

    async def sync_channel_message_async(
        self,
        request: dingtalkats__1__0_models.SyncChannelMessageRequest,
    ) -> dingtalkats__1__0_models.SyncChannelMessageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.SyncChannelMessageHeaders()
        return await self.sync_channel_message_with_options_async(request, headers, runtime)

    def sync_channel_message_with_options(
        self,
        request: dingtalkats__1__0_models.SyncChannelMessageRequest,
        headers: dingtalkats__1__0_models.SyncChannelMessageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.SyncChannelMessageResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.create_time):
            body['createTime'] = request.create_time
        if not UtilClient.is_unset(request.receiver_user_id):
            body['receiverUserId'] = request.receiver_user_id
        if not UtilClient.is_unset(request.sender_user_id):
            body['senderUserId'] = request.sender_user_id
        if not UtilClient.is_unset(request.uuid):
            body['uuid'] = request.uuid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.SyncChannelMessageResponse(),
            self.do_roarequest('SyncChannelMessage', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/channels/messages/sync', 'json', req, runtime)
        )

    async def sync_channel_message_with_options_async(
        self,
        request: dingtalkats__1__0_models.SyncChannelMessageRequest,
        headers: dingtalkats__1__0_models.SyncChannelMessageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.SyncChannelMessageResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.create_time):
            body['createTime'] = request.create_time
        if not UtilClient.is_unset(request.receiver_user_id):
            body['receiverUserId'] = request.receiver_user_id
        if not UtilClient.is_unset(request.sender_user_id):
            body['senderUserId'] = request.sender_user_id
        if not UtilClient.is_unset(request.uuid):
            body['uuid'] = request.uuid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.SyncChannelMessageResponse(),
            await self.do_roarequest_async('SyncChannelMessage', 'ats_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/ats/channels/messages/sync', 'json', req, runtime)
        )

    def update_application_reg_form(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.UpdateApplicationRegFormRequest,
    ) -> dingtalkats__1__0_models.UpdateApplicationRegFormResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateApplicationRegFormHeaders()
        return self.update_application_reg_form_with_options(flow_id, request, headers, runtime)

    async def update_application_reg_form_async(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.UpdateApplicationRegFormRequest,
    ) -> dingtalkats__1__0_models.UpdateApplicationRegFormResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateApplicationRegFormHeaders()
        return await self.update_application_reg_form_with_options_async(flow_id, request, headers, runtime)

    def update_application_reg_form_with_options(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.UpdateApplicationRegFormRequest,
        headers: dingtalkats__1__0_models.UpdateApplicationRegFormHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateApplicationRegFormResponse:
        UtilClient.validate_model(request)
        flow_id = OpenApiUtilClient.get_encode_param(flow_id)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.ding_pan_file):
            body['dingPanFile'] = request.ding_pan_file
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateApplicationRegFormResponse(),
            self.do_roarequest('UpdateApplicationRegForm', 'ats_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/ats/flows/{flow_id}/applicationRegForms', 'json', req, runtime)
        )

    async def update_application_reg_form_with_options_async(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.UpdateApplicationRegFormRequest,
        headers: dingtalkats__1__0_models.UpdateApplicationRegFormHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateApplicationRegFormResponse:
        UtilClient.validate_model(request)
        flow_id = OpenApiUtilClient.get_encode_param(flow_id)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.ding_pan_file):
            body['dingPanFile'] = request.ding_pan_file
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateApplicationRegFormResponse(),
            await self.do_roarequest_async('UpdateApplicationRegForm', 'ats_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/ats/flows/{flow_id}/applicationRegForms', 'json', req, runtime)
        )

    def update_interview_sign_in_info(
        self,
        interview_id: str,
        request: dingtalkats__1__0_models.UpdateInterviewSignInInfoRequest,
    ) -> dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateInterviewSignInInfoHeaders()
        return self.update_interview_sign_in_info_with_options(interview_id, request, headers, runtime)

    async def update_interview_sign_in_info_async(
        self,
        interview_id: str,
        request: dingtalkats__1__0_models.UpdateInterviewSignInInfoRequest,
    ) -> dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateInterviewSignInInfoHeaders()
        return await self.update_interview_sign_in_info_with_options_async(interview_id, request, headers, runtime)

    def update_interview_sign_in_info_with_options(
        self,
        interview_id: str,
        request: dingtalkats__1__0_models.UpdateInterviewSignInInfoRequest,
        headers: dingtalkats__1__0_models.UpdateInterviewSignInInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse:
        UtilClient.validate_model(request)
        interview_id = OpenApiUtilClient.get_encode_param(interview_id)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.sign_in_time_millis):
            body['signInTimeMillis'] = request.sign_in_time_millis
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse(),
            self.do_roarequest('UpdateInterviewSignInInfo', 'ats_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/ats/interviews/{interview_id}/signInInfos', 'none', req, runtime)
        )

    async def update_interview_sign_in_info_with_options_async(
        self,
        interview_id: str,
        request: dingtalkats__1__0_models.UpdateInterviewSignInInfoRequest,
        headers: dingtalkats__1__0_models.UpdateInterviewSignInInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse:
        UtilClient.validate_model(request)
        interview_id = OpenApiUtilClient.get_encode_param(interview_id)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.sign_in_time_millis):
            body['signInTimeMillis'] = request.sign_in_time_millis
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse(),
            await self.do_roarequest_async('UpdateInterviewSignInInfo', 'ats_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/ats/interviews/{interview_id}/signInInfos', 'none', req, runtime)
        )

    def update_job_deliver(
        self,
        request: dingtalkats__1__0_models.UpdateJobDeliverRequest,
    ) -> dingtalkats__1__0_models.UpdateJobDeliverResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateJobDeliverHeaders()
        return self.update_job_deliver_with_options(request, headers, runtime)

    async def update_job_deliver_async(
        self,
        request: dingtalkats__1__0_models.UpdateJobDeliverRequest,
    ) -> dingtalkats__1__0_models.UpdateJobDeliverResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateJobDeliverHeaders()
        return await self.update_job_deliver_with_options_async(request, headers, runtime)

    def update_job_deliver_with_options(
        self,
        request: dingtalkats__1__0_models.UpdateJobDeliverRequest,
        headers: dingtalkats__1__0_models.UpdateJobDeliverHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateJobDeliverResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.job_id):
            query['jobId'] = request.job_id
        body = {}
        if not UtilClient.is_unset(request.channel_outer_id):
            body['channelOuterId'] = request.channel_outer_id
        if not UtilClient.is_unset(request.deliver_user_id):
            body['deliverUserId'] = request.deliver_user_id
        if not UtilClient.is_unset(request.error_code):
            body['errorCode'] = request.error_code
        if not UtilClient.is_unset(request.error_msg):
            body['errorMsg'] = request.error_msg
        if not UtilClient.is_unset(request.op_time):
            body['opTime'] = request.op_time
        if not UtilClient.is_unset(request.op_user_id):
            body['opUserId'] = request.op_user_id
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateJobDeliverResponse(),
            self.do_roarequest('UpdateJobDeliver', 'ats_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/ats/jobs/deliveryStatus', 'json', req, runtime)
        )

    async def update_job_deliver_with_options_async(
        self,
        request: dingtalkats__1__0_models.UpdateJobDeliverRequest,
        headers: dingtalkats__1__0_models.UpdateJobDeliverHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateJobDeliverResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.job_id):
            query['jobId'] = request.job_id
        body = {}
        if not UtilClient.is_unset(request.channel_outer_id):
            body['channelOuterId'] = request.channel_outer_id
        if not UtilClient.is_unset(request.deliver_user_id):
            body['deliverUserId'] = request.deliver_user_id
        if not UtilClient.is_unset(request.error_code):
            body['errorCode'] = request.error_code
        if not UtilClient.is_unset(request.error_msg):
            body['errorMsg'] = request.error_msg
        if not UtilClient.is_unset(request.op_time):
            body['opTime'] = request.op_time
        if not UtilClient.is_unset(request.op_user_id):
            body['opUserId'] = request.op_user_id
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateJobDeliverResponse(),
            await self.do_roarequest_async('UpdateJobDeliver', 'ats_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/ats/jobs/deliveryStatus', 'json', req, runtime)
        )
