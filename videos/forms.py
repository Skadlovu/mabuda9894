from django import forms 
from . models import VidStream, Comment



class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=['text']
		widgets={
			'text':forms.Textarea(attrs={'placeholder':'add a comment....'})
		}




class LikeForm(forms.Form):
	video_id=forms.IntegerField(widget=forms.HiddenInput())




class VideoUploadForm(forms.ModelForm):

	class Meta:
		model= VidStream
		fields= ['category','title', 'description', 'video', 'tags']


class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label='Search the site')
	

