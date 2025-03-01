import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from datetime import date, timedelta

@csrf_exempt  # Esto desactiva la verificación CSRF para esta vista
def check_subscription(request):
    if request.method == "POST":
        try:
            # Obtener el cuerpo de la solicitud y cargar el JSON
            data = json.loads(request.body)
            phone_id = data.get('phone')  # Obtener el número de teléfono (ID)

            if phone_id is None:
                return JsonResponse({'error': 'Phone ID is missing'}, status=400)

            # Intentar obtener el usuario de la base de datos
            try:
                user = User.objects.get(id=phone_id)
                # Si existe, comprobar si la suscripción es válida
                is_subscribed = user.subscription_until >= date.today()

                if not is_subscribed:
                    return JsonResponse({'is_subscribed': 0})

                # Si está suscrito, retornar la respuesta con los resultados
                return JsonResponse({
                    'id': user.id,  # Incluir el ID del usuario en la respuesta
                    'is_subscribed': 1,
                    'subscription_until': user.subscription_until
                })

            except User.DoesNotExist:
                # Si no existe el usuario, se crea uno nuevo con 7 días de prueba
                trial_date = date.today() + timedelta(days=7)
                new_user = User.objects.create(
                    id=phone_id,
                    subscription_until=trial_date
                )
                return JsonResponse({
                    'id': new_user.id,
                    'is_subscribed': 1,
                    'subscription_until': new_user.subscription_until
                })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
