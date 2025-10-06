from django.core.management.base import BaseCommand
from ...models import Vessel
import threading
from django.db import transaction
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Simulate condition when withdrawing refrigerant from a vessel."

    def handle(self, *args, **kwargs):
        Vessel.objects.create(name="Test Vessel", content=50.0)
        self.stdout.write("Simulating condition...")
        self.run_simulation()

    def run_simulation(self):
        barrier = threading.Barrier(2)

        #Refactored the update logic to one method
        def withdraw():
            with transaction.atomic():
                try:
                    #Lock the row so only one thread can modify it at a time (needs to be inside a transaction)
                    vessel = Vessel.objects.select_for_update().get(id=1)
                    vessel.content -= 10.0
                    vessel.save()
                except ValidationError as e:
                    #Print the error thrown by save in case of negative content
                    print(e.messages[0])

        def user1():
            barrier.wait()
            withdraw()

        def user2():
            barrier.wait()
            withdraw()

        t1 = threading.Thread(target=user1)
        t2 = threading.Thread(target=user2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        vessel = Vessel.objects.get(id=1)
        self.stdout.write(f"Remaining content: {vessel.content} kg")
