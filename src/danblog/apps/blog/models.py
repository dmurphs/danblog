from django.db import models
from redactor.fields import RedactorField
from django.contrib.auth.models import User

RECORD_STATUS = ((0, 'Inactive'), (1, 'Active'))

class CommonFields(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(
        choices=RECORD_STATUS, default=1, verbose_name='Status')

    class Meta:
        abstract = True

class PostCategory(CommonFields):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Post(CommonFields):
    name = models.CharField(max_length=255)
    content = RedactorField(verbose_name='')
    category = models.ManyToManyField(PostCategory)
    user = models.ForeignKey(User)
    liked_by = models.ManyToManyField(User, related_name='user_liked')
    url = models.URLField(null=True)

    def __unicode__(self):
        return u'%s' % self.name