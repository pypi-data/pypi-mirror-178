from django.http import JsonResponse, HttpResponse
from rest_framework import request
from rest_framework.views import APIView
# from ..services.payment_wechat_service import PaymentWechatService
from ..services.payment_temporary_wechat_service import PaymentWechatService
from ..utils.model_handle import parse_data


class PaymentWechat(APIView):
    # 获取唯一标识
    def get_user_info(self):
        code = self.GET.get('code', 0)
        wxpay_params = PaymentWechatService.get_user_info(code)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': wxpay_params
        })

    # 小程序支付
    def payment_applets_pay(self):
        params = parse_data(self)
        wxpay_params = PaymentWechatService.payment_applets_pay(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': wxpay_params
        })

    # 扫码支付
    def payment_scan_pay(self):
        params = parse_data(self)
        wxpay_params = PaymentWechatService.payment_scan_pay(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': wxpay_params
        })

    # 微信小程序红包
    def payment_red_envelopes(self):
        params = parse_data(self)
        wxpay_params = PaymentWechatService.payment_red_envelopes(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': wxpay_params
        })

    # 回调接口
    def callback(self):
        body = self.body
        wxpay_params = PaymentWechatService.callback_old(body)
        return HttpResponse(wxpay_params)

    # 回调接口 v3
    def callback_v3(self):
        body = self.body
        headers = {}
        headers.update({'Wechatpay-Signature': self.META.get('HTTP_WECHATPAY_SIGNATURE')})
        headers.update({'Wechatpay-Timestamp': self.META.get('HTTP_WECHATPAY_TIMESTAMP')})
        headers.update({'Wechatpay-Nonce': self.META.get('HTTP_WECHATPAY_NONCE')})
        headers.update({'Wechatpay-Serial': self.META.get('HTTP_WECHATPAY_SERIAL')})
        wxpay_params = PaymentWechatService.callback(headers, body)
        return JsonResponse(wxpay_params)
