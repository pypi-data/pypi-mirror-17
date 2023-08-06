from PyInstaller.utils.hooks import collect_data_files

# Collecting additional files:
# HACK: collect that nose/usage.txt file
nosefiles = collect_data_files('nose')
# HACK: add gravely.tests as plain files, not compiled module
tests = [('gravely', 'gravely')]
datas = nosefiles + tests

hiddenimports=[
	'unittest.mock',
	'h5py._proxy', 'h5py.utils', 'h5py.h5ac', 'h5py.defs'
]
excludes = [
	'tkinter',
	'PyQt4',
	'PyQt5',
	'gi.repository',
	'h5py.ipy_completer',
	'IPython',
	'matplotlib.backends'
	'matplotlib.backends.qt_compat'
	'matplotlib.backends.gtk3'
	'matplotlib.backends.tkagg'
	'matplotlib.backends.backend_qt_compat'
	'matplotlib.backends.backend_gtk3'
	'matplotlib.backends.backend_tkagg'
]

a = Analysis(['__main__.py'], datas=datas, hiddenimports=hiddenimports, excludes=excludes)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, name='gravely')
