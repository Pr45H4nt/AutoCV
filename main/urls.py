from django.urls import path
from .views import ResumeFormView, PersonalInfoFormView, EducationFormView, ExperienceFormView, skillformview, AchieveCertiView, homeview, ProjectFormView
from .editviews import EducationList, ExperienceList, SkillsList, EducationEdit, PersonalInfoEdit, ResumetitleEdit, ExperienceEdit, AchievementCertiList,AchieveCertiEdit, ListResumeView, ProjectList
from .editviews import EducationDeleteView, ExperienceDeleteView, AcheievementDeleteView, SkillsDeleteView, ResumeDeleteView, ProjectsDeleteView, ProjectEdit
from .views import ClassicSEPreview, ModernV1, ModernV2, ModernV3, ResumeDownloadView

urlpatterns = [
    path('', homeview, name='home'),
    path('buildresume/', ResumeFormView.as_view(), name='buildresume' ),
    path('listresume/', ListResumeView.as_view(), name='listresume' ),
    path('<int:resume_id>/personalinfo/', PersonalInfoFormView.as_view(), name='personalinfoform' ),
    path('<int:resume_id>/education/', EducationFormView.as_view(), name='educationform' ),
    path('<int:resume_id>/experience/', ExperienceFormView.as_view(), name='experienceform' ),
    path('<int:resume_id>/projects/', ProjectFormView.as_view(), name='projectsform' ),
    path('<int:resume_id>/skills/', skillformview, name='skillsform' ),
    path('<int:resume_id>/achievecerti/', AchieveCertiView.as_view(), name='achievecertiform' ),


    path('editeducation/<int:inst_id>', EducationEdit.as_view(), name='editeducation' ),
    path('editexperience/<int:inst_id>', ExperienceEdit.as_view(), name='editexperience' ),
    path('editprojects/<int:inst_id>', ProjectEdit.as_view(), name='editproject' ),
    path('editachievecerti/<int:inst_id>', AchieveCertiEdit.as_view(), name='editachievecerti' ),
    path('<int:resume_id>/editpersonalinfo/', PersonalInfoEdit.as_view(), name='editpersonalinfo' ),
    path('<int:resume_id>/editresumetitle/', ResumetitleEdit.as_view(), name='editresumetitle' ),

    path('deleteeducation/<int:inst_id>', EducationDeleteView.as_view(), name='deleteeducation' ),
    path('deleteexperience/<int:inst_id>', ExperienceDeleteView.as_view(), name='deleteexperience' ),
    path('deleteproject/<int:inst_id>', ProjectsDeleteView.as_view(), name='deleteproject' ),
    path('deleteskill/<int:inst_id>', SkillsDeleteView.as_view(), name='deleteskill' ),
    path('deleteachievecerti/<int:inst_id>', AcheievementDeleteView.as_view(), name='deleteachievecerti' ),
    path('<int:resume_id>/delteresume/', ResumeDeleteView.as_view(), name='deleteresume' ),






    path('<int:resume_id>/listachievecerti/', AchievementCertiList.as_view(), name='listachievecerti' ),
    path('<int:resume_id>/listeducation/', EducationList.as_view(), name='listeducation' ),
    path('<int:resume_id>/listexperience/', ExperienceList.as_view(), name='listexperience' ),
    path('<int:resume_id>/listprojects/', ProjectList.as_view(), name='listprojects' ),
    path('<int:resume_id>/listskills/', SkillsList.as_view(), name='listskills' ),


    path('<int:resume_id>/classic-se/', ClassicSEPreview.as_view(), name='classic_se' ),
    path('<int:resume_id>/modern-v1/', ModernV1.as_view(), name='modern_v1' ),
    path('<int:resume_id>/modern-v2/', ModernV2.as_view(), name='modern_v2' ),
    path('<int:resume_id>/modern-v3/', ModernV3.as_view(), name='modern_v3' ),

    path('<int:resume_id>/download/<int:style_id>/', ResumeDownloadView.as_view(), name='resume_download')


]