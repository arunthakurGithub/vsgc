from django.contrib import admin
from acrpapp.models import DesignApp,DesignApp1,DesignApp2,DesignApp3
from django.contrib.auth.models import Permission



class dApps1(admin.ModelAdmin):
	def get_queryset(self, request):
		if request.user.has_perm('acrpapp.view_Airport_Environment_Interactions'):
			query = super(dApps1, self).get_queryset(request)
			filtered_query = query.filter(design_area='AE')
			return filtered_query
	list_display = ('title', 'design_area', 'Inst', 'Upload')

class dApps2(admin.ModelAdmin):
	def get_queryset(self, request):
		if request.user.has_perm('acrpapp.view_Airport_Management_and_Planning'):
			query = super(dApps2, self).get_queryset(request)
			filtered_query = query.filter(design_area='AM')
			return filtered_query
	list_display = ('title', 'design_area', 'Inst', 'Upload')

class dApps3(admin.ModelAdmin):
	def get_queryset(self, request):
		if request.user.has_perm('acrpapp.view_Airport_Operations_and_Maintenance'):
			query = super(dApps3, self).get_queryset(request)
			filtered_query = query.filter(design_area='AP')
			return filtered_query
	list_display = ('title', 'design_area', 'Inst', 'Upload')


class dApps4(admin.ModelAdmin):
	def get_queryset(self, request):
		if request.user.has_perm('acrpapp.view_Runway_Safety/Runway_Incursions/Runway_Excursions'):
			query = super(dApps4, self).get_queryset(request)
			filtered_query = query.filter(design_area='RS')
			return filtered_query
	list_display = ('title', 'design_area', 'Inst', 'Upload')

# Register your models here.
admin.site.register(DesignApp,dApps1)
admin.site.register(DesignApp1,dApps2)
admin.site.register(DesignApp2,dApps3)
admin.site.register(DesignApp3,dApps4)
admin.site.register(Permission)

# Register your models here.
