import factory
from django.contrib.auth.models import Group, User
from factory.django import DjangoModelFactory

from .models import Country, Employee, Office, UserRole


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: "username%s" % n)
    is_staff = False
    is_superuser = False

    class Meta:
        model = User
        django_get_or_create = ("username",)


class CountryFactory(DjangoModelFactory):
    name = factory.Iterator(
        ["Afghanistan", "Ukraine", "Somalia", "Sudan", "South Sudan"]
    )

    class Meta:
        model = Country
        django_get_or_create = ("name",)


class OfficeFactory(DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    name = factory.LazyAttribute(lambda o: "%s Office" % o.country.name)

    class Meta:
        model = Office
        django_get_or_create = ("country", "name")


class GroupFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "group %s" % n)

    class Meta:
        model = Group
        django_get_or_create = ("name",)


class UserRoleFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
    office = factory.SubFactory(OfficeFactory)

    class Meta:
        model = UserRole
        django_get_or_create = "user", "office"


class EmployeeFactory(DjangoModelFactory):
    office = factory.SubFactory(OfficeFactory)
    name = factory.Sequence(lambda n: "Employee %s" % n)

    class Meta:
        model = Employee
        django_get_or_create = "name", "office"
