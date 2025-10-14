from django.views.generic import ListView, DetailView
from base.models import Item, Category, Tag
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404


class IndexListView(ListView):
    model = Item
    template_name = 'pages/index.html'
    queryset = Item.objects.filter(is_published=True)
    paginate_by = 10 #１ページに表示するアイテムの数


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
    fields = '__all__'
    
class ItemUpdateView(UpdateView):
    model = Item
    fields = '__all__'
    #template_name_suffix = '_update_form'
    template_name = 'pages/update.html'
    

#class BookmarkView(request. pk):
class BookmarkView(ListView):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        request.user.bookmark.add(item)
        return redirect('list')
