import datetime

from rest_framework import serializers


class MessageKeySerializer(serializers.Serializer):
    RequestUUID = serializers.CharField(max_length=120, required=False, allow_null=True)
    ServiceRequestId = serializers.CharField(max_length=120, required=False, allow_null=True)
    ServiceRequestVersion = serializers.CharField(max_length=10, required=False, allow_null=True)
    ChannelId = serializers.CharField(max_length=10, required=False, allow_null=True)
    LanguageId = serializers.CharField(max_length=20, required=False, allow_null=True)


class MessageInfoSerializer(serializers.Serializer):
    BankId = serializers.CharField(max_length=20, required=False, allow_null=True)
    TimeZone = serializers.CharField(max_length=20, required=False, allow_null=True)
    EntityId = serializers.CharField(max_length=20, required=False, allow_null=True)
    EntityType = serializers.CharField(max_length=20, required=False, allow_null=True)
    ArmCorrelationId = serializers.CharField(max_length=20, required=False, allow_null=True)
    MessageDateTime = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')


class ReversalSerializer(serializers.Serializer):
    ParentRequestUUID = serializers.CharField(max_length=120, required=False, allow_null=True)


class PasswordTokenSerializer(serializers.Serializer):
    UserId = serializers.CharField(max_length=120, required=False, allow_null=True)
    Password = serializers.CharField(max_length=120, required=False, allow_null=True)


class TokenSerializer(serializers.Serializer):
    Certificate = serializers.CharField(max_length=1000, required=False, allow_null=True)
    PasswordToken = PasswordTokenSerializer()


class SecuritySerializer(serializers.Serializer):
    Token = TokenSerializer()
    FICertToken = serializers.CharField(max_length=1000, required=False, allow_null=True)
    RealUserLoginSessionId = serializers.CharField(max_length=120, required=False, allow_null=True)
    RealUser = serializers.CharField(max_length=120, required=False, allow_null=True)
    RealUserPwd = serializers.CharField(max_length=120, required=False, allow_null=True)
    SSOTransferToken = serializers.CharField(max_length=1000, required=False, allow_null=True)


class TableSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=120, required=False, allow_null=True)
    value = serializers.CharField(max_length=120, required=False, allow_null=True)


class CustomInfoSerializer(serializers.Serializer):
    table = TableSerializer()


class RequestHeaderSerializer(serializers.Serializer):
    MessageKey = MessageKeySerializer()
    RequestMessageInfo = MessageInfoSerializer()
    Reversal = ReversalSerializer(required=False, allow_null=True)
    Security = SecuritySerializer()
    CustomInfo = CustomInfoSerializer(required=False, allow_null=True)


class ExecuteFinacleScriptInputVOSerializer(serializers.Serializer):
    requestId = serializers.CharField(max_length=120)


class ExecuteFinacleScriptCustomDataRequestSerializer(serializers.Serializer):
    PROPOSALID = serializers.CharField(max_length=120)
    AGREEMENTNO = serializers.CharField(max_length=120)
    ACCTOPENDATE = serializers.DateField(format='%d-%m-%Y')
    LOANAMOUNT = serializers.IntegerField()
    EMIAMOUNT = serializers.IntegerField()
    INSTSTARTDATE = serializers.DateField(format='%d-%m-%Y')
    EFFRATE = serializers.IntegerField()
    INSTLNUM = serializers.IntegerField()
    TENOR = serializers.IntegerField()
    MORTLOAN = serializers.CharField(max_length=120)
    MORTINTRATE1 = serializers.IntegerField(required=False, allow_null=True)
    MORTINTRATE2 = serializers.IntegerField(required=False, allow_null=True)
    MORTPERIOD1 = serializers.IntegerField(required=False, allow_null=True)
    MORTPERIOD2 = serializers.IntegerField(required=False, allow_null=True)


class ExecuteFinacleScriptRequestSerializer(serializers.Serializer):
    ExecuteFinacleScriptInputVO = ExecuteFinacleScriptInputVOSerializer()
    executeFinacleScript_CustomData = ExecuteFinacleScriptCustomDataRequestSerializer()


class HeaderRequestSerializer(serializers.Serializer):
    RequestHeader = RequestHeaderSerializer()


