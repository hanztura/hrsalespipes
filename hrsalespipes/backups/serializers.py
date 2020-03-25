from django.core.files.storage import FileSystemStorage

from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter


class FileSystemStorageSerializer(BaseSerializer):
    def serialize(self):
        return self.value.location, {
            'from django.core.files.storage import FileSystemStorage'
        }


MigrationWriter.register_serializer(
    FileSystemStorage, FileSystemStorageSerializer)
