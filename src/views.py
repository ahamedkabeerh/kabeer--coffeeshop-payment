from django.shortcuts import render
from .forms import CoffeePaymentForm
import razorpay
from .models import ColdCoffee
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def coffee_payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount'))* 100

        #create razorpay client
        client = razorpay.Client(auth=('rzp_test_VhKN7S9724qqXU','PrXAcRCbqUpfhJx1ZPEg0T76'))

        #create order

        response_payment = client.order.create(dict(amount=amount,currency='INR'))
        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status == 'created':
            cold_coffee = ColdCoffee(
                name=name,
                amount=amount,
                order_id=order_id
            )
            cold_coffee.save()
            response_payment['name'] = name


            form = CoffeePaymentForm(request.POST or None)
            return render(request,'coffee_payment.html',{'form':form,'payment': response_payment})
    form = CoffeePaymentForm()
    return render(request,'coffee_payment.html',{'form':form})

@csrf_exempt
def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    #client instance
    client = razorpay.Client(auth=('rzp_test_VhKN7S9724qqXU','PrXAcRCbqUpfhJx1ZPEg0T76'))
    try:
        status = client.utility.verify_payment_signature(params_dict)
        cold_coffee = ColdCoffee.objects.get(order_id=response['razorpay_order_id'])
        cold_coffee.razorpay_payment_id = response['razorpay_payment_id']
        cold_coffee.paid = True
        cold_coffee.save()
        return render(request,'payment_status.html',{'status':True})
    except:
        return render(request,'payment_status.html',{'status':False})