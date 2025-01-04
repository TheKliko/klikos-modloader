class ModGeneratorError(Exception):
    pass


class DeployHistoryError(ModGeneratorError):
    pass


class ImageSetsNotFoundError(ModGeneratorError):
    pass


class ImageSetDataNotFoundError(ModGeneratorError):
    pass