#!/usr/bin/env python3

from setuptools import setup, find_packages, os
import sys, shutil


with open(os.path.dirname(os.path.realpath(__file__)) + "/src/__version__") as reader:
    version = reader.read().strip()


def files_in_folder(folder):
    file_paths = []
    for file in [filename for filename in os.listdir(folder)]:
        file_paths.append(folder + file)
    return file_paths


# Python package
if "egg_info" in sys.argv or "sdist" in sys.argv or "bdist_wheel" in sys.argv:
    for argv in sys.argv:
        if "/in_process/_in_process.py" in argv:
            package_type_var = "python_package"

# Debian, RPM, Arch Linux another other package
else:
    package_type_var = "debian_rpm_archlinux_or_another_package"


print("\n" + "_____package_type: " + package_type_var + "_____" + "\n")



if package_type_var == "debian_rpm_archlinux_or_another_package":

    install_requires=["PyGObject"]
    entry_points={}

    os.chmod("integration/io.github.hakandundar34coding.system-monitoring-center.desktop", 0o644)
    os.chmod("locale/de/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/cs/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/fa/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/hu/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/pl/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/pt_BR/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/pt_PT/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/ru_RU/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/tr/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    for file in files_in_folder("database/"):
        os.chmod(file, 0o644)
    for file in files_in_folder("src/"):
        os.chmod(file, 0o644)
    for file in files_in_folder("ui/"):
        os.chmod(file, 0o644)
    for file in files_in_folder("icons/hicolor/scalable/actions/"):
        os.chmod(file, 0o644)
    os.chmod("icons/hicolor/scalable/apps/system-monitoring-center.svg", 0o644)

    data_files = [
        ("/usr/share/applications/", ["integration/io.github.hakandundar34coding.system-monitoring-center.desktop"]),
        ("/usr/share/polkit-1/actions/", ["integration/io.github.hakandundar34coding.system-monitoring-center.policy"]),
        ("/usr/share/system-monitoring-center/locale/de/LC_MESSAGES/", ["locale/de/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/cs/LC_MESSAGES/", ["locale/cs/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/fa/LC_MESSAGES/", ["locale/fa/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/hu/LC_MESSAGES/", ["locale/hu/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/pl/LC_MESSAGES/", ["locale/pl/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/pt_BR/LC_MESSAGES/", ["locale/pt_BR/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/pt_PT/LC_MESSAGES/", ["locale/pt_PT/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/ru_RU/LC_MESSAGES/", ["locale/ru_RU/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/tr/LC_MESSAGES/", ["locale/tr/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/database/", files_in_folder("database/")),
        ("/usr/share/system-monitoring-center/src/", files_in_folder("src/")),
        ("/usr/share/system-monitoring-center/ui/", files_in_folder("ui/")),
        ("/usr/share/icons/hicolor/scalable/actions/", files_in_folder("icons/hicolor/scalable/actions/")),
        ("/usr/share/icons/hicolor/scalable/apps/", ["icons/hicolor/scalable/apps/system-monitoring-center.svg"]),
        ("/usr/share/man/man1/", ["man/system-monitoring-center.1.gz"]),
        ("/usr/bin/", ["integration/system-monitoring-center"])
    ]


if package_type_var == "python_package":

    install_requires=["PyGObject", "pycairo"]
    entry_points={"gui_scripts": ["system-monitoring-center = systemmonitoringcenter.start:start_app"]}

    data_files = [
        ("/systemmonitoringcenter/integration/", ["integration/io.github.hakandundar34coding.system-monitoring-center.desktop"]),
        ("/systemmonitoringcenter/locale/de/LC_MESSAGES/", ["locale/de/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/cs/LC_MESSAGES/", ["locale/cs/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/fa/LC_MESSAGES/", ["locale/fa/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/hu/LC_MESSAGES/", ["locale/hu/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/pl/LC_MESSAGES/", ["locale/pl/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/pt_BR/LC_MESSAGES/", ["locale/pt_BR/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/pt_PT/LC_MESSAGES/", ["locale/pt_PT/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/ru_RU/LC_MESSAGES/", ["locale/ru_RU/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/tr/LC_MESSAGES/", ["locale/tr/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/database/", files_in_folder("database/")),
        ("/systemmonitoringcenter/src/", files_in_folder("src/")),
        ("/systemmonitoringcenter/ui/", files_in_folder("ui/")),
        ("/systemmonitoringcenter/icons/hicolor/scalable/actions/", files_in_folder("icons/hicolor/scalable/actions/")),
        ("/systemmonitoringcenter/icons/hicolor/scalable/apps/", ["icons/hicolor/scalable/apps/system-monitoring-center.svg"]),
    ]


setup(
    name="system-monitoring-center",
    version=version,
    description="Multi-featured system monitor.",
    long_description="Provides information about CPU/RAM/Disk/Network/GPU performance, sensors, processes, users, services and system.",
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    url="https://github.com/hakandundar34coding/system-monitoring-center",
    keywords="system monitor task manager performance cpu ram swap memory disk network gpu processes users services",
    license="GPLv3",
    install_requires=install_requires,
    python_requires=">=3.6",
    packages=find_packages(),
    data_files=data_files,
    entry_points=entry_points,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Monitoring",
    ],
)
