from django.views.generic import TemplateView
from django.db.models import Q
from editor.models import SiteBroadcast
from django.utils.timezone import now
from datetime import timedelta
from editor.models import EditorItem, NewQuestion, NewExam, Project, Extension, Theme, CustomPartType, TimelineItem
from django.contrib.auth.models import User

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['navtab'] = 'home'
        context['sticky_broadcasts'] = SiteBroadcast.objects.visible_now().filter(sticky=True)
        return context

class TermsOfUseView(TemplateView):
    template_name = 'terms_of_use.html'
class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'

class GlobalStatsView(TemplateView):
    template_name = 'global_stats.html'

    def get_context_data(self, **kwargs):
        context = super(GlobalStatsView, self).get_context_data(**kwargs)
        t = now()
        periods = [
            timedelta(days=1),
            timedelta(days=7),
            timedelta(days=30),
        ]
        context['recent_data'] = [
            {
                'created': EditorItem.objects.filter(created__gt=t-d).count(),
                'modified': EditorItem.objects.filter(last_modified__gt=t-d).count(),
                'users_active': User.objects.filter(timelineitems__date__gt=t-d).distinct().count(),
            }
            for d in periods
        ]

        active_users = User.objects.filter(is_active=True)

        context['counts'] = {
            'questions': NewQuestion.objects.count(),
            'public_questions': NewQuestion.objects.filter(editoritem__published=True).count(),
            'exams': NewExam.objects.count(),
            'public_exams': NewExam.objects.filter(editoritem__published=True).count(),
            'projects': Project.objects.count(),
            'public_projects': Project.objects.filter(public_view=True).count(),
            'extensions': Extension.objects.count(),
            'themes': Theme.objects.count(),
            'custom_part_types': CustomPartType.objects.count(),
            'users': active_users.count(),
            'user_domains': len(set(u.email.split('@')[1] for u in active_users if '@' in u.email)),
        }
        return context
