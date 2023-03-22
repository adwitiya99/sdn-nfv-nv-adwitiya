from django.urls import path
from policymanagement import views

urlpatterns = [
    path('evidence/add/', views.addata, name='addata'),
    path('evidence/manage/', views.managedata, name='managedata'),

    path('manage/', views.managepolicy, name='managepolicy'),
    path('verify/', views.verifypolicy, name='verifypolicy'),

    path('report/', views.reportmanagement, name='reportmanagement'),
    path('report/<int:report_id>/', views.verificationreportdetails, name='policyverificationreport'),
]
