from django.conf.urls import patterns, url
from .views import login, register, logout, user_detail, edit_profile

urlpatterns = patterns('',
                       url(
                           regex=r"^login/",
                           view=login,
                           name="login"
                       ),
                       url(
                       		regex=r"^register/",
                       		view=register,
                       		name="register"
                       	),
                       url(
                          regex=r"^logout/",
                          view=logout,
                          name="logout"
                        ),
                       url(
                          regex=r"^profile/(?P<user_id>\d+)/",
                          view=user_detail,
                          name="profile"
                        ),
                       url(
                          regex=r"^edit/",
                          view=edit_profile,
                          name="edit"
                        ),
)