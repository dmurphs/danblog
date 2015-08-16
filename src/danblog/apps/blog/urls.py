from django.conf.urls import patterns, url
from .views import AllPostsView, PostDetail, CreatePost, like_post
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       url(
                           regex=r"^$",
                           view=AllPostsView.as_view(),
                           name="blog"
                       ),
                       url(
                       		regex=r"^post/(?P<pk>\d+)/$",
                       		view=PostDetail.as_view(),
                       		name="post_detail"
                       	),
                       url(
                          regex=r"^new_post/$",
                          view=login_required(CreatePost.as_view()),
                          name="new_post"
                        ),
                       url(
                          regex=r"^like_post/$",
                          view=like_post,
                          name="like_post"
                        ),
)