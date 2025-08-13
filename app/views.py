from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, PostForm
from .models import Post, CodeBlock,LANGUAGE_CHOICES

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'app/home.html', {'posts': posts})

from django.shortcuts import render, redirect
from .models import Post, CodeBlock
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            # Save post but don't commit yet
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            # Loop through each language choice and create CodeBlocks if provided
            for lang, _ in LANGUAGE_CHOICES:
                code_content = request.POST.get(f'code_{lang}', '').strip()
                if code_content:
                    CodeBlock.objects.create(post=post, language=lang, code=code_content)

            return redirect('all_posts')  # Redirect to all posts page

    else:
        post_form = PostForm()

    return render(request, 'app/create_post.html', {'form': post_form, 'languages': LANGUAGE_CHOICES})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # এখানে user তৈরি হয়
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # 🔥 Debugging এর জন্য
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')
from django.shortcuts import get_object_or_404

#from .models import Post
#def post_detail(request, post_id):
  #  post = get_object_or_404(Post, id=post_id)
   # return render(request, 'app/post_detail.html', {'post': post})

def all_posts(request):
    posts = Post.objects.all()
    languages = ['python', 'java', 'cpp']

    post_list = []
    for post in posts:
        code_list = []
        for lang in languages:
            cb = post.code_blocks.filter(language=lang).first()
            code = cb.code if cb else None
            code_list.append({'language': lang, 'code': code})
        post_list.append({'post': post, 'codes': code_list})

    return render(request, 'app/all_posts.html', {'post_list': post_list})

