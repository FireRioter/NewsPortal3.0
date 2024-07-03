from django.views.generic import ListView, DetailView
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Comment, Category
from django.shortcuts import render


class PostList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'posts.html'
    context_object_name = 'posts'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_news'] = "Свежие новости завтра!"
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):  # модернизация контекста для отображения комментариев


# на отдельной странице поста
        context = super().get_context_data(**kwargs)
        context['comm'] = Comment.objects.filter(post_id=self.kwargs['pk'])
        form = PostForm(initial={'title': self.object.title,
                                 'content': self.object.content,
                                 'create_time': self.object.create_time,
                                 'author': self.object.author,
                                 'postType': self.object.postType})
        form.fields['author'].disabled = True
        form.fields['title'].disabled = True
        form.fields['content'].disabled = True
        form.fields['create_time'].disabled = True
        form.fields['postType'].disabled = True
        context['form'] = form
        context['id'] = self.object.pk  # переменная контекста, передающая id поста
        return context

class PostFilterView(ListView): # класс для отображения фильтра поста на отдельной HTML странице 'search.html'
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'post'
    paginate_by =3

    def get_queryset(self):
        queryset=super().get_queryset()
        self.filter = PostFilter(self.request.GET,queryset)
        return self.filter.qs

    def get_context_data(self,  **kwargs): #добавление в контекст фильтра
        context=super().get_context_data(**kwargs)
        context['filter']=self.filter
        return context

def create_post(request): # функция для создания и добавления новой публикации
    form=PostForm()
    form.fields['create_time'].disabled = True
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(**form.cleaned_data)
            return render(request, 'flatpages/messages.html', {'state':'Новая публикация добавлена успешно!'})
    return render(request, 'flatpages/edit.html', {'form':form, 'button':'Опубликовать'})

def edit_post(request, pk): # функция для редактирования названия и содержания поста
    post = Post.objects.get(pk=pk)
    form=PostForm(initial={'create_time':post.date_in,
                           'author':post.author,
                           'posts_type':post.posts_type,
                           'title': post.title,
                           'text': post.text
                           })
    form.fields['postType'].disabled = True
    form.fields['author'].disabled = True
    form.fields['create_time'].disabled = True
    if request.method=='POST':
        form=PostForm(request.POST, post)
        form.fields['posts_type'].required = False
        form.fields['author'].required = False
        form.fields['create_time'].required = False
        try:
            if form.is_valid():
                Post.objects.filter(pk=pk).update(**{'author':post.author,
                                                     'postType':post.postType,
                                                     'create_time':post.create_time,
                                                     'title':form.cleaned_data['title'],
                                                     'content':form.cleaned_data['content']})
                return render(request, 'flatpages/messages.html', {'state': 'Изменения успешно сохранены.'})
        except TypeError:
            return render(request, 'flatpages/messages.html', {'state':'Возникла ошибка! Возможно причина в превышении лимита названия поста, попавшего в БД не через форму'})
    return render(request, 'flatpages/edit.html', {'form':form, 'button':'Сохранить изменения'})

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method=='POST':
        post.delete()
        return render(request, 'flatpages/messages.html', {'state': 'Пост успешно удален'})
    return render(request, 'flatpages/del_post.html',{'post':post})


# Неиспользуемые классы ниже
class CommListView(ListView):  # класс для отобрпажения
    model = Comment
    template_name = 'flatpages/comm.html'
    context_object_name = 'cmts'
