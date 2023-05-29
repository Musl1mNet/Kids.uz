import time

from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


def build_book_category_tree(choice=False):
    parents = {}
    for row in Category.objects.order_by("id").all():
        if row.parent_id not in parents:
            parents[row.parent_id] = []

        parents[row.parent_id].append(row)

    result = []

    def build_tree(parent_id=None, depth=0):
        if parent_id not in parents:
            return

        margin = ">> " * depth

        for row in parents[parent_id]:
            txt = f"{margin} {row.name}"
            if choice:
                result.append((row.id, txt))
            else:
                result.append({"value": row.id, "text": txt})
            build_tree(row.id, depth + 1)

    build_tree()

    return result


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = build_book_category_tree(True)

    def clean_date(self):
        date = self.cleaned_data["date"]
        now = time.time()
        if now < date.timestamp():
            raise ValidationError("Hozirgi vaqtdan katta bo'lmasligi kerak!")
        return date

    class Meta:
        model = Post
        fields = "__all__"
