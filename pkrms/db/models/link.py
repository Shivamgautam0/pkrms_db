from django.db import models
from django.core.exceptions import ValidationError

class Link(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, null=True, blank=True,db_column='adminCode')
    link_no = models.CharField(max_length=255, null=False, blank=False, unique=True, db_column='linkNo')
    link_code = models.CharField(max_length=255, null=False, blank=False, db_column='linkCode')
    link_name = models.CharField(max_length=255, null=False, blank=False, db_column='linkName')
    status = models.CharField(max_length=255, null=True, blank=True, db_column='status')
    function = models.CharField(max_length=255, null=True, blank=True, db_column='function')
    class_field = models.CharField(max_length=255,null=True, blank=True, db_column='class')
    link_length_official = models.CharField(max_length=255, null=True, blank=True, db_column='linkLengthOfficial')
    link_length_actual = models.CharField(max_length=255, null=False, blank=False, db_column='linkLengthActual')
    wti = models.CharField(max_length=255, null=True, blank=True, db_column='wti')
    mca2 = models.CharField(max_length=255, null=True, blank=True, db_column='mca2')
    mca3 = models.CharField(max_length=255, null=True, blank=True, db_column='mca3')
    mca4 = models.CharField(max_length=255, null=True, blank=True, db_column='mca4')
    mca5 = models.CharField(max_length=255, null=True, blank=True, db_column='mca5')
    project_number = models.CharField(max_length=255, null=True, blank=True, db_column='projectNumber')
    cumesa = models.CharField(max_length=255, null=True, blank=True, db_column='cumesa')
    esa0 = models.CharField(max_length=255, null=True, blank=True, db_column='esa0')
    aadt = models.CharField(max_length=255, null=True, blank=True, db_column='aadt')
    accessstatus = models.CharField(max_length=255, null=True, blank=True, db_column='accessStatus')

    # @classmethod
    # def create_with_admin_code(cls, province_code, kabupaten_code, **kwargs):
    #     admin_code = int(f"{province_code}{kabupaten_code:02d}")
    #     return cls(Province_Code=province_code, Kabupaten_Code=kabupaten_code, **kwargs)

    def clean(self):
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        
        if not self.link_no:
            errors['link_no'] = 'This field is required.'
        if not self.link_name:
            errors['link_name'] = 'This field is required.'
        if not self.link_length_actual:
            errors['link_length_actual'] = 'This field is required.'
        if not self.link_code:
            errors['link_code'] = 'This field is required.'
            
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e

    def __str__(self):
        return f"{self.link_no}"
    
    class Meta:
        db_table = 'link'
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
