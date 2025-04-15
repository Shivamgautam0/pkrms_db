from django.db import models
from django.forms import ValidationError
from .link import Link

class RoadCondition(models.Model):
    id = models.AutoField(primary_key=True,db_column='id')
    year = models.IntegerField(db_column='year', null=False, blank=False)
    admin_code = models.IntegerField(db_column='adminCode', null=False, blank=False)
    link_no = models.CharField(max_length=50,db_column='linkNo')
    chainagefrom = models.FloatField(db_column='chainageFrom', null=False, blank=False)
    chainageto = models.FloatField(db_column='chainageTo', null=False, blank=False)
    roughness = models.FloatField(db_column='roughness', null=True, blank=True)
    bleeding_area = models.FloatField(db_column='bleedingArea', null=True, blank=True)
    ravelling_area = models.FloatField(db_column='ravellingArea', null=True, blank=True)
    desintegration_area = models.FloatField(db_column='desintegrationArea', null=True, blank=True)
    crackdep_area = models.FloatField(db_column='crackdepArea', null=True, blank=True)
    patching_area = models.FloatField(db_column='patchingArea', null=True, blank=True)
    othcrack_area = models.FloatField(db_column='othcrackArea', null=True, blank=True)
    pothole_area = models.FloatField(db_column='potholeArea', null=True, blank=True)
    rutting_area = models.FloatField(db_column='ruttingArea', null=True, blank=True)
    edgedamage_area = models.FloatField(db_column='edgeDamageArea', null=True, blank=True)
    crossfall_area = models.FloatField(db_column='crossfallArea', null=True, blank=True)
    depressions_area = models.FloatField(db_column='depressionsArea', null=True, blank=True)
    erosion_area = models.FloatField(db_column='erosionArea', null=True, blank=True)
    waviness_area = models.FloatField(db_column='wavinessArea', null=True, blank=True)
    gravelthickness_area = models.FloatField(db_column='gravelThicknessArea', null=True, blank=True)
    concrete_cracking_area = models.FloatField(db_column='concreteCrackingArea', null=True, blank=True)
    concrete_spalling_area = models.FloatField(db_column='concreteSpallingArea', null=True, blank=True)
    concrete_structuralcracking_area = models.FloatField(db_column='concreteStructuralCrackingArea', null=True, blank=True)
    concrete_cornerbreakno = models.IntegerField(db_column='concreteCornerBreakNo', null=True, blank=True)
    concrete_pumpingno = models.IntegerField(db_column='concretePumpingNo', null=True, blank=True)
    concrete_blowouts_area = models.FloatField(db_column='concreteBlowoutsArea', null=True, blank=True)
    crack_width = models.FloatField(db_column='crackWidth', null=True, blank=True)
    pothole_count = models.IntegerField(db_column='potholeCount', null=True, blank=True)
    rutting_depth = models.FloatField(db_column='ruttingDepth', null=True, blank=True)
    shoulder_l = models.FloatField(db_column='shoulderL', null=True, blank=True)
    shoulder_r = models.FloatField(db_column='shoulderR', null=True, blank=True)
    drain_l = models.FloatField(db_column='drainL', null=True, blank=True)
    drain_r = models.FloatField(db_column='drainR', null=True, blank=True)
    slope_l = models.FloatField(db_column='slopeL', null=True, blank=True)
    slope_r = models.FloatField(db_column='slopeR', null=True, blank=True)
    footpath_l = models.FloatField(db_column='footPathL', null=True, blank=True)
    footpath_r = models.FloatField(db_column='footPathR', null=True, blank=True)
    sign_l = models.FloatField(db_column='signL', null=True, blank=True)
    sign_r = models.FloatField(db_column='signR', null=True, blank=True)
    guidepost_l = models.FloatField(db_column='guidePostL', null=True, blank=True)
    guidepost_r = models.FloatField(db_column='guidePostR', null=True, blank=True)
    barrier_l = models.FloatField(db_column='barrierL', null=True, blank=True)
    barrier_r = models.FloatField(db_column='barrierR', null=True, blank=True)
    roadmarking_l = models.FloatField(db_column='roadMarkingL', null=True, blank=True)
    roadmarking_r = models.FloatField(db_column='roadMarkingR', null=True, blank=True)
    iri = models.FloatField(db_column='iri', null=True, blank=True)
    rci = models.FloatField(db_column='rci', null=True, blank=True)
    analysisbaseyear = models.BooleanField(db_column='analysisBaseYear', null=True, blank=True)
    segmenttti = models.FloatField(db_column='segmentTTI', null=True, blank=True)
    surveyby = models.CharField(max_length=255, db_column='surveyBy', null=True, blank=True)
    paved = models.BooleanField(db_column='paved', null=True, blank=True)
    pavement = models.CharField(max_length=255, db_column='pavement', null=True, blank=True)
    checkdata = models.BooleanField(db_column='checkData', null=True, blank=True)
    composition = models.CharField(max_length=255, db_column='composition', null=True, blank=True)
    cracktype = models.CharField(max_length=255, db_column='crackType', null=True, blank=True)
    potholesize = models.CharField(max_length=255, db_column='potholeSize', null=True, blank=True)
    shouldcond_l = models.CharField(max_length=255, db_column='shouldCondL', null=True, blank=True)
    shouldcond_r = models.CharField(max_length=255, db_column='shouldCondR', null=True, blank=True)
    crossfallshape = models.CharField(max_length=255, db_column='crossfallShape', null=True, blank=True)
    gravelsize = models.CharField(max_length=255, db_column='gravelSize', null=True, blank=True)
    gravelthickness = models.FloatField(db_column='gravelThickness', null=True, blank=True)
    distribution = models.CharField(max_length=255, db_column='distribution', null=True, blank=True)
    edgedamage_area_r = models.FloatField(db_column='edgeDamageAreaR', null=True, blank=True)
    surveyby2 = models.CharField(max_length=255, db_column='surveyBy2', null=True, blank=True)
    surveydate = models.CharField(max_length=50,db_column='surveyDate', null=False, blank=False)
    sectionstatus = models.IntegerField(db_column='sectionStatus', null=True, blank=True)

    # @classmethod
    # def create_with_admin_code(cls, province_code, kabupaten_code, **kwargs):
    #     return cls(Province_Code=province_code, Kabupaten_Code=kabupaten_code, **kwargs)

    def clean(self):
        required_fields = [
            self.admin_code,
            self.link_no,
            self.chainagefrom,
            self.chainageto,
            self.surveydate
        ]   
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")
        
        # Validate that chainagefrom is less than chainageto
        if self.chainagefrom >= self.chainageto:
            raise ValidationError("ChainageFrom must be less than ChainageTo")

    def save(self, *args, **kwargs):
        # Skip chainage validation for the first record
        if not self.pk:  # If this is a new record
            self.full_clean(exclude=['chainagefrom'])  # Exclude chainage_from from validation
        else:
            self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'road_condition'
        verbose_name = 'Road Condition'
        verbose_name_plural = 'Road Conditions'

    def __str__(self):
        return f"{self.link_no}"
