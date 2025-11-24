from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class BookmarkListView( ListView): #LoginRequiredMixin,
    model = Item
    template_name = 'pages/bookmark.html'

    def get_queryset(self): #モデルをフィルタリング。全部出さないようにする。ログインユーザーのidを抽出・ブックマークテーブルからユーザーIDに一致するアイテムを拾ってくる・拾ったアイテムIDと一致するIDリストをフィルタリング
        cart = self.request.session.get('cart', None) #フェイバリットクラスビューに名称変更,名称cart→bookmark
        if cart is None or len(cart) == 0:
            return redirect('/')
        self.queryset = []
        self.total = 0
        for item_pk, quantity in cart['items'].items():
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            self.queryset.append(obj)
            self.total += obj.subtotal
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
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





