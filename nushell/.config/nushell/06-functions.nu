def --env proxy [action: string = "status"] {
    let proxy_host = $env.PROXY_HOST? | default "127.0.0.1"
    let http_port = $env.PROXY_HTTP_PORT? | default "10808"
    let socks_port = $env.PROXY_SOCKS_PORT? | default "10809"
    let http_proxy_addr = $"http://($proxy_host):($http_port)"
    let socks_proxy_addr = $"socks5h://($proxy_host):($socks_port)"

    match $action {
        "on" | "o" | "set" => {
            load-env {
                HTTP_PROXY: $http_proxy_addr
                HTTPS_PROXY: $http_proxy_addr
                http_proxy: $http_proxy_addr
                https_proxy: $http_proxy_addr
                ALL_PROXY: $socks_proxy_addr
                all_proxy: $socks_proxy_addr
            }

            proxy status
            proxy test
        }
        "off" | "x" | "unset" => {
            hide-env --ignore-errors HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy
            print "代理已关闭"
        }
        "status" | "s" => {
            if ($env.ALL_PROXY? | default "") != "" {
                print $"状态：已开启
HTTP_PROXY  = ($env.HTTP_PROXY? | default "")
HTTPS_PROXY = ($env.HTTPS_PROXY? | default "")
ALL_PROXY   = ($env.ALL_PROXY)"
            } else {
                print "状态：已关闭"
            }
        }
        "test" | "t" | "check" => {
            print "测试连接..."

            let ok = (try {
                curl -I --max-time 5 https://www.google.com out+err> /dev/null
                $env.LAST_EXIT_CODE == 0
            } catch {
                false
            })

            if $ok {
                print "正常"
            } else {
                print "异常"
            }
        }
        _ => {
            print "用法:
  proxy on|o       开启代理
  proxy off|x      关闭代理
  proxy status|s   查看状态
  proxy test|t     测试连接"
        }
    }
}

def --env "proxy set" [] {
    proxy on
}

def --env "proxy unset" [] {
    proxy off
}

def "proxy check" [] {
    proxy test
}

def --env "config update" [] {
    let old_dir = (pwd)

    cd ~/.config

    print "Updating main repo and submodules..."

    git pull --recurse-submodules
    git submodule update --remote --merge

    print "Submodule status:"
    git submodule status

    cd $old_dir
}

def nuconfig [] {
    ^$env.EDITOR $nu.default-config-dir
}

def --env y [...args] {
    let tmp = (mktemp -t "yazi-cwd.XXXXXX")
    yazi ...$args --cwd-file $tmp
    let cwd = (open $tmp)
    if $cwd != "" and $cwd != $env.PWD {
        cd $cwd
    }
    rm -fp $tmp
}
