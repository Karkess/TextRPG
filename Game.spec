# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Game.py'],
    pathex=[],
    binaries=[],
    datas=[('Game.py', '.'), ('installer.py', '.'), ('Player.py', '.'), ('updater.py', '.'), ('utils.py', '.'), ('__init__.py', '.'), ('combat\\CombatLogic.py', '.'), ('combat\\CombatManager.py', '.'), ('combat\\CombatMenu.py', '.'), ('combat\\GearMenu.py', '.'), ('combat\\SpecialAttacks.py', '.'), ('combat\\Status_Effects.py', '.'), ('combat\\__init__.py', '.'), ('dungeons\\__init__.py', '.'), ('enemies\\AdvancedAI.py', '.'), ('enemies\\Enemies.py', '.'), ('enemies\\Enemy_Generator.py', '.'), ('enemies\\__init__.py', '.'), ('items\\__init__.py', '.'), ('npcs\\__init__.py', '.'), ('saves\\__init__.py', '.'), ('skills\\Fishing.py', '.'), ('skills\\Gathering.py', '.'), ('skills\\Hunting.py', '.'), ('skills\\LevelUpTableGenerator.py', '.'), ('skills\\Mining.py', '.'), ('skills\\__init__.py', '.'), ('towns\\__init__.py', '.'), ('combat/*', 'combat'), ('dungeons/*', 'dungeons'), ('enemies/*', 'enemies'), ('items/*', 'items'), ('npcs/*', 'npcs'), ('saves/*', 'saves'), ('skills/*', 'skills'), ('towns/*', 'towns')],
    hiddenimports=['platform', 'os', 'numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
