from django.shortcuts import render
from arp_kic.models import Human
from arp_kic.forms import *


# Create your views here.
def is_at_kic(request):
    submit_text = "確認する"
    if request.method == "POST":   
        human = Human.objects.get(name=request.POST["name"])
        human.is_at_kic = False
        human.save() 
        devicies = Device.objects.filter(owner=human)
        if not(devicies) :
            return render(request, 'arp_kic/is_at_kic.html',{"human":human,})
        for device in devicies:
            latest_log = Arp_log.objects.filter(device = device).order_by("-datetime")[0]
            if not(latest_log):
                return render(request, 'arp_kic/is_at_kic.html',{"human":human,})
            from datetime import datetime,timedelta
            from django.utils import timezone
            now   = timezone.now()
            limit = now - timedelta(minutes=5)
            print(now)
            print(limit)
            if  latest_log.datetime > limit:
                human.is_at_kic = True
                human.save()
                break
        return render(request, 'arp_kic/is_at_kic.html',{"human":human,} )
    form = HumanForm()
    return render(
            request,
            'arp_kic/search.html',
            {
                'form':form, 
                'submit_text':submit_text,

            }
        )

