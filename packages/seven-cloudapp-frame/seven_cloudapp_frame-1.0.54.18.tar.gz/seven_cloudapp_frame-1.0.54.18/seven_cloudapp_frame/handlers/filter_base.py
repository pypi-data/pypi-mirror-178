# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-04-24 15:15:19
@LastEditTime: 2022-07-08 14:42:18
@LastEditors: HuangJianYi
@Description: 
"""

from seven_framework.web_tornado.base_handler.base_api_handler import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.customize.cryptography_helper import *
from seven_cloudapp_frame.libs.customize.riskmanage_helper import *
from seven_cloudapp_frame.models.app_base_model import *
from urllib.parse import parse_qs


def filter_check_params(must_params=None, check_user_code=False):
    """
    :description: 参数过滤装饰器 仅限handler使用,
                  提供参数的检查及获取参数功能
                  装饰器使用方法:
                  @client_filter_check_params("param_a,param_b,param_c")  或
                  @client_filter_check_params(["param_a","param_b,param_c"])
                  参数获取方法:
                  self.request_params[param_key]
    :param must_params: 必须传递的参数集合
    :param check_user_code: 是否校验用户标识必传
    :last_editors: HuangJianYi
    """
    def check_params(handler):
        def wrapper(self, **args):
            finally_must_params = must_params
            if hasattr(self, "must_params"):
                finally_must_params = self.must_params
            if type(finally_must_params) == str:
                must_array = finally_must_params.split(",")
            if type(finally_must_params) == list:
                must_array = finally_must_params

            if finally_must_params:
                for must_param in must_array:
                    if not must_param in self.request_params or self.request_params[must_param] == "":
                        self.response_json_error("param_error", f"参数错误,缺少必传参数{must_param}")
                        return
            if check_user_code == True and not self.get_user_id():
                self.response_json_error("param_error", f"参数错误,缺少必传参数user_code")
                return

            return handler(self, **args)

        return wrapper

    return check_params


def filter_check_current_limit():
    """
    :description: 流量限制过滤装饰器 仅限handler使用
    :last_editors: HuangJianYi
    """
    def check_current(handler):
        def wrapper(self, **args):
            app_base_model = AppBaseModel(context=self)
            app_id = self.get_app_id()
            app_info_dict = app_base_model.get_app_info_dict(app_id,True,"current_limit_count")
            if app_info_dict and RiskManageHelper.check_current_limit(app_id, app_info_dict["current_limit_count"]) == True:
                self.response_json_error("current_limit", "系统繁忙,请稍后再试")
                return

            return handler(self, **args)

        return wrapper

    return check_current


def filter_check_head_sign(is_check=True, no_check_params=None):
    """
    :description: 头部过滤装饰器 仅限handler使用
    :param is_check: 是否开启校验
    :param no_check_params: 不加入参数校验的参数集合
    :last_editors: HuangJianYi
    """
    def check_head(handler):
        def wrapper(self, **args):
            encrypt_key = config.get_value("encrypt_key", "r8C1JpyAXxrFV26V")
            is_check_head = config.get_value("is_check_head", False)
            if is_check_head == False:
                is_check = False
            else:
                is_check = True
            if is_check == True:
                try:
                    if type(no_check_params) == str:
                        no_check_array = no_check_params.split(",")
                    elif type(no_check_params) == list:
                        no_check_array = no_check_params
                    else:
                        no_check_array = []
                    # 验证是否有设备信息
                    clientheaderinfo_string = self.request.headers._dict.get("Clientheaderinfo")
                    if clientheaderinfo_string:
                        # 将设备信息字符串转为字典类型
                        device_info_dict = self.device_info_dict(clientheaderinfo_string)
                        # 验证签名超时 10分钟过期
                        now_time = TimeHelper.get_now_timestamp(True)
                        if now_time - device_info_dict["timestamp"] > int(1000 * 60 * 10):
                            return self.response_json_error("timestamp", "超时操作")
                        # 验证是否有头部信息签名
                        if not device_info_dict.__contains__("signature_md5"):
                            return self.response_json_error("signature_md5", "缺少参数signature_md5")
                        # 验证头部签名是否成功
                        client_head_dict = dict([(k, v[0]) for k, v in parse_qs(clientheaderinfo_string, True).items() if not k in no_check_array])
                        head_signature_md5 = CryptographyHelper.signature_md5(client_head_dict, encrypt_key)
                        signature_md5 = device_info_dict["signature_md5"].lower()
                        if signature_md5 != head_signature_md5:
                            return self.response_json_error("signature_fail", "头部签名验证失败")
                    else:
                        return self.response_json_error("no_device_info", "没有提交设备信息")
                except Exception as ex:
                    self.logging_link_error("【头部校验异常】" + traceback.format_exc())
                    return self.response_json_error("error", "头部验证失败")

            return handler(self, **args)

        return wrapper

    return check_head


def filter_check_params_sign(is_check=True, no_check_params=None):
    """
    :description: 请求参数过滤装饰器 仅限handler使用
    :param is_check: 是否开启校验
    :param no_check_params: 不加入参数校验的参数集合
    :last_editors: HuangJianYi
    """
    def check_params(handler):
        def wrapper(self, **args):
            encrypt_key = config.get_value("encrypt_key", "r8C1JpyAXxrFV26V")
            client_encrypt_type = config.get_value("client_encrypt_type", 0)
            server_encrypt_type = config.get_value("server_encrypt_type", 0)
            if ("/server/" in self.request.uri and server_encrypt_type != 2) or ("/client/" in self.request.uri and client_encrypt_type != 2):
                is_check = False
            else:
                is_check = True
            if is_check == True:
                try:
                    if type(no_check_params) == str:
                        no_check_array = no_check_params.split(",")
                    elif type(no_check_params) == list:
                        no_check_array = no_check_params
                    else:
                        no_check_array = []
                    # 验证参数
                    request_param_dict = {}
                    try:
                        if "Content-Type" in self.request.headers and self.request.headers["Content-type"].lower().find("application/json") >= 0 and self.request.body:
                            request_param_dict = json.loads(self.request.body)
                        else:
                            request_param_dict = dict([(k, v[0]) for k, v in parse_qs(self.request.query, True).items() if not k in no_check_array])
                    except:
                        pass
                    if not request_param_dict.__contains__("param_signature_md5"):
                        return self.response_json_error("signature_fail", "缺少参数param_signature_md5")
                    check_request_signature_md5 = CryptographyHelper.signature_md5(request_param_dict, encrypt_key)
                    param_signature_md5 = request_param_dict["param_signature_md5"].lower()
                    if check_request_signature_md5 != param_signature_md5:
                        return self.response_json_error("signature_fail", "参数签名验证失败")

                except Exception as ex:
                    self.logging_link_error("【请求参数校验异常】" + traceback.format_exc())
                    return self.response_json_error("error", "请求参数验证失败")

            return handler(self, **args)

        return wrapper

    return check_params
