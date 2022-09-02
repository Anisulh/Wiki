from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from encyclopedia.forms.encyclopedia.forms import CreatePage, EditingForm, LoginForm, RegisterForm, Search
from . import util
import markdown2

search_form = Search()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": search_form
    })
    
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login)
    form = RegisterForm()
    return render(request, 'encyclopedia/register.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(index)
        else:
            return render(request, "encyclopedia/error.html", {
                'message': "Invalid Credentials",
                "search_form": search_form
                })
    form = LoginForm()
    return render(request, 'encyclopedia/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(index)

def entry_page(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            'message': "Unable to find page in DB",
            "search_form": search_form
        })
    entry = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "entry": entry,
        "search_form": search_form
    })
    
@login_required(login_url=login)
def create_page(request):
    if request.method == "POST":
        form = CreatePage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            title = title.capitalize()
            content = form.cleaned_data['content']
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                'message': "Page Already Exists",
                "search_form": search_form
                })
            util.save_entry(title, content)
            new_entry = util.get_entry(title)
            if not new_entry:
                return render(request, "encyclopedia/error.html", {
                'message': "Unable to save new page",
                "search_form": search_form
                })
            return redirect(entry_page, title)
    form = CreatePage()
    return render(request, "encyclopedia/create_page.html", {'form': form, "search_form": search_form})

def search(request):
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = util.find_entry(query)
            if not results:
                return render(request, "encyclopedia/error.html", {
                'message': "Unable to find page",
                "search_form": search_form
                })
            return render(request, "encyclopedia/search_results.html", {"title": results, "search_form": search_form})
    return(request, "encyclopedia/index.html", {"search_form": search_form})

def random(request):
    title = util.random_entry()
    if not title:
        return render(request, "encyclopedia/error.html", {
            'message': 'Unable to get page :(',
            'search_form': search_form
        })
    return redirect(entry_page, title)

@login_required(login_url=login)
def edit_page(request, title):
    if request.method == "POST":
        form = EditingForm(request.POST)
        if form.is_valid():
            new_entry = form.cleaned_data['entry']
            if not new_entry:
                util.delete_entry(title)
                return redirect(index)
            util.save_entry(title, new_entry)
            return redirect(entry_page, title)
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
        'message': "Unable to find page",
        "search_form": search_form
        })
    form = EditingForm(initial={"entry": entry})
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form,
        "search_form": search_form
    })