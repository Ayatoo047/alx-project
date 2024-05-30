from core.models import Client, Domain

from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Periodic Task Creation"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        print('Creating tenants....')
        
        tenant = Client(schema_name='public', name = 'Public')
        tenant.save()
        domain = Domain(domain='localhost', tenant=tenant ,is_primary=True)
        domain.save()
        
        
        pet_tenant = Client(schema_name='ajibade', name = 'ajibade')
        pet_tenant.save()
        new_domain = Domain(domain='ajibade.localhost', tenant=pet_tenant ,is_primary=True)
        new_domain.save()
        
        pet_tenant = Client(schema_name='another', name = 'another')
        pet_tenant.save()
        new_domain = Domain(domain='another.localhost', tenant=pet_tenant ,is_primary=True)
        new_domain.save()
        
        pet_tenant = Client(schema_name='alx', name = 'alx')
        pet_tenant.save()
        new_domain = Domain(domain='alx.localhost', tenant=pet_tenant ,is_primary=True)
        new_domain.save()
        print('DONE')
        # return super().handle(*args, **options)