typeset -U fpath
fpath+=/usr/share/zsh/site-functions

if [[ -n $SSH_CONNECTION ]]; then
    export EDITOR=vim
else
    export EDITOR=nvim
fi

export RUSTUP_DIST_SERVER=https://rsproxy.cn
export RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup

export GOPATH="$HOME/go"
export PNPM_HOME="$HOME/.local/share/pnpm"

typeset -U path

path=(
    "$PNPM_HOME/bin"
    "$GOPATH/bin"
    "$HOME/.local/bin"
    $path
)

