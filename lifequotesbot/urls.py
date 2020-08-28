from django.urls import path

from lifequotesbot import views
from lifequotesbot.views import MyBotView

urlpatterns = [
    #path('receive_message', views.GreenBotView, name='receive_message'),
    path('greenbot66d2b8f4a09cd35cb2307/', MyBotView.as_view())
]