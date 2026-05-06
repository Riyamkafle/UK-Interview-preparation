from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import University, Question
from .serializers import (
    UniversitySerializer,
    QuestionSerializer,
    EvaluateInputSerializer,
)

CAREER_KEYWORDS = ["career", "job", "profession", "work", "industry", "future",
    "goal", "aspire", "employment", "opportunity", "field"]
FINANCIAL_KEYWORDS = ["fund", "finance", "scholarship", "sponsor", "savings", "loan",
    "family", "support", "cost", "afford", "tuition", "bank"]
UK_KEYWORDS = ["uk", "united kingdom", "england", "british", "britain",
    "quality", "ranked", "reputation", "world-class", "recognised", "recognized", "standard"]


def _score_answer(answer_text, question_text):
    text = answer_text.strip().lower()
    score = 0
    issues = []
    suggestions = []

    if len(text) > 50:
        score += 20
    else:
        issues.append("answer is too short")
        suggestions.append("Write at least 2-3 sentences to explain your point clearly.")

    if any(kw in text for kw in CAREER_KEYWORDS):
        score += 20
    else:
        issues.append("no career-related content")
        suggestions.append("Mention your career goals or how this course helps your future.")

    if any(kw in text for kw in UK_KEYWORDS):
        score += 20
    else:
        issues.append("no UK-specific justification")
        suggestions.append("Explain why studying in the UK is better than alternatives.")

    if any(kw in text for kw in FINANCIAL_KEYWORDS):
        score += 20
    else:
        issues.append("no financial justification")
        suggestions.append("Briefly mention how you plan to fund your studies.")

    sentence_count = max(text.count("."), text.count("!"), text.count("?"))
    if sentence_count >= 2:
        score += 20
    else:
        issues.append("answer lacks structure")
        suggestions.append("Use multiple sentences to make your answer more convincing.")

    return {"question": question_text, "score": score, "issues": issues, "suggestions": suggestions}


def _overall_status(score):
    if score > 75:
        return {"status": "strong", "color": "green", "final_message": "Great preparation! You are well-ready for the interview."}
    elif score >= 50:
        return {"status": "moderate", "color": "yellow", "final_message": "You're close — improve the flagged areas and you'll do well."}
    else:
        return {"status": "weak", "color": "red", "final_message": "Significant preparation needed. Review each area carefully."}


def _improvement_topics(feedback):
    topics = set()
    for item in feedback:
        for issue in item["issues"]:
            if "career" in issue: topics.add("career clarity")
            if "financial" in issue: topics.add("financial explanation")
            if "UK" in issue: topics.add("UK study justification")
            if "short" in issue or "structure" in issue: topics.add("answer depth & structure")
    return sorted(topics)


class UniversityListView(APIView):
    def get(self, request):
        search = request.query_params.get("search", "").strip()
        qs = University.objects.all()
        if search:
            qs = qs.filter(name__icontains=search)
        serializer = UniversitySerializer(qs, many=True)
        return Response({"count": qs.count(), "results": serializer.data})


class QuestionListView(APIView):
    def get(self, request):
        university_id = request.query_params.get("university_id")
        if not university_id:
            return Response({"error": "university_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            university = University.objects.get(pk=university_id)
        except University.DoesNotExist:
            return Response({"error": "University not found."}, status=status.HTTP_404_NOT_FOUND)

        common_qs = Question.objects.filter(is_common=True)
        if university.has_custom_questions:
            custom_qs = Question.objects.filter(university=university, is_common=False)
            questions = list(common_qs) + list(custom_qs)
        else:
            questions = list(common_qs)

        serializer = QuestionSerializer(questions, many=True)
        return Response({"university": university.name, "has_custom_questions": university.has_custom_questions, "count": len(questions), "questions": serializer.data})


class EvaluateView(APIView):
    def post(self, request):
        serializer = EvaluateInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Invalid input.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        answers = serializer.validated_data["answers"]
        feedback = []
        for item in answers:
            try:
                question = Question.objects.get(pk=item["question_id"])
            except Question.DoesNotExist:
                feedback.append({"question": f"Question ID {item['question_id']}", "score": 0, "issues": ["question not found"], "suggestions": ["Use a valid question_id from /api/questions/"]})
                continue
            feedback.append(_score_answer(item["answer"], question.text))

        overall_score = round(sum(f["score"] for f in feedback) / len(feedback)) if feedback else 0
        status_info = _overall_status(overall_score)
        return Response({"overall_score": overall_score, **status_info, "feedback": feedback, "improvement_topics": _improvement_topics(feedback)})
