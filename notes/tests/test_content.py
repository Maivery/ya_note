from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestNoteList(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        Note.objects.bulk_create(
            Note(
                title='Заметка',
                text='Просто текст.',
                slug=f'zametka{index}',
                author=cls.author
            )
            for index in range(10)
        )

    def test_notes_order(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        all_id = [note.id for note in object_list]
        sorted_id = sorted(all_id)
        self.assertEqual(all_id, sorted_id)
