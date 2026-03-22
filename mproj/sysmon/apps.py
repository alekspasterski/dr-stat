from django.apps import AppConfig


class SysmonConfig(AppConfig):
    name = 'sysmon'
    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        try:
            task = PeriodicTask.objects.get(task="sysmon.tasks.check_memory_and_cpu")
        except PeriodicTask.DoesNotExist:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=10,
                period=IntervalSchedule.SECONDS,
            )

            PeriodicTask.objects.update_or_create(
                name='System polling',
                defaults={
                    'task':'sysmon.tasks.check_memory_and_cpu',
                    "interval":schedule,
                }
            )
