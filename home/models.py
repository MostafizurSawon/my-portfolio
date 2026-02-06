from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from .forms import ContactForm
from wagtail.snippets.models import register_snippet

# অন্য অ্যাপ থেকে মডেল ইম্পোর্ট করা
from portfolio.models import ProjectPage

class HomePage(Page):
    # Hero Section Fields
    hero_title = models.CharField(max_length=100, blank=True, help_text="Main headline for the hero section")
    hero_subtitle = models.CharField(max_length=250, blank=True, help_text="Sub-headline or introduction")
    hero_cta_text = models.CharField(max_length=50, blank=True, verbose_name="CTA Button Text", default="View My Work")
    
    # Body Section
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_cta_text'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # লেটেস্ট ৩টি প্রজেক্ট আনা হচ্ছে
        context['latest_projects'] = ProjectPage.objects.live().public().order_by('-first_published_at')[:3]
        context['form'] = ContactForm()
        return context
    

@register_snippet
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"