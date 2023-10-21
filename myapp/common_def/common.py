import os, random, string
from django.conf import settings

def create_dir(n):
    """一時フォルダ名生成関数"""
    # return os.path.join(settings.MEDIA_ROOT, str(random.choices(string.ascii_letters + string.digits, k=n)))
    return 'image\\' + ''.join(random.choices(string.ascii_letters + string.digits, k=n))

