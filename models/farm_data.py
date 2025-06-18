from tortoise import fields
from tortoise.models import Model


class UserFarmData(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('models.User', related_name='farm_data', on_delete=fields.CASCADE)
    balance = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_farm_time = fields.DatetimeField(null=True, default=None)

    class Meta:
        table = 'user_farm_data'
