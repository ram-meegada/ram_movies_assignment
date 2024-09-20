import factory
from django.contrib.auth.models import User
from movies_app.models import MoviesModel, CollectionModel, MoviesCollectionModel

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass')

class MoviesModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MoviesModel

    uuid = factory.Faker('uuid4')
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    genres = factory.Faker('word')

class CollectionModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CollectionModel


    user = factory.SubFactory(UserFactory)
    uuid = factory.Faker('uuid4')
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')

class MoviesCollectionModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MoviesCollectionModel

    collection = factory.SubFactory(CollectionModelFactory)
    movie = factory.SubFactory(MoviesModelFactory)