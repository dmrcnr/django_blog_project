from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from django.contrib import messages
from .forms import ArticleForm
from .models import Article,Comment
# Create your views here.


def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles" : articles})
    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})


def detail(request,id):
    
    article = get_object_or_404(Article,id = id)
    
    comments = article.comments.all() #models.py içerisinde related_name="comments" olarak vermiştik.

    return render(request,"detail.html",{"article":article, "comments":comments})


def addComment(request,id):
    article = get_object_or_404(Article,id=id)
    
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()

    return redirect(reverse("article:detail",kwargs={"id":id})) #dinamik bir url redirect ederken reverse fonksiyonunu kullanmamız gerekiyor.


def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")


@login_required(login_url= "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user) #Sisteme kim giriş yapmışsa onun articlelarını almış oluyoruz.

    return render(request,"dashboard.html",{"articles": articles})

@login_required(login_url= "user:login")
def addArticle(request):
    
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid(): #GET request ise buraya girmeyecek.
        article = form.save(commit=False) #İlk olarak article objesini oluşturuyor, daha sonra kaydediyor. commit=False araya girip kullanıcı eklemek için.

        article.author = request.user
        article.save() #commit'i kendimiz yapıyoruz.

        messages.success(request,"Makale Kaydedildi")
        return redirect("index")

    return render(request,"addarticle.html",{"form":form})


@login_required(login_url= "user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article) #instance = article formun mevcut bilgileri ile gelmesi için.
    if form.is_valid():
        article = form.save(commit=False) #İlk olarak article objesini oluşturuyor, daha sonra kaydediyor. commit=False araya girip kullanıcı eklemek için.

        article.author = request.user
        article.save() #commit'i kendimiz yapıyoruz.

        messages.success(request,"Makale Başarıyla Güncellendi")
        return redirect("article:dashboard")

    return render(request,"update.html",{"form": form})

@login_required(login_url= "user:login")
def delete(request,id):
    article = get_object_or_404(Article,id = id)
    article.delete()
    messages.success(request,"Makale Başarıyla Silindi.")
    return redirect("article:dashboard")   #article uygulamasının altındaki dashboarda git. urls.py'de name="dashboard" olarak vermiştik.


