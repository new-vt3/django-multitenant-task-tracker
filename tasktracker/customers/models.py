from django.db import models 
import datetime
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(default=datetime.date.today)  # or other suitable date
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    
    auto_create_schema = True
    auto_drop_schema = True

class Domain(DomainMixin):
    pass