from .models import citizen
from django.dispatch import receiver
from django.db.models.signals import post_save

from registers.models import register
from blocks.models import block


# catch post_save event of citizen model
@receiver(post_save, sender=citizen)
def reception(sender, **kwargs):
    """handler of post_save signal from citizen model"""
    # recover citizen data saved
    registeredCitizen = kwargs['instance']
    # create register
    citizenRegister = register(reg_citizen=registeredCitizen,
                               reg_block=block.getLastBlock())
    citizenRegister.save()
    citizenRegister.registerCitizen()
    citizenRegister.save()