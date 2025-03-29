from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import requests
import sys
from django.utils import timezone
from .models import SliderImage, AboutImage, ServiceImage, VideoImage, TeamImage, BlogImage
from openai import OpenAI
import logging

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event

logger = logging.getLogger(__name__)

stripe.api_key = 'sk_test_your_secret_key'  # Replace with your Stripe Secret Key
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)




def index(request):
    slider_images = SliderImage.objects.all().order_by('-created_at')[:2]  # 2 for slider
    about_images = AboutImage.objects.all().order_by('-created_at')[:2]    # 2 for about
    service_images = ServiceImage.objects.all().order_by('-created_at')[:3]  # Exactly 3 for services
    video_image = VideoImage.objects.first()  # 1 for video
    team_images = TeamImage.objects.all().order_by('-created_at')[:2]     # 2 for team
    blog_images = BlogImage.objects.all().order_by('-post_date')[:2]      # 2 for blog

    context = {
        'slider_images': slider_images,
        'about_images': about_images,
        'service_images': service_images,
        'video_image': video_image,
        'team_images': team_images,
        'blog_images': blog_images,
    }
    return render(request, 'codesign/index.html', context)
def index_2(request):
    context={
        "page_title":"Home 2"
    }
    return render(request,'codesign/index-2.html',context)

def index_3(request):
    context={
        "page_title":"Home 3"
    }
    return render(request,'codesign/index-3.html',context)

def index_4(request):
    context={
        "page_title":"Home 4"
    }
    return render(request,'codesign/index-4.html',context)

def index_5(request):
    context={
        "page_title":"Home 5"
    }
    return render(request,'codesign/index-5.html',context)

def index_6(request):
    context={
        "page_title":"Home 6"
    }
    return render(request,'codesign/index-6.html',context)

def about_us(request):
    about_images = AboutImage.objects.all().order_by('-created_at')[:2]  # 2 images for About Us
    team_images = TeamImage.objects.all().order_by('-created_at')[:2]   # 2 images for Team
    context = {
        'about_images': about_images,
        'team_images': team_images,
    }
    return render(request, 'codesign/about-us.html', context)


def team(request):
    team_images = TeamImage.objects.all().order_by('-created_at')[:2]  # Limit to 2 as per your original layout
    context = {
        'team_images': team_images,
    }
    return render(request, 'codesign/team.html', context)
def events(request):
    events = Event.objects.all()
    return render(request, 'codesign/portfolio.html', {'events': events, 'page_title': 'Events'})

def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'codesign/event_details.html', {'event': event})

def portfolio_details(request):
    context={
        "page_title":"Portfolio Details"
    }
    return render(request,'codesign/portfolio-details.html',context)

def services_details(request):
    context={
        "page_title":"Services Details"
    }
    return render(request,'codesign/services-details.html',context)

def services(request):
    service_images = ServiceImage.objects.all().order_by('-created_at')[:3]  # Limit to 3 for Services
    context = {
        'service_images': service_images,
    }
    return render(request, 'codesign/services.html', context)
 
def blog_grid(request):
    context={
        "page_title":"Blog Grid"
    }
    return render(request,'codesign/blog-grid.html',context)

def blog_large_left_sidebar(request):
    context={
        "page_title":"Large Left Sidebar"
    }
    return render(request,'codesign/blog-large-left-sidebar.html',context) 

def blog_list_left_sidebar(request):
    context={
        "page_title":"List Left Sidebar"
    }
    return render(request,'codesign/blog-list-left-sidebar.html',context)

def blog_details(request, blog_id):
    blog = get_object_or_404(BlogImage, id=blog_id)
    next_blog = BlogImage.objects.filter(created_at__lt=blog.created_at).order_by('-created_at').first()
    prev_blog = BlogImage.objects.filter(created_at__gt=blog.created_at).order_by('created_at').first()
    context = {
        'blog': blog,
        'next_blog': next_blog,
        'prev_blog': prev_blog,
    }
    return render(request, 'codesign/blog-details.html', context)

def contact_us(request):
    context={
        "page_title":"Contact Us"
    }
    return render(request,'codesign/contact-us.html',context)

def coming_soon(request):
    context={
        "page_title":"Coming Soon"
    }
    return render(request,'codesign/give.html',context)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            amount = int(float(request.POST.get('amount')) * 100)  # Convert dollars to cents
            if amount < 100:  # Minimum $1
                return JsonResponse({'error': 'Amount must be at least $1'}, status=400)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': amount,
                            'product_data': {
                                'name': 'Donation',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/give/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def success(request):
    return render(request, 'codesign/success.html', {'message': 'Thank you for your donation!'})


@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message')
            if not user_message:
                return JsonResponse({'error': 'Message is required'}, status=400)

            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for the Codesign website."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150
            )
            bot_message = response.choices[0].message.content.strip()
            return JsonResponse({'message': bot_message})
        except Exception as e:
            logger.error(f"Error in chatbot: {str(e)}")
            return JsonResponse({'error': 'An error occurred while processing your request'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def under_construct(request):
    context={
        "page_title":"Under Construct"
    }
    return render(request,'codesign/under-construct.html',context)

def error_404(request):
    context={
        "page_title":"Error 404"
    }
    return render(request,'404.html',context)


def contact(request):
    print("Contact view triggered - Entering view", file=sys.stderr)
    print(f"Request method: {request.method}", file=sys.stderr)
    print(f"Request path: {request.path}", file=sys.stderr)
    
    if request.method == 'POST':
        print("POST request received - Processing form", file=sys.stderr)
        first_name = request.POST.get('dzFirstName')
        last_name = request.POST.get('dzLastName')
        email = request.POST.get('dzEmail')
        phone = request.POST.get('dzPhoneNumber')
        subject = request.POST.get('dzOther[subject]')
        message = request.POST.get('dzMessage')

        print(f"Form data received: FirstName={first_name}, LastName={last_name}, Email={email}, Phone={phone}, Subject={subject}, Message={message}", file=sys.stderr)
        full_message = f"Name: {first_name} {last_name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
        
        print(f"Attempting to send email from {email} to {settings.CONTACT_EMAIL}", file=sys.stderr)
        try:
            send_mail(
                subject=f"MFM Dallas Contact: {subject}",
                message=full_message,
                from_email=email,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            print("Email sent successfully", file=sys.stderr)
            success_msg = "Message sent on " + str(timezone.now()) + "!"
            messages.success(request, success_msg)
            print(f"Success message set to '{success_msg}'", file=sys.stderr)
        except Exception as e:
            print(f"Email sending failed with error: {str(e)}", file=sys.stderr)
            messages.error(request, f"Error sending message: {str(e)}. Please try again.")
        
        print("Redirecting to codesign:contact-us", file=sys.stderr)
        return redirect('codesign:contact-us')

    print("Rendering contact-us.html for GET request", file=sys.stderr)
    return render(request, 'codesign/contact-us.html')