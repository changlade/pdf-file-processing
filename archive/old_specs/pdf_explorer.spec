# -*- mode: python ; coding: utf-8 -*-

import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath('pdf_explorer_app.py'))

a = Analysis(
    ['pdf_explorer_mac.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[
        ('web', 'web'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'BaseHTTPServer',  # Python 2 compatibility
        'http.server',     # Python 3 compatibility
        'webbrowser',
        'threading',
        'socket',
        'signal',
        'platform',
        'subprocess'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', '_tkinter', 'tkinter.ttk', 'tk',
        'concurrent.futures',  # Not available in old Python
        'asyncio',  # Not available in old Python
        'multiprocessing',  # Can cause issues on old systems
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
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
    codesign_identity=None,  # Will be set via environment variable if available
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF Document Explorer',
)

# For macOS, create an app bundle
if os.name == 'posix':
    app = BUNDLE(
        coll,
        name='PDF Document Explorer.app',
        icon=None,  # Add icon file path here if you have one
        bundle_identifier='com.pdfexplorer.app',
        info_plist={
            'CFBundleDisplayName': 'PDF Document Explorer',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.9.0',  # Support macOS 10.9 (Mavericks)
            'LSArchitecturePriority': ['x86_64', 'arm64'],  # Intel first, then Apple Silicon
            'LSRequiresNativeExecution': False,  # Allow Rosetta if needed
            'CFBundleIdentifier': 'com.pdfexplorer.app',
            'CFBundleName': 'PDF Document Explorer',
            'CFBundleExecutable': 'PDF Document Explorer',
            'CFBundlePackageType': 'APPL',
            'CFBundleSignature': 'PDFE',
            'NSAppTransportSecurity': {
                'NSAllowsArbitraryLoads': True,  # Allow HTTP connections
                'NSExceptionDomains': {
                    'localhost': {
                        'NSExceptionAllowsInsecureHTTPLoads': True,
                        'NSExceptionMinimumTLSVersion': '1.0'
                    }
                }
            },
            'NSAppleEventsUsageDescription': 'This app needs to open web browsers.',
            'LSApplicationCategoryType': 'public.app-category.productivity'
        }
    )
