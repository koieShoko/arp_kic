from django.db import models

class Human(models.Model):
    name        = models.CharField(
        max_length = 100,
        default = 'someone',
    )
    is_at_kic   = models.BooleanField(
        default    = False,
    )
    def __str__(self):
        return self.name


class Device(models.Model):
    name        = models.CharField(
        max_length = 100,
    )
    mac_address = models.CharField(
        max_length = 100,
    )
    owner       = models.ForeignKey(
        Human, 
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )
    def __str__(self):
        return self.name + self.mac_address

class Arp_log(models.Model):
    datetime    = models.DateTimeField(
    )
    place       = models.CharField(
        max_length = 500,
    )
    device = models.ForeignKey(
        Device,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )
    def __str__(self):
        return str(self.datetime) + ', ' + str(self.device)