class BodyRequestSerializer(serializers.Serializer):
    executeFinacleScriptRequest = ExecuteFinacleScriptRequestSerializer()


class HeaderBodyRequestSerializer(serializers.Serializer):
    Header = HeaderRequestSerializer()
    Body = BodyRequestSerializer()


# --------RESPONSE--------------------------------------------


class RepaymentReturnSerializer(serializers.Serializer):
    executeServiceReturn = serializers.CharField(max_length=10000)


class UBUSTransactionSerializer(serializers.Serializer):
    Id = serializers.CharField(max_length=120, required=False, allow_null=True)
    Status = serializers.CharField(max_length=120, required=False, allow_null=True)


class HostTransactionSerializer(serializers.Serializer):
    Id = serializers.CharField(max_length=120, required=False, allow_null=True)
    Status = serializers.CharField(max_length=120, required=False, allow_null=True)


class HostParentTransaction(serializers.Serializer):
    Id = serializers.CharField(max_length=120, required=False, allow_null=True)
    Status = serializers.CharField(max_length=120, required=False, allow_null=True)


class ResponseHeaderSerializer(serializers.Serializer):
    RequestMessageKey = MessageKeySerializer()
    ResponseMessageInfo = MessageInfoSerializer()
    UBUSTransaction = UBUSTransactionSerializer(required=False, allow_null=True)
    HostTransaction = HostTransactionSerializer(required=False, allow_null=True)
    HostParentTransaction = HostParentTransaction(required=False, allow_null=True)
    CustomInfo = CustomInfoSerializer(required=False, allow_null=True)


class InstPeriodSerializer(serializers.Serializer):
    PROPINSTLID = serializers.CharField(max_length=120, required=False, allow_null=True)
    INSTLNUM = serializers.IntegerField()
    DUEDATE = serializers.DateTimeField(format="%d-%m-%Y")
    INSTLAMT = serializers.IntegerField()
    PRINCOMP = serializers.IntegerField()
    INTCOMP = serializers.IntegerField()
    EFFRATE = serializers.DecimalField(max_digits=20, decimal_places=6)
    BALPRIN = serializers.IntegerField()
    DAYS = serializers.IntegerField()
    REPAYFEE = serializers.IntegerField()
    TOTALAMT = serializers.IntegerField()


class ExecuteFinacleScriptCustomDataResponseSerializer(serializers.Serializer):
    AGREEMENTNO = serializers.CharField(max_length=120, required=False, allow_null=True)
    PROPOSALID = serializers.CharField(max_length=120, required=False, allow_null=True)
    MORTLOAN = serializers.CharField(max_length=120, required=False, allow_null=True)
    INSTPERIOD = InstPeriodSerializer(many=True)
    OUTFLAG = serializers.CharField(max_length=120, required=False, allow_null=True)
    OUTMESSAGE = serializers.CharField(max_length=120, required=False, allow_null=True)


# TODO: check response and create serializer for ExecuteFinacleScriptOutputVO (dummy used for now)
class ExecuteFinacleScriptResponseSerializer(serializers.Serializer):
    ExecuteFinacleScriptOutputVO = ExecuteFinacleScriptInputVOSerializer(required=False, allow_null=True)
    executeFinacleScript_CustomData = ExecuteFinacleScriptCustomDataResponseSerializer(required=False, allow_null=True)


class HeaderResponseSerializer(serializers.Serializer):
    ResponseHeader = ResponseHeaderSerializer(required=False, allow_null=True)


class BodyResponseSerializer(serializers.Serializer):
    executeFinacleScriptResponse = ExecuteFinacleScriptResponseSerializer(required=False, allow_null=True)


class HeaderBodyResponseSerializer(serializers.Serializer):
    Header = HeaderResponseSerializer(required=False, allow_null=True)
    Body = BodyResponseSerializer(required=False, allow_null=True)

    def is_valid(self, raise_exception=False):
        try:
            for i in self.initial_data['Body']['executeFinacleScriptResponse']['executeFinacleScript_CustomData']['INSTPERIOD']:
                i['DUEDATE'] = datetime.datetime.strptime(i['DUEDATE'], "%d-%m-%Y")
        except:
            pass
        return super(HeaderBodyResponseSerializer, self).is_valid(raise_exception)
