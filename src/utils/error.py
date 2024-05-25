class ModuleError(BaseException):
    pass


class ModuleLoadError(ModuleError):
    pass


class ModuleRuntimeError(ModuleError):
    pass


class ModuleCheckError(ModuleRuntimeError):
    def __init__(self, name: str, error: Exception):
        super().__init__(f"{name} checkout error - {error.args[0]}")
