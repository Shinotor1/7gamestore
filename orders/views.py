from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from games.models import Game
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required 


def checkout(request, game_id):
    """
    Страница оформления заказа одной игры.
    """
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == 'POST':

        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Пожалуйста, введите email для доставки ключа.')
            return redirect('orders:checkout', game_id=game.id)
        
        # Создаём заказ
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=email,
            total_price=game.price,
            status='paid'  
        )
        
  
        OrderItem.objects.create(
            order=order,
            game=game,
            price=game.price
        )
        
        # TODO: Здесь будет отправка email с ключом
        
        messages.success(request, f'Заказ успешно оформлен! Ключ отправлен на {email}')
        return redirect('orders:order_success', order_id=order.id)
    

    initial_email = request.user.email if request.user.is_authenticated else ''
    
    return render(request, 'orders/checkout.html', {
        'game': game,
        'initial_email': initial_email
    })


def order_success(request, order_id):
    """
    Страница успешного оформления заказа.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required  
def order_history(request):
    """
    Страница истории заказов текущего пользователя.
    """
    orders = request.user.orders.prefetch_related('items__game').all()
    
    return render(request, 'orders/order_history.html', {'orders': orders})