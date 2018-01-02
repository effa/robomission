from setuptools import setup
from setuptools.command.develop import develop as _develop
from notebook.nbextensions import install_nbextension
from notebook.services.config import ConfigManager
import os

extension_dir = os.path.join(os.path.dirname(__file__), "visualization", "static")

class develop(_develop):
    def run(self):
        _develop.run(self)
        install_nbextension(
            extension_dir,
            symlink=True,
            overwrite=True,
            user=False,
            sys_prefix=True,  # to install it inside virtualenv
            destination="visualization")
        cm = ConfigManager()
        cm.update('notebook', {"load_extensions": {"visualization/index": True } })

setup(
    name='visualization',
    cmdclass={'develop': develop},
    version='0.0.1',
    description='Visualization components for RoboMission',
    url='https://github.com/adaptive-learning/robomission',
    author='Tomas Effenberger',
    author_email='xeffenberger@gmail.com',
    license='MIT',
    packages=['visualization'],
    zip_safe=False,
    data_files=[
        ('share/jupyter/nbextensions/visualization', ['visualization/static/index.js']),
        ('share/jupyter/nbextensions/visualization/media', ['visualization/static/media/*'])
    ],
    install_requires=[
        "ipython",
        "jupyter-react"
    ])
