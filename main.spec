# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['E:\\BackupControl\\main.py'],
             pathex=['E:\\BackupControl'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('main_icon.ico', 'E:\\BackupControl\\icons\\main_icon.ico', "DATA"), 
            ('catalog_icon.png', 'E:\\BackupControl\\icons\\catalog_icon.png', "DATA"), 
            ('check_icon.png', 'E:\\BackupControl\\icons\\check_icon.png', "DATA"), 
            ('logo.png', 'E:\\BackupControl\\icons\\logo.png', "DATA"), 
            ('quit_icon.png', 'E:\\BackupControl\\icons\\quit_icon.png', "DATA"), 
           ]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='BackupControl',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='E:\\BackupControl\\icons\\main_icon.ico')
