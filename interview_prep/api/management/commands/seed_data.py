from django.core.management.base import BaseCommand
from api.models import University, Question


UNIVERSITIES = [
    {"name": "University of Greenwich",          "has_custom_questions": True},
    {"name": "University of East London",         "has_custom_questions": True},
    {"name": "Middlesex University",              "has_custom_questions": False},
    {"name": "Coventry University",               "has_custom_questions": True},
    {"name": "University of Hertfordshire",       "has_custom_questions": False},
    {"name": "University of West London",         "has_custom_questions": True},
    {"name": "Birmingham City University",        "has_custom_questions": False},
    {"name": "University of Sunderland",          "has_custom_questions": False},
    {"name": "University of Essex",               "has_custom_questions": False},
    {"name": "University of Leicester",           "has_custom_questions": False},
    {"name": "University of Westminster",         "has_custom_questions": False},
    {"name": "Northumbria University",            "has_custom_questions": False},
    {"name": "De Montfort University",            "has_custom_questions": False},
    {"name": "University of Bedfordshire",        "has_custom_questions": False},
    {"name": "University of Roehampton",          "has_custom_questions": True},
    {"name": "University of South Wales",         "has_custom_questions": False},
    {"name": "Teesside University",               "has_custom_questions": False},
    {"name": "Anglia Ruskin University",          "has_custom_questions": False},
    {"name": "University of Gloucestershire",     "has_custom_questions": False},
    {"name": "University of Northampton",         "has_custom_questions": False},
    {"name": "University of Bradford",            "has_custom_questions": False},
    {"name": "University of Derby",               "has_custom_questions": False},
    {"name": "Sheffield Hallam University",       "has_custom_questions": False},
    {"name": "Liverpool John Moores University",  "has_custom_questions": False},
    {"name": "University of Portsmouth",          "has_custom_questions": False},
    # Added universities
    {"name": "BPP University",                    "has_custom_questions": True},
    {"name": "Ravensbourne University London",    "has_custom_questions": True},
    {"name": "Ulster University",                 "has_custom_questions": True},
]

COMMON_QUESTIONS = [
    "Why did you choose this course?",
    "Why did you choose this university?",
    "Why do you want to study in the UK?",
    "What are your career goals after completing this course?",
    "How will you fund your studies in the UK?",
    "What will you do after graduation — return home or stay in the UK?",
]

CUSTOM_QUESTIONS = {
    "University of Greenwich": [
        "Why do you prefer a practical, industry-based learning environment?",
        "How does Greenwich's location in London benefit your studies?",
    ],
    "University of East London": [
        "How does UEL's diverse campus environment align with your values?",
        "What specific UEL facilities or resources attracted you to apply?",
    ],
    "Coventry University": [
        "How does this course at Coventry match current industry demand?",
        "Why do you believe Coventry's work-placement approach suits you?",
    ],
    "University of West London": [
        "How does UWL's industry-focused curriculum align with your goals?",
        "Can you explain why West London's location suits your study plans?",
    ],
    "University of Roehampton": [
        "What attracted you to Roehampton's campus-based university experience?",
        "How does Roehampton's focus on personal development match your needs?",
    ],
    "BPP University": [
        "Why do you prefer a professional, career-focused institution like BPP?",
        "How does BPP's strong industry links benefit your career path?",
        "Can you explain how BPP's flexible learning model suits your situation?",
    ],
    "Ravensbourne University London": [
        "Why are you drawn to a specialist creative and digital media university?",
        "How does Ravensbourne's industry partnerships support your creative career?",
        "What specific creative discipline are you pursuing and why Ravensbourne?",
    ],
    "Ulster University": [
        "Why did you choose Ulster University over universities in England?",
        "How do you feel about studying and living in Northern Ireland?",
        "What does Ulster's research-led teaching approach mean for your studies?",
    ],
}


class Command(BaseCommand):
    help = "Seed the database with universities and questions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"] or not University.objects.exists():
            Question.objects.all().delete()
            University.objects.all().delete()
            self.stdout.write("Cleared existing data.")

        if University.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Data already exists. Run with --clear to reseed."
            ))
            return

        uni_objects = {}
        for data in UNIVERSITIES:
            uni = University.objects.create(
                name=data["name"], country="UK",
                has_custom_questions=data["has_custom_questions"]
            )
            uni_objects[data["name"]] = uni
            self.stdout.write(f"  ✓ {uni.name}")

        self.stdout.write(f"\nCreated {len(uni_objects)} universities.")

        for text in COMMON_QUESTIONS:
            Question.objects.create(text=text, is_common=True, university=None)

        self.stdout.write(f"Created {len(COMMON_QUESTIONS)} common questions.")

        custom_count = 0
        for uni_name, questions in CUSTOM_QUESTIONS.items():
            uni = uni_objects.get(uni_name)
            if not uni:
                continue
            for text in questions:
                Question.objects.create(text=text, is_common=False, university=uni)
                custom_count += 1

        self.stdout.write(f"Created {custom_count} custom questions.")
        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Seed complete! "
            f"{University.objects.count()} universities, "
            f"{Question.objects.filter(is_common=True).count()} common, "
            f"{Question.objects.filter(is_common=False).count()} custom questions."
        ))
