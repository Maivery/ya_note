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
        cls.reader = User.objects.create(username='Человек')
        cls.notes_list = Note.objects.bulk_create(
            Note(
                title='Заметка',
                text='Просто текст.',
                slug=f'zametka{index}',
                author=cls.author
            )
            for index in range(10)
        )
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='zametka',
            author=cls.author,
            )

    def test_notes_order(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        all_id = [notes_list.id for notes_list in object_list]
        sorted_id = sorted(all_id)
        self.assertEqual(all_id, sorted_id)

    def test_note_in_list(self):
        users = (
            (self.author, True),
            (self.reader, False),
        )
        for name, bool in users:
            self.client.force_login(name)
            with self.subTest(name=name, bool=bool):
                response = self.client.get(self.LIST_URL)
                object_list = response.context['object_list']
                check = self.note in object_list
                self.assertIs(check,  bool)

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:add', None),
        )
        for name, args in urls:
            self.client.force_login(self.author)
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
        self.assertIn('form', response.context)
