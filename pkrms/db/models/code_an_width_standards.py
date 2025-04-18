from django.db import models

class CODE_AN_WidthStandards(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    status = models.CharField(max_length=100, null=True, blank=True,db_column='status')
    aadt1 = models.CharField(max_length=255, null=True, blank=True,db_column='aadt1')
    aadt2 = models.CharField(max_length=255, null=True, blank=True,db_column='aadt2')
    pave_width = models.CharField(max_length=255, null=True, blank=True,db_column='paveWidth')
    row = models.CharField(max_length=255, null=True, blank=True,db_column='row')
    shldwidth = models.CharField(max_length=255, null=True, blank=True,db_column='shldWidth')
    minwidening = models.CharField(max_length=255, null=True, blank=True,db_column='minWidening')
    maxvcr = models.CharField(max_length=255, null=True, blank=True,db_column='maxVcr')

    def __str__(self):
        return f"{self.status}"
    
    class Meta:
        db_table = 'code_an_widthstandards'
        verbose_name = 'Code An Widthstandards'
        verbose_name_plural = 'Code An Widthstandardss'
