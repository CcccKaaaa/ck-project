
from django.forms import ModelForm
from .models import *

class createForm(ModelForm):
    class Meta():
        model = Auctions
        fields = ["title", "description", "image_url", "category"]

    # User this to define the class of the fields (work the same with form.Form)
    def __init__(self, *args, **kwargs):
        super(createForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class bid(ModelForm):
    class Meta():
        model = Bids
        fields = ["price"]

    def __init__(self, *args, **kwargs):
        super(bid, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class comment(ModelForm):
    class Meta():
        model = Comments
        fields = ["content"]
        labels = {
        "content": "Comment"
        }
