import sys
import inspect
import copy
from ..lib.customer import find_usecase
from django.apps import AppConfig

def get_default_configuration():
    return """
    This app requires low code configuration implemented using the app
    sdk or other means. Please get in touch with the platform manager.
    """

def get_default_resources():
    return """
    """

class EnrichAppConfig(AppConfig):

    name="default"
    category = "default"
    verbose_name = "default"
    description = "default"
    filename = None
    enable = False
    multiple = False
    composition = False
    status = "active"
    entry = "index"
    include_custom_urls = False
    tags = ["store"]
    _readme = ""
    _configuration = ""
    _resources = ""

    @property
    def readme(cls):
        if hasattr(cls, 'get_readme'):
            return cls.get_readme()
        elif cls._readme == "":
            return cls.description
        else:
            return cls._readme

    @property
    def configuration(cls):
        if hasattr(cls, 'get_configuration'):
            return cls.get_configuration()
        elif cls._configuration == "":
            return get_default_configuration()
        else:
            return cls._configuration

    @property
    def resources(cls):
        if hasattr(cls, 'get_resources'):
            return cls.get_resources()
        elif cls._resources == "":
            return get_default_resources()
        else:
            return cls._resources

    @property
    def instanceid(self):
        return str(id(self))

    def get_usecase(self):

        if self.filename is None:
            return {}

        usecase = find_usecase(self.filename)
        self.usecase = copy.deepcopy(usecase)
        return self.usecase

    def is_composition(self):
        return self.composition

    def get_name(self):
        return self.name

    def get_verbose_name(self):
        return self.verbose_name

    def get_description(self):
        return self.description

    def is_enabled(self):
        return self.enable

    def __str__(self):
        return f"{self.name}: {self.verbose_name}"


