#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Tools"))

from dependency_updater import Step, Updater

URL = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/{version}.tar.gz"


def update_source(updater):
    updater.replace_source()
    updater.update_config()


def create_headers(updater):
    updater.cmake("-DENABLE_SHARED=false")
    updater.copy_from_build("", ["jconfig.h", "jconfigint.h", "jversion.h"], "src")
    updater.remove_build()


def apply_patches(updater):
    updater.apply_patches()


updater = Updater(__file__, "libjpeg-turbo", URL)
updater.run([
    Step("Replace the source with the release and update Config.txt", update_source,
        "Updated libjpeg-turbo to {version}"),
    Step("Create header files with cmake", create_headers,
        "Created header files with cmake."),
    Step("Apply the patches", apply_patches,
        "Fixed exports, enabled SIMD and added a patch for the 32-bit build."),
    updater.clone_dependencies_step(),
])
