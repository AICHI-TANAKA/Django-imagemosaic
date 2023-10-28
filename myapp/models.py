from django.db import models
from .common_def.common import create_dir    

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='mosbefore/'+create_dir(10)+"/")   #一時フォルダの生成
    user_id = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)