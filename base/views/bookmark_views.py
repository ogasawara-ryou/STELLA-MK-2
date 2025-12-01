from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class BookmarkListView(LoginRequiredMixin,ListView): #
    model = Item
    template_name = 'pages/bookmark.html'

    def get_queryset(self): #モデルをフィルタリング。全部出さないようにする。ログインユーザーのidを抽出・ブックマークテーブルからユーザーIDに一致するアイテムを拾ってくる・拾ったアイテムIDと一致するIDリストをフィルタリング
        bookmark = self.request.session.get('bookmark', None) #フェイバリットクラスビューに名称変更,名称cart→bookmark
        if bookmark is None or len(bookmark) == 0:
            return redirect('/')
        self.queryset = []
        self.total = 0
        for item_pk, quantity in bookmark['items'].items():
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            self.queryset.append(obj)
            self.total += obj.subtotal
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        bookmark['total'] = self.total
        bookmark['tax_included_total'] = self.tax_included_total
        self.request.session['bookmark'] = bookmark
        return super().get_queryset()

class BookmarkAddView(View): #別にデリートのビューも必要
    def post(self, request, pk):
        print("ブックマーク"+pk)
        item = get_object_or_404(Item, pk=pk)
        
        # Bookmarkインスタンスを作成し、それをuser_bookmarkに追加
        bookmark = Bookmark(user=request.user, item=item)
        bookmark.save()  # データベースに保存します
        
        #request.user.user_bookmark.add(bookmark)
        return redirect('list')

"""    
class BookmarkDeleteView(View):
    def post(self, request, pk):
        # 指定されたpkでブックマークを取得
        bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
        
        # ブックマークを削除
        bookmark.delete()

        # リダイレクト先を指定
        return redirect('list')
    
"""
    
class BookmarkDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('list')