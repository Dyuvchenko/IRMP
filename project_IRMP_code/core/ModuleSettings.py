class ModuleSettings:
    name = ""
    path = ""
    is_disabled = False
    module_is_supported = True
    error_init_module = False
    url_path = None

    def __init__(self, name, is_disabled, module_is_supported):
        self.name = name
        self.is_disabled = is_disabled
        self.module_is_supported = module_is_supported
