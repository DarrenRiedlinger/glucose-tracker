from django.template import RequestContext
from django.shortcuts import render_to_response

from .forms import SubscriberForm
from .models import Subscriber


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)

         # Check if the email address already exists.
        if Subscriber.objects.filter(email=request.POST['email']).exists():
            return render_to_response('home.html', {'exists': True},
                                      context_instance=RequestContext(request))

        if form.is_valid():
            subscriber = form.save(commit=False)

            # Set the subscriber's source IP.
            subscriber.source_ip = get_client_ip(request)
            subscriber.save()

            return render_to_response('home.html', {'success': True},
                                      context_instance=RequestContext(request))

    return render_to_response('home.html', {'error': True},
                              context_instance=RequestContext(request))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip