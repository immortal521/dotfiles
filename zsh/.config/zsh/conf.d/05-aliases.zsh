alias ll="ls -lah"

alias n="nvim"

alias zshconfig="$EDITOR ~/.config/zsh"

alias reload="source ~/.config/zsh/.zshrc"

alias ...='cd ../..'
alias ....='cd ../../..'

alias sd='sudoedit'
alias gc="git clone"

neovide() {
  command neovide --fork "$@"
}
