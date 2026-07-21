$env.XDG_CONFIG_HOME = ($env.HOME | path join ".config")
$env.XDG_CACHE_HOME = ($env.HOME | path join ".cache")
$env.STARSHIP_CONFIG = ($env.HOME | path join ".config/starship/starship.toml")

if ($env.SSH_CONNECTION? | default "") != "" {
    $env.EDITOR = "vim"
} else {
    $env.EDITOR = "nvim"
}

$env.RUSTUP_DIST_SERVER = "https://rsproxy.cn"
$env.RUSTUP_UPDATE_ROOT = "https://rsproxy.cn/rustup"

$env.GOPATH = ($env.HOME | path join "go")
$env.PNPM_HOME = ($env.HOME | path join ".local/share/pnpm/bin")
$env.PROXY_HOST = "127.0.0.1"
$env.PROXY_HTTP_PORT = "10808"
$env.PROXY_SOCKS_PORT = "10809"

$env.PATH = (
    [
        $env.PNPM_HOME
        ($env.GOPATH | path join "bin")
        ($env.HOME | path join ".local/bin")
    ]
    | append $env.PATH
    | uniq
)
