# reference from https://stackoverflow.com/questions/44160666/valueerror-missing-staticfiles-manifest-entry-for-favicon-ico
from whitenoise.storage import CompressedManifestStaticFilesStorage

class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False