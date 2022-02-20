# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)


block_cipher = None


a = Analysis(['main.py','AutoElec.py','constant.py','gui.py','thread_control.py','torch_method.py'],
             pathex=['D:\\Code\\python\\AutoElective3.0'],
             binaries=[],
             datas=[('captcha','captcha'),('qt','qt'),('show','show'),('webdriver','webdriver'),('info.txt','info.txt')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
