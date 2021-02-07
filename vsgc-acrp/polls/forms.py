from django.forms import ModelForm
from django import forms
from .models import Applicant,Faculty,Recommendation_fields,user_profile
from django.conf import settings


class DateInput(forms.DateInput):
    input_type = 'date'

Ethni =(
	    ('American Indian or Alaskan Native: origin in any of the original peoples of North America', 'American Indian or Alaskan Native: origin in any of the original peoples of North America'),
	    ('Black: origin in any of the black racial groups', 'Black: origin in any of the black racial groups'),
	    ('Hispanic: Mexican, Puerto Rican, Central or South America, or other Spanish culture or origin, regardless of race', 'Hispanic: Mexican, Puerto Rican, Central or South America, or other Spanish culture or origin, regardless of race'),
	    ('Asian or Pacific Islander: origin in any of the original peoples of the Far East, Southeast Asia, or the Pacific Islands. Includes China, Japan, Korea, the Philippine Islands, Samoa, and the Indian Subcontinent', 'Asian or Pacific Islander: origin in any of the original peoples of the Far East, Southeast Asia, or the Pacific Islands. Includes China, Japan, Korea, the Philippine Islands, Samoa, and the Indian Subcontinent'),
	    ('White: origin in any of the original peoples of Europe, North Africa, or the Middle East', 'White: origin in any of the original peoples of Europe, North Africa, or the Middle East'),
	   	)

