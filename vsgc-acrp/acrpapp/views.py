from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm
from .forms import DesignAppForm,StatusForm,ResponceForm,ApplicantForm,TeamForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import DesignApp, TeamMember,emp,responce,Applicant,user_profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Avg
from django.contrib.auth.models import Permission
from django.core.files.storage import default_storage
from encrypted_id import decode
from encrypted_id import ekey
from django.db.models import Count,Sum

def is_faasupport(user):
    return user.groups.filter(name='faasupport').exists()
    return True


class DesignAppListView(ListView):
    model = DesignApp
    paginate_by = 10

    def get_queryset(self):
        if is_faasupport(self.request.user):
            return DesignApp.objects.all()
        else:
            raise PermissionDenied



class DesignAppDetailView(DetailView):

    model = DesignApp

# Create your views here.
def Thankyou(request):
    return render(request,'acrpapp/Thankyou.html')

def application(request):
    form=ApplicantForm()
    if request.method == "POST":
        form=ApplicantForm(request.POST)
        if form.is_valid():
            f=form.save()
            messages.success(request, 'Submited Successfully')
            return render(request,'acrpapp/Thankyou.html',{'f':f})
        else:
            return render(request,'acrpapp/errormsg.html',{'form':form})
                      
    else:
        form = ApplicantForm()
    return render(request, 'acrpapp/application.html', {'form': form})

def index(request):
    form=DesignAppForm()
    if request.method == "POST" and request.FILES['Upload']:
        form=DesignAppForm(request.POST,request.FILES)
        file = request.FILES['Upload']
        file_name = default_storage.save(file.name, file)
        if form.is_valid():
            design_app_instance = form.save()
            for i in range(int(request.POST["num_team_members"])):
                team_member_name = request.POST["teamMemberName-" + str(i)]
                team_member_email = request.POST["teamMemberEmail-" + str(i)]
                team_member_level=request.POST["teamMemberLevel-" + str(i)]
                team_member = TeamMember(name=team_member_name, email=team_member_email,level=team_member_level,design_app=design_app_instance)
                team_member.save()
            return render(request,'acrpapp/Thankyou.html',{'f':design_app_instance})
        else:
            return render(request,'acrpapp/errormsg.html',{'form':form})
    else:
        form = DesignAppForm()
    return render(request, 'acrpapp/index.html', {'form': form})






def acrp(request):
    daDb = {}
    perms = getPermissionsFAAS(request)
    if len(perms) > 0:
        for i in perms: 
            daDb[i] = DesignApp.objects.filter(design_area=i,stat=('Application is submitted'))
        return render(request,'acrpapp/acrp_support.html',{'dApps' : daDb})
    return render(request,'acrpapp/errormsg.html')

    
def getPermissionsFAAS(request):
    daDetails = []
    if request.user.has_perm('acrpapp.view_Airport_Management_and_Planning_FAAS'):
        daDetails.append('AM')

    if request.user.has_perm('acrpapp.view_Airport_Environment_Interactions_FAAS'):
        daDetails.append('AE')

    if request.user.has_perm('acrpapp.view_Airport_Operations_and_Maintenance_FAAS'):
        daDetails.append('AO')

    if request.user.has_perm('acrpapp.view_Runway_Safety/Runway_Incursions/Runway_Excursions_FAAS'):
        daDetails.append('RS')
    return daDetails


@login_required(login_url='/login/')
def process(request):
    daDetails = []
    daDb = {}
    daResults = {}
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    perms = getPermissionsFAAS(request)
    if len(perms) > 0:
        for i in perms: 
            daDb[i] = DesignApp.objects.filter(design_area=i,stat=('Application is submitted'))
        return render(request,'acrpapp/process.html',{'dApps' : daDb,'dType':daType})




