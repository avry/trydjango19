from urllib.parse import quote_plus

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

from . forms import PostForm
from . models import Post


def post_create(request):
	# if not request.user.is_staff or not request.user.is_superuser:
	# 	raise Http404 #unnecessary. As long as they authenticated, they may post

	if not request.user.is_authenticated:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		print("valid")
		instance = form.save(commit=False) #form is saved
		instance.user = request.user
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
	# register.filter('urlify', urlify)
	instance = get_object_or_404(Post, id = id)
	share_string = quote_plus(instance.content)
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
	}
	return render(request, "post_detail.html", context)


def post_list(request):
	queryset_list = Post.objects.active()#.order_by("-timestamp")
	
	query =  request.GET.get("query")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
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
	# if not request.user.is_staff or not request.user.is_superuser:
	# 	raise Http404
	if not request.user.is_authenticated:
		raise Http404
	instance = get_object_or_404(Post, id = id)

	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
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
	# if not request.user.is_staff or not request.user.is_superuser:
	# 	raise Http404
	if not request.user.is_authenticated:
		raise Http404
	instance = get_object_or_404(Post, id = id)
	instance.delete()
	messages.success(request, "Item Deleted")

	return HttpResponseRedirect(reverse('posts:list'))

