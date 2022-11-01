from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from vendor.models import Vendor
from my_shop.models import Category, ProductItem

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
    context = {
        'vendor': vendor,
        'categories': categories,
    }
    return render(request, 'marketplace/vendor_detail.html', context)
