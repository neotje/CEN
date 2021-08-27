from setuptools import setup, find_packages

PROJECT_NAME = "CEN-UIU"
PROJECT_PACKAGE_NAME = "cen_uiu"

PROJECT_GITHUB_USERNAME = "neotje"

PACKAGES = find_packages()

REQUIRED = [
    #"kivy[full]>=2.0.0",
    #"pyqt5>=5.15",
    #"pyqtwebengine>=5.15",
    "pywebview[gtk]>=3.4"
    "pyserial>=3.5",
    "dbus-python>=1.2.16",
    "screeninfo>=0.6.7",
    "websockets>=9.1"
]

setup(
    name=PROJECT_PACKAGE_NAME,
    packages=PACKAGES,
    install_requires=REQUIRED,
    entry_points={"console_scripts": [
        "cen-uiu = cen_uiu.__main__:main"]}
)
