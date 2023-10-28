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
import logging
logger = logging.getLogger('django')

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm

class UploadView(generic.FormView):
    def get(self, request):
        # フォームのインスタンスを作成してテンプレートをレンダリング
        form = UploadForm()
        return render(request, 'upload_form.html', {'testform': form})

    def post(self, request):
        # POSTリクエストを処理
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # フォームが有効な場合、ファイルを保存(現在未使用)
            # form.save()
            # ファイル情報をDB(sqlite)に保存
            for file in request.FILES.getlist('document'):
                file_data_object = UploadedFile(file=file,user_id=1) #user_idは仮で1とする
                file_data_object.save()
            return HttpResponse('ファイルがアップロードされました。')
        else:
            # フォームが無効な場合、エラーを表示
            del file_data_object
            # return render(request, 'upload_form.html', {'form': form, 'upload_err_msg':'アップロードに失敗しました'})
            return HttpResponse('ファイルがアップロードに失敗しました。フォーム画面に戻ってやり直してください。')

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

class OnlyYouMixin(UserPassesTestMixin):
    """自分しかアクセスできないようにするMixin(My Pageのため)"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk']

class MyPage(OnlyYouMixin, generic.DetailView):
    model = get_user_model()
    template_name = 'my_page.html'