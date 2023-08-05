import uuid

from rest_framework import status
from rest_framework.permissions import AllowAny

from base_app.views import BaseAPIView
from fec_gcl.serializers import GCLRequestSerializer, GCLReturnSerializer, APS_GCLRequestSerializer, APS_GCLResponseSerializer
from fec_gcl.conf import settings
from fec_gcl import constants as fec_cons
from base_app.tasks import generic_task
from base_app.utils import make_dict, get_celery_queue, add_entry_to_celery_audit_tracker
from base_app import utils


class GetTotalConsumedCRL(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            response = self.soap_request(settings.GCL_WSDL,
                                         'GetTotalConsumedCRL',
                                         data=serializer.data,
                                         username=settings.GCL_USERNAME,
                                         password=settings.GCL_PASSWORD)
            response_serializer = GCLReturnSerializer(data=make_dict(response))
            if response_serializer.is_valid():
                response_code = response_serializer.data.get('Sys', {}).get('Code')
                if response_code == '1' or response_code == 1:
                    return utils.response(response_serializer.data)
                elif response_code in fec_cons.GCL_RETURN_CODES.keys():
                    error = fec_cons.GCL_RETURN_CODES[response_code]
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
                else:
                    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
            # Returning Error response
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type':'t','reason':error.get('message')})
            return utils.response(make_dict(response), error=error)
        error = serializer.errors
        error.update({'type':'s','reason':'bad request'})
        return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)


class GetTotalConsumedCRLAsync(BaseAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        pass

    def post(self, request):
        # Save request to database
        # enqueue task and return response
        serializer = GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            task_id = str(uuid.uuid4())
            queue_name = get_celery_queue("gclTotalConsumedCheckCRL")
            celery_audit_tracker_obj = add_entry_to_celery_audit_tracker(queue_name, 'gclTotalConsumedCheckCRL', '', request.data,
                                                                         1, task_id, serializer.validated_data)
            generic_task.apply_async(args=[celery_audit_tracker_obj.id], queue=queue_name, task_id=task_id)
            return utils.response({"task_id": task_id, "message": "Request enqueued successfully"})
        else:
            error = serializer.errors
            error.update({'type': 's', 'reason': 'bad request'})
            return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)


class GetConsumedCRLPEGA(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            response = self.soap_request(settings.GCL_WSDL,
                                         'GetConsumedCRLPEGA',
                                         data=serializer.data,
                                         username=settings.GCL_USERNAME,
                                         password=settings.GCL_PASSWORD)
            response_serializer = GCLReturnSerializer(data=make_dict(response))
            if response_serializer.is_valid():
                response_code = response_serializer.data.get('Sys', {}).get('Code')
                if response_code == '1' or response_code == 1:
                    return utils.response(response_serializer.data)
                elif response_code in fec_cons.GCL_RETURN_CODES.keys():
                    error = fec_cons.GCL_RETURN_CODES[response_code]
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
                else:
                    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
            # Returning Error response
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type':'t','reason':error.get('message')})
            return utils.response(make_dict(response), error=error)
        error = serializer.errors
        error.update({'type':'s','reason':'bad request'})
        return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)


class GetConsumedCRLPEGAAsync(BaseAPIView):
    permission_classes = (AllowAny,)

    def get(self):
        pass

    def post(self, request):
        serializer = GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            task_id = str(uuid.uuid4())
            queue_name = get_celery_queue("gclConsumedCRLPEGA")
            celery_audit_tracker_obj = add_entry_to_celery_audit_tracker(queue_name, 'gclConsumedCRLPEGA', '',
                                                                         request.data,
                                                                         1, task_id, serializer.validated_data)
            generic_task.apply_async(args=[celery_audit_tracker_obj.id], queue=queue_name, task_id=task_id)
            return utils.response({"task_id": task_id, "message": "Request enqueued successfully"})
        else:
            error = serializer.errors
            error.update({'type': 's', 'reason': 'bad request'})
            return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)


