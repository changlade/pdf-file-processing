# -*- mode: python ; coding: utf-8 -*-

import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath('pdf_explorer_app.py'))

a = Analysis(
    ['pdf_explorer_windows.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[
        ('web', 'web'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'http.server',
        'webbrowser',
        'threading',
        'socket',
        'signal',
        'platform'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', '_tkinter', 'tkinter.ttk'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PDF Document Explorer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window for end users
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