from django.shortcuts import get_object_or_404
@login_required(login_url='/login/')
def process_detail(request,ekey):
    da={'AM':78,'AE':77,'AO':79,'RS':80}
    designapp = DesignApp.objects.get_by_ekey_or_404(ekey)
    designapp_id = designapp.id
    teammember=TeamMember.objects.filter(design_app_id=designapp_id)
    status=DesignApp.objects.get(pk=designapp_id)
    f=StatusForm()
    if( status.stat=="Approved" or status.stat=="Rejected"):
        return HttpResponseRedirect("/acrp/")
    else:
        if request.method == "POST":
            status.stat = request.POST["stat"]
            status.reason=request.POST["reason"]
            status.save()
            permissions = Permission.objects.get(id=da[designapp.design_area])
            users = User.objects.filter(user_permissions=permissions)
            if status.stat=="Approved":
                for user in users:
                    up=user_profile(evalutor_id=user,design_app=designapp,stat="Pending")
                    up.save()
                    print("profile created for ",user.id)
            return HttpResponseRedirect("/process/")
        else:
            f=StatusForm()
        context={'designapp':designapp,'teammember':teammember,'f':f}
        return render(request,'acrpapp/process_details.html',context)
    
@login_required(login_url='/login/')
def processed(request):
    daDetails = []
    daDb = {}
    daResults = {}
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    perms = getPermissionsFAAS(request)
    if len(perms) > 0:
        for i in perms: 
            daDb[i] = DesignApp.objects.filter(design_area=i,stat__in=('Approved','Rejected'))
        return render(request,'acrpapp/processed.html',{'dApps' : daDb,'dType':daType})       


def processed_detail(request,ekey):
    designapp = DesignApp.objects.get_by_ekey_or_404(ekey)
    designapp_id = designapp.id
    teammember=TeamMember.objects.filter(design_app_id=designapp_id)
    status=DesignApp.objects.get(pk=designapp_id)
    f=StatusForm()
    if request.method == "POST":
        status.stat = request.POST["stat"]
        status.save()
    else:
        f=StatusForm()
    context={'designapp':designapp,'teammember':teammember,'f':f}
    return render(request,'acrpapp/processed_details.html',context)

@login_required(login_url='/login/')
def Applicanturl(request):
    daDetails = []
    daDb = {}
    daResults = {}
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    perms = getPermissionsFAAS(request)
    if len(perms) > 0:
        for i in perms: 
            daDb[i] = Applicant.objects.filter(design_area=i)
            
        return render(request,'acrpapp/Applicant.html',{'dApps' : daDb,'dType':daType})

def Applicantdetail(request,ekey):
    saved = Applicant.objects.get_by_ekey_or_404(ekey)
    applicant_id=saved.id
    print(saved.ekey)
    if request.method == "POST":
        updated_form = ApplicantForm(request.POST,request.FILES, instance = saved)
        if updated_form.is_valid():
            f = updated_form.save()
    else:
        f=ApplicantForm(instance = saved)
        return render(request,'acrpapp/ApplicantDetail.html',{'form':f})


def getPermissions(request):
    daDetails = []
    if request.user.has_perm('acrpapp.view_Airport_Management_and_Planning'):
        daDetails.append('AM')

    if request.user.has_perm('acrpapp.view_Airport_Environment_Interactions'):
        daDetails.append('AE')

    if request.user.has_perm('acrpapp.view_Airport_Operations_and_Maintenance'):
        daDetails.append('AO')

    if request.user.has_perm('acrpapp.view_Runway_Safety/Runway_Incursions/Runway_Excursions'):
        daDetails.append('RS')
    return daDetails

@login_required(login_url='/elogin/')
def acrpmembers(request):
    return render(request,'acrpapp/acrpmembers.html')


def evaluator(request):
    daDetails = []
    daDb = {}
    daResults = {}
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    perms = getPermissions(request)
    if len(perms) > 0:
        print(request.user.id)
        for i in perms: 
            d_eval = user_profile.objects.filter(evalutor_id_id=request.user.id,stat__in=('Pending','Evaluation Saved'))
            daDb[i]=[]
            for j in d_eval:
                daDb[i].append((DesignApp.objects.get(id=j.design_app_id),j))
        print('daDb',daDb)
        return render(request,'acrpapp/evaluator.html',{'dApps' : daDb,'dType':daType, 'stat':d_eval})




