import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from .models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "Cancel.html"

class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        context = super(ProductLandingPageView,self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY":settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        print(product)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency':'usd',
                        'unit_amount':product.price,
                        'product_data':{
                            'name': product.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return JsonResponse({
            'id': checkout_session.id
        })
    
