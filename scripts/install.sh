#!/bin/bash

# Build the internal Rust module
./scripts/build_internals.sh

# Create the installation directory
mkdir -p $HOME/.dbl

# Copy necessary files
cp rust_internal.so $HOME/.dbl/rust_internal.so
cp dbl.py $HOME/.dbl/dbl.py
cp conf.py $HOME/.dbl/conf.py

# Add alias to dbl command
ALIAS_LINE="alias dbl=\"PYTHONPATH=$PYTHONPATH:$HOME/.dbl python3 $HOME/.dbl/dbl.py\""

# Check if the alias already exists in .bashrc or .zshrc
if grep -Fxq "$ALIAS_LINE" $HOME/.bashrc || grep -Fxq "$ALIAS_LINE" $HOME/.zshrc; then
    echo "Alias already exists in .bashrc or .zshrc"
    exit 0
else
    echo "Adding alias to .bashrc and .zshrc"   
    echo $ALIAS_LINE >> $HOME/.bashrc
    echo $ALIAS_LINE >> $HOME/.zshrc
fi

echo "✅ Installed dbl module to $HOME/.dbl/"
