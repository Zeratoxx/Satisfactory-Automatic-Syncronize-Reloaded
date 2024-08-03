define string1
 - add above line 1:

      from kivy_deps import sdl2, glew

endef
export string1
define string2
 - starting from line 20:

      exe = EXE(
          pyz,
          Tree('src\\'),
          Tree('src\\libs\\content\\'),
          Tree('src\\res\\'),
          Tree('src\\res\\images\\'),
          Tree('src\\res\\fonts\\'),
          a.scripts,
          a.binaries,
          a.datas,
          [],
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          ...
      )

endef
export string2

package-windows:
	python -m PyInstaller --log-level=INFO "Satisfactory Automatic Synchronize Reloaded.spec" --noconfirm

generate-windows-spec:
	python -m PyInstaller --log-level=INFO --onefile --noconsole --hidden-import=win32file --add-data src/libs:libs --name "Satisfactory Automatic Synchronize Reloaded" --icon src/res/icon.ico src/main.py
	@echo " "
	@echo "To be edited in created .spec file:"
	@echo "$$string1"
	@echo "$$string2"
