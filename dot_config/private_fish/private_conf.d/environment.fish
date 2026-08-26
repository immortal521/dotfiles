# XDG Base Directory
set -q XDG_CONFIG_HOME; or set -gx XDG_CONFIG_HOME $HOME/.config
set -q XDG_DATA_HOME; or set -gx XDG_DATA_HOME $HOME/.local/share
set -q XDG_STATE_HOME; or set -gx XDG_STATE_HOME $HOME/.local/state
set -q XDG_CACHE_HOME; or set -gx XDG_CACHE_HOME $HOME/.cache

# editor
if set -q SSH_CONNECTION
    set -gx EDITOR vim
else
    set -gx EDITOR nvim
end

# Rust mirror
set -gx RUSTUP_DIST_SERVER https://rsproxy.cn
set -gx RUSTUP_UPDATE_ROOT https://rsproxy.cn/rustup

# Go
set -gx GOPATH $HOME/go

# pnpm
set -gx PNPM_HOME $HOME/.local/share/pnpm

# PATH
fish_add_path \
    $PNPM_HOME/bin \
    $HOME/go/bin \
    $HOME/.local/bin
