from django.urls import path
from django.contrib.auth.decorators import login_required
from umessages import views


urlpatterns = [
    path(
        "home/messages/",
        login_required(views.MessageListView.as_view()),
        name="umessages_list",
    ),
    path(
        "home/messages/view/<username>/",
        login_required(views.MessageDetailListView.as_view()),
        name="umessages_detail",
    ),
    path(
        "home/message/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="messages_update",
    ),
    path(
        "home/message/<int:pk>/remove/",
        views.MessageDeleteView.as_view(),
        name="messages_remove",
    ),
    path(
        "home/messages/compose/",
        views.message_compose,
        name="umessages_compose",
    ),
]
