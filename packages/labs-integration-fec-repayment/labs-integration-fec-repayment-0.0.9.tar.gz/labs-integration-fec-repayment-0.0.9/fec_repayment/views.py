import dicttoxml
import xmltodict

from rest_framework import status
from rest_framework.permissions import AllowAny

from base_app import utils
from base_app.views import BaseAPIView
from fec_repayment.conf import settings
from fec_repayment.serializers import RepaymentReturnSerializer, \
                                            HeaderBodyRequestSerializer, \
                                            HeaderBodyResponseSerializer


class ExecuteServiceMORA(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = HeaderBodyRequestSerializer(data=request.data)
        if serializer.is_valid():
            header_body = dicttoxml.dicttoxml(serializer.data, attr_type=False, root=False).decode("utf-8")
            response = self.soap_request(settings.REPAYMENT_WSDL,
                                         'executeService',
                                         data={
                                             "arg_0_0": settings.REPAYMENT_REQUEST_MORA.format(header_body),
                                         },username=settings.REPAYMENT_USERNAME, password=settings.REPAYMENT_PASSWORD)
            response_serializer = RepaymentReturnSerializer(data={"executeServiceReturn": response})
            if response_serializer.is_valid():
                response_dict = xmltodict.parse(response_serializer.data['executeServiceReturn'], encoding='utf-8')
                response_serializer = HeaderBodyResponseSerializer(data=response_dict['FIXML'])
                if response_serializer.is_valid():
                    return utils.response({"executeServiceReturn": response_serializer.data})
                return utils.response(response_serializer.errors, status.HTTP_502_BAD_GATEWAY, request.data)
            return utils.response(response_serializer.errors, status.HTTP_502_BAD_GATEWAY, request.data)
        return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST, request.data)


class ExecuteServiceNONMORA(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = HeaderBodyRequestSerializer(data=request.data)
        if serializer.is_valid():
            header_body = dicttoxml.dicttoxml(serializer.data, attr_type=False, root=False).decode("utf-8")
            response = self.soap_request(settings.REPAYMENT_WSDL,
                                         'executeService',
                                         data={
                                             "arg_0_0": settings.REPAYMENT_REQUEST_NONMORA.format(header_body),
                                         },username=settings.REPAYMENT_USERNAME, password=settings.REPAYMENT_PASSWORD)
            response_serializer = RepaymentReturnSerializer(data={"executeServiceReturn": response})
            if response_serializer.is_valid():
                response_dict = xmltodict.parse(response_serializer.data['executeServiceReturn'], encoding='utf-8')
                response_serializer = HeaderBodyResponseSerializer(data=response_dict['FIXML'])
                if response_serializer.is_valid():
                    return utils.response({"executeServiceReturn": response_serializer.data})
                return utils.response(response_serializer.errors, status.HTTP_502_BAD_GATEWAY, request.data)
            return utils.response(response_serializer.errors, status.HTTP_502_BAD_GATEWAY, request.data)
        return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST, request.data)


class ExecuteServiceAPS(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = HeaderBodyRequestSerializer(data=request.data)
        if serializer.is_valid():
            header_body = dicttoxml.dicttoxml(serializer.data, attr_type=False, root=False).decode("utf-8")
            response = self.soap_request(settings.REPAYMENT_WSDL,
                                         'executeService',
                                         data={
                                             "arg_0_0": settings.REPAYMENT_REQUEST_APS.format(header_body),
                                         },username=settings.REPAYMENT_USERNAME, password=settings.REPAYMENT_PASSWORD)
            response_serializer = RepaymentReturnSerializer(data={"executeServiceReturn": response})
            if response_serializer.is_valid():
                response_dict = xmltodict.parse(response_serializer.data['executeServiceReturn'], encoding='utf-8')
                response_serializer = HeaderBodyResponseSerializer(data=response_dict['FIXML'])
                if response_serializer.is_valid():
                    return utils.response({"executeServiceReturn": response_serializer.data})
                return utils.response(response_serializer.errors, status.HTTP_502_BAD_GATEWAY, request.data)
            return utils.response(response_serializer.errors, status.HTTP_502_BAD_GATEWAY, request.data)
        return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST, request.data)
