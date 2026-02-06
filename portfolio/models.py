from django.db import models
from django.shortcuts import render  # HTMX এর জন্য লাগবে
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Pagination এর জন্য
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

# 1. Portfolio Index Page (প্রজেক্টের ফোল্ডার)
class PortfolioIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    # এই পেজের নিচে শুধু ProjectPage তৈরি করা যাবে
    subpage_types = ['portfolio.ProjectPage']

    def get_context(self, request):
        context = super().get_context(request)
        
        # আগে ছিল: self.get_children()... (এতে শুধু বেসিক পেজ আসে)
        # এখন আমরা সরাসরি 'ProjectPage' কল করছি যাতে ইমেজসহ সব ফিল্ড আসে
        all_projects = ProjectPage.objects.child_of(self).live().order_by('-first_published_at')
        
        # Pagination Logic (Same as before)
        paginator = Paginator(all_projects, 3) 
        page = request.GET.get('page')
        
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)

        context['projects'] = projects
        return context

    # HTMX রিকোয়েস্ট হ্যান্ডেল করার জন্য serve মেথড ওভাররাইড
    def serve(self, request):
        if request.headers.get('HX-Request'):
            # যদি রিকোয়েস্টটি HTMX থেকে আসে, তাহলে পুরো পেজ না পাঠিয়ে শুধু কার্ডগুলো পাঠাবো
            context = self.get_context(request)
            return render(request, "portfolio/portfolio_projects_partial.html", context)
        
        # আর সাধারণ রিকোয়েস্ট হলে ডিফল্ট বিহেভিয়ার (পুরো পেজ লোড)
        return super().serve(request)


# 2. Single Project Page (এক একটি প্রজেক্ট)
class ProjectPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    
    # প্রজেক্টের ছবি
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )
    
    # লিংকস
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('image'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('github_link'),
        FieldPanel('live_link'),
    ]

    # এই পেজের নিচে আর কোনো পেজ বানানো যাবে না
    subpage_types = []
    # এটি শুধু PortfolioIndexPage-এর নিচে থাকবে
    parent_page_types = ['portfolio.PortfolioIndexPage']