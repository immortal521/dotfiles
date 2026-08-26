setopt AUTO_CD
setopt INTERACTIVE_COMMENTS

# =========================
# History
# =========================
HISTFILE="$HOME/.local/state/zsh/history"

HISTSIZE=100000
SAVEHIST=100000

# 追加写入，不覆盖
setopt APPEND_HISTORY

# 命令执行后立即写历史
setopt INC_APPEND_HISTORY

# 多终端共享历史
setopt SHARE_HISTORY

# 去重
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_SAVE_NO_DUPS

# 清理多余空格
setopt HIST_REDUCE_BLANKS

# 保存时间戳
setopt EXTENDED_HISTORY

mkdir -p "$(dirname "$HISTFILE")"

# =========================
# Completion
# =========================
autoload -Uz compinit

# 补全缓存
zcompdump="$XDG_CACHE_HOME/zsh/.zcompdump"

compinit -d "$zcompdump"

# 大小写不敏感
# down -> Downloads
zstyle ':completion:*' matcher-list \
    'm:{a-z}={A-Za-z}' \
    'r:|[._-]=* r:|=*'

# 补全菜单
zstyle ':completion:*' menu select

# 彩色补全
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"

# 补全缓存目录
zstyle ':completion:*' cache-path "$HOME/.cache/zsh/zcompcache"

mkdir -p "$HOME/.cache/zsh"


# =========================
# 补全增强
# =========================

# 隐藏末尾 /
setopt AUTO_PARAM_SLASH

# 输入目录名后自动补 /
setopt AUTO_LIST

# 更智能 cd 补全
zstyle ':completion:*:*:cd:*' tag-order local-directories directory-stack path-directories files

zmodload zsh/complist
bindkey -M menuselect '^[[Z' reverse-menu-complete
