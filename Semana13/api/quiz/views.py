from django.db import transaction
from django.db.models import Count
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, viewsets

from .models import Choice, Exam, Question
from .serializers import ChoiceSerializer, ExamSerializer, QuestionSerializer


class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    queryset = Exam.objects.annotate(question_count=Count("questions")).order_by("id")


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("exam", int, description="Solo las preguntas de este examen."),
        ]
    )
)
class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]

    def get_queryset(self):
        queryset = Question.objects.select_related("exam").prefetch_related("choices")
        exam = self.request.query_params.get("exam")
        if exam and exam.isdigit():
            queryset = queryset.filter(exam_id=int(exam))
        return queryset


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.select_related("question")

    def get_queryset(self):
        queryset = Choice.objects.select_related("question").prefetch_related("question__exam")
        question = self.request.query_params.get("question")
        if question and question.isdigit():
            queryset = queryset.filter(question_id=int(question))
        return queryset

    @staticmethod
    def check_options(question, instance=None, attrs=None, deleting=False):
        options = list(question.choices.values("id", "is_correct"))
        if instance is None:
            options.append({"id": None, "is_correct": attrs.get("is_correct", False)})
        elif deleting:
            options = [item for item in options if item["id"] != instance.id]
        else:
            for item in options:
                if item["id"] == instance.id:
                    item["is_correct"] = attrs.get("is_correct", instance.is_correct)
        if len(options) < 2 or sum(item["is_correct"] for item in options) != 1:
            raise ValidationError({"choices": "Una pregunta necesita al menos dos opciones y exactamente una opción correcta."})

    @transaction.atomic
    def perform_create(self, serializer):
        question = Question.objects.select_for_update().get(pk=serializer.validated_data["question"].pk)
        self.check_options(question, attrs=serializer.validated_data)
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        question = Question.objects.select_for_update().get(pk=serializer.instance.question_id)
        self.check_options(question, instance=serializer.instance, attrs=serializer.validated_data)
        serializer.save()

    @transaction.atomic
    def perform_destroy(self, instance):
        question = Question.objects.select_for_update().get(pk=instance.question_id)
        self.check_options(question, instance=instance, deleting=True)
        instance.delete()
