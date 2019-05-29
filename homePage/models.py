import os
from datetime import timezone
from django.utils.timezone import now
from datetime import datetime

from django.db import models
from django.conf import settings


# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

# these two methods 'upload_propic_image' and 'upload_cvoerpic_image_path' is temporary methods.
# it should be changed to one methods by changing the return file path.
def upload_propic_image_path(instance, filename):
    # print(instance)
    # print(filename)
    # new_filename = random.randint(1, 9999999999)
    new_filename = datetime.now()
    name, ext = get_filename_ext(filename)
    final_filename = '{name}-{new_filename}{ext}'.format(new_filename=new_filename, ext=ext, name=name)
    print(new_filename, final_filename, name, ext, filename, instance)
    return 'images/profilePic/{final_filename}'.format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_coverpic_image_path(instance, filename):
    # print(instance)
    # print(filename)
    # new_filename = random.randint(1, 9999999999)
    new_filename = datetime.now()
    name, ext = get_filename_ext(filename)
    final_filename = '{name}-{new_filename}{ext}'.format(new_filename=new_filename, ext=ext, name=name)
    print(new_filename, final_filename, name, ext, filename, instance)
    return 'images/coverPic/{final_filename}'.format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class UserDetails(models.Model):
    user_Id = models.OneToOneField(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    user_DOB = models.DateField(null=True)
    user_gender = models.CharField(max_length=1, null=True)
    user_profile_pic = models.ImageField(upload_to=upload_propic_image_path, null=True,
                                         blank=True, )
    user_cover_pic = models.ImageField(upload_to=upload_coverpic_image_path,
                                       null=True,
                                       blank=True, )

    def __str__(self):
        return str(self.user_Id)


class Post(models.Model):
    post_user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_body = models.CharField(max_length=250)
    post_image = models.ImageField(upload_to='images/',
                                   null=True,
                                   blank=True, )
    post_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    post_created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    post_updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.post_body


class Comments(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_content = models.TextField(max_length=255)
    comment_created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    comment_updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    # def __str__(self):
    #     return '{}={}'.format(self.comment_content, str(self.user.id))
    def __str__(self):
        return self.comment_content


class Friends(models.Model):
    friends_friend = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
                                     related_name='owner')
    created_at = models.DateTimeField(default=datetime.now())

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.friends_friend.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.friends_friend.remove(new_friend)

    def __str__(self):
        return str(self.current_user)+str(self.id)


class Follower(models.Model):
    following_user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followingThem')
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
                                     related_name='follower')
    created_at = models.DateTimeField(default=datetime.now())

    @classmethod
    def make_follow(cls, current_user, new_following):
        following, created = cls.objects.get_or_create(
            current_user=current_user
        )
        following.following_user.add(new_following)

        print(following)
        print(following.following_user)
        print(new_following)

    @classmethod
    def remove_follow(cls, current_user, new_following):
        following, created = cls.objects.get_or_create(
            current_user=current_user
        )
        following.following_user.remove(new_following)

    def __str__(self):
        return str(self.current_user)


class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='request_sender', blank=True, default=0)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='requests_receiver')
    created = models.DateTimeField(default=datetime.now())
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)
    added = models.BooleanField(blank=True, null=True)
    friend_created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    @classmethod
    def friend_request(cls, from_user, to_user):
        print('abbb')
        print(from_user)
        print(to_user)
        req, created = cls.objects.get_or_create(
            to_user=to_user
        )
        print('aaaa')
        print(req, created)
        req.from_user.add(from_user)
        print(req)
        # print(request.following_user)

    @classmethod
    def remove_request(cls, from_user, to_user):
        req, created = cls.objects.get_or_create(
            to_user=to_user
        )
        req.from_user.remove(from_user)

    def get_all_friend_request(self):
        friendRequest = FriendshipRequest.objects.get(to_user=self)
        print(friendRequest)
        print('friend request')
        allRequest = friendRequest.from_user.all()
        print(allRequest)
        return allRequest

    class Meta:
        verbose_name = 'Friendship Request'
        verbose_name_plural = 'Friendship Requests'
        # unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "Name = " + " " + str(self.to_user) + ", " + "ID = " + str(self.to_user_id)
