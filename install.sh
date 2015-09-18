#!/usr/bin/env bash
function link_file {
    source="${PWD}/$1"
    target="${HOME}/${1/_/.}"
    echo "source" $source
    echo "target" $target
    if [ -e "${target}" ] && [ ! -L "${target}" ]; then
        echo "mv $target $target.df.bak"
        mv $target $target.df.bak
    fi

    echo "ln -sf ${source} ${target}"
    ln -sf ${source} ${target}
}

function unlink_file {
    source="${PWD}/$1"
    target="${HOME}/${1/_/.}"

    if [ -e "${target}.df.bak" ] && [ -L "${target}" ]; then
        unlink ${target}
        mv $target.df.bak $target
    fi
}

if [ "$1" = "restore" ]; then
    for i in _*
    do
        unlink_file $i
    done
    exit
elif [ "$1" == "update" ]; then
    git submodule update --init --recursive
    git submodule foreach --recursive git pull origin master    
elif [ -e "$1" ]; then
    echo "installing $1 ..."
    for i in ${1}*
    do
        link_file $i
    done
else
    echo "hu?", $1
fi

