import importlib
import os
from loguru import logger
from fastapi_hive.ioc_framework.cornerstone_model import Cornerstone, CornerstoneMeta


class CornerstoneContainer:
    def __init__(self):
        self._modules = {}
        self._module_package_paths = set([])

    @property
    def modules(self):
        return self._modules

    def register_module_package_paths(self, module_package_paths):
        module_package_paths = set(module_package_paths)
        current_package_paths = self._module_package_paths

        self._module_package_paths = current_package_paths | module_package_paths

        logger.info(
            f"after registering, module package paths = {self._module_package_paths}")

    def unregister_module_package_paths(self, module_package_paths):
        module_package_paths = set(module_package_paths)
        current_package_paths = self._module_package_paths

        self._module_package_paths = current_package_paths - module_package_paths

        logger.info(
            f"after unregistering, module package paths = {self._module_package_paths}")

    def resolve_modules(self):
        module_package_paths = self._module_package_paths
        logger.info(f"module package paths = {module_package_paths}")

        for one_package_path in module_package_paths:
            module_paths = self._get_module_paths(one_package_path)
            package_name = os.path.basename(one_package_path)

            for one_module in module_paths:
                one_module_path = module_paths[one_module]

                one_module_entity = importlib.import_module(one_module_path)

                module_instance = CornerstoneMeta()
                module_instance.name = one_module
                module_instance.package = package_name
                module_instance.imported_module = one_module_entity

                self._modules[one_module] = module_instance

    def get_module(self, module_name: str):
        module_name = module_name.upper()

        for one_name, one_module_instance in self._modules.items():
            one_name = one_name.upper()
            if module_name == one_name:
                return one_module_instance

    def _get_module_paths(self, package_path):
        module_names = self._get_module_names(package_path)

        module_paths = {}

        for one_name in module_names:
            module_path = os.path.join(package_path, one_name)

            module_path = module_path.replace("./", "")
            module_path = module_path.replace(os.path.sep, ".")

            logger.info(f"module path = {module_path}")

            module_paths[one_name] = module_path

        return module_paths

    def _get_module_names(self, package_path):
        folder_names = os.listdir(package_path)

        module_names = []

        for file in folder_names:
            if file == '__pycache__':
                continue

            file_path = os.path.join(package_path, file)

            if os.path.isdir(file_path):
                print("====================")
                print(file)
                module_names.append(file)

        return module_names
