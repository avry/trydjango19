from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect 
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from . forms import PostForm
from . models import Post


def post_create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		print("valid")
		instance = form.save(commit=False) #form is saved
		instance.save() #saves into database
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(reverse('posts:detail', args=(instance.id,)))
	else:
		print("not valid")
		messages.error(request, "Not Successfully Created")

	
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)


def post_detail(request, id=None):
	instance = get_object_or_404(Post, id = id)
	context = {
		"title": instance.title,
		"instance": instance,
	}
	return render(request, "post_detail.html", context)


def post_list(request):
	queryset_list = Post.objects.all()#.order_by("-timestamp")
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page

	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	queryset = paginator.get_page(page)
	context = {
		"objects_list": queryset,
		"page_request_var": page_request_var
	}


	if request.user.is_authenticated:
		context["title"] = "My User List"

	else:
		context["title"] = "List"
		
	return render(request, "post_list.html", context)







def post_update(request, id=None):
	instance = get_object_or_404(Post, id = id)

	form = PostForm(request.POST or None, instance=instance)
	if form.is_valid():
		print("valid")
		instance = form.save(commit=False) #form is saved
		instance.save() #saves into database
		messages.success(request, "Item Saved")


		return HttpResponseRedirect(reverse('posts:detail', args=(instance.id,)))
	else:
		print("not valid")

	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}
	return render(request, "post_form.html", context)


def post_delete(request, id=None):
	instance = get_object_or_404(Post, id = id)
	instance.delete()
	messages.success(request, "Item Deleted")

	return HttpResponseRedirect(reverse('posts:list'))

