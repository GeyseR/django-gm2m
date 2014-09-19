from ..base import TestCase

from ..models import Project
from .models import Links, RelLinks


class ThroughTests(TestCase):

    def setUp(self):
        self.project1 = Project.objects.create()
        self.project2 = Project.objects.create()
        self.links = Links.objects.create()
        RelLinks.objects.create(links=self.links, target=self.project1)

    def test_accessors(self):
        self.assertEqual(self.project1.links_set.count(), 1)
        self.assertIn(self.links, self.project1.links_set.all())

        self.assertEqual(self.links.related_objects.count(), 1)
        self.assertIn(self.project1, self.links.related_objects.all())

    def test_add_relation(self):
        RelLinks.objects.create(links=self.links, target=self.project2)

        self.assertEqual(self.project2.links_set.count(), 1)
        self.assertIn(self.links, self.project1.links_set.all())

        self.assertEqual(self.links.related_objects.count(), 2)
        self.assertIn(self.project2, self.links.related_objects.all())

    def test_cannot_add(self):
        with self.assertRaises(AttributeError):
            self.links.related_objects.add(self.project2)

    def test_cannot_remove(self):
        with self.assertRaises(AttributeError):
            self.links.related_objects.remove(self.project1)