class ApplicantForm(forms.ModelForm):
	Ethnicity= forms.MultipleChoiceField(label='Ethnicity (optional):',choices=Ethni, widget=forms.CheckboxSelectMultiple(), required=False)
	Upload = forms.FileField(label='Upload File (Single PDF file):', required=False)
	# Expected_Graduation = forms.CharField(widget=CalendarWidget)
	dob=forms.DateField(label='Date of birth', required=False,widget=forms.TextInput(attrs={'placeholder':'(example: 05/31/70)'}))
	# Expected_Graduation=forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,widget=forms.TextInput(attrs={'class':'datepicker',}))
	visa_expiration=forms.DateField(widget=forms.TextInput(attrs={'placeholder':'(example: 05/31/70)'}),required=False)



	class Meta:
		model=Applicant
		fields=["App_FirstName","App_MiddleName",'App_LastName','dob','place_of_birth','Citizenship','Describe_type_and_status_if_visa_option_is_checked',
		'visa_expiration','Gender','Ethnicity','Mailing_Address','Mailing_City','Mailing_State','Mailing_Zip_Code','Current_phone','Permanent_Home_Address',
		'Permanent_City','Permanent_State','Permanent_Zip_Code','Permanent_Home_phone','Email','clg_or_univ_Enrolled','Major_Field','Degree_objective','Expected_Graduation',
		'Ref1_Name','Ref1_Title','Ref1_Dept','Ref1_Inst','Ref1_Phone','Ref2_Name','Ref2_Title','Ref2_Dept','Ref2_Inst','Ref2_Phone','clg_or_univ_1','Location_1',
		'Major_1','Dates_Attended_1','GPA_1','Degree_1','degree_expected_1','clg_or_univ_2','Location_2','Major_2','Dates_Attended_2','GPA_2','Degree_2','degree_expected_2','clg_or_univ_3','Location_3',
		'Major_3','Dates_Attended_3','GPA_3','Degree_3','degree_expected_3','clg_or_univ_4','Location_4',
		'Major_4','Dates_Attended_4','GPA_4','Degree_4','degree_expected_4','clg_or_univ_5','Location_5',
		'Major_5','Dates_Attended_5','GPA_5','Degree_5','degree_expected_5','clg_or_univ_6','Location_6',
		'Major_6','Dates_Attended_6','GPA_6','Degree_6','degree_expected_6','clg_or_univ_7','Location_7',
		'Major_7','Dates_Attended_7','GPA_7','Degree_7','degree_expected_7','Interruptions_of_schooling','Emp1_Name','Emp1_Location','Emp1_Dates','Emp1_Nature_of_work',
		'Emp2_Name','Emp2_Location','Emp2_Dates','Emp2_Nature_of_work','Emp3_Name','Emp3_Location','Emp3_Dates','Emp3_Nature_of_work','Emp4_Name','Emp4_Location',
		'Emp4_Dates','Emp4_Nature_of_work','Prof_exp_Notes','Award1_Name','Award1_Date','Award1_Description','Award2_Name','Award2_Date','Award2_Description',
		'Award3_Name','Award3_Date','Award3_Description','Award4_Name','Award4_Date','Award4_Description','Award5_Name','Award5_Date','Award5_Description',
		'Award6_Name','Award6_Date','Award6_Description','Awards_Notes','Carrer_goals','Title_of_reserach_project',
		'Ref3_Name','Ref3_Title','Ref3_Inst','Ref3_Phone','Upload','stat','cheque_no']

		labels={'App_FirstName':'First Name:','App_MiddleName':'Middle Name:','App_LastName':'Last Name:','dob':'Date of birth:','place_of_birth':'Place of birth:',
		'Citizenship':'Citizenship:','Describe_type_and_status_if_visa_option_is_checked':'Describe type and status if visa option is checked:','visa_expiration':'Expiration date for student visa:',
		'Gender':'Gender Identity (optional):','Ethnicity':'Ethnicity (optional):','Mailing_Address':'Mailing Address:','Mailing_City':'City:','Mailing_State':'State:',
		'Mailing_Zip_Code':'Zip Code:','Current_phone':'Current Phone:','Permanent_Home_Address':'Permanent Home Address:','Permanent_City':'City:','Permanent_State':'State:',
		'Permanent_Zip_Code':'Zip Code:','Permanent_Home_phone':'Permanent Home Phone:','Email':'Email:','clg_or_univ_Enrolled':'College or University currently enrolled:','Major_Field':'Major Field:',
		'Degree_objective':'Degree Objective:','Expected_Graduation':'Expected Year of graduation:','Ref1_Name':'Name:','Ref1_Title':'Title:','Ref1_Dept':'Department:',
		'Ref1_Inst':'Institutional Affiliation:','Ref1_Phone':'Phone:','Ref2_Name':'Name:','Ref2_Title':'Title:','Ref2_Dept':'Department:',
		'Ref2_Inst':'Institutional Affiliation:','Ref2_Phone':'Phone:','clg_or_univ':'College / University','Location':'Location','Major_Field':'Major Field',
		'Dates_Attended':'Dates Attended','GPA':'GPA','Degree':'Degree','Date_degree_expected':'Date degree awarded / expected','Interruptions_of_schooling':'Please explain any interruption(s) of schooling, i.e., military training, illness, etc.):',
		'Emp1_Name':'Name of Employer','Emp1_Location':'Location','Emp1_Dates':'Dates','Emp1_Nature_of_work':'Nature of Work','Emp2_Name':'Name of Employer',
		'Emp2_Location':'Location','Emp2_Dates':'Dates','Emp2_Nature_of_work':'Nature of Work','Emp3_Name':'Name of Employer','Emp3_Location':'Location','Emp3_Dates':'Dates','Emp3_Nature_of_work':'Nature of Work',
		'Emp4_Name':'Name of Employer','Emp4_Location':'Location','Emp4_Dates':'Dates','Emp4_Nature_of_work':'Nature of Work','Prof_exp_Notes':'Additional Notes may be added here:',
		'Award1_Name':'Award, Honor, or Publication','Award1_Date':'Date(s)','Award1_Description':'Description','Award2_Name':'Award, Honor, or Publication','Award2_Date':'Date(s)','Award2_Description':'Description',
		'Award3_Name':'Award, Honor, or Publication','Award3_Date':'Date(s)','Award3_Description':'Description','Award4_Name':'Award, Honor, or Publication','Award4_Date':'Date(s)','Award4_Description':'Description',
		'Award5_Name':'Award, Honor, or Publication','Award5_Date':'Date(s)','Award5_Description':'Description','Award6_Name':'Award, Honor, or Publication','Award6_Date':'Date(s)','Award6_Description':'Description',
		'Awards_Notes':'Additional Notes may be added here:','Carrer_goals':'Describe your career goals and how this research will contribute to achieving those goals:',
		'Title_of_reserach_project':'Title of Research Project:','Ref3_Name':'Name:','Ref3_Title':'Title:','Ref3_Inst':'Institution:','Ref3_Phone':'Phone:',
		'Upload':'Upload File (Single PDF file):','cheque_no':'Nine-Character ID'}


		widgets={
				'Describe_type_and_status_if_visa_option_is_checked':forms.Textarea(attrs={'rows':3, 'cols':6}),
				'Interruptions_of_schooling':forms.Textarea(attrs={'rows':3, 'cols':6}),
				'Prof_exp_Notes':forms.Textarea(attrs={'rows':3, 'cols':6}),
				'Awards_Notes':forms.Textarea(attrs={'rows':3, 'cols':6}),
				'Carrer_goals':forms.Textarea(attrs={'rows':3, 'cols':6}),
				'stat' :forms.RadioSelect(),
				'Expected_Graduation': DateInput(),

				}
		error_messages  = {
        'category_name': {
        'unique': ('True')
        }
        }
	#Used for conditionally marking fields as required.
	def fields_required(self, fields):
		for field in fields:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)


	def clean(self):
		stat = self.cleaned_data.get('stat')
		if stat == 'Evaluation Saved':
			self.cleaned_data
		else:
			self.fields_required(["App_FirstName","App_MiddleName",'App_LastName','dob','place_of_birth','Citizenship','Gender','Ethnicity','Mailing_Address','Mailing_City','Mailing_State','Mailing_Zip_Code','Current_phone','Permanent_Home_Address',
        'Permanent_City','Permanent_State','Permanent_Zip_Code','Permanent_Home_phone','Email','clg_or_univ_Enrolled','Major_Field','Degree_objective','Expected_Graduation',
        'Ref1_Name','Ref1_Title','Ref1_Dept','Ref1_Inst','Ref1_Phone','Ref2_Name','Ref2_Title','Ref2_Dept','Ref2_Inst','Ref2_Phone','clg_or_univ_1','Location_1',
        'Major_1','Dates_Attended_1','GPA_1','Degree_1','degree_expected_1','Emp1_Name','Emp1_Location','Emp1_Dates','Emp1_Nature_of_work',
        'Title_of_reserach_project','Ref3_Name','Ref3_Title','Ref3_Inst','Ref3_Phone','Upload','stat','cheque_no'])
		return self.cleaned_data




