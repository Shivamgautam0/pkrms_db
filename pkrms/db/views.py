from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from django.core.exceptions import ValidationError
from .parsers import CustomJSONParser
import math
import numpy as np
from .utils.helpers import generate_admin_code
from .serializers import (
    BridgeInventorySerializer,
    CODE_AN_ParametersSerializer,
    CODE_AN_UnitCostsPERSerializer,
    CODE_AN_UnitCostsPERUnpavedSerializer,
    CODE_AN_UnitCostsREHSerializer,
    CODE_AN_UnitCostsRIGIDSerializer,
    CODE_AN_UnitCostsRMSerializer,
    CODE_AN_UnitCostsUPGUnpavedSerializer,
    CODE_AN_UnitCostsWideningSerializer,
    CODE_AN_WidthStandardsSerializer,
    CulvertConditionSerializer,
    CulvertInventorySerializer,
    LinkSerializer,
    RetainingWallConditionSerializer,
    RetainingWallInventorySerializer,
    RoadConditionSerializer,
    RoadInventorySerializer,
    TrafficVolumeSerializer,
    FormDataSerializer,
    TrafficWeightingFactorsSerializer,
    DRPSerializer,
    AlignmentSerializer,
    RoadHazardSerializer
)

def clean_nan_values(data):
    if isinstance(data, dict):
        return {k: clean_nan_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_nan_values(item) for item in data]
    elif isinstance(data, float) and (math.isnan(data) or np.isnan(data)):
        return None
    return data

# Map model names to their serializers
SERIALIZER_MAP = {
    'BridgeInventory': BridgeInventorySerializer,
    'CODE_AN_Parameters': CODE_AN_ParametersSerializer,
    'CODE_AN_UnitCostsPER': CODE_AN_UnitCostsPERSerializer,
    'CODE_AN_UnitCostsPERUnpaved': CODE_AN_UnitCostsPERUnpavedSerializer,
    'CODE_AN_UnitCostsREH': CODE_AN_UnitCostsREHSerializer,
    'CODE_AN_UnitCostsRIGID': CODE_AN_UnitCostsRIGIDSerializer,
    'CODE_AN_UnitCostsRM': CODE_AN_UnitCostsRMSerializer,
    'CODE_AN_UnitCostsUPGUnpaved': CODE_AN_UnitCostsUPGUnpavedSerializer,
    'CODE_AN_UnitCostsWidening': CODE_AN_UnitCostsWideningSerializer,
    'CODE_AN_WidthStandards': CODE_AN_WidthStandardsSerializer,
    'CulvertCondition': CulvertConditionSerializer,
    'CulvertInventory': CulvertInventorySerializer,
    'Link': LinkSerializer,
    'RetainingWallCondition': RetainingWallConditionSerializer,
    'RetainingWallInventory': RetainingWallInventorySerializer,
    'RoadCondition': RoadConditionSerializer,
    'RoadInventory': RoadInventorySerializer,
    'TrafficVolume': TrafficVolumeSerializer,
    'FormData': FormDataSerializer,
    'TrafficWeightingFactors': TrafficWeightingFactorsSerializer,
    'DRP': DRPSerializer,
    'Alignment': AlignmentSerializer,
    'RoadHazard': RoadHazardSerializer
}

class UploadDataView(APIView):
    parser_classes = [CustomJSONParser]

    def post(self, request):
        try:
            data = clean_nan_values(request.data)
            results = {}
            validation_errors = {}
            form_data_validation_failed = False

            # First check FormData validation
            if 'FormData' in data:
                form_data_records = data['FormData']
                if not isinstance(form_data_records, list):
                    form_data_records = [form_data_records]
                
                for i, record in enumerate(form_data_records):
                    record = {k.lower(): v for k, v in record.items()}
                    serializer = FormDataSerializer(data=record)
                    if not serializer.is_valid():
                        form_data_validation_failed = True
                        validation_errors[f"FormData_record_{i}"] = {
                            'record': record,
                            'errors': serializer.errors
                        }
                        break

            # If FormData validation failed, reject all data
            if form_data_validation_failed:
                return Response({
                    'status': 'validation_error',
                    'message': 'FormData validation failed - rejecting all data',
                    'errors': validation_errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # Process other models
            for model_name, records in data.items():
                if model_name == 'FormData':
                    continue  # Skip FormData as it's already processed
                    
                try:
                    if not isinstance(records, list):
                        continue
                        
                    model = apps.get_model('db', model_name)
                    serializer_class = SERIALIZER_MAP.get(model_name)
                    if not serializer_class:
                        results[model_name] = {
                            'status': 'error',
                            'message': f'No serializer found for model {model_name}'
                        }
                        continue

                    processed_records = []
                    for record in records:
                        record = {k.lower(): v for k, v in record.items()}
                        if 'province_code' in record and 'kabupaten_code' in record:
                            province_code = record['province_code']
                            kabupaten_code = record['kabupaten_code']
                            if province_code is not None and kabupaten_code is not None:
                                record['admin_code'] = int(f"{int(province_code)}{int(kabupaten_code):02d}")
                        processed_records.append(record)

                    objects = []
                    model_validation_errors = {}
                    for i, record in enumerate(processed_records):
                        try:
                            record_id = record.get('id')
                            if record_id is not None:
                                try:
                                    existing_obj = model.objects.get(id=record_id)
                                    serializer = serializer_class(existing_obj, data=record, partial=True)
                                    if serializer.is_valid():
                                        obj = serializer.save()
                                        objects.append(obj)
                                    else:
                                        model_validation_errors[f"{model_name}_record_{i}"] = {
                                            'record': record,
                                            'errors': serializer.errors
                                        }
                                except model.DoesNotExist:
                                    serializer = serializer_class(data=record)
                                    if serializer.is_valid():
                                        obj = serializer.save()
                                        objects.append(obj)
                                    else:
                                        model_validation_errors[f"{model_name}_record_{i}"] = {
                                            'record': record,
                                            'errors': serializer.errors
                                        }
                            else:
                                serializer = serializer_class(data=record)
                                if serializer.is_valid():
                                    obj = serializer.save()
                                    objects.append(obj)
                                else:
                                    model_validation_errors[f"{model_name}_record_{i}"] = {
                                        'record': record,
                                        'errors': serializer.errors
                                    }
                        except ValidationError as e:
                            model_validation_errors[f"{model_name}_record_{i}"] = {
                                'record': record,
                                'errors': str(e)
                            }

                    if model_validation_errors:
                        results[model_name] = {
                            'status': 'validation_error',
                            'errors': model_validation_errors
                        }
                        validation_errors.update(model_validation_errors)
                    else:
                        results[model_name] = {
                            'status': 'success',
                            'objects': serializer_class(objects, many=True).data
                        }

                except Exception as e:
                    results[model_name] = {
                        'status': 'error',
                        'message': str(e)
                    }

            # Check if any model had validation errors
            has_validation_errors = any(result.get('status') == 'validation_error' for result in results.values())
            
            if has_validation_errors:
                # Extract only the errors from results
                error_details = {
                    model: result['errors']
                    for model, result in results.items()
                    if result.get('status') == 'validation_error'
                }
                
                return Response({
                    'status': 'partial_success',
                    'message': 'Some records failed validation',
                    'errors': error_details,
                    'successful_models': [
                        model for model, result in results.items()
                        if result.get('status') == 'success'
                    ]
                }, status=status.HTTP_207_MULTI_STATUS)
            
            return Response({
                'status': 'success',
                'message': 'All data processed successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
