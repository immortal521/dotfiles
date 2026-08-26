export ZDOTDIR="$HOME/.config/zsh"

export XDG_CONFIG_HOME="$HOME/.config"
export XDG_CACHE_HOME="$HOME/.cache"

export STARSHIP_CONFIG="$HOME/.config/starship/starship.toml"

if [[ ! -d "$XDG_CACHE_HOME/zsh" ]]; then
    mkdir -p "$XDG_CACHE_HOME/zsh"
fi

# 加载配置
for file in "$ZDOTDIR/conf.d/"*.zsh; do
    source "$file"
done

# 私有配置
[[ -f "$ZDOTDIR/local.zsh" ]] && \
source "$ZDOTDIR/local.zsh"
