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
# from django.urls import reverse_lazy
import logging
logger = logging.getLogger('django')

class OnlyYouMixin(UserPassesTestMixin):
    """自分しかアクセスできないようにするMixin(My Pageのため)"""
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
    def get(self, request, pk):
        """GETリクエストを処理"""
        logger.info("user_id::::"+str(pk))
        # フォームのインスタンスを作成してテンプレートをレンダリング
        form = UploadForm()
        return render(request, 'upload_form.html', {'testform': form})

    def post(self, request):
        """POSTリクエストを処理"""
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # フォームが有効な場合、ファイルを保存(現在未使用)
            # form.save()
            # ファイル情報をDB(sqlite)に保存
            for file in request.FILES.getlist('document'):
                file_data_object = UploadedFile(file=file,user_id=1) #user_idは仮で1とする
                file_data_object.save()
            # return HttpResponse('ファイルがアップロードされました。')
            messages.success(request, 'ファイルが正常にアップロードされました')
            return redirect('/')

        else:
            # フォームが無効な場合、エラーを表示
            del file_data_object
            # return render(request, 'upload_form.html', {'form': form, 'upload_err_msg':'アップロードに失敗しました'})
            # return HttpResponse('ファイルがアップロードに失敗しました。フォーム画面に戻ってやり直してください。')
            messages.success(request, 'ファイルのアップロードに失敗しました。もう一度やり直してください。')
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
    model = get_user_model()
    template_name = 'my_page.html'