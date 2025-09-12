# -*- mode: python ; coding: utf-8 -*-

import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath('pdf_explorer_mac_v2.py'))

a = Analysis(
    ['../pdf_explorer_mac_v2.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[
        ('../web', 'web'),
        ('../data', 'data'),
    ],
    hiddenimports=[
        'http.server',
        'webbrowser',
        'threading',
        'socket',
        'signal',
        'platform',
        'subprocess',
        'json',
        'requests',
        'flask',
        'flask_cors',
        'werkzeug',
        'jinja2',
        'markupsafe',
        'itsdangerous',
        'click',
        'blinker',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', '_tkinter', 'tkinter.ttk', 'tk',
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'matplotlib', 'numpy', 'scipy',
        'pandas', 'sklearn'
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
    target_arch='x86_64',  # Specifically target Intel x86_64 architecture
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
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
app = BUNDLE(
    coll,
    name='PDF Document Explorer Intel.app',
    icon=None,
    bundle_identifier='com.pdfexplorer.semanticsearch.intel',
    info_plist={
        'CFBundleDisplayName': 'PDF Document Explorer (Intel)',
        'CFBundleShortVersionString': '2.0.0',
        'CFBundleVersion': '2.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.15.0',  # macOS Catalina minimum for Python 3.8+
        'LSArchitecturePriority': ['x86_64'],  # Intel only
        'LSRequiresNativeExecution': False,  # Allow Rosetta translation if needed
        'CFBundleIdentifier': 'com.pdfexplorer.semanticsearch.intel',
        'CFBundleName': 'PDF Document Explorer (Intel)',
        'CFBundleExecutable': 'PDF Document Explorer',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'PDFI',
        'NSAppTransportSecurity': {
            'NSAllowsArbitraryLoads': True,  # Allow HTTP connections for local servers
            'NSExceptionDomains': {
                'localhost': {
                    'NSExceptionAllowsInsecureHTTPLoads': True,
                    'NSExceptionMinimumTLSVersion': '1.0'
                },
                '127.0.0.1': {
                    'NSExceptionAllowsInsecureHTTPLoads': True,
                    'NSExceptionMinimumTLSVersion': '1.0'
                },
                'dbc-0619d7f5-0bda.cloud.databricks.com': {
                    'NSExceptionRequiresForwardSecrecy': False,
                    'NSExceptionMinimumTLSVersion': '1.2',
                    'NSIncludesSubdomains': True
                }
            }
        },
        'NSAppleEventsUsageDescription': 'This app needs to open web browsers.',
        'NSNetworkVolumesUsageDescription': 'This app needs network access for semantic search.',
        'LSApplicationCategoryType': 'public.app-category.productivity',
        'LSUIElement': False,  # Show in Dock
        'NSSupportsAutomaticTermination': True,
        'NSSupportsSuddenTermination': True,
        # Intel-specific info
        'LSRequiresIPhoneOS': False,
        'LSMultipleInstancesProhibited': False,
        # Python and architecture info
        'CFBundleSupportedPlatforms': ['MacOSX'],
        'DTCompiler': 'com.apple.compilers.llvm.clang.1_0',
        'DTPlatformName': 'macosx',
        'LSMinimumSystemVersionByArchitecture': {
            'x86_64': '10.15.0'  # Intel minimum
        }
    }
)
