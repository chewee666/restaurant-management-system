from django.db import models
from food_menu.models import FoodItem

class Order(models.Model):
    food_items = models.ManyToManyField(FoodItem, related_name='orders')  # 添加 related_name 避免冲突
    special_requirement = models.TextField(blank=True, null=True)  # 特殊需求
    confirmed = models.BooleanField(default=False)  # 是否确认
    created_at = models.DateTimeField(auto_now_add=True)
