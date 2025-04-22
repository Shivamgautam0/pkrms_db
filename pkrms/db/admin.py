from django.contrib import admin

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


admin.site.register(BridgeInventory)
admin.site.register(CODE_AN_Parameters)
admin.site.register(CODE_AN_UnitCostsPER)
admin.site.register(CODE_AN_UnitCostsPERUnpaved)
admin.site.register(CODE_AN_UnitCostsREH)
admin.site.register(CODE_AN_UnitCostsRIGID)
admin.site.register(CODE_AN_UnitCostsRM)
admin.site.register(CODE_AN_UnitCostsUPGUnpaved)
admin.site.register(CODE_AN_UnitCostsWidening)
admin.site.register(CODE_AN_WidthStandards)
admin.site.register(CulvertCondition)
admin.site.register(CulvertInventory)
admin.site.register(Link)
admin.site.register(RetainingWallCondition)
admin.site.register(RetainingWallInventory)
admin.site.register(RoadCondition)
admin.site.register(RoadInventory)
admin.site.register(TrafficVolume)
admin.site.register(FormData)
admin.site.register(TrafficWeightingFactors)
admin.site.register(DRP)
admin.site.register(Alignment)
admin.site.register(RoadHazard)
    
