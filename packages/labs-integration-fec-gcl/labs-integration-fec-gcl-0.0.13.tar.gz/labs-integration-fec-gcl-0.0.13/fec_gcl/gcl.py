
from base_app.models import CeleryAuditTracker
from base_app.views import BaseAPIView
from base_app.utils import make_dict
from base_app.exceptions import GenericException
from base_app import utils
from fec_gcl import serializers as fec_gcl_serializers
from fec_gcl.conf import settings
from fec_gcl import constants as fec_cons


def gclGeTotalConsumedCRLPost(id, async_taskname):
    audit_tracker_obj = CeleryAuditTracker.objects.get(id=id)
    try:
        serializer = fec_gcl_serializers.GCLRequestSerializer(data=audit_tracker_obj.request)
        if serializer.is_valid():
            response = BaseAPIView().soap_request(settings.GCL_WSDL,
                                                       'GetTotalConsumedCRL',
                                         data=serializer.data,
                                         username=settings.GCL_USERNAME,
                                         password=settings.GCL_PASSWORD)
        else:
            error = serializer.errors
            error.update({'type': 's', 'reason': 'bad request'})
            audit_tracker_obj.response = utils.celery_response(None,audit_tracker_obj.metadata.get('process_instance_id'),
                                                               async_taskname=async_taskname,
                                                               code=400, error=error).data
            audit_tracker_obj.save()
            return False

    except GenericException as e:
        return True

    response_serializer = fec_gcl_serializers.GCLReturnSerializer(data=make_dict(response))
    if response_serializer.is_valid():
        audit_tracker_obj.response = utils.celery_response(response_serializer.data,
                                                           audit_tracker_obj.metadata.get('process_instance_id'),
                                                           async_taskname=async_taskname).data
        audit_tracker_obj.save()
        response_code = response_serializer.data.get('Sys', {}).get('Code')
        if response_code == '1' or response_code == 1:
            return False
        elif response_code == '2' or response_code == 2:
            return True
        elif response_code in fec_cons.GCL_RETURN_CODES.keys():
            error = fec_cons.GCL_RETURN_CODES[response_code]
            error.update({'type': 't', 'reason': error.get('message')})
            audit_tracker_obj.error = utils.celery_response(response_serializer.data,
                                                            audit_tracker_obj.metadata.get('process_instance_id'),
                                                            async_taskname=async_taskname, error=error,
                                                            code=error['http_status']).data
            audit_tracker_obj.save()
            return False
        else:
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type': 't', 'reason': error.get('message')})
            audit_tracker_obj.save()
            audit_tracker_obj.error = utils.celery_response(response_serializer.data,
                                                            audit_tracker_obj.metadata.get('process_instance_id'),
                                                            async_taskname=async_taskname, error=error,
                                                            code=error['http_status']).data
            audit_tracker_obj.save()
            return False
    # Returning Error response
    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
    error.update({'type': 't', 'reason': error.get('message')})
    audit_tracker_obj.error = utils.celery_response(make_dict(response),
                                                    audit_tracker_obj.metadata.get('process_instance_id'),
                                                    async_taskname=async_taskname, error=error).data
    audit_tracker_obj.save()
    return True


def gclGetConsumedCRLPEGAPost(id, async_taskname):
    audit_tracker_obj = CeleryAuditTracker.objects.get(id=id)
    try:
        serializer = fec_gcl_serializers.GCLRequestSerializer(data=audit_tracker_obj.request)
        if serializer.is_valid():
            response = BaseAPIView().soap_request(settings.GCL_WSDL,
                                         'GetConsumedCRLPEGA',
                                         data=serializer.data,
                                         username=settings.GCL_USERNAME,
                                         password=settings.GCL_PASSWORD)
        else:
            error = serializer.errors
            error.update({'type': 's', 'reason': 'bad request'})
            audit_tracker_obj.response = utils.celery_response(None,
                                                               audit_tracker_obj.metadata.get('process_instance_id'),
                                                               async_taskname=async_taskname,
                                                               code=400, error=error).data
            audit_tracker_obj.save()
            return False

    except GenericException as e:
            return True

    response_serializer = fec_gcl_serializers.GCLReturnSerializer(data=make_dict(response))
    if response_serializer.is_valid():
        audit_tracker_obj.response = utils.celery_response(response_serializer.data,
                                                           audit_tracker_obj.metadata.get('process_instance_id'),
                                                           async_taskname=async_taskname).data
        audit_tracker_obj.save()
        response_code = response_serializer.data.get('Sys', {}).get('Code')
        if response_code == '1' or response_code == 1:
            audit_tracker_obj.save()
            return False
        elif response_code == '2' or response_code == 2:
            return True
        elif response_code in fec_cons.GCL_RETURN_CODES.keys():
            error = fec_cons.GCL_RETURN_CODES[response_code]
            error.update({'type': 't', 'reason': error.get('message')})
            audit_tracker_obj.save()
            return False
        else:
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type': 't', 'reason': error.get('message')})
            audit_tracker_obj.save()
            return False
    # Returning Error response
    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
    error.update({'type': 't', 'reason': error.get('message')})
    audit_tracker_obj.error = utils.celery_response(make_dict(response),
                                                    audit_tracker_obj.metadata.get('process_instance_id'),
                                                    async_taskname=async_taskname, error=error).data
    audit_tracker_obj.save()
    return True


