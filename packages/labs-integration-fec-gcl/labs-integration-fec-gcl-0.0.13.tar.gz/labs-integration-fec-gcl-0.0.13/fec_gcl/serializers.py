import datetime

from rest_framework import serializers


class SysRequestSerializer(serializers.Serializer):
    TransID = serializers.RegexField(
        regex='^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')
    RequestorID = serializers.CharField()
    DateTime = serializers.DateTimeField(default=datetime.datetime.now(), format="%Y-%m-%dT%H:%M:%S.%f")


class GCLRequestSerializer(serializers.Serializer):
    Sys = SysRequestSerializer()
    NationalID = serializers.CharField()

    def is_valid(self, raise_exception=False):
        validity = super(GCLRequestSerializer, self).is_valid(raise_exception)
        if not validity:
            return validity
        self.data['Sys']['DateTime'] = datetime.datetime.strptime(self.data['Sys']['DateTime'], "%Y-%m-%dT%H:%M:%S.%f")
        return validity


class SysResponseSerializer(serializers.Serializer):
    TransID = serializers.RegexField(
        regex='^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')
    Code = serializers.CharField()
    DateTime = serializers.DateTimeField(default=datetime.datetime.now(), format="%Y-%m-%dT%H:%M:%S.%f")
    Description = serializers.CharField(required=False, allow_null=True)


# class GetTotalConsumedCRLReturnSerializer(serializers.Serializer):
#     Sys = SysResponseSerializer()
#     TotalAvailCrAmt = serializers.IntegerField(required=False, allow_null=True)


class GCLReturnSerializer(serializers.Serializer):
    Sys = SysResponseSerializer()
    TotalConsumedCrAmt = serializers.IntegerField(required=False, allow_null=True)
    NumberOfApp = serializers.IntegerField(required=False, allow_null=True)
    TotalEMI = serializers.IntegerField(required=False, allow_null=True)
    TotalAvailCrAmt = serializers.IntegerField(required=False, allow_null=True)

class APS_GCLRequestSerializer(serializers.Serializer):
    Sys = SysRequestSerializer()
    NationalId = serializers.CharField()

    def is_valid(self, raise_exception=False):
        validity = super(APS_GCLRequestSerializer, self).is_valid(raise_exception)
        if not validity:
            return validity
        self.data['Sys']['DateTime'] = datetime.datetime.strptime(self.data['Sys']['DateTime'], "%Y-%m-%dT%H:%M:%S.%f")
        return validity

class APS_GCLResponseSerializer(serializers.Serializer):
    Sys = SysResponseSerializer()
    OutstandingAmount = serializers.IntegerField(required=False, allow_null=True)
    RequestedLoanAmount = serializers.IntegerField(required=False, allow_null=True)