from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from vendor.models import Vendor
from my_shop.models import Category, ProductItem

from .models import Cart

from marketplace.context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required

# Create your views here.

#  helper
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    # prefetch_related is a django method to get access to a particular modeusing is foreign key in this case productitem through category
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'productitem',
            queryset = ProductItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, item_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                productitem = ProductItem.objects.get(id=item_id)
                print(productitem)
                # check if the user has already added the item to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, productitem=productitem)
                    # increase cart quantity
                    chkCart.quantity +=1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Cart quantity increased!', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, productitem=productitem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'added the item to the cart!', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'this item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})    
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

def decrease_cart(request, item_id):
    if request.user.is_authenticated:
        # return HttpResponse(item_id)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                productitem = ProductItem.objects.get(id=item_id)
                print(productitem)
                # check if the user has already added the item to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, productitem=productitem)
                    if chkCart.quantity > 1:
                        # decrease cart quantity
                        chkCart.quantity -=1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity,
                    'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'this item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})    
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})




@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})