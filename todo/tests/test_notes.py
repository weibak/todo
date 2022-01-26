import pytest
from django.contrib.auth.models import User
from django.test import Client

from notes.models import Note


@pytest.mark.django_db
class TestNotes:
    def test_notes_index_views(self):
        client = Client()

        response = client.get("/")
        assert response.status_code == 200

    def test_notes_add_views(self):
        client = Client()

        user = User.objects.create(username="test", email="test@mail.ru", password="test")
        client.force_login(user)

        response = client.post("/", {"title": "test", "text": "test"})
        assert response.status_code == 302
        assert Note.objects.count() == 1

        response = client.post("/", {"title": "test", "text": "test"}, follow=True)
        assert response.status_code == 200
        assert Note.objects.count() == 2
