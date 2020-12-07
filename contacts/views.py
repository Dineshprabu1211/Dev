from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(user_id=user_id, listing_id=listing_id)
            if has_contacted:
                messages.error(request, "You had already made an inquiry for this Listing")
                return redirect('/listings/'+listing_id)

        contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        send_mail(
            'Propert Listing Inquiry',
            'You had Recieved an Inquiry in '+ listing +'.Click the link below to go Admin to see full details',
            'dineshprabu1211@gmail.com',
            [realtor_email, 'dineshprabu9@gmail.com'],
            fail_silently = False
        )

        messages.success(request, 'You Request has been recieved...Our Realtor will contact you soon!!')

        return redirect('/listings/'+listing_id)
