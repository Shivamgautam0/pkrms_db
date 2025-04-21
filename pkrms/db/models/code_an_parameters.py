from django.db import models
from django.core.exceptions import ValidationError

class CODE_AN_Parameters(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    cumesa1 = models.CharField(max_length=255, null=True, blank=True, db_column='cumesa1')
    cumesa2 = models.CharField(max_length=255, null=True, blank=True, db_column='cumesa2')
    profilename = models.CharField(max_length=100, null=True, blank=True, db_column='profilename')
    irif = models.CharField(max_length=255, null=True, blank=True, db_column='irif')
    iri_wf = models.CharField(max_length=255, null=True, blank=True, db_column='iri_wf')
    surfaceloss_wf = models.CharField(max_length=255, null=True, blank=True, db_column='surfaceloss_wf')
    bleeding_wf = models.FloatField(max_length=255, null=True, blank=True, db_column='bleeding_wf')
    ravelling_wf = models.FloatField(max_length=255, null=True, blank=True, db_column='ravelling_wf')
    desintegration_wf = models.CharField(max_length=255, null=True, blank=True, db_column='desintegration_wf')
    crackdep_wf = models.CharField(max_length=255, null=True, blank=True, db_column='crackdep_wf')
    patching_wf = models.CharField(max_length=255, null=True, blank=True, db_column='patching_wf')
    othcrack_wf = models.FloatField(max_length=255, null=True, blank=True, db_column='othcrack_wf')
    pothole_wf = models.FloatField(max_length=255, null=True, blank=True, db_column='pothole_wf')
    rutting_wf = models.FloatField(max_length=255, null=True, blank=True, db_column='rutting_wf')
    edgedamage_wf = models.CharField(max_length=255, null=True, blank=True, db_column='edgedamage_wf')
    bleeding_wf_noiri = models.FloatField(max_length=255, null=True, blank=True, db_column='bleeding_wf_noiri')
    ravelling_wf_noiri = models.FloatField(max_length=255, null=True, blank=True, db_column='ravelling_wf_noiri')
    desintegration_wf_noiri = models.CharField(max_length=255, null=True, blank=True, db_column='desintegration_wf_noiri')
    crackdep_wf_noiri = models.CharField(max_length=255, null=True, blank=True, db_column='crackdep_wf_noiri')
    patching_wf_noiri = models.CharField(max_length=255, null=True, blank=True, db_column='patching_wf_noiri')
    othcrack_wf_noiri = models.CharField(max_length=255, null=True, blank=True, db_column='othcrack_wf_noiri')
    pothole_wf_noiri = models.FloatField(max_length=255, null=True, blank=True, db_column='pothole_wf_noiri')
    rutting_wf_noiri = models.CharField(max_length=255, null=True, blank=True, db_column='rutting_wf_noiri')
    edgedamage_wf_noiri = models.CharField(max_length=255, null=True, blank=True, db_column='edgedamage_wf_noiri')
    crossfall_wf = models.FloatField(max_length=255, null=True, blank=True, db_column='crossfall_wf')
    depression_wf = models.FloatField(max_length=255, null=True, blank=True, db_column='depression_wf')
    erosion_wf = models.FloatField(max_length=255, null=True, blank=True, db_column='erosion_wf')
    waviness_wf = models.CharField(max_length=255, null=True, blank=True, db_column='waviness_wf')
    gravelthickness_wf = models.CharField(max_length=255, null=True, blank=True, db_column='gravelthickness_wf')
    tti_prog_a1 = models.FloatField(max_length=255, null=True, blank=True, db_column='tti_prog_a1')
    tti_prog_a2 = models.FloatField(max_length=255, null=True, blank=True, db_column='tti_prog_a2')
    tti_prog_a3 = models.FloatField(max_length=255, null=True, blank=True, db_column='tti_prog_a3')
    tti_per = models.CharField(max_length=255, null=True, blank=True, db_column='tti_per')
    tti_reh = models.CharField(max_length=255, null=True, blank=True, db_column='tti_reh')
    tti_max = models.CharField(max_length=255, null=True, blank=True, db_column='tti_max')
    tpi_a0 = models.CharField(max_length=255, null=True, blank=True, db_column='tpi_a0')
    tpi_a1 = models.FloatField(max_length=255, null=True, blank=True, db_column='tpi_a1')
    tti_trigger1 = models.CharField(max_length=255, null=True, blank=True, db_column='tti_trigger1')
    tti_trigger2 = models.CharField(max_length=255, null=True, blank=True, db_column='tti_trigger2')
    tti_trigger3 = models.CharField(max_length=255, null=True, blank=True, db_column='tti_trigger3')
    tti_reset_per = models.CharField(max_length=255, null=True, blank=True, db_column='tti_reset_per')
    tti_reset_reh = models.CharField(max_length=255, null=True, blank=True, db_column='tti_reset_reh')

    def clean(self):
        errors = {}
        if not self.cumesa1:
            errors['cumesa1'] = 'This field is required.'
        if not self.cumesa2:
            errors['cumesa2'] = 'This field is required.'
            
        if errors:
            raise ValidationError(errors)
    
    
    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e
    def __str__(self):
        return f"{self.profilename}"
    
    class Meta:
        db_table = 'code_an_parameters'
        verbose_name = 'Code An Parameters'
        verbose_name_plural = 'Code An Parameters'
