from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm
from django.views import View
from django.http import HttpResponse
from .forms import UploadForm  # 自分のフォームのインポート
from .models import UploadedFile
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
            # フォームが有効な場合、ファイルを保存
            form.save()
            return HttpResponse('ファイルがアップロードされました。')
        else:
            # フォームが無効な場合、エラーを表示
            return render(request, 'upload_form.html', {'form': form})