from django.shortcuts import render ,redirect
from .forms import *
from .models import *
from  django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth.decorators import login_required




@login_required(login_url='login_user')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    orders_count = orders.count()
    orders_delivered_count = Order.objects.filter(status='Delivered').count()
    orders_pending_count = Order.objects.filter(status='Pending').count()
    context = {
        'customers':customers,
        'orders':orders,
        'orders_count':orders_count,
        'orders_delivered_count':orders_delivered_count,
        'orders_pending_count':orders_pending_count,
    }
    return render(request, 'accounts/pages/dashbord.html',context)




@login_required(login_url='login_user')
def products(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, 'accounts/pages/products.html',context)





@login_required(login_url='login_user')
def customer(request,customer_id):
    customer = Customer.objects.get(pk=customer_id)
    orders = customer.order_set.all()
    orders_count = orders.count()
    my_filter = order_filter(request.GET,queryset=orders)
    orders = my_filter.qs
    context = {
        'customer':customer,
        'orders':orders,
        'orders_count':orders_count,
        'my_filter':my_filter,
    }
    return render(request, 'accounts/pages/customer.html',context)





@login_required(login_url='login_user')
def update_order(request,order_id):
    if request.method == "GET":
        order = Order.objects.get(pk=order_id)
        form = Order_form(instance=order)
        context = {
            'form': form,
            'order_id' : order_id,
        }
        return render(request, 'accounts/pages/update-order.html', context)
    else:
        order = Order.objects.get(pk=order_id)
        form = Order_form(request.POST,instance=order)
        if form.is_valid():
            form.save()
        return redirect('home')






@login_required(login_url='login_user')
def create_order(request,customer_id) :
    order_form_set =inlineformset_factory(Customer,Order,fields=('product' , 'status'),extra=7)
    customer = Customer.objects.get(pk=customer_id)
    form_set = order_form_set(queryset=Order.objects.none(),instance = customer)
    if request.method == "GET" :
        context = {
            'form_set' : form_set,
        }
        return render(request, 'accounts/pages/create-order.html', context)
    else :
        form = order_form_set(request.POST,instance = customer)
        if form.is_valid() :
            form.save()
        return redirect('customer',customer_id)




@login_required(login_url='login_user')
def delete_order(request,order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == "GET" :
        context = {
            'order' : order,
        }
        return render(request, 'accounts/pages/delete_order.html', context)
    else :
        order.delete()
        return redirect('home')

