from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from wedding.utils import get_status_update_msg, notify_with_ntfy


@csrf_exempt
def ntfy_update_view(request):
    if request.method == "GET":
        try:
            ntfy_msg = get_status_update_msg()
            notify_with_ntfy(ntfy_msg)
            return JsonResponse({'status': 'ok'}, safe=False)
        except Exception:
            return JsonResponse({'status': 'error'}, safe=False)