def evaluator_detail(request,ekey):
    f=StatusForm()
    designapp = DesignApp.objects.get_by_ekey_or_404(ekey)
    designapp_id = designapp.id
    qBank = {}
    stat=user_profile.objects.get(design_app_id=designapp_id,evalutor_id_id=request.user.id)
    if(stat.stat=="Evaluation Saved" or stat.stat=="Evaluation Completed"):
        return HttpResponseRedirect("/acrpmembers/")
    else:
        for i in range(1,36):
            qBank['quest'+str(i)]=emp.objects.get(id=i)
            res={}
        if request.method == "POST":
            print("--> ",request.POST["stat"])
            print("--> updating data for user : ",stat)
            for i in range(1,36):
                comments = 'N/A' if i == 35 else request.POST['C'+str(i)]
                res[str(i)]=responce(design_app=designapp,description=qBank['quest'+str(i)],Q_score=float(request.POST['R'+str(i)]),Q_comments=comments,evalutor_id=request.user)
                res[str(i)].save()
            stat.stat = request.POST["stat"]
            stat.save()
            return HttpResponseRedirect("/evaluator/")
        else:
            f=StatusForm()
        qBank['designapp'] = designapp
        qBank['f'] = f
        return render(request,'acrpapp/evaluator_details.html',qBank)

def saved(request,ekey):
    f=StatusForm()
    designapp = DesignApp.objects.get_by_ekey_or_404(ekey)
    designapp_id = designapp.id
    designapp=get_object_or_404(DesignApp,pk=designapp_id)
    stat=user_profile.objects.get(design_app_id=designapp_id,evalutor_id_id=request.user.id)
    if( stat.stat=="Evaluation Completed"):
        return HttpResponseRedirect("/acrpmembers/")
    else:
        if request.method == "POST":
            for i in range(1,36):
                esc = get_object_or_404(responce,design_app_id=designapp_id,description_id=i,evalutor_id_id=request.user)
                esc.Q_score = request.POST['R'+str(i)]
                esc.Q_comments = 'N/A' if i == 35 else request.POST['C'+str(i)]
                esc.save()
            stat.stat = request.POST["stat"]
            stat.save()
            return HttpResponseRedirect("/evaluator/")
        else:
            f=StatusForm()
        context={'designapp':designapp,'f':f}
        reslist=[]
        print('-> requesting data for user : ',request.user.id)
        for i in range(1,36):
            res=responce.objects.get(design_app_id=designapp_id,description_id=i, evalutor_id_id=request.user.id)
            context['res_'+str(i)]=res
        return render(request,'acrpapp/saved.html',context)
        
def user_login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('acrpmembers'))     
            
            else:
                return HttpResponse("ACCount not active!!")

        else:
            print("someone tried to login and falied!")
            print("Username : {} and Password : {}".format(username,password))
            return HttpResponse("Invalid credentials!")

    else:
        return render(request , 'registration/login.html' , {})


def evaluator_login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('acrp'))     
            
            else:
                return HttpResponse("ACCount not active!!")

        else:
            print("someone tried to login and falied!")
            return HttpResponse("Invalid credentials!")

    else:
        return render(request , 'registration/login.html' , {}) 




   
def completedsubmissions(request):
    daDetails = []
    daDb = {}
    daResults = {}
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    perms = getPermissions(request)
    if len(perms) > 0:
        for i in perms:
            d_eval = user_profile.objects.filter(evalutor_id_id=request.user.id,stat='Evaluation Completed')
            daDb[i]=[]
            for j in d_eval:
                daDb[i].append(DesignApp.objects.get(id=j.design_app_id))
        return render(request,'acrpapp/completedsubmissions.html',{'dApps' : daDb,'dType':daType})


    

def completedsubmissions_detail(request,ekey):
    designapp = DesignApp.objects.get_by_ekey_or_404(ekey)
    designapp_id = designapp.id
    context={'designapp':designapp}
    reslist=[]
    for i in range(1,36):
        res=get_object_or_404(responce,design_app_id=designapp_id,description_id=i,evalutor_id_id=request.user.id)
        context['res_'+str(i)]=res
    return render(request,'acrpapp/completedsubmissions_detail.html',context)

