"""
Home page models for Wagtail CMS
"""
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    """Main homepage"""
    
    hero_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hero_cta_text = models.CharField(max_length=100, blank=True, default="Shop Now")
    hero_cta_link = models.URLField(blank=True)
    
    # Featured section
    featured_title = models.CharField(max_length=255, blank=True, default="Featured Products")
    featured_description = RichTextField(blank=True)
    
    # About section
    about_title = models.CharField(max_length=255, blank=True, default="About LUVORA")
    about_content = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_image'),
        FieldPanel('hero_cta_text'),
        FieldPanel('hero_cta_link'),
        FieldPanel('featured_title'),
        FieldPanel('featured_description'),
        FieldPanel('about_title'),
        FieldPanel('about_content'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Add featured products
        from shop.models import ProductPage
        context['featured_products'] = ProductPage.objects.live().public().filter(
            is_featured=True,
            is_available=True
        )[:6]
        
        return context
    
    class Meta:
        verbose_name = "Home Page"
