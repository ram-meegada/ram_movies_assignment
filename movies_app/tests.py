from django.test import TestCase
from .models import MoviesModel, CollectionModel, MoviesCollectionModel
from .factories import *

class MoviesModelTests(TestCase):
    def setUp(self):
       self.movie = MoviesModelFactory()
    def test_movie_creation(self):
        self.assertIsInstance(self.movie, MoviesModel)
        self.assertTrue(MoviesModel.objects.filter(uuid=self.movie.uuid).exists())

class CollectionModelTests(TestCase):
    def setUp(self):
        self.collection = CollectionModelFactory()
    def test_collection_creation(self):
        self.assertIsInstance(self.collection, CollectionModel)
        self.assertTrue(CollectionModel.objects.filter(uuid=self.collection.uuid).exists())
        self.assertEqual(self.collection.user.username, self.collection.user.username)

class MoviesCollectionModelTests(TestCase):
    def setUp(self):
        self.movies_collection = MoviesCollectionModelFactory()

    def test_movies_collection_creation(self):
        self.assertIsInstance(self.movies_collection, MoviesCollectionModel)
        self.assertTrue(MoviesCollectionModel.objects.filter(collection=self.movies_collection.collection).exists())
        self.assertEqual(self.movies_collection.movie.title, self.movies_collection.movie.title)
