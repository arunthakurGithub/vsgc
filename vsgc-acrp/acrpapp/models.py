from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import gettext_lazy
from django.conf import settings
from django.contrib.auth.models import User
from encrypted_id.models import EncryptedIDModel

# Create your models here.
class Applicant(EncryptedIDModel):
    Advisor1_FirstName=models.CharField(max_length=128,null=True)
    Advisor1_LastName=models.CharField(max_length=30,default=None,null=True)
    Advisor1_Department=models.CharField(max_length=100,default=None,null=True)
    Advisor1_Inst = models.CharField(max_length=128,default='')
    Advisor1_Street_Address=models.CharField(max_length=128,default=None,null=True)
    Advisor1_City=models.CharField(max_length=50,default=None,null=True)
    US_STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]
    Advisor1_State=models.CharField(max_length=50,choices=US_STATES,default="",null=True)
    Advisor1_Zip_Code=models.IntegerField(max_length=13,default=None,null=True)
    Advisor1_Telephone=models.BigIntegerField(max_length=13,default=None,null=True)
    Advisor1_Fax=models.CharField(max_length=30,default=None,null=True)
    Advisor1_Email=models.EmailField(max_length=128,default=None,null=True)
    Advisor2_FirstName=models.CharField(max_length=128,default='',blank=True)
    Advisor2_LastName=models.CharField(max_length=30,default='',blank=True)
    Advisor2_Department=models.CharField(max_length=100,default='',blank=True)
    Advisor2_Inst = models.CharField(max_length=128,default='',blank=True)
    Advisor2_Street_Address=models.CharField(max_length=128,default='',blank=True)
    Advisor2_City=models.CharField(max_length=50,default='',blank=True)
    US___STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]
    Advisor2_State=models.CharField(max_length=50,choices=US___STATES,default='',blank=True) 
    Advisor2_Zip_Code=models.CharField(max_length=20,default='',blank=True)
    Advisor2_Telephone=models.CharField(max_length=13,default='',blank=True)
    Advisor2_Fax=models.CharField(max_length=30,default='',blank=True)
    Advisor2_Email=models.EmailField(max_length=128,default='',blank=True)
    FAAAE = 'AE'
    FAAAM = 'AM'
    FAAAO = 'AO'
    FAARS = 'RS'
    DesignAreaChoices = [
        (FAAAE, 'Airport Environmental Interactions'),
        (FAAAM, 'Airport Management and Planning'),
        (FAAAO, 'Airport Operations and Maintenance'),
        (FAARS, 'Runway Safety/Runway Incursions/Runway Excursions'),
    ]
    design_area = models.CharField(max_length=50,choices=DesignAreaChoices,default="")
    Specific_Challenge=models.CharField(max_length=264,default="")
    Briefly_Describe=models.CharField(max_length=264,default="")
    team=[
             ('Student Team','Student Team'),
             ('Individual Student','Individual Student'),
         ]
    project_team=models.CharField(max_length=50,choices=team,default="")
    undertaken=[
               ('Design Class','Design Class'),
               ('Independent Study','Independent Study'),
               ('Student Society Chapter','Student Society Chapter'),
               ('Other','Other'),
               ]
    project_undertaken=models.CharField(max_length=50,choices=undertaken,default="")
    Other = models.CharField(max_length=100,blank=True)
    RADIOS = [
    ('Undergraduate','Undergraduate'),
    ('Graduate','Graduate'),
    ('Both','Both'),
    ]
    Students_Involved=models.CharField(
         max_length=50,
         choices=RADIOS,
         default="",
    )
    UG_level=models.CharField(max_length=50,blank=True)
    no_of_participants_UG=models.PositiveIntegerField(default="0")
    no_of_participants_G=models.PositiveIntegerField(default="0")
    no_of_participants_FA=models.PositiveIntegerField(default="0")
    no_of_participants_Other = models.CharField(max_length=200,blank=True)


    semester=models.CharField(max_length=50,default="",)
    created_at = models.DateField(auto_now_add=True, blank=True)