class SearchForm(forms.Form):
    searchValue = forms.CharField(label="PassCode ", max_length=128)




class FacultyForm(forms.ModelForm):
    class Meta:
        model=Faculty
        fields=['Ref1_Email','Ref2_Email','Ref3_Email']
        labels={
        'Ref1_Email':'E-mail','Ref2_Email':'E-mail','Ref3_Email':'Email:'}


class Recommendation_fields_Form(forms.ModelForm):
	class Meta:
		model=Recommendation_fields
		fields=['In_what_capacity_do_you_know_the_applicant','How_Long_have_you_known_the_applicant','Knowledge_of_major_field','Research_skills','Problem_solving_skills',
		        'Creativity','Leadership','Written_communication','Oral_communication','Comment_on_the_ability_of_the_applicant','Add_other_comments_to_the_evaluation',
		        'Signed_letter_of_reference']

		labels={'In_what_capacity_do_you_know_the_applicant':'1. In what capacity do you know the applicant?','How_Long_have_you_known_the_applicant':'2. How long have you known the applicant?','Knowledge_of_major_field':'Knowledge of major field','Research_skills':'Research skills',
               'Problem_solving_skills':'Problem solving skills','Creativity':'Creativity','Leadership':'Leadership','Written_communication':'Written communication',
               'Oral_communication':'Oral communication','Comment_on_the_ability_of_the_applicant':'Please comment on the ability of the applicant to carry out the proposed research in a timely manner:',
               'Add_other_comments_to_the_evaluation':'Please add any other comments that you consider to be pertinent to the evaluation of the applicant and that are not covered adequately by your other responses',
               'Signed_letter_of_reference':'Please upload a signed letter of reference on institution letterhead here:'
               }

class Status(forms.ModelForm):
    class Meta:
        model=user_profile
        fields=['stat','ranking']
        labels={'stat':'Approve/Disqualify','ranking':'Select ranking for the applicant:'}
        widgets={
                'stat' :forms.RadioSelect(),

                }