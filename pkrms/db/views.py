from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from django.core.exceptions import ValidationError
from .parsers import CustomJSONParser
from .models.form_data import FormData
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

def standardize_field_names(record):
    """Convert all field names to lowercase and handle special cases"""
    standardized = {}
    for key, value in record.items():
        # Convert to lowercase and handle special cases
        new_key = key.lower()
        if new_key in ['id', 'pk']:
            new_key = 'id'
        standardized[new_key] = value
    return standardized

def process_admin_code(record):
    """Generate admin_code if province_code and kabupaten_code are present"""
    if 'province_code' in record and 'kabupaten_code' in record:
        province_code = record['province_code']
        kabupaten_code = record['kabupaten_code']
        if province_code is not None and kabupaten_code is not None:
            try:
                record['admin_code'] = int(f"{int(province_code)}{int(kabupaten_code):02d}")
            except (ValueError, TypeError):
                pass
    return record

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
                
                form_data_objects = []
                for i, record in enumerate(form_data_records):
                    record = standardize_field_names(record)
                    serializer = FormDataSerializer(data=record)
                    if not serializer.is_valid():
                        # Check if the error is due to unique constraint
                        if 'non_field_errors' in serializer.errors and 'unique set' in str(serializer.errors['non_field_errors']):
                            # If it's a duplicate, try to get the existing record
                            try:
                                existing_record = FormData.objects.get(
                                    admin_code=record.get('admin_code'),
                                    email=record.get('email')
                                )
                                form_data_objects.append(existing_record)
                                continue  # Skip to next record
                            except FormData.DoesNotExist:
                                pass
                        
                        form_data_validation_failed = True
                        validation_errors[f"FormData_record_{i+2}"] = {
                            'record': record,
                            'errors': serializer.errors
                        }
                        break
                    else:
                        form_data_objects.append(serializer.save())

            # If FormData validation failed for non-unique constraint reasons, reject all data
            if form_data_validation_failed:
                return Response({
                    'status': 'validation_error',
                    'message': 'FormData validation failed - rejecting all data',
                    'errors': validation_errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # Add FormData results if validation passed or if we found existing records
            if form_data_objects:
                results['FormData'] = {
                    'status': 'success',
                    'count': len(form_data_objects),
                    'objects': FormDataSerializer(form_data_objects, many=True).data
                }

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
                        record = standardize_field_names(record)
                        record = process_admin_code(record)
                        processed_records.append(record)

                    # First validate all records
                    model_validation_errors = {}
                    for i, record in enumerate(processed_records):
                        try:
                            record_id = record.get('id')
                            if record_id is not None:
                                try:
                                    existing_obj = model.objects.get(id=record_id)
                                    serializer = serializer_class(existing_obj, data=record, partial=True)
                                except model.DoesNotExist:
                                    serializer = serializer_class(data=record)
                            else:
                                serializer = serializer_class(data=record)
                            
                            if not serializer.is_valid():
                                model_validation_errors[f"{model_name}_record_{i+2}"] = {
                                    'record': record,
                                    'errors': serializer.errors
                                }
                        except ValidationError as e:
                            model_validation_errors[f"{model_name}_record_{i+2}"] = {
                                'record': record,
                                'errors': str(e)
                            }

                    # If any validation errors, reject all records for this model
                    if model_validation_errors:
                        results[model_name] = {
                            'status': 'validation_error',
                            'message': f'Validation failed for {model_name} - rejecting all records',
                            'errors': model_validation_errors
                        }
                        validation_errors.update(model_validation_errors)
                        continue

                    # If all validations passed, save all records
                    objects = []
                    for record in processed_records:
                        try:
                            record_id = record.get('id')
                            if record_id is not None:
                                try:
                                    existing_obj = model.objects.get(id=record_id)
                                    serializer = serializer_class(existing_obj, data=record, partial=True)
                                except model.DoesNotExist:
                                    serializer = serializer_class(data=record)
                            else:
                                serializer = serializer_class(data=record)
                            
                            if serializer.is_valid():
                                obj = serializer.save()
                                objects.append(obj)
                            else:
                                raise ValidationError(serializer.errors)
                        except ValidationError as e:
                            model_validation_errors[f"{model_name}_record_{processed_records.index(record)+2}"] = {
                                'record': record,
                                'errors': str(e)
                            }
                            break  # Stop processing if any record fails

                    if model_validation_errors:
                        results[model_name] = {
                            'status': 'validation_error',
                            'message': f'Validation failed for {model_name} - rejecting all records',
                            'errors': model_validation_errors
                        }
                        validation_errors.update(model_validation_errors)
                        continue

                    results[model_name] = {
                        'status': 'success',
                        'count': len(objects),
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
                    'message': 'Some models failed validation - all records for those models were rejected',
                    'errors': error_details,
                    'successful_models': [
                        model for model, result in results.items()
                        if result.get('status') == 'success'
                    ]
                }, status=status.HTTP_207_MULTI_STATUS)
            
            return Response({
                'status': 'success',
                'message': 'All data processed successfully',
                'results': results
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