def gclGetConsumedCRLF1CASPost(id, async_taskname):
    audit_tracker_obj = CeleryAuditTracker.objects.get(id=id)
    try:
        serializer = fec_gcl_serializers.GCLRequestSerializer(data=audit_tracker_obj.request)
        if serializer.is_valid():
            response = BaseAPIView().soap_request(settings.GCL_WSDL,
                                         'GetConsumedCRLF1CAS',
                                         data=serializer.data,
                                         username=settings.GCL_USERNAME,
                                         password=settings.GCL_PASSWORD)

    except GenericException as e:
        return True

    response_serializer = fec_gcl_serializers.GCLReturnSerializer(data=make_dict(response))
    if response_serializer.is_valid():
        audit_tracker_obj.response = utils.celery_response(response_serializer.data,
                                                           audit_tracker_obj.metadata.get('process_instance_id'),
                                                           async_taskname=async_taskname).data
        audit_tracker_obj.save()
        response_code = response_serializer.data.get('Sys', {}).get('Code')
        if response_code == '1' or response_code == 1:
            audit_tracker_obj.save()
            return False
        elif response_code == '2' or response_code == 2:
            return True
        elif response_code in fec_cons.GCL_RETURN_CODES.keys():
            error = fec_cons.GCL_RETURN_CODES[response_code]
            error.update({'type': 't', 'reason': error.get('message')})
            audit_tracker_obj.error = utils.celery_response(response_serializer.data,
                                                            audit_tracker_obj.metadata.get('process_instance_id'),
                                                            async_taskname=async_taskname, error=error,
                                                            code=error['http_status']).data
            audit_tracker_obj.save()
            return False
        else:
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type': 't', 'reason': error.get('message')})
            audit_tracker_obj.error = utils.celery_response(response_serializer.data,
                                                            audit_tracker_obj.metadata.get('process_instance_id'),
                                                            async_taskname=async_taskname, error=error,
                                                            code=error['http_status']).data
            audit_tracker_obj.save()
            return False
    # Returning Error response
    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
    error.update({'type': 't', 'reason': error.get('message')})
    audit_tracker_obj.error = utils.celery_response(response_serializer.data,
                                                    audit_tracker_obj.metadata.get('process_instance_id'),
                                                    async_taskname=async_taskname, error=error,
                                                    code=error['http_status']).data
    audit_tracker_obj.save()
    return True


def gclConsumedCRLAcctDBPost(id, async_taskname):
    audit_tracker_obj = CeleryAuditTracker.objects.get(id=id)

    try:
        serializer = fec_gcl_serializers.GCLRequestSerializer(data=audit_tracker_obj.request)
        if serializer.is_valid():
            response = BaseAPIView().soap_request(settings.GCL_WSDL,
                                         'GetConsumedCRLAcctDB',
                                         data=serializer.data,
                                         username=settings.GCL_USERNAME,
                                         password=settings.GCL_PASSWORD)
    except GenericException as e:
        return True

    response_serializer = fec_gcl_serializers.GCLReturnSerializer(data=make_dict(response))
    if response_serializer.is_valid():
        audit_tracker_obj.response = utils.celery_response(response_serializer.data,
                                                           audit_tracker_obj.metadata.get('process_instance_id'),
                                                           async_taskname=async_taskname).data
        audit_tracker_obj.save()
        response_code = response_serializer.data.get('Sys', {}).get('Code')
        if response_code == '1' or response_code == 1:
            audit_tracker_obj.save()
            return False
        elif response_code == '2' or response_code == 2:
            return True
        elif response_code in fec_cons.GCL_RETURN_CODES.keys():
            error = fec_cons.GCL_RETURN_CODES[response_code]
            error.update({'type': 't', 'reason': error.get('message')})
            audit_tracker_obj.error = utils.celery_response(response_serializer.data,
                                                            audit_tracker_obj.metadata.get('process_instance_id'),
                                                            async_taskname=async_taskname, error=error,
                                                            code=error['http_status']).data
            audit_tracker_obj.save()
            return False
        else:
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type': 't', 'reason': error.get('message')})
            audit_tracker_obj.error = utils.celery_response(response_serializer.data,
                                                            audit_tracker_obj.metadata.get('process_instance_id'),
                                                            async_taskname=async_taskname, error=error,
                                                            code=error['http_status']).data
            audit_tracker_obj.save()
            return False
    # Returning Error response
    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
    error.update({'type': 't', 'reason': error.get('message')})
    audit_tracker_obj.error = utils.celery_response(make_dict(response),
                                                    audit_tracker_obj.metadata.get('process_instance_id'),
                                                    async_taskname=async_taskname, error=error).data
    audit_tracker_obj.save()
    return True