class GetConsumedCRLF1CAS(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            response = self.soap_request(settings.GCL_WSDL,
                                         'GetConsumedCRLF1CAS',
                                         data=serializer.data,
                                         username=settings.GCL_USERNAME,
                                         password=settings.GCL_PASSWORD)
            response_serializer = GCLReturnSerializer(data=make_dict(response))
            if response_serializer.is_valid():
                response_code = response_serializer.data.get('Sys', {}).get('Code')
                if response_code == '1' or response_code == 1:
                    return utils.response(response_serializer.data)
                elif response_code in fec_cons.GCL_RETURN_CODES.keys():
                    error = fec_cons.GCL_RETURN_CODES[response_code]
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
                else:
                    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
            # Returning Error response
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type': 't', 'reason': error.get('message')})
            return utils.response(make_dict(response), error=error)
        error = serializer.errors
        error.update({'type': 's', 'reason': 'bad request'})
        return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)


class GetConsumedCRLF1CASAsync(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            task_id = str(uuid.uuid4())
            queue_name = get_celery_queue('gclConsumedCRLF1CAS')
            celery_audit_tracker_obj = add_entry_to_celery_audit_tracker(queue_name, 'gclConsumedCRLF1CAS', '',
                                                                         request.data, 1, task_id,
                                                                         serializer.validated_data)
            generic_task.apply_async(args=[celery_audit_tracker_obj.id], queue=queue_name, task_id=task_id)
            return utils.response({"task_id": task_id, "message": "Request enqueued successfully"})
        else:
            error = serializer.errors
            error.update({'type':  's', 'reason': 'bad request'})
            return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)


class GetConsumedCRLAcctDB(BaseAPIView):
    permission_classes = (AllowAny,)
    print("Start GetConsumedCRLAcctDB")

    def post(self, request):
        serializer = GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            response = self.soap_request(settings.GCL_WSDL,
                                         'GetConsumedCRLAcctDB',
                                         data=serializer.data,
                                         username=settings.GCL_USERNAME,
                                         password=settings.GCL_PASSWORD)
            response_serializer = GCLReturnSerializer(data=make_dict(response))
            if response_serializer.is_valid():
                response_code = response_serializer.data.get('Sys', {}).get('Code')
                if response_code == '1' or response_code == 1:
                    return utils.response(response_serializer.data)
                elif response_code in fec_cons.GCL_RETURN_CODES.keys():
                    error = fec_cons.GCL_RETURN_CODES[response_code]
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
                else:
                    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
            # Returning Error response
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type': 't', 'reason': error.get('message')})
            return utils.response(make_dict(response), error=error)
        error = serializer.errors
        error.update({'type': 's', 'reason': 'bad request'})
        return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)


class GetConsumedCRLAcctDBAsync(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            task_id = str(uuid.uuid4())
            queue_name = get_celery_queue('gclConsumedCRLAcctDB')
            celery_audit_tracker_obj = add_entry_to_celery_audit_tracker(queue_name, 'gclConsumedCRLAcctDB', '',
                                                                         request.data, 1, task_id,
                                                                         serializer.validated_data)
            generic_task.apply_async(args=[celery_audit_tracker_obj.id], queue=queue_name, task_id=task_id)
            return utils.response({"task_id": task_id, "message": "Request enqueued successfully"})
        else:
            error = serializer.errors
            error.update({'type': 's', 'reason': 'bad request'})
            return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)

class GetGCLValidation(BaseAPIView):
    permission_classes = (AllowAny,)
    print("Start GetGCLValidation")

    def post(self, request):
        serializer = APS_GCLRequestSerializer(data=request.data)
        if serializer.is_valid():
            response = self.soap_request(settings.GCL_WSDL_APS,
                                        'GetGCLValidation',
                                        data=serializer.data,
                                        username=settings.GCL_USERNAME,
                                        password=settings.GCL_PASSWORD)
            response_serializer = APS_GCLResponseSerializer(data=make_dict(response))
            if response_serializer.is_valid():
                response_code = response_serializer.data.get('Sys', {}).get('Code')
                if response_code == '1' or response_code == 1:
                    return utils.response(response_serializer.data)
                elif response_code in fec_cons.GCL_RETURN_CODES.keys():
                    error = fec_cons.GCL_RETURN_CODES[response_code]
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
                else:
                    error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
                    error.update({'type':'t','reason':error.get('message')})
                    return utils.response(data=response_serializer.data, error=error, code=error.get('http_status'))
            # Returning Error response
            error = fec_cons.GCL_RETURN_CODES['unknown_error_code']
            error.update({'type': 't', 'reason': error.get('message')})
            return utils.response(make_dict(response), error=error)
        error = serializer.errors
        error.update({'type': 's', 'reason': 'bad request'})
        return utils.response(None, status.HTTP_400_BAD_REQUEST, error=error)
