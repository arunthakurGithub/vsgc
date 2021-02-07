from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import gettext_lazy
from django.core.validators import MaxValueValidator
from django.core.validators import RegexValidator
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Applicant(models.Model):
    App_FirstName=models.CharField(max_length=128)
    App_MiddleName=models.CharField(max_length=128,null=True)
    App_LastName=models.CharField(max_length=128,null=True)
    dob = models.DateField(max_length=10,null=True)
    place_of_birth=models.CharField(max_length=128,null=True)
    citizen=[
             ('US citizen','US citizen'),
             ('Permanent Resident','Permanent Resident'),
             ('Student Visa','Student Visa')
         ]
    Citizenship=models.CharField(max_length=100,choices=citizen,default="")
    Describe_type_and_status_if_visa_option_is_checked=models.CharField(max_length=264,default="")
    visa_expiration=models.DateField(max_length=10,null=True)
    gender=[
             ('Male','Male'),
             ('Female','Female'),
             ('Other','Other')
         ]

    Gender=models.CharField(max_length=100,choices=gender,default="")
    Ethnicity=models.CharField(max_length=256,null=True)
    Mailing_Address=models.CharField(max_length=256,null=True)
    Mailing_City=models.CharField(max_length=128,null=True)
    Mailing_State=models.CharField(max_length=128,null=True)
    Mailing_Zip_Code=models.CharField(max_length=128,null=True)
    Current_phone=models.CharField(max_length=13,null=True)
    Permanent_Home_Address=models.CharField(max_length=256,null=True)
    Permanent_City=models.CharField(max_length=128,null=True)
    Permanent_State=models.CharField(max_length=128,null=True)
    Permanent_Zip_Code=models.CharField(max_length=128,null=True)
    Permanent_Home_phone=models.CharField(max_length=13,null=True)
    Email= models.EmailField(max_length=254,null=True)
    clg_or_univ_Enrolled=models.CharField(max_length=128,null=True)
    Major_Field=models.CharField(max_length=128,null=True)
    Degree=[
             ("Master's","Master's"),
             ("Doctorate","Doctorate")
         ]
    Degree_objective=models.CharField(max_length=128,null=True,choices=Degree,default="")
    Expected_Graduation=models.DateField(max_length=20,null=True)
    Ref1_Name=models.CharField(max_length=128,null=True)
    Ref1_Title=models.CharField(max_length=128,null=True)
    Ref1_Dept=models.CharField(max_length=128,null=True)
    Ref1_Inst=models.CharField(max_length=128,null=True)
    Ref1_Phone=models.CharField(max_length=70,blank=True)
    Ref2_Name=models.CharField(max_length=128,null=True)
    Ref2_Title=models.CharField(max_length=128,null=True)
    Ref2_Dept=models.CharField(max_length=128,null=True)
    Ref2_Inst=models.CharField(max_length=128,null=True)
    Ref2_Phone=models.CharField(null=False,max_length=128)
    clg_or_univ_1=models.CharField(max_length=128,null=True)
    Location_1=models.CharField(max_length=128,null=True)
    Major_1=models.CharField(max_length=128,null=True)
    Dates_Attended_1=models.DateField(max_length=20,null=True)
    GPA_1=models.CharField(max_length=128,null=True)
    Degree_1=models.CharField(max_length=128,null=True)
    degree_expected_1=models.DateField(max_length=20,null=True)
    clg_or_univ_2=models.CharField(max_length=128,null=True)
    Location_2=models.CharField(max_length=128,null=True)
    Major_2=models.CharField(max_length=128,null=True)
    Dates_Attended_2=models.DateField(max_length=20,null=True)
    GPA_2=models.CharField(max_length=128,null=True)
    Degree_2=models.CharField(max_length=128,null=True)
    degree_expected_2=models.DateField(max_length=20,null=True)
    clg_or_univ_3=models.CharField(max_length=128,null=True)
    Location_3=models.CharField(max_length=128,null=True)
    Major_3=models.CharField(max_length=128,null=True)
    Dates_Attended_3=models.DateField(max_length=10,null=True)
    GPA_3=models.CharField(max_length=128,null=True)
    Degree_3=models.CharField(max_length=128,null=True)
    degree_expected_3=models.DateField(max_length=20,null=True)
    clg_or_univ_4=models.CharField(max_length=128,null=True)
    Location_4=models.CharField(max_length=128,null=True)
    Major_4=models.CharField(max_length=128,null=True)
    Dates_Attended_4=models.DateField(max_length=20,null=True)
    GPA_4=models.CharField(max_length=128,null=True)
    Degree_4=models.CharField(max_length=128,null=True)
    degree_expected_4=models.DateField(max_length=20,null=True)
    clg_or_univ_5=models.CharField(max_length=128,null=True)
    Location_5=models.CharField(max_length=128,null=True)
    Major_5=models.CharField(max_length=128,null=True)
    Dates_Attended_5=models.DateField(max_length=20,null=True)
    GPA_5=models.CharField(max_length=128,null=True)
    Degree_5=models.CharField(max_length=128,null=True)
    degree_expected_5=models.DateField(max_length=20,null=True)
    clg_or_univ_6=models.CharField(max_length=128,null=True)
    Location_6=models.CharField(max_length=128,null=True)
    Major_6=models.CharField(max_length=128,null=True)
    Dates_Attended_6=models.DateField(max_length=20,null=True)
    GPA_6=models.CharField(max_length=128,null=True)
    Degree_6=models.CharField(max_length=128,null=True)
    degree_expected_6=models.DateField(max_length=20,null=True)
    clg_or_univ_7=models.CharField(max_length=128,null=True)
    Location_7=models.CharField(max_length=128,null=True)
    Major_7=models.CharField(max_length=128,null=True)
    Dates_Attended_7=models.DateField(max_length=10,null=True)
    GPA_7=models.CharField(max_length=128,null=True)
    Degree_7=models.CharField(max_length=128,null=True)
    degree_expected_7=models.DateField(max_length=10,null=True)
    Interruptions_of_schooling=models.CharField(max_length=264,default="")
    Emp1_Name=models.CharField(max_length=128,null=True)
    Emp1_Location=models.CharField(max_length=128,null=True)
    Emp1_Dates=models.CharField(max_length=128,null=True)
    Emp1_Nature_of_work=models.CharField(max_length=128,null=True)
    Emp2_Name=models.CharField(max_length=128,null=True)
    Emp2_Location=models.CharField(max_length=128,null=True)
    Emp2_Dates=models.CharField(max_length=128,null=True)
    Emp2_Nature_of_work=models.CharField(max_length=128,null=True)
    Emp3_Name=models.CharField(max_length=128,null=True)
    Emp3_Location=models.CharField(max_length=128,null=True)
    Emp3_Dates=models.CharField(max_length=128,null=True)
    Emp3_Nature_of_work=models.CharField(max_length=128,null=True)
    Emp4_Name=models.CharField(max_length=128,null=True)
    Emp4_Location=models.CharField(max_length=128,null=True)
    Emp4_Dates=models.CharField(max_length=128,null=True)
    Emp4_Nature_of_work=models.CharField(max_length=128,null=True)
    Prof_exp_Notes=models.CharField(max_length=128,null=True)
    Award1_Name=models.CharField(max_length=128,null=True)
    Award1_Date=models.CharField(max_length=128,null=True)
    Award1_Description=models.CharField(max_length=128,null=True)
    Award2_Name=models.CharField(max_length=128,null=True)
    Award2_Date=models.CharField(max_length=128,null=True)
    Award2_Description=models.CharField(max_length=128,null=True)
    Award3_Name=models.CharField(max_length=128,null=True)
    Award3_Date=models.CharField(max_length=128,null=True)
    Award3_Description=models.CharField(max_length=128,null=True)
    Award4_Name=models.CharField(max_length=128,null=True)
    Award4_Date=models.CharField(max_length=128,null=True)
    Award4_Description=models.CharField(max_length=128,null=True)
    Award5_Name=models.CharField(max_length=128,null=True)
    Award5_Date=models.CharField(max_length=128,null=True)
    Award5_Description=models.CharField(max_length=128,null=True)
    Award6_Name=models.CharField(max_length=128,null=True)
    Award6_Date=models.CharField(max_length=128,null=True)
    Award6_Description=models.CharField(max_length=128,null=True)
    Awards_Notes=models.CharField(max_length=128,null=True)
    Carrer_goals=models.CharField(max_length=128,null=True)
    Title_of_reserach_project=models.CharField(max_length=128,null=True)
    Ref3_Name=models.CharField(max_length=128,null=True)
    Ref3_Title=models.CharField(max_length=128,null=True)
    Ref3_Inst=models.CharField(max_length=128,null=True)
    Ref3_Phone=models.CharField(max_length=128,null=True)
    Upload=models.FileField(max_length=256,upload_to='app/',null=True)


    RADIOS = [
    ('Evaluation Saved','Save for later submission'),
    ('Evaluation Completed','Final submission'),
    ('Approved','Application Approved'),
    ('Rejected','Application Rejected'),
    ]
    stat=models.CharField(
         max_length=25,
         choices=RADIOS,
         default="",
    )
    cheque_no = models.CharField(validators=[RegexValidator(regex='^.{9}$', message='Length has to be 9 numbers', code='nomatch')],max_length=128,unique=True)


