from django.shortcuts import render
from django.views import View
from people.models import Person, Checkin, HomeServices
from django.db.models import Count, Q
import json


class DashboardView(View):
    def get(self, request):
        # 1. totalizadores (Cards Superiores)
        total_people = Person.objects.count()
        active_checkins = Checkin.objects.filter(active=True).count()
        total_services = HomeServices.objects.count()

        # 2. dados para o grafico de perfis de check-in (Pizza/Rosca)
        reasons_data = Checkin.objects.values("reason").annotate(total=Count("id"))
        reason_map = {
            "patient": "Paciente",
            "companion": "Acompanhante",
            "professional": "Profissional",
            "voluntary": "Voluntário",
            "visitor": "Visitante",
            "other": "Outros",
        }
        chart_reasons_labels = [
            reason_map.get(item["reason"], item["reason"]) for item in reasons_data
        ]
        chart_reasons_values = [item["total"] for item in reasons_data]

        # 3. dados para o grafico de serviços mais utilizados (barras)
        services_agg = HomeServices.objects.aggregate(
            breakfast=Count("id", filter=Q(breakfast=True)),
            lunch=Count("id", filter=Q(lunch=True)),
            snack=Count("id", filter=Q(snack=True)),
            dinner=Count("id", filter=Q(dinner=True)),
            shower=Count("id", filter=Q(shower=True)),
            sleep=Count("id", filter=Q(sleep=True)),
        )
        chart_services_labels = [
            "Café da Manhã",
            "Almoço",
            "Lanche",
            "Jantar",
            "Banho",
            "Pernoite",
        ]
        chart_services_values = [
            services_agg["breakfast"] or 0,
            services_agg["lunch"] or 0,
            services_agg["snack"] or 0,
            services_agg["dinner"] or 0,
            services_agg["shower"] or 0,
            services_agg["sleep"] or 0,
        ]

        # 4. mais informacoes: ultimos 5 check-ins realizados
        recent_checkins = Checkin.objects.select_related("person").order_by(
            "-created_at"
        )[:5]

        context = {
            "total_people": total_people,
            "active_checkins": active_checkins,
            "total_services": total_services,
            # json.dumps converte a lista do Python para uma lista do Javascript
            "chart_reasons_labels": json.dumps(chart_reasons_labels),
            "chart_reasons_values": json.dumps(chart_reasons_values),
            "chart_services_labels": json.dumps(chart_services_labels),
            "chart_services_values": json.dumps(chart_services_values),
            "recent_checkins": recent_checkins,
        }
        return render(request, "dashboard.html", context)
