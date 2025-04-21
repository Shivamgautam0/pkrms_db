from django.forms import ValidationError
from rest_framework import serializers
from .models import (
    BridgeInventory,
    CODE_AN_Parameters,
    CODE_AN_UnitCostsPER,
    CODE_AN_UnitCostsPERUnpaved,
    CODE_AN_UnitCostsREH,
    CODE_AN_UnitCostsRIGID,
    CODE_AN_UnitCostsRM,
    CODE_AN_UnitCostsUPGUnpaved,
    CODE_AN_UnitCostsWidening,
    CODE_AN_WidthStandards,
    CulvertCondition,
    CulvertInventory,
    Link,
    RetainingWallCondition,
    RetainingWallInventory,
    RoadCondition,
    RoadInventory,
    TrafficVolume,
    FormData,
    TrafficWeightingFactors,
    DRP,
    Alignment,
    RoadHazard
)

class BridgeInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BridgeInventory
        fields = '__all__'

class CODE_AN_ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_Parameters
        fields = '__all__'

class CODE_AN_UnitCostsPERSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_UnitCostsPER
        fields = '__all__'

class CODE_AN_UnitCostsPERUnpavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_UnitCostsPERUnpaved
        fields = '__all__'

class CODE_AN_UnitCostsREHSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_UnitCostsREH
        fields = '__all__'

class CODE_AN_UnitCostsRIGIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_UnitCostsRIGID
        fields = '__all__'

class CODE_AN_UnitCostsRMSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_UnitCostsRM
        fields = '__all__'

class CODE_AN_UnitCostsUPGUnpavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_UnitCostsUPGUnpaved
        fields = '__all__'

class CODE_AN_UnitCostsWideningSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_UnitCostsWidening
        fields = '__all__'

class CODE_AN_WidthStandardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODE_AN_WidthStandards
        fields = '__all__'

class CulvertConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CulvertCondition
        fields = '__all__'

class CulvertInventorySerializer(serializers.ModelSerializer):
    def validate(self, data):
        try:
            instance = CulvertInventory(**data)
            instance.clean()
        except ValidationError as e:
            error_message = str(e)
            if isinstance(e.messages, list) and len(e.messages) > 0:
                error_message = e.messages[0]
            raise serializers.ValidationError({'error': error_message})
        return data

    class Meta:
        model = CulvertInventory
        fields = '__all__'

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'

class RetainingWallConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetainingWallCondition
        fields = '__all__'

class RetainingWallInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RetainingWallInventory
        fields = '__all__'

class RoadConditionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        try:
            instance = RoadCondition(**data)
            instance.clean()
        except ValidationError as e:
            error_message = str(e)
            if isinstance(e.messages, list) and len(e.messages) > 0:
                error_message = e.messages[0]
            raise serializers.ValidationError({'error': error_message})
        return data

    class Meta:
        model = RoadCondition
        fields = '__all__'

class RoadInventorySerializer(serializers.ModelSerializer):
    def validate(self, data):
        try:
            instance = RoadInventory(**data)
            instance.clean()
        except ValidationError as e:
            # Convert the error message to a string without the non_field_errors prefix
            error_message = str(e)
            if isinstance(e.messages, list) and len(e.messages) > 0:
                error_message = e.messages[0]
            # Return a dictionary with a custom key instead of using non_field_errors
            raise serializers.ValidationError({'error': error_message})
        return data

    class Meta:
        model = RoadInventory
        fields = '__all__'

class TrafficVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficVolume
        fields = '__all__' 

class FormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormData
        fields = '__all__'
        

class TrafficWeightingFactorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficWeightingFactors
        fields = '__all__'

class DRPSerializer(serializers.ModelSerializer):
    def validate(self, data):
        try:
            instance = DRP(**data)
            instance.clean()
        except ValidationError as e:
            error_message = str(e)
            if isinstance(e.messages, list) and len(e.messages) > 0:
                error_message = e.messages[0]
            raise serializers.ValidationError({'error': error_message})
        return data

    class Meta:
        model = DRP
        fields = '__all__'

class AlignmentSerializer(serializers.ModelSerializer):
    def validate(self, data):
        try:
            instance = Alignment(**data)
            instance.clean()
        except ValidationError as e:
            error_message = str(e)
            if isinstance(e.messages, list) and len(e.messages) > 0:
                error_message = e.messages[0]
            raise serializers.ValidationError({'error': error_message})
        return data

    class Meta:
        model = Alignment
        fields = '__all__'

class RoadHazardSerializer(serializers.ModelSerializer):
    def validate(self, data):
        try:
            instance = RoadHazard(**data)
            instance.clean()
        except ValidationError as e:
            error_message = str(e)
            if isinstance(e.messages, list) and len(e.messages) > 0:
                error_message = e.messages[0]
            raise serializers.ValidationError({'error': error_message})
        return data

    class Meta:
        model = RoadHazard
        fields = '__all__'  
