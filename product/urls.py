from django.urls import path
from .views      import (Allproducts,
                        RecommendView, 
                        DetailView, 
                        OpenProduct,
                        BasicInformation,
                        TitleAndCover,
                        Introduce
                        )
urlpatterns = [
    path('', Allproducts.as_view()),
    path('/recommend',RecommendView.as_view()),
    path('/detail',DetailView.as_view()),
    # path('/detail_recommend',DetailView_Recommend.as_view()),
    # path('/detail_image',Detailimage.as_view()),
    path('/open',OpenProduct.as_view()),
    path('/basic',BasicInformation.as_view()),
    path('/title', TitleAndCover.as_view()),
    path('/introduce', Introduce.as_view())

]
