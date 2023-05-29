from typing import Optional

from django.http import FileResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import TemplateView, DetailView, ListView

from main.models import Post, Category


class MainIndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        muhim = Post.objects.select_related('category').filter(is_date=True, category__name__icontains="muhim sanalar")[
                :4]
        bayram = Post.objects.select_related('category').filter(is_date=True, category__name__icontains="bayramlar")[:4]
        tugilgan_kun = Post.objects.select_related('category').filter(is_date=True,
                                                                      category__name__icontains="tavallud kunlar")[:4]

        last_books = Post.objects.select_related('category').order_by("-id")[:4]
        kwargs["oxirgi_postlar"] = last_books
        kwargs["muhim"] = muhim
        kwargs["bayram"] = bayram
        kwargs["tugilgan_kun"] = tugilgan_kun

        return kwargs


class MainList(ListView):
    template_name = "main/list.html"
    paginate_by = 10

    def get_queryset(self):
        cid = self.kwargs.get("id", None)
        query = Post.objects.order_by("-id")
        if cid is not None:
            query = Post.objects.filter(category_id=cid).order_by("-id")
        return query

    def dispatch(self, request, *args, **kwargs):
        cid = kwargs.get("id", None)
        self.cat_objects = None
        if cid is not None:
            self.cat_objects = cat = Category.objects.get(id=cid)
            if kwargs.get("slug") != cat.slug:
                return redirect("main:list", cat.slug, cat.id, permanent=True)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        children = Category.objects.filter(
            parent_id=None if self.cat_objects is None else self.cat_objects.id).order_by("-id").all()

        if not children:
            children = Category.objects.filter(parent_id=self.cat_objects.parent_id).order_by("-id").all()
        context['breadcrumb'] = MainList.category_bc(self.cat_objects)
        context["children"] = children
        context['cid'] = None if self.cat_objects is None else self.cat_objects.id

        return context

    @staticmethod
    def category_bc(object, last_active=False):
        bc = [{
            "url": resolve_url("main:posts") if object else None,
            "title": "Barcha postlar"
        }]
        if object:
            path = object.path.strip('-').split('-')
            path.pop()

            parents = list(Category.objects.filter(id__in=path).all())

            parents.sort(key=lambda r: path.index(str(r.id)))
            for row in parents:
                bc.append({
                    "url": resolve_url("main:list", row.slug, row.id),
                    "title": row.name
                })

            bc.append({
                "url": resolve_url("main:list", object.slug, object.id) if last_active else None,
                "title": object.name
            })

            return bc


class MainPostView(DetailView):
    model = Post
    template_name = "main/book.html"

    def get_queryset(self):
        if self.queryset:
            self.queryset.select_related("category").all()

        return Post.objects.select_related("category").all()

    def get_object(self, queryset=None):
        if not self.object:
            self.object = super().get_object(queryset=queryset)

        return self.object

    def dispatch(self, request, *args, **kwargs):
        self.object = None
        obj = self.get_object()
        if kwargs.get("slug") != obj.slug:
            return redirect("main:post", obj.slug, obj.id, permanent=True)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bc = MainList.category_bc(self.object.category, True)
        bc.append({
            "url": None,
            "title": self.object.title
        })
        context["breadcrumb"] = bc
        context["filenomi"] = self.object.file.path.split('/')[-1] if self.object.file else None
        context["fileolchami"] = round((self.object.file.size / 1024 ** 2), 2) if self.object.file else None
        context["similar"] = Post.objects.filter(category_id=self.object.category_id).exclude(
            id=self.object.id).order_by(
            "?").all()[:4]

        return context


class FileDownloadView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        file_path = self.object.file.path

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename=' + file_path.split('/')[-1]
        return response


class MainSearchView(ListView):
    template_name = "main/search.html"
    paginate_by = 10
    queryset = Post.objects.all()[:1]

    def get_context_data(self, *, object_list=None, **kwargs):
        q = self.request.GET.get("q")
        if q:
            query = Post.objects.filter(title__icontains=q).order_by("-id")
            object_list = query
            if query:
                result = True
            else:
                result = False
        else:
            result = False

        context = super().get_context_data(object_list=object_list, **kwargs)

        context["result"] = result

        return context
