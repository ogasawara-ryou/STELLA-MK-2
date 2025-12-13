from django.views.generic import ListView, DetailView
from base.models import Item, Category, Tag, Bookmark
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from base.forms import ItemForm, ImageForm, FileForm



class IndexListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/index.html'
    paginate_by = 10 #１ページに表示するアイテムの数
    # ordering = ['-created_at']  # 降順の例　登校日が新しいのが頭
    # ordering = ['created_at']  # 昇順の例
    
    def get_queryset(self):
        queryset=super().get_queryset()
        queryset = queryset.filter(is_published=True)
        order = self.request.GET.get('order', 'created_at')  # デフォルトは作成日時
        if order == 'updated_at':
            queryset = queryset.order_by('-updated_at')  # 更新日時でソート
        else:
            queryset = queryset.order_by('created_at')  # 作成日時でソート
        return queryset
    """
        name = self.request.GET.get('name')
        if name:
            queryset=queryset.filter(name__icontains=name)
        return queryset
    """
    
    def item_list(request):
        order = request.GET.get('order', 'created_at')  # デフォルトは作成日時
        if order == 'updated_at':
            items = Item.objects.filter(is_published=True).order_by('-updated_at')  # 更新日時でソート
        else:
            items = Item.objects.filter(is_published=True).order_by('created_at')  # 作成日時でソート
        return render(request, 'your_template.html', {'items': items})
        

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
    #form_class = ItemForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageForm()
        context['file_form'] = FileForm()
        return context
    
    def form_valid(self, form):
        item = form.save(commit=False)  # まずは保存せずに取得
        item.latest_author = self.request.user  # 現在のユーザーを最新の作者として設定
        item.save()  # 保存
        
         # 画像とファイルの保存処理
        image_form = ImageForm(self.request.POST, self.request.FILES)
        file_form = FileForm(self.request.POST, self.request.FILES)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.item = item
            image.save()
        if file_form.is_valid():
            file = file_form.save(commit=False)
            file.item = item
            file.save()
                
        return super().form_valid(form)  # スーパークラスのメソッドを呼び出す
    
    
class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'pages/update.html'
    form_class = ItemForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageForm()
        context['file_form'] = FileForm()
        return context
    
    def form_valid(self, form):
        item = form.save(commit=False)  # まずは保存せずに取得
        item.latest_author = self.request.user  # 現在のユーザーを最新の作者として設定
        item.save()  # 保存
        
        # 画像とファイルの保存処理
        image_form = ImageForm(self.request.POST, self.request.FILES)
        file_form = FileForm(self.request.POST, self.request.FILES)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.item = item
            image.save()
        if file_form.is_valid():
            file = file_form.save(commit=False)
            file.item = item
            file.save()
        
        return super().form_valid(form)  # スーパークラスのメソッドを呼び出す





