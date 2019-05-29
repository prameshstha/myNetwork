from django.contrib import admin
from .models import Post, Comments, Friends, FriendshipRequest, Follower, UserDetails

# Register your models here.
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Friends)
admin.site.register(FriendshipRequest)
admin.site.register(Follower)
admin.site.register(UserDetails)
