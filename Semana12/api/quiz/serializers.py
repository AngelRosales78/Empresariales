from django.db import transaction
from rest_framework import serializers

from .models import Choice, Exam, Question


class NestedChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]
        read_only_fields = ["id"]


class ChoiceSerializer(NestedChoiceSerializer):
    class Meta(NestedChoiceSerializer.Meta):
        fields = ["id", "question", "text", "is_correct"]

    def validate(self, attrs):
        if self.instance and attrs.get("question", self.instance.question) != self.instance.question:
            raise serializers.ValidationError({"question": "No se puede cambiar la pregunta de una opción."})
        return attrs


class ExamSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = ["id", "title", "created_at", "question_count"]
        read_only_fields = ["id", "created_at"]


class QuestionSerializer(serializers.ModelSerializer):
    # Choices travel nested inside the question; the exam travels as an identifier.
    choices = NestedChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "exam", "text", "choices", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_choices(self, value):
        # PATCH replaces the nested collection: each new child must be complete.
        if any(not choice.get("text") for choice in value):
            raise serializers.ValidationError("Cada opción necesita un texto.")
        if len(value) < 2:
            raise serializers.ValidationError("Una pregunta necesita al menos dos opciones.")
        if sum(1 for choice in value if choice.get("is_correct")) != 1:
            raise serializers.ValidationError("Debe haber exactamente una opción correcta.")
        return value

    def create(self, validated_data):
        choices = validated_data.pop("choices")
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            Choice.objects.bulk_create(Choice(question=question, **choice) for choice in choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop("choices", None)
        with transaction.atomic():
            instance = Question.objects.select_for_update().get(pk=instance.pk)
            instance = super().update(instance, validated_data)
            if choices is not None:  # sent choices replace the old ones
                instance.choices.all().delete()
                Choice.objects.bulk_create(Choice(question=instance, **choice) for choice in choices)
        return instance
