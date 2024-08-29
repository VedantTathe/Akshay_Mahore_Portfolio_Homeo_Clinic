from django.utils.deprecation import MiddlewareMixin
from .models import Visit  # Adjust the import according to your project structure

class VisitCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/':  # Check if the request is for the index page
            try:
                # Fetch or create the Visit record
                visit, created = Visit.objects.get_or_create(id=1)  # Assuming there's only one Visit record
                visit.count += 1
                visit.save()
            except Exception as e:
                print(f"An error occurred: {e}")
