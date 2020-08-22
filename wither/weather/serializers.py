from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    class Meta:
        fields = (
            "avg",
            "min",
            "max",
            "median",
        )
        read_only_fields = fields
