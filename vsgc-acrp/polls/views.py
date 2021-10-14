from django.shortcuts import render
from django.forms import ModelForm
from .forms import ApplicantForm,SearchForm,FacultyForm,Recommendation_fields_Form,Status,FacultyAdvisor_fields_Form
from .models import Applicant_details,Faculty_details,Recommendation_fields_details,user_profile_details,FacultyAdvisor_fields
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib import messages 
from collections import defaultdict
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from encrypted_id import decode
from encrypted_id import ekey
# Create your views here.

def index(request):
    form=ApplicantForm()
    if request.method == "POST":
        form=ApplicantForm(request.POST,request.FILES)
        email=FacultyForm(request.POST)
        if form.is_valid() and email.is_valid():
            cheque_no=request.POST.get('cheque_no')
            print(cheque_no)
            if Applicant_details.objects.filter(cheque_no=cheque_no).count() == 0:
                f=form.save()
                rqt = request.POST.keys()
                fDetails = {}
                for i in rqt:
                    fDetails[i] = request.POST[i]
                print('--> saving email...')
                #--- save ref1
                refDict = {}
                ref1Email = request.POST['Ref1_Email']
                print('ref1Email',ref1Email)
                ref2Email = request.POST['Ref2_Email']
                ref3Email = request.POST['Ref3_Email']
                refMail = Faculty_details(Ref1_Email=ref1Email, Ref2_Email=ref2Email, Ref3_Email=ref3Email, Applicant_details=f)
                refMail.save()
                if fDetails['stat'] == 'Evaluation Completed':
                    if fDetails['Citizenship'] == 'Student Visa' and fDetails['visa_expiration'] == '' and fDetails['Describe_type_and_status_if_visa_option_is_checked']=='':
                        messages.error(request,('Please fill the visa expiration date and status of your student visa '))
                    #send an email
                    else:
                        if ref1Email == '' or ref2Email == '' or ref3Email =='':
                            messages.error(request,('Please fill all three reference emails '))
                        else:
                            for i in range(1,3):
                                msg_html =render_to_string('polls/error.html',{'details' : fDetails,'url':'https://vsgcapps.odu.edu/graward/advisor/'+fDetails['cheque_no']+'/'+str(i),'name':fDetails['Ref'+str(i)+'_Name']})
                                send_mail('2021-2022 ACRP Graduate Award Application Forms','Hello '+fDetails['Ref'+str(i)+'_Name'],settings.EMAIL_HOST_USER,[fDetails['Ref'+str(i)+'_Email']],html_message=msg_html,fail_silently=False)    
                            for i in range(3,4):
                                msg_html =render_to_string('polls/advisorRecommendation.html',{'details' : fDetails,'url':'https://vsgcapps.odu.edu/graward/FacultyAdvisorRecommendation/'+fDetails['cheque_no']+'/'+'3','name':fDetails['Ref'+'3'+'_Name']})
                                send_mail('django test mail','Hello '+fDetails['Ref'+'3'+'_Name'],settings.EMAIL_HOST_USER,[fDetails['Ref'+'3'+'_Email']],html_message=msg_html,fail_silently=False)
                            return render(request,'polls/Thankyou.html',{'f':f})
                            return HttpResponseRedirect("/graward/")
                else:
                    return render(request,'polls/Thankyou.html',{'f':f})
            else:
                messages.error(request,('Enter unique Nine character id '))
        else:
            print('----> Form Not Valid....')
            print('form.errors')
            print(form.errors)
            messages.error(request,(form.errors))
    else:
        form = ApplicantForm()
        email=FacultyForm() # faculty
    return render(request, 'polls/index.html', {'form': form,'email':email})

def search(request):
    form = SearchForm()
    if request.method == "POST":
        if request.POST.get('searchValue'):
            passCode=request.POST.get('searchValue')
            try:
                x = Applicant_details.objects.get(cheque_no=passCode)
                print(x.Email)
                return render(request,'polls/searchbox.html',{'form' : form,'Applicant_details' : x})
            except Applicant_details.DoesNotExist:
                messages.error(request,('Enter unique Nine character id '))
            return render(request,'polls/searchbox.html',{'form' : form})
        else:
            print(form.errors)
    else:
        return render(request,'polls/searchbox.html',{'form' : form})





