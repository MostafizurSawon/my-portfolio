from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # এখানে আপনি ইমেইল পাঠানোর কোড লিখবেন (আপাতত কনসোলে প্রিন্ট করছি)
            print("Message received:", form.cleaned_data)
            
            # সাকসেস মেসেজ রিটার্ন করা
            return HttpResponse("""
                <div class="p-6 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-xl text-center fade-in">
                    <svg class="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <h3 class="text-xl font-bold">Message Sent!</h3>
                    <p class="mt-2">Thank you for reaching out. I'll get back to you soon.</p>
                </div>
            """)
    else:
        form = ContactForm()

    return render(request, 'home/contact_form.html', {'form': form})



from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from .models import ContactSubmission 

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # ডাটাবেসে সেভ করা হচ্ছে
            ContactSubmission.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            
            # সাকসেস মেসেজ রিটার্ন করা
            return HttpResponse("""
                <div class="p-6 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-xl text-center fade-in">
                    <svg class="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <h3 class="text-xl font-bold">Message Sent!</h3>
                    <p class="mt-2">Thank you for reaching out. I'll get back to you soon.</p>
                </div>
            """)
    else:
        form = ContactForm()

    return render(request, 'home/contact_form.html', {'form': form})