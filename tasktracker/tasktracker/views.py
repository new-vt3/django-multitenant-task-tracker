from django.http import HttpResponse
from django.core.management import call_command

def migrate_schemas_view(request):
    call_command('migrate_schemas', '--shared')
    return HttpResponse("Tenant shared migration completed.")
