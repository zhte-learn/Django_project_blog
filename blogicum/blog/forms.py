from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Post, Comment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'pub_date',
            'location',
            'category',
            'image',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pub_date:
            self.initial['pub_date'] = self.instance.pub_date.strftime(
                '%Y-%m-%dT%H:%M'
            )

    def clean_pub_date(self):
        pub_date = self.cleaned_data.get('pub_date')
        if (
            pub_date is not None
            and pub_date.time() == timezone.datetime.min.time()
        ):
            now = timezone.now()
            pub_date = timezone.make_aware(
                timezone.datetime.combine(pub_date.date(), now.time())
            )
        return pub_date


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