def saved_application(request,Applicant_details_id):
    saved=get_object_or_404(Applicant_details,pk=Applicant_details_id)
    saved_faculty = get_object_or_404(Faculty_details,Applicant_details_id = Applicant_details_id)
    if request.method == "POST":
        updated_form = ApplicantForm(request.POST,request.FILES, instance = saved)
        updated_faculty=FacultyForm(request.POST,instance=saved_faculty)
        # print('--> Request ', request.POST)
        Citizenship=request.POST.get('Citizenship')
        if updated_form.is_valid() and updated_faculty.is_valid():
            f = updated_form.save()
            rqt = request.POST.keys()
            fDetails = {}
            for i in rqt:
                fDetails[i] = request.POST[i]
            print('--> saving email...')
            print('Applicant data updated...')
            refDict = {}
            ref1Email = request.POST['Ref1_Email']
            ref2Email = request.POST['Ref2_Email']
            ref3Email = request.POST['Ref3_Email']
            Faculty_details.objects.filter(Applicant_details_id = Applicant_details_id).update(Ref1_Email=ref1Email, Ref2_Email=ref2Email, Ref3_Email=ref3Email)
            print('faculty data saved...')
            if fDetails['stat'] == 'Evaluation Completed':
                print('Completed')
                if fDetails['Citizenship'] == 'Student Visa' and fDetails['visa_expiration'] == '' and fDetails['Describe_type_and_status_if_visa_option_is_checked']=='':
                    messages.error(request,('Please fill the visa expiration date and status of your student visa '))
                else:
                    if ref1Email == '' or ref2Email == '' or ref3Email =='':
                        messages.error(request,('Please fill all three reference emails '))
                    else:
                        for i in range(1,3):
                            msg_html =render_to_string('polls/error.html',{'details' : fDetails,'url':'https://vsgcapps.odu.edu/graward/advisor/'+fDetails['cheque_no']+'/'+str(i),'name':fDetails['Ref'+str(i)+'_Name']})
                            send_mail('django test mail','Hello '+fDetails['Ref'+str(i)+'_Name'],settings.EMAIL_HOST_USER,[fDetails['Ref'+str(i)+'_Email']],html_message=msg_html,fail_silently=False)    
                        for i in range(3,4):
                            msg_html =render_to_string('polls/advisorRecommendation.html',{'details' : fDetails,'url':'https://vsgcapps.odu.edu/graward/FacultyAdvisorRecommendation/'+fDetails['cheque_no']+'/'+'3','name':fDetails['Ref'+'3'+'_Name']})
                            send_mail('django test mail','Hello '+fDetails['Ref'+'3'+'_Name'],settings.EMAIL_HOST_USER,[fDetails['Ref'+'3'+'_Email']],html_message=msg_html,fail_silently=False)
                        return HttpResponseRedirect("/graward/evaluator/search")
            else:
                return HttpResponseRedirect("/graward/evaluator/search")
        else:
            # return HttpResponseRedirect("/graward/errorreq")
            print(updated_form.errors)
            messages.error(request,(updated_form.errors))
            return HttpResponseRedirect('/graward/evaluator/saved_application/'+str(Applicant_details_id))
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        return render(request,'polls/saved_application.html',{'form' : saved,'f':f, 'faculty':faculty_form})
    return render(request,'polls/saved_application.html')



