mise activate fish | source
if status is-interactive
  set -gx STARSHIP_CONFIG $HOME/.config/starship/starship.toml
  starship init fish | source
  zoxide init fish | source
end
