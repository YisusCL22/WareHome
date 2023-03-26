#!/bin/bash

echo "Clonar el repositorio" 
mkdir -p ~/Documents/git-lab && git clone --depth=1 https://github.com/YisusCL22/Especialidad-I.git ~/Documents/git-lab/Especialidad-I && cd ~/Documents/git-lab/Especialidad-I
echo "Proceso de creación del entorno virtual"
conda create -n Warehome python==3.7
conda activate Warehome
echo "Proceso de instalación de los requerimientos"
pip3 install -r requirements.txt
echo "Proceso Finalizado"

exit