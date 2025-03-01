import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from datetime import date, timedelta

@csrf_exempt
def check_subscription(request):
    print(f"Request method received: {request.method}")  # 🔹 Agrega esto

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_id = data.get('phone')

            if phone_id is None:
                return JsonResponse({'error': 'Phone ID is missing'}, status=400)

            try:
                user = User.objects.get(id=phone_id)
                is_subscribed = user.subscription_until >= date.today()

                if not is_subscribed:
                    return JsonResponse({'is_subscribed': 0})

                return JsonResponse({
                    'id': user.id,
                    'is_subscribed': 1,
                    'subscription_until': str(user.subscription_until)
                })

            except User.DoesNotExist:
                trial_date = date.today() + timedelta(days=7)
                new_user = User.objects.create(
                    id=phone_id,
                    subscription_until=trial_date
                )
                return JsonResponse({
                    'id': new_user.id,
                    'is_subscribed': 1,
                    'subscription_until': str(new_user.subscription_until)
                })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
