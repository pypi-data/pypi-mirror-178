# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_dingtalk.rcs_call_1_0 import models as dingtalkrcs_call__1__0_models
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

    def run_call_user(
        self,
        request: dingtalkrcs_call__1__0_models.RunCallUserRequest,
    ) -> dingtalkrcs_call__1__0_models.RunCallUserResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkrcs_call__1__0_models.RunCallUserHeaders()
        return self.run_call_user_with_options(request, headers, runtime)

    async def run_call_user_async(
        self,
        request: dingtalkrcs_call__1__0_models.RunCallUserRequest,
    ) -> dingtalkrcs_call__1__0_models.RunCallUserResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkrcs_call__1__0_models.RunCallUserHeaders()
        return await self.run_call_user_with_options_async(request, headers, runtime)

    def run_call_user_with_options(
        self,
        request: dingtalkrcs_call__1__0_models.RunCallUserRequest,
        headers: dingtalkrcs_call__1__0_models.RunCallUserHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkrcs_call__1__0_models.RunCallUserResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.authorize_corp_id):
            query['authorizeCorpId'] = request.authorize_corp_id
        if not UtilClient.is_unset(request.authorize_user_id):
            query['authorizeUserId'] = request.authorize_user_id
        if not UtilClient.is_unset(request.order_id):
            query['orderId'] = request.order_id
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
            dingtalkrcs_call__1__0_models.RunCallUserResponse(),
            self.do_roarequest('RunCallUser', 'rcsCall_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/rcsCall/users/call', 'json', req, runtime)
        )

    async def run_call_user_with_options_async(
        self,
        request: dingtalkrcs_call__1__0_models.RunCallUserRequest,
        headers: dingtalkrcs_call__1__0_models.RunCallUserHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkrcs_call__1__0_models.RunCallUserResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.authorize_corp_id):
            query['authorizeCorpId'] = request.authorize_corp_id
        if not UtilClient.is_unset(request.authorize_user_id):
            query['authorizeUserId'] = request.authorize_user_id
        if not UtilClient.is_unset(request.order_id):
            query['orderId'] = request.order_id
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
            dingtalkrcs_call__1__0_models.RunCallUserResponse(),
            await self.do_roarequest_async('RunCallUser', 'rcsCall_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/rcsCall/users/call', 'json', req, runtime)
        )
