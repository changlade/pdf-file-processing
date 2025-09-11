# -*- mode: python ; coding: utf-8 -*-

import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath('pdf_explorer_app.py'))

a = Analysis(
    ['pdf_explorer_windows_hybrid.py'],
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
        'platform',
        'ctypes',
        'ctypes.wintypes'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', '_tkinter', 'tkinter.ttk', 'tk'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF Document Explorer Hybrid',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console initially, then hide it programmatically
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# Create a COLLECT directory structure for Windows
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF Document Explorer Hybrid',
)
