from rest_framework import serializers
from .models import University, Question


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name", "country", "has_custom_questions"]


class QuestionSerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(
        source="university.name", read_only=True, default=None
    )

    class Meta:
        model = Question
        fields = ["id", "text", "is_common", "university_name"]


class AnswerInputSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField(min_length=1)


class EvaluateInputSerializer(serializers.Serializer):
    answers = AnswerInputSerializer(many=True, min_length=1)
