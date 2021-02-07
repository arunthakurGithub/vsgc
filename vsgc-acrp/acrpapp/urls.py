from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
# from django.contrib.auth import views
urlpatterns = [
    path('', views.index, name='index'),
    path('application/', views.application, name='application'),
    path('<int:pk>/', views.DesignAppDetailView.as_view(), name='designapp_detail'),
    path('login/',views.evaluator_login,name='evaluator_login'),
    path('acrp/', views.acrp, name='acrp'),
    path('process/', views.process, name='process'),
    path('process_detail/<str:ekey>/', views.process_detail, name='process_detail'),
    path('processed/', views.processed, name='processed'),
    path('processed_detail/<str:ekey>/', views.processed_detail, name='processed_detail'),
    path('Applicant/', views.Applicanturl, name='Applicanturl'),
    path('Applicantdetail/<str:ekey>/', views.Applicantdetail, name='Applicantdetail'),
    path('elogin/',views.user_login,name='user_login'),
    path('acrpmembers/', views.acrpmembers, name='acrpmembers'),
    path('evaluator/', views.evaluator, name='evaluator'),
    path('sorted/', views.sorted_id, name='sorted_id'),
    path('sorted_area/', views.sorted_area, name='sorted_area'),
    path('avgscore_designarea/', views.avgscore_designarea, name='avgscore_designarea'),
    path('avgscore/', views.avgscore, name='avgscore'),
    path('evaluator_detail/<str:ekey>/', views.evaluator_detail, name='evaluator_detail'),
    path('saved/<str:ekey>/', views.saved, name='saved'),
    path('completedsubmissions/', views.completedsubmissions, name='completedsubmissions'),
    path('completedsubmissions_detail/<str:ekey>/', views.completedsubmissions_detail, name='completedsubmissions_detail'),
    path('completedsubmissions_detail/<str:ekey>/<int:evalutor_id>/', views.sort_detail, name='sort_detail'),
    path('reedit/',views.reedit,name='reedit')
    
]
