from django.db import models

from myojeong_be.const import emoji_list


class Wish(models.Model):
    from_name = models.CharField(max_length=6, db_index=True)
    to_name = models.CharField(max_length=6, null=True, default=None)
    content = models.CharField(max_length=150)
    emoji = models.CharField(max_length=2, choices=emoji_list)
    is_open = models.BooleanField(default=True)
    password = models.CharField(max_length=256, null=True, default=None)
    sp1 = models.IntegerField(default=0)
    sp2 = models.IntegerField(default=0)
    sp3 = models.IntegerField(default=0)
    sp_sum = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
