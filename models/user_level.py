from tortoise import fields, Model


class UserLevel(Model):
    id = fields.IntField(pk=True)

    user = fields.OneToOneField('models.User', related_name='level', on_delete=fields.CASCADE)

    level = fields.IntField(default=1)  # уровень по умолчанию 1
    experience = fields.IntField(default=0)

    class Meta:
        table = "levels"

    BASE_EXP = 100  # базовый опыт для повышения с 1 на 2 уровень

    def exp_to_next_level(self) -> int:
        level = self.level

        # Базовое значение опыта для следующего уровня
        exp_needed = self.BASE_EXP

        # Логика прогрессии:
        # умножаем базу на коэффициенты для каждого диапазона уровней, пока не дойдём до нужного
        for lvl in range(1, level + 1):
            if 1 <= lvl <= 5:
                multiplier = 2.0
            elif 6 <= lvl <= 10:
                multiplier = 1.5
            elif 11 <= lvl <= 15:
                multiplier = 1.25
            else:
                multiplier = 1.1  # например, для уровней выше 15, чуть меньше прирост

            exp_needed *= multiplier

        return int(exp_needed)
