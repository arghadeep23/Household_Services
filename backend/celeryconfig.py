from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],  # Updated key
        broker=app.config['broker_url']        # Updated key
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery