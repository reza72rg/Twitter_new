import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView

from .forms import UserRegisterForm
from .models import Post, User


class SignUpView(CreateView):
    form_class = UserRegisterForm
    template_name = 'network/register.html'
    success_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/")
            # Redirect to the task list page if user is already authenticated
        return super(SignUpView, self).get(*args, **kwargs)


class PostListView(LoginRequiredMixin, ListView):
    template_name = "network/index.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        if self.request.path == "/explore/":
            queryset = Post.objects.all().order_by("-create_date")
            return queryset
        if self.request.path == "/":
            user = self.request.user
            user_follow = User.objects.filter(connect_people=user)
            queryset = Post.objects.filter(owner=user) | Post.objects.filter(owner__in=user_follow)
            return queryset
'''
    def get_context_data(self, *, object_list=None, **kwargs):
        pass
'''
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "network/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        current_user: User = self.request.user
        obj: User = self.get_object()
        if current_user != obj:
            data['has_follow'] = current_user.has_follower(obj)

        return data


@login_required
def new_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_content = data.get('post_content', None)
        if post_content is not None:
            user = request.user
            new_post = Post.objects.create(owner=user, text=post_content)
            new_post.save()
            return JsonResponse({"message": "Post created successfully"}, status=201)
        else:
            return JsonResponse({"error": "Post content cannot be empty"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=400)


@login_required
def update_post(request):
    pass


@login_required
def follow_toggle(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        user_follow = data['user_id']
        try:
            user_followed = User.objects.get(id=user_follow)
        except:
            return JsonResponse({"error": "User not found"}, status=404)

        if user_followed == user:
            return JsonResponse({"error": "You cannot follow yourself"}, status=400)

        if user.followers.filter(id=user_followed.id).exists():
            user.followers.remove(user_followed)
            return JsonResponse({"message": "You are no longer following this user"}, status=200)
        else:
            user.followers.add(user_followed)
            return JsonResponse({"message": "You are now following this user"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=400)


@login_required
def like_toggle(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        post_id = data['post_id']
        post = Post.objects.get(id=post_id)
        result = post.likes.filter(id=user.id).exists()
        if result:
            post.likes.remove(user)
            return JsonResponse({"message": "You unlike this post"}, status=201)
        else:
            post.likes.add(user)
            return JsonResponse({"message": "You like this post"}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=400)
