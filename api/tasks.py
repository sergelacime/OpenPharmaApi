import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings

# Importez votre fonction fetch_pharmacies_data ici
from .views import fetch_pharmacies_data

def update_pharmacies_data():
    data = fetch_pharmacies_data()
    with open(os.path.join(settings.BASE_DIR, 'pharmacies.json'), 'w', encoding='utf-8') as f:
        f.write(data)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    # Planifiez la tâche pour s'exécuter tous les jours à minuit
    scheduler.add_job(
        update_pharmacies_data,
        trigger='cron',
        hour=16,
        minute=10,
        id='update_pharmacies_data',
        replace_existing=True,
    )

    scheduler.start()