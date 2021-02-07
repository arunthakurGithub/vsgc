from django.shortcuts import render
from django.forms import ModelForm
from .forms import ApplicantForm,ApplicantFilter, SearchForm,FacultyForm,Recommendation_fields_Form
from .models import Applicant,Faculty,Recommendation_fields
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, get_template

# Create your views here.
def index(request):
    form=ApplicantForm()
    if request.method == "POST":
        form=ApplicantForm(request.POST,request.FILES)
        email=FacultyForm(request.POST)
        print(request.POST.get('stat')) 
        if form.is_valid() and email.is_valid():
            f=form.save()
            rqt = request.POST.keys()
            fDetails = {}
            for i in rqt:
                fDetails[i] = request.POST[i]
            print('--> saving email...')
            #--- save ref1
            refDict = {}
            ref1Email = request.POST['Ref1_Email']
            ref2Email = request.POST['Ref2_Email']
            ref3Email = request.POST['Ref3_Email']
            refMail = Faculty(Ref1_Email=ref1Email, Ref2_Email=ref2Email, Ref3_Email=ref3Email, Applicant=f)
            refMail.save()
            if fDetails['stat'] == 'Evaluation Completed':
                #send an email
                for i in range(1,4):
                    msg_html =render_to_string('polls/error.html',{'details' : fDetails,'url':'http://127.0.0.1:8000/advisor/'+fDetails['cheque_no']+'/'+str(i)})
                    send_mail('django test mail','Hello '+fDetails['Ref'+str(i)+'_Name'],settings.EMAIL_HOST_USER,[fDetails['Ref'+str(i)+'_Email']],html_message=msg_html,fail_silently=False)    
            return render(request,'polls/Thankyou.html',{'f':f})
        else:
            print('----> Form Not Valid....')
            print('form.errors')
            print(form.errors)
            return render(request,'polls/errormsg.html',{'form':form})
    else:
        form = ApplicantForm()
        email=FacultyForm() # faculty
    return render(request, 'polls/index.html', {'form': form,'email':email})


def search(request):
    form = SearchForm()
    if request.method == "POST":
        passCode = request.POST.get('searchValue')
        print(passCode)
        x = Applicant.objects.get(cheque_no=passCode)
        print(x.Email)
        return render(request,'polls/searchbox.html',{'form' : form,'Applicant' : x})
    else:
        return render(request,'polls/searchbox.html',{'form' : form})


def saved_application(request,Applicant_id):
    saved=get_object_or_404(Applicant,pk=Applicant_id)
    saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
    if request.method == "POST":
        updated_form = ApplicantForm(request.POST,request.FILES, instance = saved)
        print('--> Request ', request.POST)
        if updated_form.is_valid():
            f = updated_form.save()
            print('Applicant data updated...')
            ref1Email = request.POST['Ref1_Email']
            ref2Email = request.POST['Ref2_Email']
            ref3Email = request.POST['Ref3_Email']
            Faculty.objects.filter(Applicant_id = Applicant_id).update(Ref1_Email=ref1Email, Ref2_Email=ref2Email, Ref3_Email=ref3Email)
            print('faculty data saved...')
            return render(request,'polls/Thankyou.html') 
        print(' !!! Form Invalid !!!')
        print(updated_form.errors)
        return render(request,'polls/errormsg.html',{'form':updated_form})
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        return render(request,'polls/saved_application.html',{'form' : saved,'f':f, 'faculty':faculty_form})


def advisor(request,cheque_no, ref_num):
    if (ref_num>3 or ref_num<=0):
        return render(request,'polls/errormsg.html')
    else:
        if not submitted(cheque_no,ref_num):          
            saved=get_object_or_404(Applicant,cheque_no=cheque_no)
            saved_faculty = get_object_or_404(Faculty,Applicant_id = saved.id)
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
                    recom=Recommendation_fields(In_what_capacity_do_you_know_the_applicant=ref1,How_Long_have_you_known_the_applicant=ref2,
                        Knowledge_of_major_field=ref3,Research_skills=ref4,Problem_solving_skills=ref5,Creativity=ref6,Leadership=ref7,
                        Written_communication=ref8,Oral_communication=ref9,Comment_on_the_ability_of_the_applicant=ref10,
                        Add_other_comments_to_the_evaluation=ref11,Signed_letter_of_reference=ref12,Applicant=saved,faculty_num=ref_num)
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
            return render(request,'polls/errormsg.html')


 
def submitted(Applicant_id,ref_num):
    try:
        found=Recommendation_fields.objects.get(Applicant_id=Applicant_id,faculty_num=ref_num)
        print('--> Data Found')
        return True
    except:
        print('--> Data Not Found')
        return False

def submit(request):
    form = SearchForm()
    if request.method == "POST":
        passCode = request.POST.get('searchValue')
        print(passCode)
        x = Applicant.objects.get(cheque_no=passCode)
        print(x.Email)
        return render(request,'polls/submit.search.html',{'form' : form,'Applicant' : x})
    else:
        return render(request,'polls/submit.search.html',{'form' : form})



