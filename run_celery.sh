celery -A celeryworker worker -l info --uid=root --gid=root
celery -A celeryworker flower -l info --uid=root --gid=root
celery -A celeryworker beat -l info --uid=root --gid=root