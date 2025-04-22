from django.db import models
from django.core.exceptions import ValidationError
from .link import Link

class BridgeInventory(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    year = models.CharField(max_length=255, db_column='year')
    admin_code = models.CharField(max_length=255, db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo',to_field='link_no')
    bridge_number = models.CharField(max_length=100, db_column='bridgeNumber')
    chainage = models.CharField(max_length=255, db_column='chainage')
    drp_from = models.CharField(max_length=255, null=True, blank=True, db_column='drpFrom')
    offset_from = models.CharField(max_length=255, null=True, blank=True, db_column='offsetFrom')
    bridge_name = models.CharField(max_length=255, db_column='bridgeName')
    bridge_length = models.CharField(max_length=255, db_column='bridgeLength')
    bridge_type = models.CharField(max_length=100, db_column='bridgeType')
    number_spans = models.CharField(max_length=255, null=True, blank=True, db_column='numberSpans')
    road_width = models.CharField(max_length=255, null=True, blank=True, db_column='roadWidth')
    footpath_width_l = models.CharField(max_length=255, null=True, blank=True, db_column='footpathWidthL')
    footpath_width_r = models.CharField(max_length=255, null=True, blank=True, db_column='footpathWidthR')
    crossing = models.CharField(max_length=255, null=True, blank=True, db_column='crossing')
    year_construction = models.CharField(max_length=255, null=True, blank=True, db_column='yearConstruction')
    bridge_north_deg = models.CharField(max_length=255, null=True, blank=True, db_column='bridgeNorthDeg')
    bridge_north_min = models.CharField(max_length=255, null=True, blank=True, db_column='bridgeNorthMin')
    bridge_north_sec = models.CharField(max_length=255, null=True, blank=True, db_column='bridgeNorthSec')
    bridge_east_deg = models.CharField(max_length=255, null=True, blank=True, db_column='bridgeEastDeg')
    bridge_east_min = models.CharField(max_length=255, null=True, blank=True, db_column='bridgeEastMin')
    bridge_east_sec = models.CharField(max_length=255, null=True, blank=True, db_column='bridgeEastSec')
    handrails = models.CharField(max_length=255, null=True, blank=True, db_column='handrails')
    cond_handrails = models.CharField(max_length=255, null=True, blank=True, db_column='condHandrails')
    guardrail = models.CharField(max_length=255, null=True, blank=True, db_column='guardrail')
    cond_guardrails = models.CharField(max_length=255, null=True, blank=True, db_column='condGuardrails')
    roadsurface = models.CharField(max_length=255, null=True, blank=True, db_column='roadsurface')
    cond_roadsurface = models.CharField(max_length=255, null=True, blank=True, db_column='condRoadsurface')
    deck = models.CharField(max_length=255, null=True, blank=True, db_column='deck')
    cond_deck = models.CharField(max_length=255, null=True, blank=True, db_column='condDeck')
    deckjoints = models.CharField(max_length=255, null=True, blank=True, db_column='deckJoints')
    cond_deckjoints = models.CharField(max_length=255, null=True, blank=True, db_column='condDeckJoints')
    beam = models.CharField(max_length=255, null=True, blank=True, db_column='beam')
    cond_beam = models.CharField(max_length=255, null=True, blank=True, db_column='condBeam')
    wingwalls = models.CharField(max_length=255, null=True, blank=True, db_column='wingWalls')
    cond_wingwalls = models.CharField(max_length=255, null=True, blank=True, db_column='condWingWalls')
    abutment = models.CharField(max_length=255, null=True, blank=True, db_column='abutment')
    cond_abutment = models.CharField(max_length=255, null=True, blank=True, db_column='condAbutment')
    piers = models.CharField(max_length=255, null=True, blank=True, db_column='piers')
    cond_piers = models.CharField(max_length=255, null=True, blank=True, db_column='condPiers')
    bearings = models.CharField(max_length=255, null=True, blank=True, db_column='bearings')
    cond_bearings = models.CharField(max_length=255, null=True, blank=True, db_column='condBearings')
    foundations = models.CharField(max_length=255, null=True, blank=True, db_column='foundations')
    cond_foundations = models.CharField(max_length=255, null=True, blank=True, db_column='condFoundations')
    stormwaterdrain = models.CharField(max_length=255, null=True, blank=True, db_column='stormWaterDrain')
    cond_stormwaterdrain = models.CharField(max_length=255, null=True, blank=True, db_column='condStormWaterDrain')
    obstruction = models.CharField(max_length=255, null=True, blank=True, db_column='obstruction')
    cond_obstruction = models.CharField(max_length=255, null=True, blank=True, db_column='condObstruction')
    scouring = models.CharField(max_length=255, null=True, blank=True, db_column='scouring')
    cond_scouring = models.CharField(max_length=255, null=True, blank=True, db_column='condScouring')
    analysisbaseyear = models.CharField(max_length=255, null=True, blank=True, db_column='analysisBaseYear')
    surveyby = models.CharField(max_length=255, null=True, blank=True, db_column='surveyBy')


    def clean(self):
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'  # More specific message needed
        if not self.year:
            errors['year'] = 'This field is required.'
        if not self.link_no:
            errors['link_no'] = 'This field is required.'
        if not self.bridge_number:
            errors['bridge_number'] = 'This field is required.'
        if not self.chainage:
            errors['chainage'] = 'This field is required.'
        if not self.bridge_length:
            errors['bridge_length'] = 'This field is required.'
        if not self.bridge_type:
            errors['bridge_type'] = 'This field is required.'
        if errors:
            raise ValidationError(errors)
            
        # Check if this is not the first record for this link
        if self.pk:  # If this is an existing record
            # Get the previous record for this link
            previous_record = BridgeInventory.objects.filter(
                link_no=self.link_no,
                chainage__lt=self.chainage
            ).order_by('-chainage').first()
            
            if previous_record and float(self.chainage) < float(previous_record.chainage):
                raise ValidationError(f"Starting chainage ({self.chainage}) must not be less than ending chainage ({previous_record.chainage}) of previous record")

    def save(self, *args, **kwargs):
        # Skip chainage validation for the first record of a link
        if not self.pk:  # If this is a new record
            existing_records = BridgeInventory.objects.filter(link_no=self.link_no).exists()
            if not existing_records:  # If this is the first record for this link
                self.full_clean(exclude=['chainage'])  # Skip chainage validation
            else:
                self.full_clean()
        else:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bridge_number}"
    
    class Meta:
        db_table = 'bridgeinventory'
        verbose_name = 'Bridge Inventory'
        verbose_name_plural = 'Bridge Inventories'
