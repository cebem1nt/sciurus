"""Service package"""

import os
from typing import TYPE_CHECKING

from lutris import settings

from lutris.services.xdg import XDGService
from lutris.services.dolphin import DolphinService
from lutris.services.flathub import FlathubService
from lutris.services.lutris import LutrisService
from lutris.services.scummvm import SCUMMVM_CONFIG_FILE, ScummvmService

from lutris.util import system
from lutris.util.dolphin.cache_reader import DOLPHIN_GAME_CACHE_FILE
from lutris.util.linux import LINUX_SYSTEM

if TYPE_CHECKING:
    from lutris.services.base import BaseService

DEFAULT_SERVICES = []

def get_services() -> dict[str, "type[BaseService]"]:
    """Return a mapping of available services"""

    services = {}

    if not LINUX_SYSTEM.is_flatpak():
        services["xdg"] = XDGService
    else:
        services["flathub"] = FlathubService

    if system.path_exists(DOLPHIN_GAME_CACHE_FILE):
        services["dolphin"] = DolphinService

    if system.path_exists(SCUMMVM_CONFIG_FILE):
        services["scummvm"] = ScummvmService

    if os.environ.get("LUTRIS_SERVICE_ENABLED") == "1":
        services["lutris"] = LutrisService
    
    return services

SERVICES = get_services()

def get_enabled_services():
    return {
        key: _class
        for key, _class in SERVICES.items()
        if settings.read_setting(key, section="services").lower() == "true"
    }
