from django.views.generic import ListView, UpdateView, DeleteView
from .forms import ResumeForm,PersonalInfoForm, EducationForm, ExperienceForm, Achievecertiform, Projectsform
from .models import Education, Resume , Experience, SkillCategory, PersonalInfo, AchievementsCertifications, Projects
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class GenericEdit(LoginRequiredMixin, UpdateView):
    form_class = EducationForm
    template_name = 'updateform.html'
    pk_url_kwarg = 'inst_id'
    success_url = None
    name = None
    next_url = None
    previous_url = None


    def get_queryset(self):
        inst = get_object_or_404(self.model, id=self.kwargs['inst_id'])
        self.kwargs['resume_id'] = inst.resume.id
        return self.model.objects.filter(resume__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.name
        context['next_url'] = reverse_lazy(self.next_url, kwargs={'resume_id': self.kwargs.get('resume_id') }) if self.next_url else None
        context['previous_url'] = reverse_lazy(self.previous_url, kwargs={'resume_id': self.kwargs.get('resume_id') }) if self.previous_url else None
        context['success_url'] = reverse_lazy(self.success_url, kwargs={'resume_id': self.kwargs.get('resume_id') }) if self.success_url else None
        
        return context

            
    
    def get_success_url(self):
        return reverse_lazy(self.success_url,kwargs={'resume_id': self.kwargs.get('resume_id') })



class EducationEdit(GenericEdit):
    model = Education
    form_class = EducationForm
    success_url = 'listeducation'
    name = 'Education'

class ProjectEdit(GenericEdit):
    model = Projects
    form_class = Projectsform
    success_url = 'listprojects'
    name = 'Project'


class ExperienceEdit(GenericEdit):
    model = Experience
    form_class = ExperienceForm
    success_url = 'listexperience'
    name = 'Experience'

class AchieveCertiEdit(GenericEdit):
    model = AchievementsCertifications
    form_class = Achievecertiform
    success_url = 'listachievecerti'
    name = 'Achievement/Certification'




class PersonalInfoEdit(UpdateView):
    model = PersonalInfo
    form_class = PersonalInfoForm
    template_name = 'updateform.html'
    success_url = 'educationform'
    pk_url_kwarg = 'resume_id'
    name = 'Personal Info'
    previous_url = 'editresumetitle'
    next_url = 'listeducation'

    def get(self, request, *args, **kwargs):
        resume_id = self.kwargs.get('resume_id')
        personal_info_exists = PersonalInfo.objects.filter(resume__id=resume_id, resume__user=request.user).exists()  
        if not personal_info_exists:
              return redirect('personalinfoform', resume_id=resume_id)

        return super().get(request, *args, **kwargs)
        
    
    def get_object(self, queryset = None):
        return get_object_or_404(PersonalInfo, resume__id=self.kwargs.get('resume_id'), resume__user=self.request.user)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.name
        context['next_url'] = reverse_lazy(self.next_url, kwargs={'resume_id': self.kwargs.get('resume_id') })
        context['previous_url'] = reverse_lazy(self.previous_url, kwargs={'resume_id': self.kwargs.get('resume_id') })
        return context
    
    def get_success_url(self):
        return reverse_lazy(self.success_url,kwargs={'resume_id': self.kwargs.get('resume_id') })



class ResumetitleEdit(UpdateView):
    model = Resume
    form_class = ResumeForm
    pk_url_kwarg = 'resume_id'
    success_url = 'editpersonalinfo'
    name = 'Resume Title'
    next_url = 'editpersonalinfo'
    template_name = 'updateform.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.name
        context['next_url'] = reverse_lazy(self.next_url, kwargs={'resume_id': self.kwargs.get('resume_id') })
        return context
    

    def get_success_url(self):
        return reverse_lazy(self.success_url,kwargs={'resume_id': self.kwargs.get('resume_id') })






class GenericList(LoginRequiredMixin,ListView):
    context_object_name = 'qs'
    template_name = 'listing.html'
    addmoreurlname = None
    nexturl = None
    previous_url = None
    selected = None
    editurl = None
    delete_url = None
    skills = False

    def get_queryset(self):
        qs = super().get_queryset()
        self.resume = get_object_or_404(Resume, id=self.kwargs['resume_id'], user= self.request.user)
        qs = qs.filter(resume = self.resume)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modelused'] = self.model
        context['skills'] = self.skills
        context['resume_id'] = self.resume.id
        context['editurl'] = self.editurl
        context['delete_url'] = self.delete_url
        context['addmorelink'] = reverse_lazy(self.addmoreurlname, kwargs={'resume_id': self.resume.id})
        context['nexturl'] = reverse_lazy(self.nexturl,kwargs={'resume_id': self.resume.id} )
        context['previous_url'] = reverse_lazy(self.previous_url, kwargs={'resume_id': self.kwargs.get('resume_id') }) if self.previous_url else None

        context[self.selected] = True
        return context

    

class EducationList(GenericList):
    model = Education
    addmoreurlname = 'educationform'
    nexturl = 'listexperience'
    selected = 'education'
    editurl = "editeducation"
    delete_url = 'deleteeducation'
    previous_url = 'editpersonalinfo'



class ExperienceList(GenericList):
    model = Experience
    addmoreurlname = 'experienceform'
    nexturl = 'listprojects'
    selected = 'experience'
    editurl = 'editexperience'
    delete_url = 'deleteexperience'
    previous_url = 'listeducation'

class ProjectList(GenericList):
    model = Projects
    addmoreurlname = 'projectsform'
    nexturl = 'listskills'
    selected = 'projects'
    editurl = 'editprojects'
    delete_url = 'deleteproject'
    previous_url = 'listexperience'


class SkillsList(GenericList):
    model = SkillCategory
    addmoreurlname = 'skillsform'
    nexturl = 'listachievecerti'
    selected = 'Skills'
    delete_url = 'deleteskill'
    previous_url = 'listprojects'
    skills = True


class AchievementCertiList(GenericList):
    model = AchievementsCertifications
    addmoreurlname = 'achievecertiform'
    nexturl = 'classic_se'
    selected = 'achievecerti'
    editurl = 'editachievecerti'
    delete_url = 'deleteachievecerti'
    previous_url = 'listskills'


class ListResumeView(ListView):
    model = Resume
    template_name = 'listresume.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs= super().get_queryset()
        return qs.filter(user = self.request.user)
    





class GenericDelete(DeleteView):
    pk_url_kwarg = 'inst_id'
    delete_url = None
    template_name = 'delete_inst.html'
    listing_url = None

    def get_queryset(self):
        qs=  super().get_queryset()
        inst = get_object_or_404(self.model, id=self.kwargs.get('inst_id'))
        self.resume = inst.resume
        return qs.filter(resume__user = self.request.user)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        return context


    def get_success_url(self):
        url = reverse_lazy(self.listing_url, kwargs = {'resume_id': self.resume.id})
        return url



class EducationDeleteView(GenericDelete):
    model = Education
    listing_url = 'listeducation'


class ExperienceDeleteView(GenericDelete):
    model = Experience
    listing_url = 'listexperience'

class ProjectsDeleteView(GenericDelete):
    model = Projects
    listing_url = 'listprojects'

class AcheievementDeleteView(GenericDelete):
    model = AchievementsCertifications
    listing_url = 'listachievecerti'

class SkillsDeleteView(GenericDelete):
    model = SkillCategory
    listing_url = 'listskills'



class ResumeDeleteView(DeleteView):
    model = Resume
    pk_url_kwarg = 'resume_id'
    template_name = 'delete_inst.html'

    def get_queryset(self):
        qs= super().get_queryset()
        return qs.filter(user= self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('listresume')
    
    

