from demoapp.factories import (
    CountryFactory,
    EmployeeFactory,
    OfficeFactory,
    UserFactory,
    UserRoleFactory,
)
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("migrate")
        afg = CountryFactory(name="Afghanistan")
        office = OfficeFactory(country=afg)

        OfficeFactory(
            country__name="Ukraine",
        )
        OfficeFactory(
            country__name="Somalia",
        )
        OfficeFactory(
            country__name="Sudan",
        )
        UserFactory(
            username="admin-none",
            is_staff=True,
            is_active=True,
        )

        UserRoleFactory(
            office__name="Afghanistan Office",
            group__name="admins",
            user__username="admin-afg",
            user__is_staff=False,
            user__is_active=True,
        )
        UserRoleFactory(
            office__name="Ukraine Office",
            group__name="admins",
            user__username="admin-ukr",
            user__is_staff=False,
            user__is_active=True,
        )
        EmployeeFactory.create_batch(size=10, office=office)
        UserRoleFactory.create_batch(size=10, office=office)
