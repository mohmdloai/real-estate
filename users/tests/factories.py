import factory
from factory.django import DjangoModelFactory
from users.models import UserAccount

class UserAccountFactory(DjangoModelFactory):
    class Meta:
        model = UserAccount


    email = factory.Sequence(lambda n: f'user{n}@example.com')
    name = factory.Faker('name')
    is_active = True
    is_staff = False
    is_realtor = factory.Faker('boolean')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')


    class Params:
        ...