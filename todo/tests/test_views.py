from django.utils import timezone

from django.test import TestCase
from django.urls import reverse

from todo.models import Task, Tag


class TaskTest(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(tag_name="tag1")
        self.tag2 = Tag.objects.create(tag_name="tag2")
        self.tag3 = Tag.objects.create(tag_name="tag3")

        self.task1 = Task.objects.create(
            content="test task1",
            deadline=timezone.now() + timezone.timedelta(days=1),
            is_done=True
        )
        self.task1.tag.add(self.tag1)

        self.task2 = Task.objects.create(
            content="test task2",
            deadline=timezone.now() + timezone.timedelta(days=2),
            is_done=False
        )
        self.task2.tag.add(self.tag1)
        self.task2.tag.add(self.tag2)

        self.task3 = Task.objects.create(
            content="test task3",
            deadline=timezone.now() + timezone.timedelta(days=3),
            is_done=True
        )
        self.task3.tag.add(self.tag1)
        self.task2.tag.add(self.tag2)
        self.task2.tag.add(self.tag3)

    def test_task_list(self):
        response = self.client.get(reverse("todo:task-list"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "test task1")
        self.assertContains(response, "test task2")
        self.assertContains(response, "test task3")

    def test_task_create(self):
        response = self.client.get(reverse("todo:task-create"))
        self.assertEqual(response.status_code, 200)

        input_data = {
            "content": "test task1",
            "deadline": timezone.now() + timezone.timedelta(days=4),
            "is_done": True,
            "tag": [self.tag1.id]
        }
        response = self.client.post(reverse("todo:task-create"), input_data)
        self.assertRedirects(response, reverse("todo:task-list"))
        self.assertEqual(Task.objects.count(), 4)

    def test_task_update(self):
        response = self.client.get(
            reverse("todo:task-update", kwargs={"pk": self.task1.pk})
        )
        self.assertEqual(response.status_code, 200)

        input_data = {
            "content": "test update task1",
            "deadline": timezone.now() + timezone.timedelta(days=5),
            "is_done": True,
            "tag": [self.tag2.id]
        }
        response = self.client.post(
            reverse("todo:task-update", kwargs={"pk": self.task1.pk}),
            input_data
        )
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.content, "test update task1")
        self.assertEqual(self.task1.is_done, True)
        self.assertIn(self.tag2, self.task1.tag.all())

    def test_task_delete(self):
        response = self.client.get(
            reverse("todo:task-delete", kwargs={"pk": self.task1.pk})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("todo:task-delete", kwargs={"pk": self.task1.pk})
        )
        self.assertRedirects(response, reverse("todo:task-list"))
        self.assertEqual(Task.objects.count(), 2)

    def test_toggle_task_status(self):
        response = self.client.get(
            reverse("todo:toggle-task-status", kwargs={"task_id": self.task1.pk})
        )
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.is_done)

    def test_tag_list(self):
        response = self.client.get(reverse("todo:tag-list"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "tag1")
        self.assertContains(response, "tag2")
        self.assertContains(response, "tag3")

    def test_tag_create(self):
        response = self.client.get(reverse("todo:tag-list"))
        self.assertEqual(response.status_code, 200)

        input_data = {
            "tag_name": "new_tag"
        }
        response = self.client.post(reverse("todo:tag-create"), input_data)
        self.assertEqual(Tag.objects.count(), 4)

    def test_tag_update(self):
        response = self.client.get(
            reverse("todo:tag-update", kwargs={"pk": self.tag1.pk})
        )
        self.assertEqual(response.status_code, 200)

        input_data = {
            "tag_name": "update new_tag"
        }
        response = self.client.post(
            reverse("todo:tag-update", kwargs={"pk": self.tag1.pk}),
            input_data
        )
        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.tag_name, "update new_tag")

    def test_tag_delete(self):
        response = self.client.get(
            reverse("todo:tag-delete", kwargs={"pk": self.tag1.pk})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("todo:tag-delete", kwargs={"pk": self.tag1.pk})
        )
        self.assertEqual(Tag.objects.count(), 2)
