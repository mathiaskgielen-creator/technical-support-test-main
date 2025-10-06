from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Vessel(models.Model):
    name = models.CharField(max_length=100)
    content = (
        models.PositiveIntegerField()
    )  # Amount of refrigerant in the vessel, in kilograms




    def save(self, *args, **kwargs):
        if self.pk:  #Make sure the vessel exists (for updating)
            old_content = Vessel.objects.get(pk=self.pk).content
            
            #Printing the update to show the user the before/after
            print(f"Vessel '{self.name}': {old_content}kg -> {self.content}kg")

            #Negative content results in a ValidationError and the content will not be saved
            if self.content < 0:
                raise ValidationError("Content cannot be negative.")
        super().save(*args, **kwargs)
