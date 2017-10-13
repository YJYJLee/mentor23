from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf

from summarize.forms import WriteForm
from summarize.models import post
#from summarize.textrank import summarize_text


def summarize(request):
    if(request.user.is_anonymous()):
        template = get_template('logout.html')
        context={}
        return HttpResponse(template.render(context))
    else:
        template = get_template('summarize.html')
        user_id = request.user
        target = post.objects.filter(author=user_id)
        page_data = Paginator(target,5)
        page = request.GET.get('page')
        if page is None:
            page = 1
        try:
            posts = page_data.page(page)
        except PageNotAnInteger:
            posts = page_data.page(1)
        except EmptyPage:
            posts = page_data.page(page_data.num_pages)

        context = {'post_list': posts,'current_page':int(page),'total_page':range(1,page_data.num_pages+1)}
        context.update(csrf(request))
        return HttpResponse(template.render(context))


def write_form(request):
    template = get_template('writeBoard.html')
    br = WriteForm(request.POST)
    if br.is_valid():
        title = br.cleaned_data['title']
        body = br.cleaned_data['body']
        post.objects.create(title=title,body=body,author=request.user)
        return redirect("/summarize/sum/")
    context = {'write':WriteForm}
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def show_form(request):
    global target
    template = get_template('showBoard.html')
    title = request.GET['title']
    target = post.objects.get(title=title,author=request.user)
    context={'title':target.title, 'body':target.body, 'author':target.author}
    return HttpResponse(template.render(context))

def summarize_form(request):
    global target
    template = get_template('showSummarize.html')
    text = request.GET['rate']
    context = {}
    #sum_text = summarize_text(target.body)
    #context={'summarize_text':sum_text,'title':target.title}
    #print(target.title)
    return HttpResponse(template.render(context))


