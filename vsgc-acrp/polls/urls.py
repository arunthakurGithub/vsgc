from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('index', views.index, name='index'),
    path('evaluator/search', views.search, name='search'),
    path('evaluator/saved_application/<int:Applicant_id>/', views.saved_application, name='saved_application'),
    path('evaluator/submit', views.submit, name='submit'),
    path('evaluator/submit_application/<int:Applicant_id>/', views.submit_application, name='submit_application'),
    path('advisor/<str:cheque_no>/<int:ref_num>', views.advisor, name='advisor'),
    path('', TemplateView.as_view(template_name='polls/urls.html')),
    path('elog/',views.user,name='user'),
    path('errorvisa/', TemplateView.as_view(template_name='polls/errorvisa.html')),

    # path('', TemplateView.as_view(template_name='polls/mainpage.html')),
    path('support/process', views.process, name='process'),
    path('support/process_detail/<int:Applicant_id>/', views.process_detail, name='process_detail'),
    path('support/processed', views.processed, name='processed'),
    path('support/processed_detail/<int:Applicant_id>/', views.processed_detail, name='processed_detail'),
    path('recom/<str:cheque_no>/<int:ref_num>', views.getrecommendations, name='getrecommendations'),
    path('support/', views.support,name='support'),
    path('openview', views.RecommendationsAllInternal, name=' RecommendationsAllInternal'),
    path('evaluators', views.evaluators,name='evaluators'),
    path('EvaluateSubmissions', views.EvaluateSubmissions, name='EvaluateSubmissions'),
    path('EvaluateSubmissions_detail/<int:Applicant_id>/', views.EvaluateSubmissions_detail, name='EvaluateSubmissions_detail'),
    path('EvaluateSubmissionsSaved_detail/<int:Applicant_id>/', views.EvaluateSubmissionsSaved_detail, name='EvaluateSubmissionsSaved_detail'),
    path('CompletedSubmissions', views.CompletedSubmissions, name='CompletedSubmissions'),
    path('compute_average_detail/<int:a_id>/', views.compute_average_detail, name='compute_average_detail'),
    path('log/',views.user_prof,name='user_prof'),
    path('support/compute_average', views.compute_average, name='compute_average'),
    path('support/compute_average_detail/<int:a_id>/', views.compute_average_detail, name='compute_average_detail'),
    path('support/enable',views.enableCompleteSubmissions,name='enableCompleteSubmissions'),
    path('support/averagescore',views.Average_score,name='Average_score'),
    path('support/lastname',views.Last_Name,name='Last_Name'),
    path('support/reedit',views.reedit,name='reedit'),
    path('support/adminupdatescore',views.adminupdatescore,name='updatescore'),
    path('support/evaluatorupdatescore',views.evaluatorupdatescore,name='evaluatorupdatescore'),
    path('support/reference_reminder',views.reference_reminder,name='reference_reminder'),
    path('support/EvaluateSubmissionsSaved_detail/<int:Applicant_id>/', views.EvaluateSubmissionsSaved_detail, name='EvaluateSubmissionsSaved_detail'),
    # path('acrp/support/userlogin/',views.user_login,name='user_login'),
    path('support/EvaluateSaved_detail/<int:Applicant_id>/<int:eval_id>/',views.EvaluateSaved_detail,name='EvaluateSaved_detail'),
    # path('acrp/support/EvaluateSaved_detail/<int:Applicant_id>/', views.EvaluateSaved_detail, name='EvaluateSaved_detail'),
    # path('acrp/login/', views.login, name ='login'), 



]