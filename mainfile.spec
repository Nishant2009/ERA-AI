# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/nisha/Downloads/NISHANT/AI_BOT/ERA_AI/mainfile.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/nisha/Downloads/NISHANT/AI_BOT/ERA_AI/screen.py', '.'), ('C:/Users/nisha/Downloads/NISHANT/AI_BOT/ERA_AI/waves.gif', '.'), ('C:/Users/nisha/Downloads/NISHANT/AI_BOT/ERA_AI/background.jpg', '.'), ('C:/Users/nisha/Downloads/NISHANT/AI_BOT/ERA_AI/circle.gif', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='mainfile',
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
)
