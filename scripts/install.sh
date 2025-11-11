#!/bin/bash

# Build the internal Rust module
./scripts/build_internals.sh

# Create the installation directory
mkdir -p $HOME/.dbl

# Copy necessary files
cp dbl_internal.so $HOME/.dbl/dbl_internal.so
cp dbl.py $HOME/.dbl/dbl.py
cp conf.py $HOME/.dbl/conf.py

# Add .dbl to PYTHONPATH
PYTHONPATH_LINE="export PYTHONPATH=$PYTHONPATH:$HOME/.dbl"

# Add alias to dbl command
ALIAS_LINE="alias dbl=$HOME/.dbl/dbl.py\""

# Check if the alias already exists in .bashrc or .zshrc
if grep -Fxq "$ALIAS_LINE" $HOME/.bashrc || grep -Fxq "$ALIAS_LINE" $HOME/.zshrc; then
    echo "Alias already exists in .bashrc or .zshrc"
    exit 0
else
    echo "Adding PYTHONPATH to .bashrc and .zshrc"
    echo $PYTHONPATH_LINE >> $HOME/.bashrc
    echo $PYTHONPATH_LINE >> $HOME/.zshrc

    echo "Adding alias to .bashrc and .zshrc"   
    echo $ALIAS_LINE >> $HOME/.bashrc
    echo $ALIAS_LINE >> $HOME/.zshrc
fi

echo "✅ Installed dbl module to $HOME/.dbl/"
