from django.views.generic import ListView, DetailView
from base.models import Item, Category, Tag, Bookmark
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from base.forms import ItemForm



class IndexListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/index.html'
    paginate_by = 10 #１ページに表示するアイテムの数
    
    def get_queryset(self):
        queryset=super().get_queryset()
        queryset = queryset.filter(is_published=True)
        name = self.request.GET.get('name')
        if name:
            queryset=queryset.filter(name__icontains=name)
        return queryset
        
        

    """
    def item_search(request):
        query = request.GET.get('q')
        results = Item.objects.filter(name__icontains=query) if query else Item.objects.all()
        return render(request, 'search.html', {'items': results})
    """

class ItemDetailView(DetailView):
    model = Item
    template_name = 'pages/item.html'


class CategoryListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 2

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(
            is_published=True, category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Category #{self.category.name}"
        return context


class TagListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 2

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(is_published=True, tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Tag #{self.tag.name}"
        return context
    
    

class ItemCreateView(CreateView): #新規作成
    model = Item
    template_name = 'snippets/item_form.html'
    fields = ("name","description","category","tags","image")
    
    def form_valid(self, form):
        item = form.save(commit=False)  # まずは保存せずに取得
        item.latest_author = self.request.user  # 現在のユーザーを最新の作者として設定
        item.save()  # 保存
        return super().form_valid(form)  # スーパークラスのメソッドを呼び出す
    
    
class ItemUpdateView(UpdateView):
    model = Item
    #fields = ("name","description","category","tags","image")
    #instance=Item  # ← ここで元の内容を初期値としてセット
    #template_name_suffix = '_update_form'
    template_name = 'pages/update.html'
    form_class = ItemForm
    
    def form_valid(self, form):
        item = form.save(commit=False)  # まずは保存せずに取得
        item.latest_author = self.request.user  # 現在のユーザーを最新の作者として設定
        item.save()  # 保存
        return super().form_valid(form)  # スーパークラスのメソッドを呼び出す
    '''
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # デバッグ用に取得したアイテム名を出力
        #print(f"取得したアイテムの名前: {obj.name}")
        print(f"取得したアイテムのデータ: {obj.__dict__}")
        return obj
    '''

#class BookmarkView(request. pk):
class BookmarkView(ListView):
    def post(self, request, pk):
        print("ブックマーク"+pk)
        item = get_object_or_404(Item, pk=pk)
        
        # Bookmarkインスタンスを作成し、それをuser_bookmarkに追加
        bookmark = Bookmark(user=request.user, item=item)
        bookmark.save()  # データベースに保存します
        
        request.user.user_bookmark.add(bookmark)
        return redirect('list')




