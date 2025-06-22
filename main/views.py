from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy, reverse
from .forms import ResumeForm,PersonalInfoForm, EducationForm, ExperienceForm, Achievecertiform, Projectsform
from .models import Resume, SkillCategory, Skill, PersonalInfo, Education, Experience, AchievementsCertifications, Projects 
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404


def homeview(request):
    return render(request, 'home.html')


class ResumeFormView(LoginRequiredMixin, FormView):
    form_class = ResumeForm
    template_name = 'resume_form.html'

    def get_success_url(self):
        return reverse_lazy('personalinfoform', kwargs={'resume_id': self.object.id})
    

    def form_valid(self, form):
        resumeinstance = form.save(commit=False)
        resumeinstance.user = self.request.user
        resumeinstance.save()
        self.object = resumeinstance
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buildresume'] = True
        return context
    

class PersonalInfoFormView(LoginRequiredMixin,FormView):
    form_class = PersonalInfoForm
    template_name = 'personal_info_form.html'

    def get_success_url(self):
        success_url = reverse_lazy('educationform', kwargs= {'resume_id': self.kwargs['resume_id']})
        return success_url
    

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.resume = get_object_or_404(Resume, id=self.kwargs['resume_id'])
        instance.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal_info'] = True
        context['resume_id'] = self.kwargs.get('resume_id')
        return context



class EducationFormView(LoginRequiredMixin,FormView):
    form_class = EducationForm
    template_name = 'form_template.html'

    def get_success_url(self):
        success_url = reverse_lazy('listeducation', kwargs= {'resume_id': self.kwargs['resume_id']})
        return success_url
    

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.resume = get_object_or_404(Resume, id=self.kwargs['resume_id'])
        instance.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['education'] = True
        context['resume_id'] = self.kwargs.get('resume_id')
        context['listing_url'] = reverse_lazy('listeducation', kwargs= {'resume_id': self.kwargs['resume_id']})
        return context

    

class ExperienceFormView(LoginRequiredMixin,FormView):
    form_class = ExperienceForm
    template_name = 'form_template.html'

    def get_success_url(self):
        success_url = reverse_lazy('listexperience', kwargs= {'resume_id': self.kwargs['resume_id']})
        return success_url
    

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.resume = get_object_or_404(Resume, id=self.kwargs['resume_id'])
        instance.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experience'] = True
        context['resume_id'] = self.kwargs.get('resume_id')
        context['listing_url'] = reverse_lazy('listexperience', kwargs= {'resume_id': self.kwargs['resume_id']})

        return context
    
class ProjectFormView(LoginRequiredMixin, FormView):
    form_class = Projectsform
    template_name = 'form_template.html'

    def get_success_url(self):
        success_url = reverse_lazy('listprojects', kwargs= {'resume_id': self.kwargs['resume_id']})
        return success_url
    

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.resume = get_object_or_404(Resume, id=self.kwargs['resume_id'])
        instance.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = True
        context['resume_id'] = self.kwargs.get('resume_id')
        context['listing_url'] = reverse_lazy('listprojects', kwargs= {'resume_id': self.kwargs['resume_id']})

        return context


    

class AchieveCertiView(LoginRequiredMixin,FormView):
    form_class = Achievecertiform
    template_name = 'form_template.html'

    def get_success_url(self):
        success_url = reverse_lazy('listachievecerti', kwargs= {'resume_id': self.kwargs['resume_id']})
        return success_url
    

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.resume = get_object_or_404(Resume, id=self.kwargs['resume_id'])
        instance.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['achievecerti'] = True
        context['resume_id'] = self.kwargs.get('resume_id')
        context['listing_url'] = reverse_lazy('listachievecerti', kwargs= {'resume_id': self.kwargs['resume_id']})

        return context

    

@login_required
def skillformview(request, resume_id):
    context = {'Skills': True, 'resume_id': resume_id, 'listing_url': reverse('listskills', kwargs={'resume_id': resume_id})}
    if request.method =="POST":
        category = request.POST.get('skillcategory').strip()
        skills = request.POST.get('skills')
        skills_list = skills.split(',')
        skills_list = [i.strip() for i in skills_list]

        resume = get_object_or_404(Resume, id= resume_id)
        category_inst, created = SkillCategory.objects.get_or_create(resume= resume,name=category)
        for skill in skills_list:
            Skill.objects.create(category= category_inst, name = skill)

        
        return redirect(reverse('listskills', kwargs={'resume_id': resume.id}))


    return render(request, 'skills_form.html', context)


class GenericResumePreview(LoginRequiredMixin,TemplateView):

    def get_context_data(self, **kwargs):
        resume_id = self.kwargs.get('resume_id')
        resume = get_object_or_404(Resume, id=resume_id, user= self.request.user)

        personal_info = None
        try:
            personal_info = PersonalInfo.objects.get(resume=resume)
        except PersonalInfo.DoesNotExist:
            pass

        experiences = Experience.objects.filter(resume=resume).order_by('-start_date')
        projects = Projects.objects.filter(resume=resume)
        educations = Education.objects.filter(resume=resume).order_by('-start_date')
        achievements_certifications = AchievementsCertifications.objects.filter(resume=resume).order_by('title')

        # Fetch SkillCategory and prefetch related Skills to avoid N+1 queries
        skill_categories = SkillCategory.objects.filter(resume=resume).prefetch_related('skills').order_by('name')

        context = {
            'resume': resume,
            'preview': True,
            'personal_info': personal_info,
            'experiences': experiences,
            'projects': projects,
            'educations': educations,
            'skill_categories': skill_categories,
            'achievements_certifications': achievements_certifications,
        }

        return context


class ClassicSEPreview(GenericResumePreview):
    template_name = 'resumes/classic_se.html'


class ModernV1(GenericResumePreview):
    template_name = 'resumes/modern_look.html'

class ModernV2(GenericResumePreview):
    template_name = 'resumes/modern_look_v2.html'

class ModernV3(GenericResumePreview):
    template_name = 'resumes/modern_look_v3.html'




class ResumeDownloadView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        download_dict = {
            '1' : 'classic_se.html',
            '2' : 'modern_look.html',
            '3' : 'modern_look_v2.html',
            '4' : 'modern_look_v3.html',
        }
        style_id = self.kwargs.get('style_id')
        temp = download_dict.get(str(style_id))
        if not temp:
            raise Http404("Page Not Found")

        resume = Resume.objects.get(pk=self.kwargs.get('resume_id'), user=request.user)

        personal_info = None
        try:
            personal_info = PersonalInfo.objects.get(resume=resume)
        except PersonalInfo.DoesNotExist:
            pass

        experiences = Experience.objects.filter(resume=resume).order_by('-start_date')
        projects = Projects.objects.filter(resume=resume)
        educations = Education.objects.filter(resume=resume).order_by('-start_date')
        achievements_certifications = AchievementsCertifications.objects.filter(resume=resume).order_by('title')

        # Fetch SkillCategory and prefetch related Skills to avoid N+1 queries
        skill_categories = SkillCategory.objects.filter(resume=resume).prefetch_related('skills').order_by('name')

        context = {
            'resume': resume,
            'preview': False,
            'personal_info': personal_info,
            'experiences': experiences,
            'projects': projects,
            'educations': educations,
            'skill_categories': skill_categories,
            'achievements_certifications': achievements_certifications,
        }



        html = render_to_string(f'resumes/{temp}', context)
    
        pdf_file = HTML(string=html).write_pdf()
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'
        return response


