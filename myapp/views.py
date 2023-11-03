from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm
from django.views import View
from django.http import HttpResponse
from .forms import UploadForm  # 自分のフォームのインポート
from .models import UploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.contrib import messages
from django.shortcuts import redirect
from .imagemosaic_def.facemosaic import imageMosaic
# from django.urls import reverse_lazy
import os
import re
import logging
logger = logging.getLogger('django')
from project.settings import MEDIA_ROOT

class OnlyYouMixin(UserPassesTestMixin):
    """自分しかアクセスできないようにするMixin"""
    raise_exception = True
    # requestとURL上のuser_idを比較
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk']

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm

class UploadView(OnlyYouMixin, generic.DetailView):
    """画像アップロードページ"""
    def get(self, request, pk):
        """GETリクエストを処理"""
        logger.info("user_id::::"+str(pk))
        # フォームのインスタンスを作成してテンプレートをレンダリング
        form = UploadForm()

        # 表示画像のパスを渡す
        file_entity = UploadedFile.objects.filter(user_id=pk, image_id=8)
        image_path = '/media/'+str(file_entity[0].file)
        return render(request, 'upload_form.html', {'testform': form, 'image1_path': image_path})

    def post(self, request, pk):
        """POSTリクエストを処理"""
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # フォームが有効な場合、ファイルを保存(現在未使用)
            # form.save()
            # ファイル情報をDB(sqlite)に保存
            for file in request.FILES.getlist('document'):
                file_data_object = UploadedFile(file=file,user_id=pk) 
                file_data_object.save()
            # return HttpResponse('ファイルがアップロードされました。')
            messages.success(request, 'ファイルが正常にアップロードされました')
            return redirect('/')
        else:
            # フォームが無効な場合、エラーを表示
            del file_data_object
            # return render(request, 'upload_form.html', {'form': form, 'upload_err_msg':'アップロードに失敗しました'})
            # return HttpResponse('ファイルがアップロードに失敗しました。フォーム画面に戻ってやり直してください。')
            messages.error(request, 'ファイルのアップロードに失敗しました。もう一度やり直してください。')
            return redirect('/upload')

class ImageMosaicView(generic.TemplateView):
    pass

class Login(LoginView):
    """ログインページ処理"""
    template_name = 'login.html'
    def get(self, request):
        logger.info('test')
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

class Logout(LogoutView):
    """ログアウトページ処理"""
    template_name = 'logout_done.html'

class MyPage(OnlyYouMixin, generic.DetailView):
    """ユーザー専用ページ"""
    model = get_user_model()
    template_name = 'my_page.html'

def imagemosaic(request):
    """リクエストを受け付け、画像のモザイク処理を実行"""
    # 加工前ファイル格納先パス取得
    file_entity = UploadedFile.objects.filter(user_id=request.POST.get("user_id"), image_id=request.POST.get("image_id"))
    # file_entity = UploadedFile.objects.filter(user_id=3, image_id=1)
    logger.info(file_entity[0].user_id)
    before_path = str(MEDIA_ROOT).replace('\\','/') +'/'+ str(file_entity[0].file)
    # 加工後ファイル格納先パス
    after_path = before_path.replace('before', 'after')

    # 一応ログ残す
    logger.info('after_path:::'+after_path)
    logger.info('before_path:::'+before_path)

    # after_pathのディレクトリを再帰的に作成
    after_path_splited = after_path.split('/')[:-1]
    after_path_makedir = "/".join(after_path_splited)
    logger.info("after_path_remake:::::"+after_path)
    os.makedirs(after_path_makedir, exist_ok=True)

    # モザイク処理実行
    imageMosaic(before_path, after_path)
    return redirect('/upload/'+request.POST.get("user_id"))