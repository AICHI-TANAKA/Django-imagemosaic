from django.db import models
from .common_def.common import create_dir    

# Create your models here.
class UploadedFile(models.Model):
    """アップロードファイルの情報を格納するテーブル"""
    file = models.FileField(upload_to='mosbefore/'+create_dir(10)+"/")   #djangoの仕様上、ファイルパスとして絶対パスを格納できない
    file_mosafter = models.FileField(null=True)
    user_id = models.IntegerField(null=False)
    image_id = models.IntegerField(null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.image_id:
            # user_idごとに最大のimage_idを取得
            max_image_id = UploadedFile.objects.filter(user_id=self.user_id).aggregate(models.Max('image_id'))['image_id__max'] or 0
            self.image_id = max_image_id + 1
        super(UploadedFile, self).save(*args, **kwargs)
    
    class Meta:
        """モデルのメタ情報。現時点では複合ユニークキーのみ設定"""
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "image_id"],
                name="image_unique"
            ),
        ]