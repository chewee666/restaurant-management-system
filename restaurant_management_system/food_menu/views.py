from django.shortcuts import render, get_object_or_404, redirect
from .models import FoodItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# 添加新食物信息
@login_required(login_url='owner_login')
def add_food(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')
        FoodItem.objects.create(name=name, description=description, price=price, image=image)
        return redirect('food_list')  # 添加完成后重定向到食物列表页面
    return render(request, 'food_menu/add_food.html')


# 修改食物信息
@login_required(login_url='owner_login')
def edit_food(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    if request.method == 'POST':
        food.name = request.POST['name']
        food.description = request.POST['description']
        food.price = request.POST['price']
        if 'image' in request.FILES:
            food.image = request.FILES['image']  # 如果上传了新图片，更新图片
        food.save()
        return redirect('food_list')

    return render(request, 'food_menu/edit_food.html', {'food': food})


# 逻辑删除食物（移动到隐藏）
@login_required(login_url='owner_login')
def hide_food(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    food.hidden = True
    food.save()
    return redirect('food_list')


# 展示食物列表（仅Owner可见）
@login_required(login_url='owner_login')
def food_list(request):
    query = request.GET.get('q')  # 获取搜索关键词
    if query:
        food_items = FoodItem.objects.filter(name__icontains=query, hidden=False)  # 根据关键词搜索
    else:
        food_items = FoodItem.objects.filter(hidden=False)  # 默认显示所有未隐藏的食物

    return render(request, 'food_menu/food_list.html', {'food_items': food_items})


# 顾客可见的食物菜单
def food_menu(request):
    query = request.GET.get('q')  # 获取搜索关键词
    if query:
        food_items = FoodItem.objects.filter(name__icontains=query, hidden=False)  # 根据关键词搜索
    else:
        food_items = FoodItem.objects.filter(hidden=False)  # 显示未隐藏的食物

    return render(request, 'food_menu/food_menu.html', {'food_items': food_items})



# Owner 登录
def owner_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # 获取 "next" 参数，如果存在并且是 "/food_menu/list/"，则跳转到菜单页面
            next_url = request.POST.get('next')
            if next_url and next_url == '/food_menu/list/':
                return redirect('food_menu')  # 跳转到 Food Menu 页面

            return redirect('owner_dashboard')  # 默认登录后跳转到 Owner 仪表盘
        else:
            return render(request, 'food_menu/login.html', {'error': 'Invalid credentials'})

    # 如果是 GET 请求，获取 "next" 参数
    next_url = request.GET.get('next', '')
    # 如果 next 参数为 /food_menu/list/，直接跳转到菜单
    if next_url == '/food_menu/list/':
        return redirect('food_menu')  # 跳转到 Food Menu 页面

    return render(request, 'food_menu/login.html', {'next': next_url})


# Owner 登出
@login_required(login_url='owner_login')
def owner_logout(request):
    logout(request)
    return redirect('food_menu')  # 登出后重定向到顾客菜单页面


# Owner 仪表盘
@login_required(login_url='owner_login')
def owner_dashboard(request):
    return render(request, 'food_menu/owner_dashboard.html')  # 渲染管理页面


# 批量逻辑删除
@login_required(login_url='owner_login')
def bulk_delete(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')  # 获取选中的食物项ID
        for item_id in selected_items:
            food = get_object_or_404(FoodItem, id=item_id)
            food.hidden = True  # 逻辑删除（隐藏食物）
            food.save()
    return redirect('food_list')  # 删除后重定向到食物列表


# 查看临时文件夹（隐藏的食物）
@login_required(login_url='owner_login')
def temporary_file(request):
    hidden_food_items = FoodItem.objects.filter(hidden=True)  # 获取已隐藏的食物
    return render(request, 'food_menu/temporary_file.html', {'hidden_food_items': hidden_food_items})


# 恢复食物（从隐藏恢复）
@login_required(login_url='owner_login')
def restore_food(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    food.hidden = False  # 将食物恢复
    food.save()
    return redirect('temporary_file')  # 恢复后重定向到临时文件页面


# 永久删除食物
@login_required(login_url='owner_login')
def delete_food_permanently(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    food.delete()  # 永久删除食物
    return redirect('temporary_file')  # 删除后重定向到临时文件页面


# 渲染主页
def home(request):
    return render(request, 'home.html')  # 渲染主页模板
