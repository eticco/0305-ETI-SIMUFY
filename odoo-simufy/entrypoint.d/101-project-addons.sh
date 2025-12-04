#!/bin/bash
#author		     : Denis Suarez Perez
#version         : 0.1
#dependencies    : jq git
#debian_packages : jq git
#alpine_packages : jq git
#==============================================================================

function check_third_party_structure {
    thirdparty_file=$1
    thirdparty_folder=$2

    if [ ! -f "${thirdparty_file}" ]; then
        echo "El fichero [thirdparty.json] no existe"
    fi

    if [ ! -d "${thirdparty_folder}" ]; then
        sudo mkdir -p ${thirdparty_folder}
    fi
}

function f_repo_download {
    #git -c http.sslVerify=false clone $1 . 2> /dev/null
    git -c http.sslVerify=false clone $1 . 
    if [ $2 != "latest" ]; then
        git checkout $2 2> /dev/null
    fi
    touch .download 
}

function f_cp_module {
    repository=$1
    revision=$2
    module=$3
    destination=$4

    if [ ! -f ".download" ]; then
        f_repo_download $repository $revision
    fi

    echo "Modulo descargado: $module"
    sudo cp -r $module $destination
    if [ $revision != "latest" ]; then
        sudo su -c "echo $revision > ${destination}/${module}/.revision"
    fi
}

function check_base_config {
    third_party_path_file=$(realpath ${dtpapathfile:=${PWD}})

    # Comprobar si existe la carpeta y el fichero de third_party
    TPA_FILE="${third_party_path_file}/project-addons.json"
    TPA_FOLDER="${PWD}/unconfirmed_third_party_addons"

    check_third_party_structure $TPA_FILE $TPA_FOLDER

    # Borrar carpeta temporal si existe
    TMP_FOLDER=/tmp/unconfirmedthirdparty
    if [ -d "${TMP_FOLDER}" ]; then
        rm -rf ${TMP_FOLDER}
    fi
}

function f_thirdparty {
    check_base_config

    # Recorrer repositorios
    for repository in $(jq -r ' keys | .[]' $TPA_FILE); do

        # Recorremos revisiones
        for revision in $(jq --arg REPOSITORY "$repository" -r '.[$REPOSITORY] | keys | .[]' $thirdparty_file); do
            mkdir ${TMP_FOLDER} && cd ${TMP_FOLDER}

            # Recorremos módulos
            for module in $(jq --arg REPOSITORY "$repository" --arg REVISION "$revision" -r '.[$REPOSITORY] | .[$REVISION] | .[]' $thirdparty_file); do

                if [ ! -d "${TPA_FOLDER}/${module}" ]; then
                    f_cp_module $repository $revision $module $TPA_FOLDER
                elif [ ! -f "${TPA_FOLDER}/${module}/.revision" ]; then
                    sudo rm -r ${TPA_FOLDER}/$module
                    f_cp_module $repository $revision $module $TPA_FOLDER
                elif [ -f "${TPA_FOLDER}/${module}/.revision" ]; then
                    currentRevision=$(cat "${TPA_FOLDER}/${module}/.revision")
                    if [ "$revision" != "$currentRevision" ]; then
                        sudo rm -r ${TPA_FOLDER}/$module
                        f_cp_module $repository $revision $module $TPA_FOLDER
                    fi
                fi

            done

            cd - > /dev/null && rm -rf ${TMP_FOLDER}
        done

    done
}

f_thirdparty
