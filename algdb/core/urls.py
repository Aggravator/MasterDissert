from django.conf.urls import url
from . import views
from . import models
from django.views.generic import ListView,DetailView

urlpatterns = [
    url(r'^$', views.MainWindow,name='main_window'),
    url(r'^algs_menu/$', views.MainWindow,name='algs_menu'),
    url(r'^tasks_menu/$', views.TaskMenu,name='tasks_menu'),
    url(r'^algconstructors/$', ListView.as_view(model=models.AlgConstructor,template_name='algconstructors.html',context_object_name = 'algconsts'),name='algconstructors'),
    url(r'^algconstructors/([0-9]+)/$', views.GeneratorView.as_view(),name='algconstructor'),
    url(r'^talgs/$', views.AlgSearch.as_view(),name='talgs'),
    url(r'^talgs/([0-9]+)/$', views.TemplateAlgoirthmView,name='talg'),
    url(r'^createtalg/$', views.CreateTemplateAlgView.as_view(),name='ctalg'),
    url(r'^algs/([0-9]+)/$', views.AlgorithmView,name='alg'),
    url(r'^implementations/([0-9]+)/$', views.ImplementationView,name='impl'),
    url(r'^downloadimpls/([0-9]+)/$', views.DownloadImplView,name='dlimpl'),
]
