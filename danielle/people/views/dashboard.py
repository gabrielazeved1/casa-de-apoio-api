from django.shortcuts import render
from django.views import View
from people.models import Person, Checkin, HomeServices


class DashboardView(View):
    def get(self, request):
        # coleta os indicadores principais para a casa de apoio
        total_people = Person.objects.count()
        active_checkins = Checkin.objects.filter(active=True).count()
        total_services = HomeServices.objects.count()

        context = {
            "total_people": total_people,
            "active_checkins": active_checkins,
            "total_services": total_services,
        }
        return render(request, "dashboard.html", context)
