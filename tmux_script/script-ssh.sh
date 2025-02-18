#!/bin/bash

# Comprueba que se haya proporcionado un archivo como parámetro
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <archivo-de-servidores>"
    exit 1
fi

# El archivo con la lista de servidores
SERVER_LIST=$1

# Comprueba que el archivo exista
if [ ! -f "$SERVER_LIST" ]; then
    echo "El archivo $SERVER_LIST no existe."
    exit 1
fi

# Lee cada línea del archivo y crea un nuevo panel en tmux para cada servidor
while IFS= read -r server
do
    # Crear un nuevo panel en tmux y conectarse al servidor mediante SSH
    # Si es el primer servidor, crea una ventana nueva. De lo contrario, crea un panel nuevo.
    if [ -z "$first_server" ]; then
        tmux new-window -n "$server" "ssh $server"
        first_server=false
    else
        tmux split-window -h "ssh $server"
        tmux select-layout tiled
    fi
done < "$SERVER_LIST"

# Reorganizar los paneles para que tengan el mismo tamaño
tmux select-layout tiled

# Vuelve a conectar el stdin a la terminal si se está ejecutando el script fuera de tmux
[ -z "$TMUX" ] && tmux attach

exit 0
