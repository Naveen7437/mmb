import json

from django.http import HttpResponse
from functools import wraps
from django.contrib.auth import get_user_model

from mmb_repo.users.models import *
from mmb_repo.mmb_data.models import *
from mmb_repo.bands.models import *


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        result = json.dumps({'not_authenticated': True})
        return HttpResponse(result, 'application/json')

    return wrapper


def category_search(request):
    data = None
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=q)[:20]
        print "query result "
        print users
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username

            results.append(user_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_location(request):
    data = None
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=q)[:20]
        print "query result "
        print users
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username

            results.append(user_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@ajax_login_required
def inc_likes(request):
    success = False
    mimetype = 'application/json'
    print request.POST.get('song_id')
    is_band = request.session.get('is_band')
    band_id = request.session.get('id')
    if request.is_ajax():
        song_id = request.GET.get('song_id')
        song_obj = Song.objects.get(id=song_id)
        song_obj.likes += 1
        song_obj.save()
        # if not is_band:
        #     band_obj = Band.objects.get(id=band_id)
        #     SongLike.objects.create(band=band_obj, song=song_obj)
        success = True

    return HttpResponse(json.dumps({'success': success, 'like_count': song_obj.likes}), mimetype)

@ajax_login_required
def dec_likes(request):
    success = False
    mimetype = 'application/json'
    if request.is_ajax():
        song_id = request.GET.get('song_id')
        try:
            song_obj = Song.objects.get(id=song_id)
            SongLike.objects.filter(user=request.user, song=song_obj).delete()
            song_obj.likes -= 1
            song_obj.save()
            success = True
        except:
            pass

    return HttpResponse(json.dumps({'success': success, 'like_count': song_obj.likes}), mimetype)


def change_profile(request):
    success = False
    mimetype = 'application/json'
    if request.is_ajax():
        request.session['id'] = 2
        request.session['is_band'] = True
        success = True

    return HttpResponse(json.dumps({'success': success}), mimetype)

@ajax_login_required
def follow(request):
    mimetype = 'application/json'
    user = request.user
    success = False
    if request.is_ajax():
        followed_user_id = int(request.GET.get('user_id'))
        followed_user = get_user_model().objects.get(id =followed_user_id)
        user_followed_profile = Profile.objects.get(user=followed_user)
        user_profile = Profile.objects.get(user=user)
        try:
            UserFollowers.objects.create(follower=user, following=followed_user)
            user_followed_profile.followed_by_count += 1
            user_profile.following_count += 1
            user_profile.save()
            user_followed_profile.save()
            success = True
        except:
            pass

    return HttpResponse(json.dumps({'success': success,
                                    'followed_by_count': user_followed_profile.followed_by_count,
                                    'following_count': user_followed_profile.following_count}),
                        mimetype)


@ajax_login_required
def unfollow(request):
    mimetype = 'application/json'
    user = request.user
    success = False
    if request.is_ajax():
        followed_user_id = request.GET.get('user_id')
        followed_user = get_user_model().objects.get(id =followed_user_id)
        user_followed_profile = Profile.objects.get(user=followed_user)
        user_profile = Profile.objects.get(user=user)
        try:
            UserFollowers.objects.filter(follower=user, following=followed_user).delete()
            user_followed_profile.followed_by_count -= 1
            user_profile.following_count -= 1
            user_profile.save()
            user_followed_profile.save()
            success = True
        except:
            pass

    return HttpResponse(json.dumps({'success': success,
                                    'followed_by_count': user_followed_profile.followed_by_count,
                                    'following_count': user_followed_profile.following_count}),
                        mimetype)

@ajax_login_required
def unfollow_band(request):
    mimetype = 'application/json'
    user = request.user
    success = False
    if request.is_ajax():
        band_id = request.GET.get('band_id')
        band_obj = Band.objects.get(id=band_id)
        user_profile = Profile.objects.get(user=user)
        try:
            BandFollowers.objects.filter(follower=user, following_band=band_obj).delete()
            band_obj.follower_count -= 1
            user_profile.band_follow_count -= 1
            user_profile.save()
            band_obj.save()
            success = True
        except:
            pass

    return HttpResponse(json.dumps({'success': success, 'band_follow_count': band_obj.follower_count}), mimetype)

@ajax_login_required
def follow_band(request):
    mimetype = 'application/json'
    user = request.user
    success = False
    if request.is_ajax():
        band_id = int(request.GET.get('band_id'))
        band_obj = Band.objects.get(id=band_id)
        user_profile = Profile.objects.get(user=user)
        try:
            BandFollowers.objects.create(follower=user, following_band=band_obj)
            band_obj.follower_count += 1
            user_profile.band_follow_count += 1
            user_profile.save()
            band_obj.save()
            success = True
        except:
            pass

    return HttpResponse(json.dumps({'success': success,'band_follow_count': band_obj.follower_count}), mimetype)


#
# @ajax_login_required
# def band_inc_likes(request):
#     success = False
#     mimetype = 'application/json'
#     if request.is_ajax():
#         band_song_id = request.GET.get('band_song_id')
#         band_song_obj = BandSong.objects.get(id=band_song_id)
#         band_song_obj.likes += 1
#         band_song_obj.save()
#         BandSongLike.objects.create(user=request.user, song=band_song_obj)
#         success = True
#
#     return HttpResponse(json.dumps({'success': success, 'like_count': band_song_obj.likes}), mimetype)
#
# @ajax_login_required
# def band_dec_likes(request):
#     success = False
#     mimetype = 'application/json'
#     if request.is_ajax():
#         band_song_id = request.GET.get('band_song_id')
#         try:
#             band_song_obj = Song.objects.get(id=band_song_id)
#             BandSongLike.objects.filter(user=request.user, song=band_song_obj).delete()
#             band_song_obj.likes -= 1
#             band_song_obj.save()
#             success = True
#         except:
#             pass
#
#     return HttpResponse(json.dumps({'success': success, 'like_count': band_song_obj.likes}), mimetype)
