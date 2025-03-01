from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    subscription_until = models.DateField()

    def __str__(self):
        return f"User {self.id} - Subscription Until {self.subscription_until}"
