# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GraphicsEngine\\ui_library.py', 'Engine\\Engine.py'],
    pathex=["./GraphicsEngine", "./Engine", "./Engine/Resources"],
    binaries=[],
    datas=[],
    hiddenimports=["Engine.py"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["IOHook.py", "editor_settings.json"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Insert Dungeon Name Here VS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['ui_resources\\dungeon_builder_iconx512.png'],
)
