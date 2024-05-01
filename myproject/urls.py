from django.urls import path
from myapp.views import RootView, ImageUploadView, ImageClassification

urlpatterns = [
    path('', RootView.as_view(), name='root'),  # Root view
    # path('upload-image/', ImageUploadView.as_view(), name='upload-image'),  # Image upload view
    path('classify-image/', ImageClassification.as_view(), name='classify-image'),  # Image classification view
]
