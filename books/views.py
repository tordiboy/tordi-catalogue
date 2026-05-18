from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Book, UserBook, Category
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


# =========================
# 📚 BOOK LIST
# =========================
@login_required
def book_list(request):
    query = request.GET.get("q")
    category_id = request.GET.get("category")

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id and category_id != "all":
        books = books.filter(category_id=category_id)

    unlocked_ids = UserBook.objects.filter(
        user=request.user,
        unlocked=True
    ).values_list("book_id", flat=True)

    return render(request, "book_list.html", {
        "books": books,
        "unlocked_ids": unlocked_ids,
        "categories": Category.objects.all(),
        "query": query
    })


# =========================
# 🔐 ADMIN DASHBOARD
# =========================
@login_required
def admin_unlock_page(request):

    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    user_query = request.GET.get("user", "")
    book_query = request.GET.get("book", "")

    users = User.objects.all()
    books = Book.objects.all()

    # 🔍 FILTER USERS
    if user_query:
        users = users.filter(username__icontains=user_query)

    # 🔍 FILTER BOOKS
    if book_query:
        books = books.filter(title__icontains=book_query)

    # convert to dict (FAST LOOKUP)
    access_dict = {
        (a.user_id, a.book_id): a.unlocked
        for a in UserBook.objects.all()
    }

    return render(request, "admin/unlock.html", {
        "users": users,
        "books": books,
        "access_dict": access_dict,
        "user_query": user_query,
        "book_query": book_query
    })


# =========================
# 🔁 TOGGLE LOCK / UNLOCK
# =========================
@login_required
def toggle_book_access(request, user_id, book_id):

    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    obj, created = UserBook.objects.get_or_create(
        user_id=user_id,
        book_id=book_id,
        defaults={"unlocked": True}
    )

    # toggle state
    obj.unlocked = not obj.unlocked
    obj.save()

    return redirect("admin_unlock")


# =========================
# 🔐 REGISTER
# =========================
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("book_list")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


# =========================
# 🔐 LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("book_list")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


# =========================
# 🚪 LOGOUT
# =========================
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")