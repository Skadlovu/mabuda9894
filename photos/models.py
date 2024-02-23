from django.db import models 
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from videos.models import Comment




class Photo(models.Model):
	uploader= models.ForeignKey(User, on_delete= models.CASCADE)
	title= models.CharField(max_length=300)
	description= models.TextField(max_length=600)
	upload_date=models.DateTimeField(auto_now_add=True)
	content=models.ImageField(upload_to='Uploaded_photos', verbose_name='Photos')
	views = models.IntegerField(blank=True, default=0)
	likes = models.IntegerField(blank=True, default=0)
	comments=models.OneToOneField(Comment,on_delete=models.CASCADE,blank=True,null=True)

	def __str__(self):
		return self.title
	

	def related_photos(self):
		related_by_title=Photo.objects.filter(title=self.title).exclude(id=self.id)
		related_by_description=Photo.objects.filter(description=self.description).exclude(id=self.id)
		related_by_uploader=Photo.objects.filter(uploader=self.uploader)

		related_photos = (related_by_title | related_by_description | related_by_uploader).distinct()

		return related_photos



	def get_absolute_url(self):
		return reverse ('photo', kwargs={'pk':self.pk})
	