class Faculty(models.Model):
    Applicant = models.ForeignKey('Applicant', on_delete=models.DO_NOTHING)
    Ref1_Email=models.EmailField(max_length=70,blank=True)
    Ref2_Email=models.EmailField(max_length=70,blank=True)
    Ref3_Email=models.CharField(max_length=128,null=True)


class Recommendation_fields(models.Model):
    Applicant = models.ForeignKey('Applicant', on_delete=models.DO_NOTHING)
    In_what_capacity_do_you_know_the_applicant=models.CharField(max_length=256)
    How_Long_have_you_known_the_applicant=models.CharField(max_length=128)
    major_field=[
             ('Below Average','Below Average'),
             ('Average','Average'),
             ('Above Average','Above Average'),
             ('Outstanding','Outstanding'),

         ]

    Knowledge_of_major_field=models.CharField(max_length=100,choices=major_field,default="")
    Research_skills=models.CharField(max_length=100,choices=major_field,default="")
    Problem_solving_skills=models.CharField(max_length=100,choices=major_field,default="")
    Creativity=models.CharField(max_length=100,choices=major_field,default="")
    Leadership=models.CharField(max_length=100,choices=major_field,default="")
    Written_communication=models.CharField(max_length=100,choices=major_field,default="")
    Oral_communication=models.CharField(max_length=100,choices=major_field,default="")
    Comment_on_the_ability_of_the_applicant=models.CharField(max_length=512)
    Add_other_comments_to_the_evaluation=models.CharField(max_length=256,null=True)
    Signed_letter_of_reference=models.FileField(max_length=256,upload_to='app/',null=True)
    faculty_num=models.CharField(max_length=10)


















