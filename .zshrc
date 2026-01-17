export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="robbyrussell"

HYPHEN_INSENSITIVE="true"

# ENABLE_CORRECTION="true"

# COMPLETION_WAITING_DOTS="true"

DISABLE_UNTRACKED_FILES_DIRTY="true"

plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh

if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='vim'
else
  export EDITOR='nvim'
fi

alias zshconfig="$EDITOR ~/.zshrc"
alias ohmyzsh="$EDITOR ~/.oh-my-zsh"

eval "$(starship init zsh)"
eval "$(zoxide init zsh)"

alias ll="ls -lah"

alias n="nvim"

export PROXY_HOST="127.0.0.1"
export PROXY_PORT="10808"

proxy_on() {
    unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

    export ALL_PROXY="socks5h://${PROXY_HOST}:${PROXY_PORT}"
    export all_proxy="$ALL_PROXY"

    proxy_test
}

proxy_off() {
    unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY
    echo "🛑 代理已关闭"
}

proxy_status() {
    if [[ -n "$http_proxy" ]]; then
        echo "📡 状态：已开启 → $http_proxy"
    else
        echo "🚫 状态：已关闭"
    fi
}

proxy_test() {
    echo "🔍 测试连接..."
    curl -I --max-time 3 https://www.google.com >/dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        echo "🟢 正常"
    else
        echo "🔴 异常"
    fi
}

export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm

export NVM_NODEJS_ORG_MIRROR=https://mirrors.bfsu.edu.cn/nodejs-release/
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"

# pnpm
export PNPM_HOME="/home/immortal/.local/share/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end
