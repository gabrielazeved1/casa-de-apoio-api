from people.models import Checkout
from rest_framework import serializers


class CheckoutSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # check if checkin is active
        # propagacao do erro 2, se o campo active continua como true, tem a possibilidade de fazer o checkout
        # entretanto tem a relacao 1->1 , vai dar erro, visto que o checkin ja tem um checkout
        # gera sujeira de um checkin que ja deveria esta false
        if not data["checkin"].active:
            raise serializers.ValidationError({"checkin": "Checkin inválido."})
        return data

    class Meta:
        model = Checkout
        fields = "__all__"