from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import gettext_lazy
from django.core.validators import MaxValueValidator
from django.core.validators import RegexValidator
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Applicant(models.Model):
    App_FirstName=models.CharField(max_length=128)
    App_MiddleName=models.CharField(max_length=128,blank=True)
    App_LastName=models.CharField(max_length=128,blank=True)
    dob = models.DateField(max_length=10,blank=True)
    place_of_birth=models.CharField(max_length=128,blank=True)
    citizen=[
             ('US citizen','US citizen'),
             ('Permanent Resident','Permanent Resident'),
             ('Student Visa','Student Visa')
         ]
    Citizenship=models.CharField(max_length=100,choices=citizen,default="",blank=True)
    Describe_type_and_status_if_visa_option_is_checked=models.CharField(max_length=264,default="",blank=True)
    visa_expiration=models.DateField(max_length=10,blank=True)
    gender=[
             ('Male','Male'),
             ('Female','Female'),
             ('Other','Other')
         ]

    Gender=models.CharField(max_length=100,choices=gender,default="",blank=True)
    Ethnicity=models.CharField(max_length=256,blank=True)
    Mailing_Address=models.CharField(max_length=256,blank=True)
    Mailing_City=models.CharField(max_length=128,blank=True)
    Mailing_State=models.CharField(max_length=128,blank=True)
    Mailing_Zip_Code=models.CharField(max_length=128,blank=True)
    Current_phone=models.CharField(max_length=13,blank=True)
    Permanent_Home_Address=models.CharField(max_length=256,blank=True)
    Permanent_City=models.CharField(max_length=128,blank=True)
    Permanent_State=models.CharField(max_length=128,blank=True)
    Permanent_Zip_Code=models.CharField(max_length=128,blank=True)
    Permanent_Home_phone=models.CharField(max_length=13,blank=True)
    Email= models.EmailField(max_length=254,blank=True)
    clg_or_univ_Enrolled=models.CharField(max_length=128,blank=True)
    Major_Field=models.CharField(max_length=128,blank=True)
    Degree=[
             ("Master's","Master's"),
             ("Doctorate","Doctorate")
         ]
    Degree_objective=models.CharField(max_length=128,blank=True,choices=Degree,default="")
    Expected_Graduation=models.DateField(max_length=20,blank=True)
    Ref1_Name=models.CharField(max_length=128,blank=True)
    Ref1_Title=models.CharField(max_length=128,blank=True)
    Ref1_Dept=models.CharField(max_length=128,blank=True)
    Ref1_Inst=models.CharField(max_length=128,blank=True)
    Ref1_Phone=models.CharField(max_length=70,blank=True)
    Ref2_Name=models.CharField(max_length=128,blank=True)
    Ref2_Title=models.CharField(max_length=128,blank=True)
    Ref2_Dept=models.CharField(max_length=128,blank=True)
    Ref2_Inst=models.CharField(max_length=128,blank=True)
    Ref2_Phone=models.CharField(blank=True,max_length=128)
    clg_or_univ_1=models.CharField(max_length=128,blank=True)
    Location_1=models.CharField(max_length=128,blank=True)
    Major_1=models.CharField(max_length=128,blank=True)
    Dates_Attended_1=models.DateField(max_length=20,blank=True)
    GPA_1=models.CharField(max_length=128,blank=True)
    Degree_1=models.CharField(max_length=128,blank=True)
    degree_expected_1=models.DateField(max_length=20,blank=True)
    clg_or_univ_2=models.CharField(max_length=128,blank=True)
    Location_2=models.CharField(max_length=128,blank=True)
    Major_2=models.CharField(max_length=128,blank=True)
    Dates_Attended_2=models.DateField(max_length=20,blank=True)
    GPA_2=models.CharField(max_length=128,blank=True)
    Degree_2=models.CharField(max_length=128,blank=True)
    degree_expected_2=models.DateField(max_length=20,blank=True)
    clg_or_univ_3=models.CharField(max_length=128,blank=True)
    Location_3=models.CharField(max_length=128,blank=True)
    Major_3=models.CharField(max_length=128,blank=True)
    Dates_Attended_3=models.DateField(max_length=10,blank=True)
    GPA_3=models.CharField(max_length=128,blank=True)
    Degree_3=models.CharField(max_length=128,blank=True)
    degree_expected_3=models.DateField(max_length=20,blank=True)
    clg_or_univ_4=models.CharField(max_length=128,blank=True)
    Location_4=models.CharField(max_length=128,blank=True)
    Major_4=models.CharField(max_length=128,blank=True)
    Dates_Attended_4=models.DateField(max_length=20,blank=True)
    GPA_4=models.CharField(max_length=128,blank=True)
    Degree_4=models.CharField(max_length=128,blank=True)
    degree_expected_4=models.DateField(max_length=20,blank=True)
    clg_or_univ_5=models.CharField(max_length=128,blank=True)
    Location_5=models.CharField(max_length=128,blank=True)
    Major_5=models.CharField(max_length=128,blank=True)
    Dates_Attended_5=models.DateField(max_length=20,blank=True)
    GPA_5=models.CharField(max_length=128,blank=True)
    Degree_5=models.CharField(max_length=128,blank=True)
    degree_expected_5=models.DateField(max_length=20,blank=True)
    clg_or_univ_6=models.CharField(max_length=128,blank=True)
    Location_6=models.CharField(max_length=128,blank=True)
    Major_6=models.CharField(max_length=128,blank=True)
    Dates_Attended_6=models.DateField(max_length=20,blank=True)
    GPA_6=models.CharField(max_length=128,blank=True)
    Degree_6=models.CharField(max_length=128,blank=True)
    degree_expected_6=models.DateField(max_length=20,blank=True)
    clg_or_univ_7=models.CharField(max_length=128,blank=True)
    Location_7=models.CharField(max_length=128,blank=True)
    Major_7=models.CharField(max_length=128,blank=True)
    Dates_Attended_7=models.DateField(max_length=10,blank=True)
    GPA_7=models.CharField(max_length=128,blank=True)
    Degree_7=models.CharField(max_length=128,blank=True)
    degree_expected_7=models.DateField(max_length=10,blank=True)
    Interruptions_of_schooling=models.CharField(max_length=264,default="",blank=True)
    Emp1_Name=models.CharField(max_length=128,blank=True)
    Emp1_Location=models.CharField(max_length=128,blank=True)
    Emp1_Dates=models.CharField(max_length=128,blank=True)
    Emp1_Nature_of_work=models.CharField(max_length=128,blank=True)
    Emp2_Name=models.CharField(max_length=128,blank=True)
    Emp2_Location=models.CharField(max_length=128,blank=True)
    Emp2_Dates=models.CharField(max_length=128,blank=True)
    Emp2_Nature_of_work=models.CharField(max_length=128,blank=True)
    Emp3_Name=models.CharField(max_length=128,blank=True)
    Emp3_Location=models.CharField(max_length=128,blank=True)
    Emp3_Dates=models.CharField(max_length=128,blank=True)
    Emp3_Nature_of_work=models.CharField(max_length=128,blank=True)
    Emp4_Name=models.CharField(max_length=128,blank=True)
    Emp4_Location=models.CharField(max_length=128,blank=True)
    Emp4_Dates=models.CharField(max_length=128,blank=True)
    Emp4_Nature_of_work=models.CharField(max_length=128,blank=True)
    Prof_exp_Notes=models.CharField(max_length=128,blank=True)
    Award1_Name=models.CharField(max_length=128,blank=True)
    Award1_Date=models.CharField(max_length=128,blank=True)
    Award1_Description=models.CharField(max_length=128,blank=True)
    Award2_Name=models.CharField(max_length=128,blank=True)
    Award2_Date=models.CharField(max_length=128,blank=True)
    Award2_Description=models.CharField(max_length=128,blank=True)
    Award3_Name=models.CharField(max_length=128,blank=True)
    Award3_Date=models.CharField(max_length=128,blank=True)
    Award3_Description=models.CharField(max_length=128,blank=True)
    Award4_Name=models.CharField(max_length=128,blank=True)
    Award4_Date=models.CharField(max_length=128,blank=True)
    Award4_Description=models.CharField(max_length=128,blank=True)
    Award5_Name=models.CharField(max_length=128,blank=True)
    Award5_Date=models.CharField(max_length=128,blank=True)
    Award5_Description=models.CharField(max_length=128,blank=True)
    Award6_Name=models.CharField(max_length=128,blank=True)
    Award6_Date=models.CharField(max_length=128,blank=True)
    Award6_Description=models.CharField(max_length=128,blank=True)
    Awards_Notes=models.CharField(max_length=128,blank=True)
    Carrer_goals=models.CharField(max_length=128,blank=True)
    Title_of_reserach_project=models.CharField(max_length=128,blank=True)
    Ref3_Name=models.CharField(max_length=128,blank=True)
    Ref3_Title=models.CharField(max_length=128,blank=True)
    Ref3_Inst=models.CharField(max_length=128,blank=True)
    Ref3_Phone=models.CharField(max_length=128,blank=True)
    Upload=models.FileField(max_length=256,upload_to='app/',blank=True)


    RADIOS = [
    ('Evaluation Saved','Save for later submission'),
    ('Evaluation Completed','Final submission'),
    ('Approved','Application Approved'),
    ('Rejected','Application Rejected'),
    ]
    stat=models.CharField(
         max_length=25,
         choices=RADIOS,
         default="",
    )
    cheque_no = models.CharField(validators=[RegexValidator(regex='^.{9}$', message='Length has to be 9 numbers', code='nomatch')],max_length=128,unique=True)


