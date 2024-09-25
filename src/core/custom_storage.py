from whitenoise.storage import CompressedManifestStaticFilesStorage

class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def url(self, name, *args, **kwargs):
        if name.endswith('.map'):
            return None
        return super().url(name, *args, **kwargs)
