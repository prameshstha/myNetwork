from itertools import chain

from django.contrib.auth import login, authenticate, get_user_model, logout as mylogout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import RedirectView, DetailView
from homePage.models import Post, Comments, Friends, Follower, FriendshipRequest, UserDetails
from django.contrib.auth.models import User
from homePage.forms import LoginForm, RegisterForm, PostForm, CommentForm, AddDetailForm
from django.template.loader import render_to_string

# Create your views here.

# class HomePostListView(ListView):

postModel = Post
User = get_user_model()


@login_required()
def HomePostList(request):
    print(request.user.id)
    queryset = Post.objects.all().order_by('-post_created_at').select_related()
    # f = Friends.objects.filter(current_user=request.user)
    # users = User.objects.exclude(id=request.user.id)
    # print(users)
    form = PostForm(request.POST or None)
    formComment = CommentForm(request.POST or None)
    # print('All post all=')
    template_name = 'homePage/home_page.html'
    # print('post all=')
    # print(queryset)
    comments = Comments.objects.all()

    print(queryset.query)
    # for qq in queryset:
    #     pid = qq.id
    #     print(qq.id)
    #     comments = Comments.objects.filter(post_id=pid).order_by('-id')
    #     print('all comment=')
    #     print(comments)
    # print(comments)

    # post_id = Post.objects.get(qq.id)
    # print(post_id)

    if form.is_valid():
        print(form.cleaned_data)
        post = form.cleaned_data.get('post')
        print('post only' + post)
        new_post = postModel.objects.create(post_body=post, post_user_id=request.user.id)
        if new_post is not None:
            print('post added')


    # friendRequest = FriendshipRequest.objects.get(to_user=request.user)
    # print(friendRequest)
    # print('friend request')
    # allRequest = friendRequest.from_user.all()
    # print(allRequest)
    user = request.user
    print(user.id)
    print('yes')
    allRequest = get_all_friend_request(user)

    try:
        ownerUserDetail = UserDetails.objects.get(user_Id=user)
    except:
        ownerUserDetail = ''
    print(ownerUserDetail)
    # ownerInLikes = ownerLiked(1)
    allUserDetails = UserDetails.objects.all() # all user details
    commentsAndUser = get_all_comments_user() # call function
    print(allUserDetails)
    print(commentsAndUser)
    context = {
        'form': form,
        'queryset': queryset,
        'formComment': formComment,
        'allFriendRequest': allRequest,
        'UserDetails': allUserDetails,
        'commentsAndUser': commentsAndUser,
        'ownerUserDetail': ownerUserDetail,
        # 'ownerInLikes': ownerInLikes,

    }
    return render(request, template_name, context)


@login_required()
def PostComments(request, pk):
    formComment = CommentForm(request.POST or None)
    queryset = Post.objects.filter(id=pk).order_by('-post_created_at')
    # print('All post all=')
    template_name = 'homePage/home_page.html'
    # print('post all=')
    # print(queryset)
    comments = Comments.objects.filter(post_id=pk).order_by('-id')
    print('all comment=')
    print(comments)
    print(comments)
    context = {'qs': queryset, 'comments': comments, 'formComment': formComment}
    return render(request, template_name, context)