class DesignApp(EncryptedIDModel):
    Inst = models.CharField(max_length=128,default="",)
    title = models.CharField(max_length=200,default="")

    FAAAE = 'AE'
    FAAAM = 'AM'
    FAAAO = 'AO'
    FAARS = 'RS'
    DesignAreaChoices = [
        (FAAAE, 'Airport Environmental Interactions'),
        (FAAAM, 'Airport Management and Planning'),
        (FAAAO, 'Airport Operations and Maintenance'),
        (FAARS, 'Runway Safety/Runway Incursions/Runway Excursions'),
    ]
    design_area = models.CharField(max_length=3,choices=DesignAreaChoices,)
    Specific_Challenge=models.CharField(max_length=264,default="")

    RADIOS = [
    ('Undergraduate','Undergraduate'),
    ('Graduate','Graduate'),
    ('Both','Both'),
    ]
    Students_Involved=models.CharField(
         max_length=20,
         choices=RADIOS,
         default="",
    )
    Advisor1_FirstName=models.CharField(max_length=128,null=True)
    Advisor1_LastName=models.CharField(max_length=30,default=None,null=True)
    Advisor1_Department=models.CharField(max_length=100,default=None,null=True)
    Advisor1_Street_Address=models.CharField(max_length=128,default=None,null=True)
    Advisor1_City=models.CharField(max_length=50,default=None,null=True)
    US_STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]
    Advisor1_State=models.CharField(max_length=50,choices=US_STATES,default="",null=True)
    Advisor1_Zip_Code=models.IntegerField(max_length=13,default=None,null=True)
    Advisor1_Telephone=models.BigIntegerField(max_length=13,default=None,null=True)
    Advisor1_Fax=models.CharField(max_length=30,default=None,null=True)
    Advisor1_Email=models.EmailField(max_length=128,default=None,null=True)
    Advisor2_FirstName=models.CharField(max_length=128,default='',blank=True)
    Advisor2_LastName=models.CharField(max_length=30,default='',blank=True)
    Advisor2_Department=models.CharField(max_length=100,default='',blank=True)
    Advisor2_Street_Address=models.CharField(max_length=128,default='',blank=True)
    Advisor2_City=models.CharField(max_length=50,default='',blank=True)
    US___STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]
    Advisor2_State=models.CharField(max_length=50,choices=US___STATES,default='',blank=True)
    Advisor2_Zip_Code=models.CharField(max_length=13,default='',blank=True)
    Advisor2_Telephone=models.CharField(max_length=13,default='',blank=True)
    Advisor2_Fax=models.CharField(max_length=30,default='',blank=True)
    Advisor2_Email=models.EmailField(max_length=128,default='',blank=True)
    num_team_members = models.PositiveIntegerField(default="0")
    Other_Participants=models.CharField(max_length=100,default="",blank=True)
    Describe=models.CharField(max_length=256,default="",blank=True)
    ACRP_University = models.CharField(max_length=256,null=True)
    Other = models.CharField(max_length=100,default='',blank=True)
    Upload=models.FileField(max_length=256,upload_to='media/', null=True)
    #Upload=models.FileField(max_length=256,upload_to=settings.MEDIA_URL,null=True)

    RADIOS = [
    ('Approved','Application Approved'),
    ('Rejected','Application Rejected'),
    ('Evaluation Saved','Save for later submission'),
    ('Evaluation Completed','Final submission'),

    ]
    stat=models.CharField(
         max_length=25,
         choices=RADIOS,
         default="Application is submitted",
    )

    reason=models.CharField(max_length=128,default="")
    created_at = models.DateField(auto_now_add=True)
    

class DesignApp1(DesignApp):
    class Meta:
        proxy = True

class DesignApp2(DesignApp):
    class Meta:
        proxy = True
class DesignApp3(DesignApp):
    class Meta:
        proxy = True



    def save(self): # ALL the signature
        super(DesignApp, self).save()
        super(Status, self).save()


class TeamMember(models.Model):
    levels = [
    ('Undergraduate','Undergraduate'),
    ('Graduate','Graduate'),
    ]

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    level=models.CharField( max_length=20,choices=levels)
    design_app = models.ForeignKey('DesignApp', on_delete=models.DO_NOTHING)



class emp(models.Model):
    Q_title=models.CharField(max_length=500)
    Q_questions=models.CharField(max_length=500)



class responce(models.Model):
    design_app = models.ForeignKey('DesignApp', on_delete=models.DO_NOTHING)
    description=models.ForeignKey('emp',on_delete=models.DO_NOTHING)
    Q_score=models.FloatField(max_length=100,default='0.5',blank=True)
    Q_comments=models.CharField(max_length=500,default="",blank=True)
    evalutor_id=models.ForeignKey(User, on_delete=models.DO_NOTHING)




class user_profile(models.Model):
    evalutor_id=models.ForeignKey(User, on_delete=models.DO_NOTHING)
    design_app = models.ForeignKey('DesignApp', on_delete=models.DO_NOTHING)
    RADIOS = [
    ('Evaluation Saved','Save for later submission'),
    ('Evaluation Completed','Final submission'),

    ]
    stat=models.CharField(
         max_length=25,
         choices=RADIOS,
    )













