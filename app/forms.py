from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
import os, random, string
from .multifileinput import MultiFileInput 

class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル',max_length=30)
    message = forms.CharField(label='メッセージ',widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力して下さい。'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'


class UploadForm(forms.Form):
    """アップロード用フォームの定義"""
    document = forms.FileField(label="画像アップロード",
        widget=MultiFileInput(), 
        )

    def save(self):
        upload_files = self.files.getlist('document')
        temp_dir = os.path.join(settings.MEDIA_ROOT, self.create_dir(10))   #一時フォルダの生成
        for image in upload_files:
            default_storage.save(os.path.join(temp_dir, image.name), image)   #一時フォルダに画像を保存
        return temp_dir
    
    def create_dir(self, n):
        """一時フォルダ名生成関数"""
        return 'image\\' + ''.join(random.choices(string.ascii_letters + string.digits, k=n))

