from django.db import migrations

def create_periodic_task(apps, schema_editor):
    IntervalSchedule = apps.get_model('django_celery_beat', 'IntervalSchedule')
    PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')

    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period='hours',
    )

    # Delete old task if exists (optional)
    PeriodicTask.objects.filter(name='Fetch and Save Funds').delete()

    PeriodicTask.objects.create(
        interval=schedule,
        name='Fetch and Save Funds',
        task='funds.tasks.fetch_and_save_funds',  
    )

class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0003_remove_fundfamily_updated_at1_and_more'),
    ]

    operations = [
        migrations.RunPython(create_periodic_task),  
    ]