def sort_detail(request,ekey, evalutor_id=0):
    if evalutor_id == 0 | evalutor_id == '':
        evalutor_id = request.user.id
    designapp = DesignApp.objects.get_by_ekey_or_404(ekey)
    designapp_id = designapp.id
    context={'designapp':designapp}
    reslist=[]
    for i in range(1,36):
        res=get_object_or_404(responce,design_app_id=designapp_id,description_id=i,evalutor_id_id=evalutor_id)
        context['res_'+str(i)]=res
    return render(request,'acrpapp/completedsubmissions_detail.html',context)

def sorted_area(request):
    daDetails = []
    daDb = {}
    upDB = {}
    daResults = {}
    daAvg = {}
    daEvals = {}
    daKeys={}
    subTotalIds = [3,6,9,16,19,22,27,29,34,35]
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    if request.user.has_perm('acrpapp.view_Airport_Management_and_Planning_FAAS'):
        daDetails.append('AM')

    if request.user.has_perm('acrpapp.view_Airport_Environment_Interactions_FAAS'):
        daDetails.append('AE')

    if request.user.has_perm('acrpapp.view_Airport_Operations_and_Maintenance_FAAS'):
        daDetails.append('AO')

    if request.user.has_perm('acrpapp.view_Runway_Safety/Runway_Incursions/Runway_Excursions_FAAS'):
        daDetails.append('RS')

    for i in daDetails:
        upDB[i] = user_profile.objects.filter(stat='Evaluation Completed', design_app_id__in = (DesignApp.objects.filter(design_area=i).only('id'))).only('design_app_id').distinct()
        avgSum = 0
        avgCount = 0
        for j in range(upDB[i].count()):
            daResults[upDB[i][j].id] = responce.objects.filter(design_app_id=int(upDB[i][j].design_app_id),  evalutor_id_id = upDB[i][j].evalutor_id_id, description_id__in = subTotalIds).only('Q_score')
            temp = responce.objects.get(design_app_id=int(upDB[i][j].design_app_id), evalutor_id_id = upDB[i][j].evalutor_id_id, description_id = 35).Q_score
            if temp > 0:
                avgSum+=float(temp)
                avgCount+=1
            daEvals[upDB[i][j].evalutor_id_id] = User.objects.get(id=upDB[i][j].evalutor_id_id).username
            daKeys[upDB[i][j].design_app_id] = DesignApp.objects.get(id = int(upDB[i][j].design_app_id)).ekey
        if avgSum > 0:
            daAvg[i] = round(avgSum/avgCount,2)
        else:
            daAvg[i] = 0
    return render(request,'acrpapp/sorted_area.html',{'dAvg':daAvg, 'dApps' : upDB, 'dType':daType,'dResult' : daResults, 'evals':daEvals,'keys':daKeys})