class PostLikeToggleRedirect(RedirectView):
    def get_absolute_url(self, *args, **kwargs):
        return 'http://127.0.0.1:8000'

    def get_redirect_url(self, pk, **kwargs):
        obj = Post.objects.get(pk=pk)
        print(pk, obj)
        url_ = self.get_absolute_url()
        user = self.request.user
        # print(request.get_absolute_url())
        print(user)
        # post_likes = Post.post_likes.get(pk=pk)
        # print(post_likes)
        print(user.is_authenticated)
        if user.is_authenticated:
            abc = obj.post_likes.all()
            for a in abc:
                print(a)
            print('ss')
            print(obj.post_likes.all())
            abcs = obj.post_likes.all()
            for aa in abcs:
                print(aa)
            if user in obj.post_likes.all():
                obj.post_likes.remove(user)
            else:
                obj.post_likes.add(user)
        return url_


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            # context['form'] = LoginForm()
            # redirect to success page
            return redirect('/')
        else:
            # return an invalid login error message.
            print('Error')
    return render(request, 'auth/login.html', context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    new_user = ''
    user = ''
    print(form.is_valid())
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        new_user = User.objects.create_user(username, email, password)
        # authenticate user then login
        user = authenticate(request, username=username, password=password)

    context = {
        'newUser': new_user,
        'form': form
    }
    print(new_user)
    print('x')
    print(user)
    print('a')
    if new_user:
        # automatic login after registering
        login(request, user)
        userid = request.user.id
        print(userid)
        ud = UserDetails(user_Id_id=userid)
        print(ud)
        ud.save()
        return redirect('../add_user_detail')
        # return render(request, 'auth/addDetail.html', context)
    else:
        return render(request, 'auth/register.html', context)


def add_user_detail(request):
    uid = request.user.id
    userDetail = get_object_or_404(UserDetails, user_Id_id=uid)
    # userDetail = UserDetails.objects.get(user_Id_id=uid)

    add_form = AddDetailForm(request.POST or None, instance=userDetail)
    new_user = ''
    print(add_form.is_valid())
    print(request.POST)

    print(uid)
    if add_form.is_valid():
        print(add_form.cleaned_data)
        # user_Id = request.user
        # dob = add_form.cleaned_data.get('dob')
        # gender = add_form.cleaned_data.get('user_gender')
        # pro_pic = add_form.cleaned_data.get('user_profile_pic')
        # cover_pic = add_form.cleaned_data.get('user_cover_pic')
        #new_user = UserDetails.objects.filter(user_Id_id=user_Id).update(user_DOB=dob, user_gender=gender, user_profile_pic=pro_pic, user_cover_pic=cover_pic)
        # print(new_user)
        saved = add_form.save()
        print(saved)
        if saved:
            return redirect('profile', pk=uid)  # returns to url profile with the profile id
        # context = ProfileView
    context = {
        'newUser': new_user,
        'add_form': add_form,
        'userDetail': userDetail,
    }

    return render(request, 'auth/addDetail.html', context)


@login_required()
def change_friend(request, addorRemove, pk):
    new_friend = User.objects.get(pk=pk)
    if addorRemove == 'add':
        FriendshipRequest.friend_request(request.user, new_friend)
        change_friend(request, 'follow', pk)
        # Friends.make_friend(request.user, new_friend)
    elif addorRemove == 'cancelRequest':
        FriendshipRequest.remove_request(request.user, new_friend)
    elif addorRemove == 'remove':
        Friends.remove_friend(request.user, new_friend)
    return redirect('http://127.0.0.1:8000/')


def accept_Friend(request, pk):
    new_friend = User.objects.get(pk=pk)
    Friends.make_friend(request.user, new_friend)
    Friends.make_friend(new_friend, request.user)
    FriendshipRequest.remove_request(new_friend, request.user)
    # Friends.remove_friend(request.user, new_friend)
    return redirect('http://127.0.0.1:8000/')


# def change_friend(request, addorRemove, pk):
#     new_friend = User.objects.get(pk=pk)
#     if addorRemove == 'add':
#         Friends.make_friend(request.user, new_friend)
#     elif addorRemove == 'remove':
#         Friends.remove_friend(request.user, new_friend)
#     return redirect('http://127.0.0.1:8000/')

@login_required()
def change_following(request, followorUnfollow, pk):
    print(request, followorUnfollow, pk)
    new_follower = User.objects.get(pk=pk)
    print(new_follower)
    if followorUnfollow == 'follow':
        Follower.make_follow(request.user, new_follower)
    elif followorUnfollow == 'unFollow':
        Follower.remove_follow(request.user, new_follower)
    return redirect('http://127.0.0.1:8000/')


@login_required()
def ProfileView(request, pk):
    # object = User.objects.get(pk=pk)
    # if user exists get the user with id=pk if not return 404 page not found error
    userProfile = get_object_or_404(User, pk=pk)
    queryset = Post.objects.filter(post_user=userProfile.id)

    try:
        # get friend object - collection of friend from many to many relation
        friend_object = Friends.objects.get(current_user=userProfile.id)
    except:
        friend_object = Friends.objects.none()

    print('f')
    print(friend_object)
    print('frie')
    try:
        # get all friend list from friend object - gives the friend list of the profile owner
        friends_profile = friend_object.friends_friend.all()
    except:
        friends_profile = ''

    print(friends_profile)
    owner = request.user.id
    print(owner)
    print('owner')
    try:
        friendObj_owner = Friends.objects.get(current_user=owner)  # friend object for current logged in user
    except:
        friendObj_owner = ''
    print(friendObj_owner)
    try:
        ownerFriends = friendObj_owner.friends_friend.all()  # friend queryset of current logged in user
    except:
        ownerFriends = ''

    print(ownerFriends)

    try:
        ownerFriends.get(id=userProfile.id)  # checking if this profile is friend with the owner logging user
        ofs = 'yes'
    except:
        ofs = 'no'
    # for of in ownerFriends:
    #     if of.id == object.id:
    #         print(of.id)
    #         ofs = 'yes'
    #     else:
    #         ofs = 'no'
    print(ofs)

    form = PostForm(request.POST or None)
    formComment = CommentForm(request.POST or None)
    # print('All post all=')
    # print('post all=')
    # print(queryset)
    # comments = Comments.objects.all().order_by('-id')
    commentsAndUser = get_all_comments_user()
    # for qq in queryset:
    #     pid = qq.id
    #     print(qq.id)
    #     comments = Comments.objects.filter(post_id=pid).order_by('-id')
    #     print('all comment=')
    #     print(comments)
    # print(comments)

    # post_id = Post.objects.get(qq.id)
    # print(post_id)

    if form.is_valid():
        print(form.cleaned_data)
        post = form.cleaned_data.get('post')
        print('post only' + post)
        new_post = postModel.objects.create(post_body=post)
        # if new_user is not None:
    allRequest = get_all_friend_request(request.user)
    try:
        fRequest = allRequest.get(id=pk)
    except:
        fRequest = ''
    print(fRequest)
    sentRequest = get_all_sent_request(userProfile.id, owner)
    try:
        ownerUserDetail = UserDetails.objects.get(user_Id=pk)  # detail of user in profile
    except:
        ownerUserDetail = ''
    print('ownerUserDetail')
    print(ownerUserDetail)
    allUserDetails = UserDetails.objects.all()
    print(allUserDetails)

    # this statement inner join with the auth_user from which primary key is foreign key for this model - select_related
    all_details_of_user = UserDetails.objects.select_related('user_Id')
    print(all_details_of_user.query)

    print('frlst')
    print(all_details_of_user)
    # merging two query set friends and allUserDetails
    friends_and_userDetails = list(chain(friends_profile, allUserDetails))
    # friends_and_userDetails = friends|allUserDetails
    print(friends_and_userDetails)
    for ffr in friends_and_userDetails:
        try:
            print(ffr.user_Id)
        except:
            print(ffr.username)
    try:
        friend_object_id = friend_object.id
    except:
        friend_object_id = ''
    print(pk, friend_object_id)
    friend_ko_details = UserDetails.objects.raw(
        """SELECT * 
        FROM `homepage_friends_friends_friend` AS A
        JOIN `homepage_userdetails` AS B
        JOIN `homepage_friends` AS C
        ON A. `user_id` = B. `user_Id_id`
        WHERE C.`current_user_id` = %s and
          `friends_id` = %s """, [pk, friend_object_id])
    # pk is the user's profile id and friend object is profile owner's friend object id which contain friend list.
    print(friend_ko_details)
    for xxx in friend_ko_details:
        print(xxx)

    context = {
        'form': form,
        'queryset': queryset,
        'commentsAndUser': commentsAndUser,
        'formComment': formComment,
        'friends': friends_profile,
        'userProfile': userProfile,
        'allFriendRequest': allRequest,
        'ofs': ofs,
        'sentRequest': sentRequest,
        'fRequest': fRequest,
        'ownerUserDetail': ownerUserDetail,
        'UserDetails': allUserDetails,
        'friends_and_userDetails': friends_and_userDetails,
        'friend_ko_details': friend_ko_details,
    }
    print('qs')
    print(queryset)
    template_name = 'profile/profile.html'
    return render(request, template_name, context)


# get owner friend request
def get_all_friend_request(self):
    try:
        friendRequest = FriendshipRequest.objects.get(to_user=self)
        print(friendRequest)
        print('friend request')
        allRequest = friendRequest.from_user.all()
        print(allRequest)
        return allRequest
    except:
        allRequest = ''
        return allRequest


# get sent friend request
def get_all_sent_request(self, request):
    try:
        fr = FriendshipRequest.objects.get(to_user=self)
        print(fr)
        print('sent request')
        sentRequest = fr.from_user.get(id=request)
        print(sentRequest)
        return sentRequest
    except:
        sentRequest = ''
        return sentRequest


def logout(request):
    mylogout(request)
    return redirect('http://127.0.0.1:8000/login')


def likeAjax(request):
    print('id')
    print(request)
    print(request.POST)
    data = request.POST
    pk = request.POST['pk'][0]
    obj = Post.objects.get(pk=pk)
    print(pk, obj)
    user = request.user
    print(user)
    print(user.is_authenticated)
    if user.is_authenticated:
        abc = obj.post_likes.all()
        print(obj.post_likes.all())
        print('all')
        for a in abc:
            print(a)
        print('ss')

        if user in obj.post_likes.all():
            obj.post_likes.remove(user)
        else:
            obj.post_likes.add(user)
    # ownerInLikes = allLikes.user.get(id=user)
    allLikes = obj.post_likes.all()
    print(allLikes)
    for aa in allLikes:
        print(aa)
        print('aa')

    queryset = Post.objects.get(pk=pk)
    form = PostForm(request.POST or None)
    formComment = CommentForm(request.POST or None)

    comments = Comments.objects.all().order_by('-id')

    if form.is_valid():
        print(form.cleaned_data)
        post = form.cleaned_data.get('post')
        print('post only' + post)
        new_post = postModel.objects.create(post_body=post)
        # if new_user is not None:
    # ownerInLikes = ownerLiked(pk)  # function called
    ownerInLikes = ''
    if user in allLikes:
        ownerInLikes = user
    context = {
        'ownerInLikes': ownerInLikes,
        'form': form,
        'post': queryset,
        'comments': comments,
        'formComment': formComment,

    }
    if request.is_ajax():
        html = render_to_string('homePage/like_section.html', context, request=request)
    return JsonResponse({'post': html})


def commentlikeAjax(request):
    pass


def searchAjax(request):
    print(request.POST)
    print(request.method)
    if request.method == 'POST':
        searchTxt = request.POST.get('searchText')
        print(searchTxt)
    else:
        searchTxt = ''
    if searchTxt == '':
        searchUser = None
    else:
        searchUser = User.objects.filter(username__icontains=searchTxt)
    context = {'searchUser': searchUser}
    if request.is_ajax():
        html = render_to_string('homePage/ajax_search.html', context, request=request)
    return JsonResponse({'search': html})


@login_required()
def CommentsOnPost(request):
    print(request.POST)
    commenter_id = request.user.id
    if request.method == 'POST':
        # request.POST['pk'][0]
        comment = request.POST['comment']
        post_id = request.POST['post_id']

        print(post_id, comment, commenter_id)
        post = Post.objects.get(id=post_id)
        new_comments = Comments(comment_content=comment, post_id_id=post_id, user_id_id=commenter_id)
        new_comments.save()
        commentsAndUser = get_comments_with_user_details(post_id)
        print(commentsAndUser)
        for aax in commentsAndUser:
            print('comt')
            print(aax.user_profile_pic)
            print(aax.id)

        #
        # Comments.object.create(
        #     comment=comment,
        #     post_id_id=post_id,
        #     user_id_id=uid
        # )
        context = {
            'post': post,
            'commentsAndUser': commentsAndUser,
        }
    if request.is_ajax():
        html = render_to_string('homePage/comment_section.html', context, request=request)
    return JsonResponse({'comment': html})


# function to get the user details who comments in a post with post_id
def get_comments_with_user_details(post_id):
    post_id = post_id
    # commentingUser = Comments.objects.filter(post_id_id=post_id).select_related()
    # above query should be like this below.
    commentsAndUser = UserDetails.objects.raw("""SELECT * FROM `homepage_comments` AS A
    JOIN `homepage_userdetails` AS B
    ON A. `user_id_id` = B. `user_Id_id`
    WHERE A.`post_id_id` = %s """, [post_id])
    return commentsAndUser


def get_all_comments_user():
    # commentingUser = Comments.objects.filter(post_id_id=post_id).select_related()
    # above query should be like this below.
    commentsAndUser = UserDetails.objects.raw("""SELECT * FROM `homepage_comments` AS A
    JOIN `homepage_userdetails` AS B
    ON A. `user_id_id` = B. `user_Id_id` """)
    return commentsAndUser