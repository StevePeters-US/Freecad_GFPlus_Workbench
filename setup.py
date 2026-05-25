from setuptools import setup
import os

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "freecad", "gridfinity_plus_workbench", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.gridfinity_plus_workbench',
      version=str(__version__),
      packages=['freecad',
                'freecad.gridfinity_plus_workbench'],
      maintainer="me",
      maintainer_email="me@foobar.com",
      url="https://foobar.com/me/coolWB",
      description="GridifintyPlusWorkbench does something cool.",
      install_requires=['numpy',],
      include_package_data=True)
