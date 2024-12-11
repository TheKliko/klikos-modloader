class ModUpdaterError(Exception):
    pass


class DeployHistoryError(ModUpdaterError):
    pass


class ImageSetsNotFoundError(ModUpdaterError):
    pass


class ImageSetDataNotFoundError(ModUpdaterError):
    pass