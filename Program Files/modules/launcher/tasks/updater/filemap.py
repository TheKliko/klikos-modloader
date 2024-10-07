import os
import logging


# A comination of the following Bloxstrap/AppData files
# - CommonAppData.cs
# - RobloxPlayerData.cs
# - RobloxStudioData.cs

class FileMap:
    COMMON: dict[str, str] = {
        'Libraries.zip': None,
        'shaders.zip': 'shaders',
        'ssl.zip': 'ssl',
        'WebView2.zip': None,
        'WebView2RuntimeInstaller.zip': 'WebView2RuntimeInstaller',

        'content-avatar.zip': os.path.join('content', 'avatar'),
        "content-configs.zip": os.path.join('content', 'configs'),
        "content-fonts.zip": os.path.join('content', 'fonts'),
        "content-sky.zip": os.path.join('content', 'sky'),
        "content-sounds.zip": os.path.join('content', 'sounds'),
        "content-textures2.zip": os.path.join('content', 'textures'),
        "content-models.zip": os.path.join('content', 'models'),

        "content-textures3.zip": os.path.join('PlatformContent', 'pc', 'textures'),
        "content-terrain.zip": os.path.join('PlatformContent', 'pc', 'terrain'),
        "content-platform-fonts.zip": os.path.join('PlatformContent', 'pc', 'fonts'),

        "extracontent-luapackages.zip": os.path.join('ExtraContent', 'LuaPackages'),
        "extracontent-translations.zip": os.path.join('ExtraContent', 'translations'),
        "extracontent-models.zip": os.path.join('ExtraContent', 'models'),
        "extracontent-textures.zip": os.path.join('ExtraContent', 'textures'),
        "extracontent-places.zip": os.path.join('ExtraContent', 'places')
    }

    ROBLOX_PLAYER: dict[str, str] = {
        'RobloxApp.zip': None
    }

    ROBLOX_STUDIO: dict[str, str] = {
        'RobloxStudio.zip': None,
        'redist.zip': None,
        'LibrariesQt5.zip': None,

        'content-studio_svg_textures.zip': os.path.join('content', 'studio_svg_textures'),
        'content-qt_translations.zip': os.path.join('content', 'qt_translations'),
        'content-api-docs.zip': os.path.join('content', 'api_docs'),

        'extracontent-scripts.zip': os.path.join('ExtraContent', 'scripts'),

        'BuiltInPlugins.zip': 'BuiltInPlugins',
        'BuiltInStandalonePlugins.zip': 'BuiltInStandalonePlugins',

        'ApplicationConfig.zip': 'ApplicationConfig',
        'Plugins.zip': 'Plugins',
        'Qml.zip': 'Qml',
        'StudioFonts.zip': 'StudioFonts'
    }

    @classmethod
    def get_path(cls, file: str) -> str|None:
        if file in cls.COMMON:
            return cls.COMMON[file]
        elif file in cls.ROBLOX_PLAYER:
            return cls.ROBLOX_PLAYER[file]
        elif file in cls.ROBLOX_STUDIO:
            return cls.ROBLOX_STUDIO[file]
        
        logging.warning("File \""+str(file)+"\" not in FileMap!")
        return None