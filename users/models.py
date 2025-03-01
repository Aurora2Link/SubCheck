from django.db import models

class User(models.Model):
    id = models.CharField(max_length=15, primary_key=True)  # Ahora es un string de hasta 15 caracteres
    subscription_until = models.DateField()

    def __str__(self):
        return f"User {self.id} - Subscription Until {self.subscription_until}"
