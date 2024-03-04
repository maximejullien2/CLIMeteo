#!/bin/bash
typeOrdinateur=$(uname -s)
echo $typeOrdinateur
if [ "$typeOrdinateur" = "Linux" ] || [ "$typeOrdinateur" = "MINGW64_NT" ] || [ "$typeOrdinateur" = "MINGW32_NT" ]
then 
    sudo apt-get update
    sudo apt-get intall python3
    $(python3 -m pip install -r requirement.txt)
elif [ "$typeOrdinateur" = "Darwin" ] 
then 
    brew update
    brew install python3
    python3 -m pip install -r requirement.txt

else 
    echo "Impossible d'installer "
fi 