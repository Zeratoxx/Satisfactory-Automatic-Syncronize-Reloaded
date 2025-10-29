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
		  Tree('src\\components\\'),
		  Tree('src\\constants\\'),
		  Tree('src\\content\\'),
		  Tree('src\\pages\\'),
		  Tree('src\\res\\'),
		  Tree('src\\res\\images\\'),
		  Tree('src\\res\\fonts\\'),
		  Tree('src\\utils\\'),
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

package-windows-onefile:
	python -m PyInstaller --log-level=INFO "Satisfactory Automatic Synchronize Reloaded.spec" --noconfirm --onefile --noconsole

#generate-windows-spec:
#	python -m PyInstaller --log-level=INFO "Satisfactory Automatic Synchronize Reloaded.spec" --onefile --noconsole --name "Satisfactory Automatic Synchronize Reloaded" --noconfirm
