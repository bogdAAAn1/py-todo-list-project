from django.db import models
from django.urls import reverse


class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse("todo:tag-list", kwargs={"pk": self.pk})

    def __str__(self):
        return self.tag_name


class Task(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag, blank=True, related_name="tasks")

    class Meta:
        ordering = ["is_done", "-created_at"]
