from kivy_deps import sdl2, glew
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('src/components', 'components'),
    ('src/constants', 'constants'),
    ('src/content', 'content'),
    ('src/logic', 'logic'),
    ('src/pages', 'pages'),
    ('src/res', 'res'),
    ('src/utils', 'utils'),
    ],
    hiddenimports=['win32timezone', 'win32file'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    Tree('src\\'),
    Tree('src\\components\\'),
    Tree('src\\constants\\'),
    Tree('src\\content\\'),
    Tree('src\\pages\\'),
    Tree('src\\res\\'),
    Tree('src\\res\\images\\'),
    Tree('src\\res\\fonts\\'),
    Tree('src\\utils\\'),
    a.scripts,
    a.binaries,
    a.datas,
    [],
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='SatisfactoryAutomaticynchronizeReloaded',
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
    icon=['src\\res\\icon.ico'],
)