def sorted_id(request):
    daDetails = []
    daDb = {}
    daTitles={}
    daResults = {}
    daAvg = {}
    daEvals={}
    daKeys={}
    subTotalIds = [3,6,9,16,19,22,27,29,34,35]
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    if request.user.has_perm('acrpapp.view_Airport_Management_and_Planning_FAAS'):
        daDetails.append('AM')

    if request.user.has_perm('acrpapp.view_Airport_Environment_Interactions_FAAS'):
        daDetails.append('AE')

    if request.user.has_perm('acrpapp.view_Airport_Operations_and_Maintenance_FAAS'):
        daDetails.append('AO')

    if request.user.has_perm('acrpapp.view_Runway_Safety/Runway_Incursions/Runway_Excursions_FAAS'):
        daDetails.append('RS')

    for i in daDetails: 
        daTitles[i] = DesignApp.objects.filter(design_area=i).values_list('title','Advisor1_LastName').distinct()
        for j in daTitles[i]:
            daResults[j[1]+'-'+j[0]+'-'+daType[i]] =  user_profile.objects.filter(stat='Evaluation Completed', design_app_id__in = (DesignApp.objects.filter(design_area=i, title=j[0],Advisor1_LastName=j[1],).only('id'))).only('design_app_id').distinct()
            for k in range(daResults[j[1]+'-'+j[0]+'-'+daType[i]].count()):
                daDb[daResults[j[1]+'-'+j[0]+'-'+daType[i]][k].id] = responce.objects.filter(design_app_id=int(daResults[j[1]+'-'+j[0]+'-'+daType[i]][k].design_app_id),evalutor_id_id = (daResults[j[1]+'-'+j[0]+'-'+daType[i]][k].evalutor_id_id), description_id__in = subTotalIds).only('Q_score')
                daKeys[daResults[j[1]+'-'+j[0]+'-'+daType[i]][k].design_app_id] = DesignApp.objects.get(id = int(daResults[j[1]+'-'+j[0]+'-'+daType[i]][k].design_app_id)).ekey
                daEvals[daResults[j[1]+'-'+j[0]+'-'+daType[i]][k].evalutor_id_id] = User.objects.get(id=daResults[j[1]+'-'+j[0]+'-'+daType[i]][k].evalutor_id_id).username
    return render(request,'acrpapp/sorted_id.html',{'dApps':daDb, 'dResult':daResults,'evals':daEvals,'keys':daKeys})


def avgscore_designarea(request):
    daDetails = []
    daDb = {}
    daTitles={}
    daResults = {}
    daAvg = {}
    daEvals={}
    daKeys={}
    subTotalIds = [3,6,9,16,19,22,27,29,34,35]
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    if request.user.has_perm('acrpapp.view_Airport_Management_and_Planning_FAAS'):
        daDetails.append('AM')

    if request.user.has_perm('acrpapp.view_Airport_Environment_Interactions_FAAS'):
        daDetails.append('AE')

    if request.user.has_perm('acrpapp.view_Airport_Operations_and_Maintenance_FAAS'):
        daDetails.append('AO')

    if request.user.has_perm('acrpapp.view_Runway_Safety/Runway_Incursions/Runway_Excursions_FAAS'):
        daDetails.append('RS')

    for i in daDetails: 
        daTitles[i] = DesignApp.objects.filter(design_area=i).values_list('title','Advisor1_LastName').distinct()
        print('daTitles[i]',daTitles[i])
        print('daTitles',daTitles)
        for j in daTitles[i]:
            daResults[daType[i]+'-'+j[1]+'-'+j[0]] =  user_profile.objects.filter(stat='Evaluation Completed', design_app_id__in = (DesignApp.objects.filter(design_area=i,title=j[0],Advisor1_LastName=j[1],).only('id'))).only('design_app_id').distinct()
            print("daResults[daType[i]+'-'+j[1]+'-'+j[0]]",daResults[daType[i]+'-'+j[1]+'-'+j[0]])
            avgSum = 0
            avgCount = 0
            for k in range(daResults[daType[i]+'-'+j[1]+'-'+j[0]].count()):
                daDb[daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].id] = responce.objects.filter(design_app_id=int(daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].design_app_id),evalutor_id_id = (daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].evalutor_id_id), description_id__in = subTotalIds).only('Q_score')
                temp = responce.objects.get(design_app_id=int(daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].design_app_id), evalutor_id_id = daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].evalutor_id_id, description_id = 35).Q_score
                if temp > 0:
                    avgSum+=float(temp)
                    avgCount+=1
                daEvals[daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].evalutor_id_id] = User.objects.get(id=daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].evalutor_id_id).username
                daKeys[daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].design_app_id] = DesignApp.objects.get(id = int(daResults[daType[i]+'-'+j[1]+'-'+j[0]][k].design_app_id)).ekey
            if avgSum > 0:
                daAvg[daType[i]+'-'+j[1]+'-'+j[0]] = round(avgSum/avgCount,2)
            else:
                daAvg[daType[i]+'-'+j[1]+'-'+j[0]] = 0
    return render(request,'acrpapp/avgscore_designarea.html',{'dAvg':daAvg,'dApps':daDb, 'dResult':daResults,'evals':daEvals,'keys':daKeys})

