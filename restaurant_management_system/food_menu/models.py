from django.db import models

class FoodItem(models.Model):
    name = models.CharField(max_length=100)  # 菜品名称
    description = models.TextField()  # 菜品描述
    price = models.DecimalField(max_digits=6, decimal_places=2)  # 价格
    available = models.BooleanField(default=True)  # 是否可用
    hidden = models.BooleanField(default=False)  # 是否隐藏（逻辑删除）
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)  # 食物图片



    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)  # 顾客姓名
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)  # 关联的食物
    special_requirement = models.TextField(blank=True)  # 特殊要求
    status = models.CharField(max_length=20, default='Pending')  # 订单状态：Pending, Cancelled, Processed

    def __str__(self):
        return f"Order by {self.customer_name} - {self.food_item.name}"
