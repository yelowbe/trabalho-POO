from setuptools import setup, Extension
import pybind11

setup(
    name="permissions_list",
    version="1.0",
    description="Retorna a lista de permissões",
    ext_modules=[
        Extension(
            "permissions_list",
            ["permissions_list.cpp"],
            include_dirs=[pybind11.get_include()],
            language="c++",
        )
    ],
)
