from django.urls import path
from . import codesign_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'codesign'

urlpatterns = [
    path('', codesign_views.index, name="index"),
    path('index/', codesign_views.index, name="index"),
    path('index-2/', codesign_views.index_2, name="index-2"),
    path('index-3/', codesign_views.index_3, name="index-3"),
    path('index-4/', codesign_views.index_4, name="index-4"),
    path('index-5/', codesign_views.index_5, name="index-5"),
    path('index-6/', codesign_views.index_6, name="index-6"),
    path('about-us/', codesign_views.about_us, name='about-us'),
    path('team/', codesign_views.team, name='team'),
    #path('portfolio/', codesign_views.portfolio, name="portfolio"),
    path('portfolio-details/', codesign_views.portfolio_details, name="portfolio-details"),
    path('services/', codesign_views.services, name="services"),
    path('services-details/', codesign_views.services_details, name="services-details"),
    path('blog-grid/', codesign_views.blog_grid, name="blog-grid"),
    path('blog-large-left-sidebar/', codesign_views.blog_large_left_sidebar, name="blog-large-left-sidebar"),
    path('blog-list-left-sidebar/', codesign_views.blog_list_left_sidebar, name="blog-list-left-sidebar"),
    path('blog/<int:blog_id>/', codesign_views.blog_details, name='blog-details'),
    path('contact-us/', codesign_views.contact, name="contact-us"),  # Changed name to 'contact-us'
    path('give/', codesign_views.coming_soon, name='give'),  # Changed to 'give'
    path('create-checkout-session/', codesign_views.create_checkout_session, name='create_checkout_session'),
    path('success/', codesign_views.success, name='success'),
    path('chatbot/', codesign_views.chatbot, name='chatbot'),
    path('under-construct/', codesign_views.under_construct, name="under-construct"),
    path('error-404/', codesign_views.error_404, name="error-404"),
    path('events/', codesign_views.events, name='events'),
    path('event/<int:event_id>/', codesign_views.event_details, name='event-details'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
