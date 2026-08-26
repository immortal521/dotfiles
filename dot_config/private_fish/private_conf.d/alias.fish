alias ll="ls -lah"

alias n="nvim"

alias fishconfig="$EDITOR ~/.config/fish"

alias reload="source ~/.config/fish/config.fish"

alias ...="cd ../.."

alias ....="cd ../../.."

alias sd="sudoedit"

alias gc="git clone"


function neovide
    command neovide --fork $argv
end
