from setuptools import setup, find_packages

PROJECT_NAME = "CEN-UIU"
PROJECT_PACKAGE_NAME = "cen_uiu"

PROJECT_GITHUB_USERNAME = "neotje"

PACKAGES = find_packages()

REQUIRED = [
    "pywebview[gtk]>=3.4"
    "pyserial>=3.5",
    "dbus-python>=1.2.16",
    "screeninfo>=0.6.7",
    "websockets>=10.1",
    "aiohttp>=3.8.1",
    "pyserial-asyncio>=0.6"
]

setup(
    name=PROJECT_PACKAGE_NAME,
    packages=PACKAGES,
    install_requires=REQUIRED,
    entry_points={"console_scripts": [
        "uiu-backend = cen_uiu.__main__:backend",
        "uiu-frontend = cen_uiu.__main__:frontend"
    ]
    }
)
