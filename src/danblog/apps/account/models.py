from django.db import models
from django.contrib.auth.models import User

class BlogUser(models.Model):
	first_name = models.CharField(max_length=50, null=False)
	last_name = models.CharField(max_length=50, null=False)
	summary = models.TextField(null=True)
	website = models.URLField(null=True)
	image = models.ImageField(upload_to='profile_images/', blank=True)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return u'%s' % self.first_name + " " + self.last_name