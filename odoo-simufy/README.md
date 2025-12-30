Para poder actualizar los cambios en Integración:

Descargar el repositorio y cambiar a la rama de integración:
```
git clone git@github.com:adminsimufy/simufy.git
git switch staging
```

Actualizar el repo:
```
rm -rf eticco/0305-ETI-SIMUFY
rm -rf .git/modules/eticco/0305-ETI-SIMUFY
git submodule update --remote eticco
git add eticco
git commit -m "Actualizar submódulo eticco"
git push origin staging
```