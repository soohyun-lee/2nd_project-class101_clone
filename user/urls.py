from django.urls    import path
from .views         import KakaoSignIn, CreatorIntro

urlpatterns = [
    path('/signin/kakao/callback', KakaoSignIn.as_view(), name = 'kakaosignin'),
    path('/creator/intro', CreatorIntro.as_view(), name = 'creatorintro'),
]