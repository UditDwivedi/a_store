from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem

import requests

def product_list(request):
    products = Product.objects.all()
    if request.method == 'POST':
        # Create a new order
        order = Order.objects.create()

        # Get product ids and their quantities from the form data
        for product_id, quantity in request.POST.items():
            
            if product_id.startswith('product_'):
                product_id = product_id.split('_')[1]
                product = Product.objects.get(id=product_id)
                quantity = int(quantity)
                if quantity > 0:
                    print(f"ProductId: {product_id} - Quantity: {quantity}")
                    # Create an OrderItem for each selected product and quantity
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)

        
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'store/product_list.html', {'products': products})

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'store/order_detail.html', {'order': order})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'store/order_list.html', {'orders': orders})

def generate_upi_qr(order):
    # External API URL for UPI QR code generation (replace with the actual API endpoint)
    api_url = 'https://api.upiqrcode.com/generate'
    print(f"Calling api: Make Amount: {order.total_price()}")
    
    # API payload (replace with the actual payload required by the API)
    payload = {
        'upi_id': 'your-upi-id@bank',  # Replace with the actual UPI ID
        'amount': order.total_price(),
        'name': 'Your Business Name',  # Replace with your business or personal name
        'order_id': order.id,
    }
    
    # Make the API call
    response = requests.post(api_url, json=payload)
    
    # Extract the QR code image URL from the API response
    qr_code_url = response.json().get('qr_code_url')
    
    return qr_code_url

def payment(request, order_id):
    order = Order.objects.get(id=order_id)
    # qr_code_url = generate_upi_qr(order)
    print(f"Calling api: Make Amount: {order.total_price()}")
    return render(request, 'store/payment.html',{"order":order})

def verify_payment(request, order_id):
    # order = Order.objects.get(id=order_id)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        
        order.transaction_id = transaction_id
        order.paid = True
        order.save()

        return redirect('order_detail', order_id=order.id)
    
def delete_order(request, order_id):
    print(f"Delete order: {order_id}")
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list') 
    
