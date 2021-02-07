from django.forms import ModelForm
from django import forms
from .models import DesignApp, TeamMember,responce,Applicant

level=[
        ('Freshman','Freshman'),
        ('Sophomore','Sophomore'),
        ('Junior','Junior'),
        ('Senior','Senior'),
    ]
sem=[
               ('Fall 2020','Fall 2020'),
               ('Spring 2021','Spring 2021'),
               ]


class ApplicantForm(forms.ModelForm):
    UG_level= forms.MultipleChoiceField(label='Check all undergraduate level that apply',choices=level, widget=forms.CheckboxSelectMultiple(),required = False)
    semester=forms.MultipleChoiceField(label='Check all that apply:',choices=sem,widget=forms.CheckboxSelectMultiple())
    class Meta:
        model=Applicant
        fields=["Advisor1_FirstName","Advisor1_LastName","Advisor1_Inst","Advisor1_Department","Advisor1_Street_Address","Advisor1_City","Advisor1_State",
        "Advisor1_Zip_Code","Advisor1_Telephone","Advisor1_Fax","Advisor1_Email","Advisor2_FirstName","Advisor2_LastName","Advisor2_Inst","Advisor2_Department",
        "Advisor2_Street_Address","Advisor2_City","Advisor2_State","Advisor2_Zip_Code","Advisor2_Telephone","Advisor2_Fax","Advisor2_Email",
        "design_area","Specific_Challenge","Briefly_Describe","project_team","project_undertaken","Other","Students_Involved",
        "UG_level","no_of_participants_UG","no_of_participants_G","no_of_participants_FA","no_of_participants_Other","semester"]


        labels={'Advisor1_FirstName':'First Name','Advisor1_LastName':'Last Name','Advisor1_Inst':'Institution','Advisor1_Department':'Department','Advisor1_Street_Address':'Street Address','Advisor1_City':'City',
                        'Advisor1_State':'State','Advisor1_Zip_Code':'Zip Code','Advisor1_Telephone':'Telephone','Advisor1_Fax':'Fax','Advisor1_Email':'E-mail',
                        'Advisor2_FirstName':'First Name','Advisor2_LastName':'Last Name','Advisor2_Inst':'Institution','Advisor2_Department':'Department','Advisor2_Street_Address':'Street Address',
                        'Advisor2_City':'City','Advisor2_State':'State','Advisor2_Zip_Code':'Zip Code','Advisor2_Telephone':'Telephone','Advisor2_Fax':'Fax',
                        'Advisor2_Email':'E-mail','design_area': 'Design Challenge Area','Specific_Challenge':'Specific Challenge Selected',
                        'Briefly_Describe':'Briefly describe planned approach, including involvement of other departments, institutions, industry or other advisors if anticipated:',
                        'project_team':'This project will be done by:','project_undertaken':'Project will be undertaken as part of:',
                        'Other':'Other (Explain):','Students_Involved':'Levels of students(s) involved:','UG_level':' Check all undergraduate levels that apply','no_of_participants_UG':
                        'Undergraduate','no_of_participants_G':'Graduate','no_of_participants_FA':'Faculty Advisors','no_of_participants_Other':'Other','semester':'Check all that apply:',}



        widgets={
                'Specific_Challenge':forms.Textarea(attrs={'rows':3, 'cols':6}),
                'Other':forms.Textarea(attrs={'rows':3, 'cols':6}),
                'Students_Involved' :forms.RadioSelect(),
                }


APPROVAL_CHOICES =(
        ('I previously participated in the Competition', 'I previously participated in the Competition'),
        ('I was referred by a colleague.', 'I was referred by a colleague.'),
        ('I received information from a Competition Partner (AAAE, ACC, ACI-NA, NASAO, and UAA.)', 'I received information from a Competition Partner (AAAE, ACC, ACI-NA, NASAO, and UAA.)'),
        ('I found it on the VSGC/ACRP website.', 'I found it on the VSGC/ACRP website.'),
        ('I received an email from the Virginia Space Grant Consortium.', 'I received an email from the Virginia Space Grant Consortium.'),
        ('I saw it on Social Media.', 'I saw it on Social Media.'),
        ('I received the Competition guidelines at a Career Fair/Conference that I attended.', 'I received the Competition guidelines at a Career Fair/Conference that I attended.'),
    )
class DesignAppForm(forms.ModelForm):
    ACRP_University= forms.MultipleChoiceField(label='How did you hear about the ACRP University Design Competition for Addressing Airport Needs?',choices=APPROVAL_CHOICES, widget=forms.CheckboxSelectMultiple())
    Upload = forms.FileField(label='Full design, including Cover Page, Executive Summary, Table of Contents, Main Body of Design and Required Appendices:')
    class Meta:
        model = DesignApp
        fields = ["Inst","title","design_area","Specific_Challenge","Students_Involved","Advisor1_FirstName","Advisor1_LastName",
                                 "Advisor1_Department","Advisor1_Street_Address","Advisor1_City","Advisor1_State","Advisor1_Zip_Code","Advisor1_Telephone",
                                 "Advisor1_Fax","Advisor1_Email","Advisor2_FirstName","Advisor2_LastName","Advisor2_Department","Advisor2_Street_Address",
                                 "Advisor2_City","Advisor2_State","Advisor2_Zip_Code","Advisor2_Telephone","Advisor2_Fax","Advisor2_Email","num_team_members",
                                 "Other_Participants","Describe","ACRP_University","Other",'Upload']

        labels = {'title':'Title of Design','Inst':'Institutions','design_area': 'Design Challenge Area','Students_Involved': 'Level of Students Involved','Specific_Challenge':'Specific Challenge Selected',
                        'Advisor1_FirstName':'First Name','Advisor1_LastName':'Last Name','Advisor1_Department':'Department','Advisor1_Street_Address':'Street Address','Advisor1_City':'City',
                        'Advisor1_State':'State','Advisor1_Zip_Code':'Zip Code','Advisor1_Telephone':'Telephone','Advisor1_Fax':'Fax','Advisor1_Email':'E-mail',
                        'Advisor2_FirstName':'First Name','Advisor2_LastName':'Last Name','Advisor2_Department':'Department','Advisor2_Street_Address':'Street Address',
                        'Advisor2_City':'City','Advisor2_State':'State','Advisor2_Zip_Code':'Zip Code','Advisor2_Telephone':'Telephone','Advisor2_Fax':'Fax',
                        'Advisor2_Email':'E-mail','num_team_members': 'Select Number of Team Members','Other_Participants':'Estimate number of other participants',
                        'Describe':'Other please describe','ACRP_University':'How did you hear about the ACRP University Design Competition for Addressing Airport Needs?','Other':'Other','Upload':'Full design, including Cover Page, Executive Summary, Table of Contents, Main Body of Design and Required Appendices:'
                        ,}

        widgets={
                'Specific_Challenge':forms.Textarea(attrs={'rows':3, 'cols':6}),
                'Students_Involved' :forms.RadioSelect(),
                }

class TeamForm(forms.ModelForm):
    class Meta:
        model=TeamMember
        fields=['name','email','level']
                        
class StatusForm(forms.ModelForm):
    class Meta:
        model=DesignApp
        fields=['stat','reason']
        labels={'stat':'Approve/Disqualify','reason':'Reasons for Disqualifcation'}
        widgets={
                'stat' :forms.RadioSelect(),
                'reason':forms.Textarea(attrs={'rows':3, 'cols':6}),

                }
class ResponceForm(forms.ModelForm):
    class Meta:
        model=responce
        fields=['description','design_app','Q_score','Q_comments']


