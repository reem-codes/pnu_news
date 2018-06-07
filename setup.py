from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], include_files = ["layout.py", "image"]

)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

bdist_msi_options = {
    'initial_target_dir': r'[PictureFolder]\pnu_news',
    }
executables = [
    Executable('pnu_news.py', 
		base=base,
		shortcutName="pnu_news",
		shortcutDir="DesktopFolder"
		)
]

setup(name='pnu_news',
      version = '1.0',
      description = 'an image processing app to make pnu ads',
      options = dict(build_exe = buildOptions),
      executables = executables)