def submit_application(request,Applicant_id):
    saved=get_object_or_404(Applicant,pk=Applicant_id)
    saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
    if request.method == "POST":
        updated_form = ApplicantForm(request.POST,request.FILES, instance = saved)
        print('--> Request ', request.POST)
        if updated_form.is_valid():
            f = updated_form.save()
            print('Applicant data updated...')
            ref1Email = request.POST['Ref1_Email']
            ref2Email = request.POST['Ref2_Email']
            rfaEmail = request.POST['RFA_Email']
            Faculty.objects.filter(Applicant_id = Applicant_id).update(Ref1_Email=ref1Email, Ref2_Email=ref2Email, RFA_Email=rfaEmail)
            print('faculty data saved...')
            return render(request,'polls/Thankyou.html') 
        print(' !!! Form Invalid !!!')
        print(updated_form.errors)
        return render(request,'polls/errormsg.html',{'form':updated_form})
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        return render(request,'polls/submit_application.html',{'form' : saved,'f':f, 'faculty':faculty_form})

def process(request):
    details={}
    saved=Applicant.objects.filter(stat="Evaluation Completed")
    for i in saved:
        details[i.id]=Recommendation_fields.objects.filter(Applicant_id=i.id)
    print(details)
    return render(request,'polls/process.html',{'saved':saved, 'rec': details})


def process_detail(request,Applicant_id):
    saved=get_object_or_404(Applicant,pk=Applicant_id)
    refRec = []
    saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
    if request.method == "POST":
        saved.stat=request.POST["stat"]
        saved.save()
        return render(request,'polls/Thankyou.html') 
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        try:
            rec=Recommendation_fields.objects.order_by('faculty_num')
            rec = rec.filter(Applicant_id=saved.id)
            numRec=Recommendation_fields.objects.filter(Applicant_id=saved.id).count()
            print('--> num of records : ', numRec)
            print('--> Retrieved Records :',rec)
            for i in rec:
                print('----> ',i.faculty_num)
                refRec.append(int(i.faculty_num))
            print(refRec)
            # rec=Recommendation_fields_Form(instance=rec)
        except:
            rec = 'Not Submitted'
        return render(request,'polls/process_detail.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec,'refRec':refRec,'final':[1,2,3]})

def processed(request):
    saved=Applicant.objects.filter(stat__in=("Approved","Rejected"))
    print(saved)
    return render(request,'polls/processed.html',{'saved':saved})


def processed_detail(request,Applicant_id):
    saved=get_object_or_404(Applicant,pk=Applicant_id)
    refRec = []
    saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
    f=ApplicantForm(instance = saved)
    faculty_form = FacultyForm(instance = saved_faculty)
    try:
        rec=Recommendation_fields.objects.order_by('faculty_num')
        rec = rec.filter(Applicant_id=saved.id)
        numRec=Recommendation_fields.objects.filter(Applicant_id=saved.id).count()
        print('--> num of records : ', numRec)
        print('--> Retrieved Records :',rec)
        for i in rec:
            print('----> ',i.faculty_num)
            refRec.append(int(i.faculty_num))
        print(refRec)
            # rec=Recommendation_fields_Form(instance=rec)
    except:
        rec = 'Not Submitted'
    return render(request,'polls/processed_detail.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec,'refRec':refRec,'final':[1,2,3]})
# def processed_detail(request,Applicant_id):
#     saved=get_object_or_404(Applicant,pk=Applicant_id)
#     refRec = []
#     if request.method == "POST":
#         saved.stat=request.POST["stat"]
#         saved.save()
#         return render(request,'polls/Thankyou.html') 
#     else:
#         saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
#         f=ApplicantForm(instance = saved)
#         faculty_form = FacultyForm(instance = saved_faculty)
#         try:
#             rec=Recommendation_fields.objects.order_by('faculty_num')
#             rec = rec.filter(Applicant_id=saved.id)
#             numRec=Recommendation_fields.objects.filter(Applicant_id=saved.id).count()
#             print('--> num of records : ', numRec)
#             print('--> Retrieved Records :',rec)
#             for i in rec:
#                 print('----> ',i.faculty_num)
#                 refRec.append(int(i.faculty_num))
#             print(refRec)
#             # rec=Recommendation_fields_Form(instance=rec)
#         except:
#             rec = 'Not Submitted'
#         return render(request,'polls/processed_detail.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec,'refRec':refRec,'final':[1,2,3]})

def getrecommendations(request,cheque_no,ref_num):
    saved=get_object_or_404(Applicant,cheque_no=cheque_no)
    saved_faculty = get_object_or_404(Faculty,Applicant_id = saved.id)
    rec=get_object_or_404(Recommendation_fields,Applicant_id=saved.id,faculty_num=ref_num)
    f=ApplicantForm(instance = saved)
    faculty_form = FacultyForm(instance = saved_faculty)
    rec=Recommendation_fields_Form(instance=rec)
    return render(request,'polls/getrecommendations.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec ,'ref_num':str(ref_num)})

def RecommendationsAllInternal(request):
    saved=Applicant.objects.filter(stat=("Approved"))
    print(saved)
    return render(request,'polls/RecommendationsAllInternal.html',{'saved':saved})
