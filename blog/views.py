from msilib.schema import ListView
from django.shortcuts import render
from django.views import generic
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

class PostList(generic.ListView):

    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'

@login_required 
def post_detail(request, slug):

    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active = True)
    new_comment = None

    #Comment posted

    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():

            # Created comment without saving to the database
            new_comment = comment_form.save(commit=False)

            # Assign the current post to the comment

            new_comment.post = post

            # Save Comment to the database

            new_comment.save()

    else:
         comment_form = CommentForm()

    return render(request, template_name, {'post':post, 'comments':comments, 'new_comment':new_comment, 'comment_form':comment_form })

from django.shortcuts import render, redirect

from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

def register_request(request):

    if request.method == "POST":

        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("post_list")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form=NewUserForm()
    return render(request=request, template_name="blog/register.html", context={'form':form})
