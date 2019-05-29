"""myNetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from homePage import views
from homePage.views import (HomePostList,
                            login_page,
                            register_page, PostLikeToggleRedirect,
                            PostComments, CommentsOnPost, change_friend,
                            ProfileView, change_following, accept_Friend,
                            logout, likeAjax, searchAjax, add_user_detail,
                            commentlikeAjax)

app_name = 'homePage'
urlpatterns = [
    path('', HomePostList, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login'),
    path('logout/', logout, name='mylogout'),
    path('register/', register_page, name='register'),
    path('add_user_detail/', add_user_detail, name='add_profile_details'),
    path('like/<int:pk>', PostLikeToggleRedirect.as_view(), name='like'),
    # path('comment/<int:post_id>/<int:postUser_id>', CommentsOnPost, name='commentsOnpost'),
    path('comment/', CommentsOnPost, name='commentsOnpost'),
    path('comment/<int:pk>', PostComments, name='comments'),
    path('friends/<str:addorRemove>/<int:pk>', change_friend, name='change_friend'),
    path('follow/<str:followorUnfollow>/<int:pk>', change_following, name='change_following'),
    path('profile/<int:pk>', ProfileView, name='profile'),
    path('accept/<int:pk>', accept_Friend, name='accept_friend'),
    path('liketest/', likeAjax, name='likeAjax'),
    path('commentlike/', commentlikeAjax, name='commentlikeAjax'),
    path('searchAjax/', searchAjax, name='searchAjax'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
