Write-Host "Building .ui classes"
pyside6-uic ui\mainwindow.ui -o src\ui\mainwindow.py
Write-Host "Done!"