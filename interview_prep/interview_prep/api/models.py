from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100, default="UK")
    has_custom_questions = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="custom_questions",
    )
    is_common = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        prefix = "[COMMON]" if self.is_common else f"[{self.university.name}]"
        return f"{prefix} {self.text[:60]}"
