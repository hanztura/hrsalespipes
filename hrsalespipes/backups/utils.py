import gzip

from django.conf import settings
from django.utils import timezone

from sh import pg_dump


def create_backup():
    """Create postgres db backup file and return file path.
    """
    try:
        storage_root = str(settings.BACKUPS_STORAGE_ROOT)
        datetime = timezone.localtime().strftime('%d%b%Y%H%M%S')
        filename = '{}/{}_{}'.format(storage_root, datetime, 'backup.gz')

        db = settings.DATABASES['default']
        host = db['HOST']
        name = db['NAME']
        user = db['USER']
        password = db['PASSWORD']

        with gzip.open(filename, 'wb') as f:
            pg_dump('-h', host, '-U', user, name, _out=f, _in=password)

        return filename
    except Exception as e:
        return None
