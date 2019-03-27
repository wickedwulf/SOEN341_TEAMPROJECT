""" Admin panel setup for home app """
from django.contrib import admin
from .models import TwitterTweet, LikedTweets, FollowingUsers, PinnedPosts, RepliesToTweet, PrivateMessage, BlockedUsers

admin.site.register(TwitterTweet)
admin.site.register(LikedTweets)
admin.site.register(FollowingUsers)
admin.site.register(PinnedPosts)
admin.site.register(RepliesToTweet)
admin.site.register(PrivateMessage)
admin.site.register(BlockedUsers)
