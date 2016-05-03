from django.conf.urls import url
from . import restviews

urlpatterns = [
    url(r'^algconstructors/$', restviews.AlgConstructorList.as_view()),
    url(r'^algconstructors/(?P<pk>[0-9]+)/$', restviews.AlgConstructorDetail.as_view()),
    url(r'^algparams/$', restviews.AlgParamList.as_view()),
    url(r'^algparams/(?P<pk>[0-9]+)/$', restviews.AlgParamDetail.as_view()),
    url(r'^slots/$', restviews.SlotList.as_view()),
    url(r'^slots/(?P<pk>[0-9]+)/$', restviews.SlotDetail.as_view()),
    url(r'^strategies/$', restviews.StrategyList.as_view()),
    url(r'^strategies/(?P<pk>[0-9]+)/$', restviews.StrategyDetail.as_view()),
]
