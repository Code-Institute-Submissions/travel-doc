from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment, Category
from .forms import CommentForm, PostForm
#from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse_lazy

from django.contrib.auth.mixins import(UserPassesTestMixin, LoginRequiredMixin)


# Create your views here.

"""class AddCategoryView(CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = ('name',)"""

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    #fields = ('title', 'category','slug', 'author', 'featured_image','content') 
    #summernote_fields = ('content',)
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Your post has been submitted and is awaiting approval.')
        #return super().form_valid(form)
        form.instance.author = self.request.user
        response = super().form_valid(form)

        if self.object.status == 0:
            messages.info(
                self.request, 'Your post has been submitted and is awaiting approval.')
        
        return response

    

    #def form_invalid(self, form):
        #print("Form is invalid")
        #print(form.errors)

        #messages.error(self.request, "There was an error with your submission. Please check all the fields again.")

        #return self.render_to_response(self.get_context_data(form=form))

class PostList(generic.ListView):
    """
    Returns all published posts in :model:`blog.Post`
    and displays them in a page of six posts.
    **Context**

    ``queryset``
        All published instances of :model:`blog.Post`
    ``paginate_by``
        Number of posts per page.

    **Template:**

    :template:`blog/index.html`
    """
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6
    cat = Category.objects.all()

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostList, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class post_detail(View):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """
    def get (self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.all().order_by("-created_on")
        comment_count = post.comments.filter(approved=True).count()
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        return render(
            request,
            "blog/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )


    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        comment_count = post.comments.filter(approved=True).count()
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blog/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_count": comment_count,
                "comment_form": comment_form,
                "liked": liked
            },
        )


def comment_edit(request, slug, comment_id):
    """View to edit comments"""
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment updated and awaiting approval!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug])
    )


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug])
    )


class PostLike(View):
    """
    Toggles like status on submission of like form/button on posts.
    Also sends notification to author
    Login required
    """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            messages.add_message(request, messages.SUCCESS, 'Thanks for liking the post!')

        return HttpResponseRedirect(reverse('post_detail', args=[slug])
        )


# Category list view
class CatListView(ListView):
    """
     Returns all published posts in :model:`blog.Category`
    and displays them on a page.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``category``
        Group of published posts in :model:`blog.Category`
    displayed on a page.
    """
    template_name = 'blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs[
                'category']).filter(status=1)
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='other')
    context = {
        "category_list": category_list,
    }
    return context