class Faculty(models.Model):
    Applicant = models.ForeignKey('Applicant', on_delete=models.DO_NOTHING)
    Ref1_Email=models.EmailField(max_length=70,blank=True)
    Ref2_Email=models.EmailField(max_length=70,blank=True)
    Ref3_Email=models.CharField(max_length=128,blank=True)


class Recommendation_fields(models.Model):
    Applicant = models.ForeignKey('Applicant', on_delete=models.DO_NOTHING)
    In_what_capacity_do_you_know_the_applicant=models.CharField(max_length=256)
    How_Long_have_you_known_the_applicant=models.CharField(max_length=128)
    major_field=[
             ('Below Average','Below Average'),
             ('Average','Average'),
             ('Above Average','Above Average'),
             ('Outstanding','Outstanding'),

         ]

    Knowledge_of_major_field=models.CharField(max_length=100,choices=major_field,default="")
    Research_skills=models.CharField(max_length=100,choices=major_field,default="")
    Problem_solving_skills=models.CharField(max_length=100,choices=major_field,default="")
    Creativity=models.CharField(max_length=100,choices=major_field,default="")
    Leadership=models.CharField(max_length=100,choices=major_field,default="")
    Written_communication=models.CharField(max_length=100,choices=major_field,default="")
    Oral_communication=models.CharField(max_length=100,choices=major_field,default="")
    Comment_on_the_ability_of_the_applicant=models.CharField(max_length=512)
    Add_other_comments_to_the_evaluation=models.CharField(max_length=256,blank=True)
    Signed_letter_of_reference=models.FileField(max_length=256,upload_to='app/',blank=True)
    faculty_num=models.CharField(max_length=10)




