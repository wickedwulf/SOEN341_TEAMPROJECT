from django.contrib import admin
from .models import Twitter_Tweet, Liked_Tweets, Following_Users, Pinned_Posts, Replies_To_Tweet, Private_Message, Blocked_Users


admin.site.register(Twitter_Tweet)
admin.site.register(Liked_Tweets)
admin.site.register(Following_Users)
admin.site.register(Pinned_Posts)
admin.site.register(Replies_To_Tweet)
admin.site.register(Private_Message)
admin.site.register(Blocked_Users)