def avgscore(request):
    daDetails = []
    daDb = {}
    daTitles={}
    daResults = {}
    daAvg = {}
    daEvals={}
    daKeys={}
    subTotalIds = [3,6,9,16,19,22,27,29,34,35]
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    if request.user.has_perm('acrpapp.view_Airport_Management_and_Planning_FAAS'):
        daDetails.append('AM')

    if request.user.has_perm('acrpapp.view_Airport_Environment_Interactions_FAAS'):
        daDetails.append('AE')

    if request.user.has_perm('acrpapp.view_Airport_Operations_and_Maintenance_FAAS'):
        daDetails.append('AO')

    if request.user.has_perm('acrpapp.view_Runway_Safety/Runway_Incursions/Runway_Excursions_FAAS'):
        daDetails.append('RS')

    for i in daDetails: 
        daTitles[i] = DesignApp.objects.filter(design_area=i).values_list('title','Advisor1_LastName').distinct()
        for j in daTitles[i]:
            daResults[j[1]+'-'+daType[i]+'-'+j[0]] = user_profile.objects.filter(stat='Evaluation Completed', design_app_id__in = (DesignApp.objects.filter(design_area=i, title=j[0],Advisor1_LastName=j[1],).only('id'))).only('design_app_id').distinct()
            avgSum = 0
            avgCount = 0
            for k in range(daResults[j[1]+'-'+daType[i]+'-'+j[0]].count()):
                daDb[daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].id] = responce.objects.filter(design_app_id=int(daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].design_app_id),evalutor_id_id = (daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].evalutor_id_id), description_id__in = subTotalIds).only('Q_score')
                temp = responce.objects.get(design_app_id=int(daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].design_app_id), evalutor_id_id = daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].evalutor_id_id, description_id = 35).Q_score
                if temp > 0:
                    avgSum+=float(temp)
                    avgCount+=1
                daEvals[daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].evalutor_id_id] = User.objects.get(id=daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].evalutor_id_id).username
                daKeys[daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].design_app_id] = DesignApp.objects.get(id = int(daResults[j[1]+'-'+daType[i]+'-'+j[0]][k].design_app_id)).ekey
                if avgSum > 0:
                    daAvg[j[1]+'-'+daType[i]+'-'+j[0]] = round(avgSum/avgCount,2)
                else:
                    daAvg[j[1]+'-'+daType[i]+'-'+j[0]] = 0
    return render(request,'acrpapp/avgscore.html',{'dAvg':daAvg,'dApps':daDb, 'dResult':daResults,'evals':daEvals, 'keys':daKeys})






@login_required(login_url='/login/')
def reedit(request):
    if request.method == "POST":
        designapp_id = request.POST.get('updateValue')
        designapp=get_object_or_404(user_profile,pk=designapp_id)
        designapp.stat = "Evaluation Saved"
        designapp.save()
        return render(request,'acrpapp/statuschange.html')
    daDetails = []
    daDb = {}
    daResults = {}
    daType = {
        'AM':'Airport Management and Planning',
        'AE':'Airport Environment Interactions',
        'AO':'Airport Operations and Maintenance',
        'RS':'Runway Safety/Runway Incursions/Runway Excursions'
    }
    perms = getPermissionsFAAS(request)
    if len(perms) > 0: 
        Finaldata = user_profile.objects.filter(stat="Evaluation Completed")
        for j in range(Finaldata.count()):
            userName=User.objects.get(id=Finaldata[j].evalutor_id_id).username
            daTitles = DesignApp.objects.filter(id=Finaldata[j].design_app_id).values_list('Advisor1_LastName','Inst','id')
            daDb[userName+'-'+str(daTitles[0][0])+'-'+str(daTitles[0][1])+'-'+str(daTitles[0][2])] = Finaldata[j]
        return render(request,'acrpapp/reedit.html',{'dApps' : daDb,'dType':daType})
    else:
        print('no Permission')