def advisor(request,cheque_no, ref_num):
    if (ref_num>3 or ref_num<=0):
        return render(request,'polls/errormsg.html')
    else:
        saved=get_object_or_404(Applicant_details,cheque_no=cheque_no)
        if not submitted(saved.id,ref_num):
            saved_faculty = get_object_or_404(Faculty_details,Applicant_details_id = saved.id)
            rec=Recommendation_fields_Form()
            if request.method == "POST":
                rec=Recommendation_fields_Form(request.POST,request.FILES)
                if rec.is_valid():
                    ref1 = request.POST['In_what_capacity_do_you_know_the_applicant']
                    ref2 = request.POST['How_Long_have_you_known_the_applicant']
                    ref3 = request.POST['Knowledge_of_major_field']
                    ref4 = request.POST['Research_skills']
                    ref5 = request.POST['Problem_solving_skills']
                    ref6 = request.POST['Creativity']
                    ref7 = request.POST['Leadership']
                    ref8 = request.POST['Written_communication']
                    ref9 = request.POST['Oral_communication']
                    ref10 = request.POST['Comment_on_the_ability_of_the_applicant']
                    ref11 = request.POST['Add_other_comments_to_the_evaluation']
                    ref12 = request.FILES['Signed_letter_of_reference']
                    recom=Recommendation_fields_details(In_what_capacity_do_you_know_the_applicant=ref1,How_Long_have_you_known_the_applicant=ref2,
                        Knowledge_of_major_field=ref3,Research_skills=ref4,Problem_solving_skills=ref5,Creativity=ref6,Leadership=ref7,
                        Written_communication=ref8,Oral_communication=ref9,Comment_on_the_ability_of_the_applicant=ref10,
                        Add_other_comments_to_the_evaluation=ref11,Signed_letter_of_reference=ref12,Applicant_details=saved,faculty_num=ref_num)
                    recom.save()
                    return render(request,'polls/Thankyou.html') 
                print(' !!! Form Invalid !!!')
                return render(request,'polls/errormsg.html',{'form':rec})
            else:
                f=ApplicantForm(instance = saved)
                faculty_form = FacultyForm(instance = saved_faculty)
                rec=Recommendation_fields_Form()
                return render(request,'polls/advisor.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec ,'ref_num':str(ref_num)})
        else:
            return render(request,'polls/advisor_error.html')


def FacultyAdvisorRecommendation(request,cheque_no, ref_num):
    if (ref_num>3 or ref_num<=2):
        return render(request,'polls/errormsg.html')
    else:
        saved=get_object_or_404(Applicant_details,cheque_no=cheque_no)
        if not submitted(saved.id,ref_num):
            saved_faculty = get_object_or_404(Faculty_details,Applicant_details_id = saved.id)
            rec=FacultyAdvisor_fields_Form()
            if request.method == "POST":
                rec=FacultyAdvisor_fields_Form(request.POST,request.FILES)
                if rec.is_valid():
                    ref1 = request.POST['Have_you_examined_the_applicant_proposed_researchplan']
                    ref2 = request.POST['Do_you_consider_the_applicant_research_plan_reasonable']
                    ref3 = request.POST['If_no_please_comment_1']
                    ref4 = request.POST['Research_within_the_time_frame_indicated']
                    ref5 = request.POST['If_no_please_comment_2']
                    ref6 = request.POST['Will_the_applicant_receive_academic_credit_this_work']
                    ref7 = request.POST['If_yes_please_indicate_the_nature_of_this_academic_credit']
                    ref8 = request.POST['Work_of_the_applicant_on_this_project']
                    ref9 = request.POST['Applicant_receives_this_research_award']
                    ref10 = request.FILES['Upload_your_reference_commitment_letter_signed']
                    recom=FacultyAdvisor_fields(Have_you_examined_the_applicant_proposed_researchplan=ref1,Do_you_consider_the_applicant_research_plan_reasonable=ref2,
                        If_no_please_comment_1=ref3,Research_within_the_time_frame_indicated=ref4,If_no_please_comment_2=ref5,
                        Will_the_applicant_receive_academic_credit_this_work=ref6,If_yes_please_indicate_the_nature_of_this_academic_credit=ref7,
                        Work_of_the_applicant_on_this_project=ref8,Applicant_receives_this_research_award=ref9,Upload_your_reference_commitment_letter_signed=ref10,
                        Applicant_details=saved,faculty_num=ref_num)
                    recom.save()
                    return render(request,'polls/Thankyou.html') 
                print(' !!! Form Invalid !!!')
                return render(request,'polls/errormsg.html',{'form':rec})
            else:
                f=ApplicantForm(instance = saved)
                faculty_form = FacultyForm(instance = saved_faculty)
                rec=FacultyAdvisor_fields_Form()
                return render(request,'polls/FacultyAdvisorRecommendation.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec ,'ref_num':str(ref_num)})
        else:
            return render(request,'polls/advisor_error.html')
def submitted(Applicant_details_id,ref_num):
    try:
        found=Recommendation_fields_details.objects.get(Applicant_details_id=Applicant_details_id,faculty_num=ref_num)
        print('--> Data Found')
        return True
    except:
        print('--> Data Not Found')
        return False


def submit(request):
    form = SearchForm()
    if request.method == "POST":
        if request.POST.get('searchValue'):
            passCode=request.POST.get('searchValue')
            try:
                x = Applicant_details.objects.get(cheque_no=passCode)
                print(x.Email)
                return render(request,'polls/submit.search.html',{'form' : form,'Applicant_details' : x})
            except Applicant_details.DoesNotExist:
                messages.error(request,('Enter unique Nine character id '))
            return render(request,'polls/submit.search.html',{'form' : form})
        else:
            print(form.errors)
    else:
        return render(request,'polls/submit.search.html',{'form' : form})


def submit_application(request,Applicant_details_id):
    saved=get_object_or_404(Applicant_details,pk=Applicant_details_id)
    saved_faculty = get_object_or_404(Faculty_details,Applicant_details_id = Applicant_details_id)
    if request.method == "POST":
        updated_form = ApplicantForm(request.POST,request.FILES, instance = saved)
        print('--> Request ', request.POST)
        if updated_form.is_valid():
            f = updated_form.save()
            print('Applicant data updated...')
            ref1Email = request.POST['Ref1_Email']
            ref2Email = request.POST['Ref2_Email']
            rfaEmail = request.POST['RFA_Email']
            Faculty_details.objects.filter(Applicant_details_id = Applicant_details_id).update(Ref1_Email=ref1Email, Ref2_Email=ref2Email, RFA_Email=rfaEmail)
            print('faculty data saved...')
            return render(request,'polls/Thankyou.html') 
        print(' !!! Form Invalid !!!')
        print(updated_form.errors)
        return render(request,'polls/errormsg.html',{'form':updated_form})
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        return render(request,'polls/submit_application.html',{'form' : saved,'f':f, 'faculty':faculty_form})

def reviewer_login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.user.groups.filter(name = 'polls_review_all_submissions').exists():
                    return HttpResponseRedirect('/graward/support/processed')
                else:
                    return HttpResponse("you don't have permission to view this page")
            else:
                return HttpResponse("Account not active")
        else:
            print('someone tried to ogin and failed')
            return HttpResponse("Invalid Credentials")
     
    else:
        return render(request, 'registration/project2.html' ,{})        
  
def user(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user=User.objects.get(username=username)
                print(user)
                if user.has_perm('polls.View_Polls_admin_page'):
                    return HttpResponseRedirect(reverse('support'))
                else:
                    messages.error(request,('Invalid credentials!'))
                    return render(request , 'registration/project2.html')
                    # return HttpResponse("Invalid credentials!")

            
            else:
                return HttpResponse("ACCount not active!!")

        else:
            print("someone tried to login and falied!")
            print("Username : {} and Password : {}".format(username,password))
            messages.error(request,('Invalid credentials!'))
            return render(request , 'registration/project2.html')
            # return HttpResponse("Invalid credentials!")

    else:
        return render(request , 'registration/project2.html' , {})

@login_required(login_url='/graward/elog/')
def support(request):
    return render(request,'polls/openpage.html')

def process(request):
    details={}
    details1={}
    saved=Applicant_details.objects.filter(stat="Evaluation Completed")
    for i in saved:
        vals=list(Recommendation_fields_details.objects.filter(Applicant_details_id=i.id).values_list('faculty_num', flat=True))
        vals1=list(FacultyAdvisor_fields.objects.filter(Applicant_details_id=i.id).values_list('faculty_num', flat=True))
        print("vals1",vals1)
        tmp = []
        for f in range(0,2):
            if str(f+1) in vals:
                tmp.append(str(f+1))
            else:
                tmp.append(0)
        details[i.id] = tmp
    savednew=Applicant_details.objects.filter(stat="Evaluation Completed")
    for i in savednew:
        vals1=list(FacultyAdvisor_fields.objects.filter(Applicant_details_id=i.id).values_list('faculty_num', flat=True))
        print("vals1",vals1)
        tmp1=[]
        for f in range(2,3):
            if str(f+1) in vals1:
                tmp1.append(str(f+1))
            else:
                tmp1.append(0)
        details1[i.id] = tmp1
    print(tmp)
    print(tmp1)
    return render(request,'polls/process.html',{'saved':saved, 'rec': details,'rec1':details1})

def process_detail(request,Applicant_details_id):
    saved=get_object_or_404(Applicant_details,pk=Applicant_details_id)
    refRec = []
    refRec1 = []
    saved_faculty = get_object_or_404(Faculty_details,Applicant_details_id = Applicant_details_id)
    if request.method == "POST":
        saved.stat=request.POST["stat"]
        saved.save()
        permissions = Permission.objects.get(id=95)
        users = User.objects.filter(user_permissions=permissions)
        if saved.stat=="Approved":
            for user in users:
                up=user_profile_details(eval_id=user,Applicant_details=saved,stat="Pending")
                up.save()
                print("profile created for ",user.id)
        # return HttpResponseRedirect("/process/")
        return HttpResponseRedirect("/graward/support/process")
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        try:
            rec=Recommendation_fields_details.objects.order_by('faculty_num')
            rec = rec.filter(Applicant_details_id=saved.id)
            numRec=Recommendation_fields_details.objects.filter(Applicant_details_id=saved.id).count()
            print('--> num of records : ', numRec)
            print('--> Retrieved Records :',rec)
            for i in rec:
                print('----> ',i.faculty_num)
                refRec.append(int(i.faculty_num))
            print(refRec)
            # rec=Recommendation_fields_Form(instance=rec)
        except:
            rec = 'Not Submitted'
        faculty_form1 = FacultyForm(instance = saved_faculty)
        try:
            rec1=FacultyAdvisor_fields.objects.order_by('faculty_num')
            rec1 = rec1.filter(Applicant_details_id=saved.id)
            numRec1=FacultyAdvisor_fields.objects.filter(Applicant_details_id=saved.id).count()
            print('--> num of records : ', numRec)
            print('--> Retrieved Records :',rec)
            for i in rec1:
                print('----> ',i.faculty_num)
                refRec1.append(int(i.faculty_num))
            print("refrec1",refRec1)
            # rec=Recommendation_fields_Form(instance=rec)
        except:
            rec1 = 'Not Submitted'
        return render(request,'polls/process_detail.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec,'refRec':refRec,'rec1':rec1,'refRec1':refRec1,'final':[1,2],'final1':[3]})


def processed(request):
    saved=Applicant_details.objects.filter(stat__in=("Approved","Rejected"))
    print(saved)
    return render(request,'polls/processed.html',{'saved':saved})


def processed_detail(request,Applicant_details_id):
    saved=get_object_or_404(Applicant_details,pk=Applicant_details_id)
    refRec = []
    saved_faculty = get_object_or_404(Faculty_details,Applicant_details_id = Applicant_details_id)
    f=ApplicantForm(instance = saved)
    faculty_form = FacultyForm(instance = saved_faculty)
    try:
        rec=Recommendation_fields_details.objects.order_by('faculty_num')
        rec = rec.filter(Applicant_details_id=saved.id)
        numRec=Recommendation_fields_details.objects.filter(Applicant_details_id=saved.id).count()
        print('--> num of records : ', numRec)
        print('--> Retrieved Records :',rec)
        for i in rec:
            refRec.append(int(i.faculty_num))
    except:
        rec = 'Not Submitted'
    return render(request,'polls/processed_detail.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec,'refRec':refRec,'final':[1,2,3]})

def getrecommendations(request,cheque_no,ref_num):
    saved=get_object_or_404(Applicant_details,cheque_no=cheque_no)
    saved_faculty = get_object_or_404(Faculty_details,Applicant_details_id = saved.id)
    rec=get_object_or_404(Recommendation_fields_details,Applicant_details_id=saved.id,faculty_num=ref_num)
    f=ApplicantForm(instance = saved)
    faculty_form = FacultyForm(instance = saved_faculty)
    rec=Recommendation_fields_Form(instance=rec)
    return render(request,'polls/getrecommendations.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec ,'ref_num':str(ref_num)})


def facultygetrecommendation(request,cheque_no,ref_num):
    saved=get_object_or_404(Applicant_details,cheque_no=cheque_no)
    saved_faculty = get_object_or_404(Faculty_details,Applicant_details_id = saved.id)
    rec=get_object_or_404(FacultyAdvisor_fields,Applicant_details_id=saved.id,faculty_num=ref_num)
    f=ApplicantForm(instance = saved)
    faculty_form = FacultyForm(instance = saved_faculty)
    rec=FacultyAdvisor_fields_Form(instance=rec)
    return render(request,'polls/facultygetrecommendations.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec ,'ref_num':str(ref_num)})

def RecommendationsAllInternal(request):
    saved=Applicant_details.objects.filter(stat=("Approved"))
    print(saved)
    return render(request,'polls/RecommendationsAllInternal.html',{'saved':saved})


@login_required(login_url='/graward/log/')
def evaluators(request):
    permission = Permission.objects.get(name='view Completed Submissions')
    if request.user.groups.filter(name='polls_evaluators_completed_submissions').exists():
        print('User belongs to the group')
    if 'polls.view_polls_completed_submissions' in request.user.get_group_permissions():
        perm = True
        print('User has permission to view completed submissions')
    else:
        perm = False
        print('User has NO permission to view completed submissions')
    return render(request,'polls/evaluators.html', context = {"perm":perm})



def EvaluateSubmissions(request):
    daDb = {}
    d_eval=user_profile_details.objects.filter(eval_id_id=request.user.id,stat__in=('Pending','Evaluation Saved'))
    for i in range(d_eval.count()):
        applicantId = d_eval[i].Applicant_details_id
        stat=user_profile_details.objects.get(Applicant_details_id=applicantId,eval_id_id=request.user.id).stat
        student=Applicant_details.objects.get(id = int(applicantId))
        if str(applicantId) not in daDb:
            daDb[str(applicantId)]={}
        daDb[str(applicantId)]["stat"] =stat
        daDb[str(applicantId)]["student"] =student 
    print('daDb',daDb)
    return render(request,'polls/EvaluateSubmissions.html',{'dApps' : daDb})




def compute_average(request):
    d_eval = user_profile_details.objects.filter(stat='Evaluation Completed')
    applicantNew1={}
    applicantNew={}
    # from the valid items iterate and populate the two data structures
    for i in range(d_eval.count()):
        applicantId = d_eval[i].Applicant_details_id
        evaluatorId = d_eval[i].eval_id_id
        score = d_eval[i].ranking
        print("score",score)
        name =Applicant_details.objects.get(id = int(applicantId)).App_FirstName
        profile=User.objects.get(id = int(evaluatorId)).username
        if str(applicantId) not in applicantNew1:
            applicantNew1[str(applicantId)] = {}
            applicantNew[str(applicantId)] = {}
        applicantNew1[str(applicantId)]["name"] = name
        applicantNew1[str(applicantId)][evaluatorId] = {profile:score}
        print("old",applicantNew1)
        # applicantNew1[str(applicantId)]["score"] = score
    # applicantNew = applicantNew1
    for k,l in applicantNew1.items():
        count=0
        e=0
        for p,m in l.items():
            if type(m) is dict: 
                for q,w in m.items():
                    e = e+float(w)
                    print('e',e)
                    count = count+1  
                    newe = e/count
                    print('newe',newe)
                    print('count',count)
                    applicantNew[k]["total"] = newe
                    print('applicantNew',applicantNew)
    for r,t in applicantNew.items():
        applicantNew1[r]["average"] = t
    print("new",applicantNew1)
    return render(request,'polls/compute_average.html',{'applicantNew':applicantNew1})
    

def compute_average_detail(request,a_id):
    applicant={}
    applicantNew1={}
    applicant_info=get_object_or_404(Applicant_details,pk=a_id)
    d_eval=user_profile_details.objects.filter(Applicant_details_id=a_id)
    for i in range(d_eval.count()):
        evaluatorId = d_eval[i].eval_id_id
        score = d_eval[i].ranking
        profile=User.objects.get(id = int(evaluatorId)).username
        if str(a_id) not in applicantNew1:
            applicantNew1[str(a_id)] = {}
        applicantNew1[str(a_id)][evaluatorId] = {profile:score}
        print("dict2",applicantNew1) 
    return render(request,'polls/compute_average_detail.html',{'applicant':applicant_info,'eval':d_eval,'applicantNew':applicantNew1})




def EvaluateSubmissions_detail(request,Applicant_details_id):
    user_data=user_profile_details.objects.get(Applicant_details_id=Applicant_details_id,eval_id_id=request.user.id)
    stat=Status()
    applicant=Applicant_details.objects.get(pk=Applicant_details_id)
    applicant_info=get_object_or_404(Applicant_details,pk=Applicant_details_id)
    profile=User.objects.get(id=user_data.eval_id_id).username
    print(profile)
    if(user_data.stat=="Evaluation Completed"):
        return HttpResponseRedirect("/evaluators/")
    else:    
        if request.method == "POST":
            user_data.stat = request.POST["stat"]
            print(user_data.stat)
            user_data.ranking = request.POST["ranking"]
            user_data.save()
            return HttpResponseRedirect("/graward/EvaluateSubmissions")
        else:
            stat=Status()
            f=ApplicantForm(instance = applicant_info)
        return render(request,'polls/EvaluateSubmissions_detail.html',{'f':f,'applicant':applicant,'form':applicant_info,'user':user_data,'stat':stat,'profile':profile})

def EvaluateSubmissionsSaved_detail(request,Applicant_details_id):
    user_data=user_profile_details.objects.get(Applicant_details_id=Applicant_details_id,eval_id_id=request.user.id)
    stat=Status()
    applicant=Applicant_details.objects.get(pk=Applicant_details_id)
    applicant_info=get_object_or_404(Applicant_details,pk=Applicant_details_id)
    profile=User.objects.get(id=user_data.eval_id_id).username
    print(profile)
    if(user_data.stat=="Evaluation Completed"):
        return HttpResponseRedirect("/evaluators/")
    else:    
        if request.method == "POST":
            user_data.stat = request.POST["stat"]
            print(user_data.stat)
            user_data.ranking = request.POST["ranking"]
            user_data.save()
            return HttpResponseRedirect("/graward/EvaluateSubmissions")
        else:
            stat=Status(instance=user_data)
            f=ApplicantForm(instance = applicant_info)
        return render(request,'polls/EvaluateSubmissionsSaved_detail.html',{'f':f,'applicant':applicant,'form':applicant_info,'user':user_data,'stat':stat,'profile':profile})




def user_prof(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user=User.objects.get(username=username)
                print(user)
                return HttpResponseRedirect(reverse('evaluators'))     
            
            else:
                return HttpResponse("ACCount not active!!")

        else:
            print("someone tried to login and falied!")
            print("Username : {} and Password : {}".format(username,password))
            return HttpResponse("Invalid credentials!")

    else:
        return render(request , 'registration/project2.html' , {})


def CompletedSubmissions(request):
    d_eval = user_profile_details.objects.filter(stat='Evaluation Completed')
    applicantNew1={}
    applicantNew={}
    profile={}
    # from the valid items iterate and populate the two data structures
    for i in range(d_eval.count()):
        applicantId = d_eval[i].Applicant__details_id
        evaluatorId = d_eval[i].eval_id_id
        score = d_eval[i].ranking
        print("score",score)
        name =Applicant__details.objects.get(id = int(applicantId)).App_FirstName
        profile=User.objects.get(id = int(evaluatorId)).username
        if str(applicantId) not in applicantNew1:
            applicantNew1[str(applicantId)] = {}
            applicantNew[str(applicantId)] = {}
        applicantNew1[str(applicantId)]["name"] = name
        applicantNew1[str(applicantId)][evaluatorId] = {profile:score}
        print("old",applicantNew1)
        # applicantNew1[str(applicantId)]["score"] = score
    # applicantNew = applicantNew1
    for k,l in applicantNew1.items():
        e=0
        count=0
        for p,m in l.items():
            if type(m) is dict:   
                for q,w in m.items():
                    count = count+1
                    e = e+float(w)
                    newe = e/count
                    applicantNew[k]["total"] = newe
                    print('applicantNew',applicantNew)
    for r,t in applicantNew.items():
        applicantNew1[r]["average"] = t
    print("new",applicantNew1)
    return render(request,'polls/CompletedSubmissions.html',{'applicantNew':applicantNew1})

# def enableCompleteSubmissions(request):
#   print(request.user.id)
#   if User.objects.get(id = request.user.id).is_superuser == 1:
#       # Enable the permissions to all users in group 'polls_evaluators_completed_submissions'
#       new_group, created = Group.objects.get_or_create(name='new_group')
#       messages.error(request,('permission Enabled '))
#       ct = ContentType.objects.get_for_model(user_profile)
#       permission = Permission.objects.create(codename='can_add_project',
#                                    name='Can add project',
#                                    content_type=ct)
#       new_group.permissions.add(permission)
#       print('permission Enabled')
#       # notify user with permission
#   else:
#       # no permission to access this feature
#       messages.error(request,('User has no permission '))
#       print('User has no permission')
#   return redirect('/acrpsite/acrp/support')


def enableCompleteSubmissions(request):
    print(request.user.id)
    if request.user.has_perm('polls.View_Polls_admin_page'):
    # if User.objects.get(id = request.user.id).is_superuser == 1:
        # Enable the permissions to all users in group 'polls_evaluators_completed_submissions'
        eval_group = Group.objects.get(name = 'polls_evaluators_completed_submissions')
        eval_permission = Permission.objects.get(name='view Completed Submissions')
        eval_group.permissions.add(eval_permission)
        messages.error(request,('permission Enabled '))
        return redirect('/graward/support/')
        print('permission Enabled')
        # notify user with permission
    else:
        # no permission to access this feature
        messages.error(request,('User has no permission '))
        print('User has no permission')
    return redirect('/graward/support/')


def Average_score(request):
    d_eval = user_profile_details.objects.filter(stat='Evaluation Completed')
    applicantNew1={}
    applicantNew={}
    prof={}
    # from the valid items iterate and populate the two data structures
    for i in range(d_eval.count()):
        applicantId = d_eval[i].Applicant_details_id
        evaluatorId = d_eval[i].eval_id_id
        score = d_eval[i].ranking
        print("score",score)
        name =Applicant_details.objects.get(id = int(applicantId))
        profile=User.objects.get(id = int(evaluatorId)).username
        if str(applicantId) not in applicantNew1:
            applicantNew1[str(applicantId)] = {}
            applicantNew[str(applicantId)] = {} 
            prof[str(applicantId)] = {}
        applicantNew1[str(applicantId)]["name"] = name
        prof[str(applicantId)][evaluatorId]={profile:score}
    for k,l in prof.items():
        e=0
        count=0
        for q,w in l.items():
            for a,b in w.items():
                count = count+1
                e = e+float(b)
                newe = e/count
                applicantNew[k]= newe
                print('applicantNew',applicantNew)
    for r,t in applicantNew.items():
        applicantNew1[r]["average"]= t
    print("new",applicantNew1)
    return render(request,'polls/AverageScore.html',{'applicantNew':applicantNew1})

def Last_Name(request):
    d_eval = user_profile_details.objects.filter(stat='Evaluation Completed')
    applicantNew1={}
    applicantNew={}
    prof={}
    # from the valid items iterate and populate the two data structures
    for i in range(d_eval.count()):
        applicantId = d_eval[i].Applicant_details_id
        evaluatorId = d_eval[i].eval_id_id
        score = d_eval[i].ranking
        print("score",score)
        name =Applicant_details.objects.get(id = int(applicantId))
        profile=User.objects.get(id = int(evaluatorId)).username
        if str(applicantId) not in applicantNew1:
            applicantNew1[str(applicantId)] = {}
            applicantNew[str(applicantId)] = {} 
            prof[str(applicantId)] = {}
        applicantNew1[str(applicantId)]["name"] = name
        prof[str(applicantId)][evaluatorId]={profile:score}
    for k,l in prof.items():
        e=0
        count=0
        for q,w in l.items():
            for a,b in w.items():
                count = count+1
                e = e+float(b)
                newe = e/count
                applicantNew[k] = newe
                print('applicantNew',applicantNew)
    for r,t in applicantNew.items():
        applicantNew1[r]["average"]= t
    print("new",applicantNew1)
    return render(request,'polls/LastName.html',{'applicantNew':applicantNew1})



def reedit(request):
    if request.method == "POST":
        id=request.POST.get('updateValue')
        applicant=get_object_or_404(user_profile_details,pk=id)
        applicant.stat="Evaluation Saved"
        applicant.save()
        return render(request,'polls/statuschange.html')
    results={}
    Finaldata=user_profile_details.objects.filter(stat="Evaluation Completed")
    for i in range(Finaldata.count()):
        username=User.objects.get(id=Finaldata[i].eval_id_id).username
        details=Applicant_details.objects.filter(id=Finaldata[i].Applicant_details_id).values_list('App_LastName','clg_or_univ_Enrolled','Major_Field')
        print('details',details)
        results[username+'-'+str(details[0][0])+'-'+str(details[0][1])+'-'+str(details[0][2])]=Finaldata[i]
    return render(request,'polls/reedit.html',{'dApps' : results})


def adminupdatescore(request):
    results={}
    Finaldata=user_profile_details.objects.filter(stat="Evaluation Completed")
    print(Finaldata)
    for i in range(Finaldata.count()):
        applicantId = Finaldata[i].Applicant_details_id
        evaluatorId = Finaldata[i].eval_id_id
        score = Finaldata[i].ranking
        details=Applicant_details.objects.get(id=int(applicantId))
        profile=User.objects.get(id = int(evaluatorId)).username
        print(details)
        print(profile)
        if str(applicantId) not in results:
            results[str(applicantId)]={}
        results[str(applicantId)]["details"]=details
        results[str(applicantId)][evaluatorId]={profile : score}
        print("results",results)
    return render(request,'polls/adminupdatescore.html',{'results':results})

def evaluatorupdatescore(request):
    results={}
    Finaldata=user_profile_details.objects.filter(stat="Evaluation Completed")
    print(Finaldata)
    for i in range(Finaldata.count()):
        applicantId = Finaldata[i].Applicant_details_id
        evaluatorId = Finaldata[i].eval_id_id
        score = Finaldata[i].ranking
        details=Applicant_details.objects.get(id=int(applicantId))
        advisor=user_profile_details.objects.get(Applicant_details_id=int(applicantId),eval_id_id=int(evaluatorId))
        profile=User.objects.get(id = int(evaluatorId)).username
        print(details)
        print(profile)
        if str(applicantId) not in results:
            results[str(applicantId)]={}
        results[str(applicantId)]["details"]=details
        results[str(applicantId)][evaluatorId]={advisor:profile}
        print("results",results)
    return render(request,'polls/evaluatorupdatescore.html',{'results':results})


def EvaluateSaved_detail(request,Applicant_details_id,eval_id):
    user_data=user_profile_details.objects.get(Applicant_details_id=Applicant_details_id,eval_id_id=eval_id)
    print('EvaluateSaved_detail',user_data)
    stat=Status()
    applicant=Applicant_details.objects.get(pk=Applicant_details_id)
    applicant_info=get_object_or_404(Applicant_details,pk=Applicant_details_id)
    profile=User.objects.get(id=user_data.eval_id_id).username
    print(profile)  
    if request.method == "POST":
        user_data.stat = request.POST["stat"]
        print(user_data.stat)
        user_data.ranking = request.POST["ranking"]
        user_data.save()
        return HttpResponseRedirect("/graward/support/evaluatorupdatescore")
    else:
        stat=Status(instance=user_data)
        f=ApplicantForm(instance = applicant_info)
    return render(request,'polls/EvaluateSubmissionsSaved_detail.html',{'f':f,'applicant':applicant,'form':applicant_info,'user':user_data,'stat':stat,'profile':profile})

def reference_reminder(request):
    appli=Applicant_details.objects.filter(stat="Evaluation Completed")
    for i in range(appli.count()):
        applicantId = appli[i].id
        applicantname = appli[i].App_FirstName
        print(applicantId)
        rec1=Recommendation_fields_details.objects.filter(Applicant_details_id=applicantId,faculty_num=1)
        rec2=Recommendation_fields_details.objects.filter(Applicant_details_id=applicantId,faculty_num=2)
        rec3=FacultyAdvisor_fields.objects.filter(Applicant_details_id=applicantId,faculty_num=3)
        if rec1.count()==0:
            fac1=get_object_or_404(Faculty_details,Applicant_details_id=applicantId)
            msg_html=render_to_string('polls/reminder.html',{'details' : applicantname,'url':'https://vsgcapps.odu.edu/graward/advisor/'+appli[i].cheque_no+'/'+'1','name':appli[i].Ref1_Name})
            send_mail('2021-2022 ACRP Graduate Award Application Forms','Hello '+appli[i].Ref1_Name,settings.EMAIL_HOST_USER,[fac1.Ref1_Email],html_message=msg_html,fail_silently=False)
        if rec2.count()==0:
            fac2=get_object_or_404(Faculty_details,Applicant_details_id=applicantId)
            msg_html=render_to_string('polls/reminder.html',{'details' : applicantname,'url':'https://vsgcapps.odu.edu/graward/advisor/'+appli[i].cheque_no+'/'+'2','name':appli[i].Ref2_Name})
            send_mail('2021-2022 ACRP Graduate Award Application Forms','Hello '+appli[i].Ref2_Name,settings.EMAIL_HOST_USER,[fac2.Ref2_Email],html_message=msg_html,fail_silently=False)
        if rec3.count()==0:
            fac3=get_object_or_404(Faculty_details,Applicant_details_id=applicantId)
            msg_html=render_to_string('polls/advisorRecommendation.html',{'details' : applicantname,'url':'https://vsgcapps.odu.edu/graward/FacultyAdvisorRecommendation/'+appli[i].cheque_no+'/'+'3','name':appli[i].Ref3_Name})
            send_mail('2021-2022 ACRP Graduate Award Application Forms','Hello '+appli[i].Ref3_Name,settings.EMAIL_HOST_USER,[fac3.Ref3_Email],html_message=msg_html,fail_silently=False)
    return render(request,'polls/reference_reminder.html')
    # advisor=faculty.objects.get(Applicant_id=)


# def user_login(request):
#   if request.method == 'POST':
#       username = request.POST.get('Username')
#       password = request.POST.get('Password')
#       user = authenticate(username = username , password = password)
#       print(user)
#       if user is not None:
#           if user.is_active:
#               login(request, user)
#               if request.user.has_perm('polls.view_evaluator_page'):
#                   return HttpResponseRedirect("/acrpsite/acrp/support/evaluatorupdatescore")
#                   print('sales users landing page')
#                   # sales users landing page
#               elif request.user.has_perm('polls.view_admin_page'):
#                   return HttpResponseRedirect("/acrpsite/acrp/support/adminupdatescore")
#                   print('operations users landing page')
#               else:
#                   return HttpResponse("Sorry!You don't have permission to access this page")

#       else:
#           print("someone tried to login and falied!")
#           print("Username : {} and Password : {}".format(username,password))
#           return HttpResponse("Invalid credentials!")
#   else:
#       return render(request , 'registration/login.html' , {})

# if request.user.has_perm('acrpapp.view_Airport_Management_and_Planning_FAAS'):
# def Average_score(request):
#     d_eval = user_profile.objects.filter(stat='Evaluation Completed')
#     applicantNew1={}
#     applicantNew={}
#     # from the valid items iterate and populate the two data structures
#     for i in range(d_eval.count()):
#         applicantId = d_eval[i].Applicant_id
#         evaluatorId = d_eval[i].eval_id_id
#         score = d_eval[i].ranking
#         print("score",score)
#         name =Applicant.objects.get(id = int(applicantId))
#         profile=User.objects.get(id = int(evaluatorId)).username
#         if str(applicantId) not in applicantNew1:
#             applicantNew1[str(applicantId)] = {}
#             applicantNew[str(applicantId)] = {}
        
#         applicantNew1[str(applicantId)]["name"] = name
#         applicantNew1[str(applicantId)][evaluatorId] = {profile:score}
#         print("old",applicantNew1)
#         # applicantNew1[str(applicantId)]["score"] = score
#     # applicantNew = applicantNew1
#     for k,l in applicantNew1.items():
#         e=0
#         count=0
#         for p,m in l.items():
#             if type(m) is dict:   
#                 for q,w in m.items():
#                     count = count+1
#                     e = e+int(w)
#                     e = e/count
#                     applicantNew[k]["total"] = e
#                     print('applicantNew',applicantNew)
#     for r,t in applicantNew.items():
#         applicantNew1[r]["average"]= t
#     print("new",applicantNew1)
#     return render(request,'polls/AverageScore.html',{'applicantNew':applicantNew1,'new':applicantNew})

