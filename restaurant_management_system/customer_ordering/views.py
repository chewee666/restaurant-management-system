from django.shortcuts import render, redirect
from .models import Order
from food_menu.models import FoodItem

def create_order(request):
    if request.method == 'POST':
        special_requirement = request.POST.get('special_requirement')
        food_ids = request.POST.getlist('food_items')
        order = Order.objects.create(special_requirement=special_requirement)

        for food_id in food_ids:
            food_item = FoodItem.objects.get(id=food_id)
            order.food_items.add(food_item)

        return redirect('confirm_order', order_id=order.id)

    food_items = FoodItem.objects.filter(hidden=False)
    return render(request, 'customer_ordering/create_order.html', {'food_items': food_items})

def confirm_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.confirmed = True
        order.save()
        return redirect('order_success')

    return render(request, 'customer_ordering/confirm_order.html', {'order': order})

def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()  # 在确认前取消订单
    return redirect('create_order')
