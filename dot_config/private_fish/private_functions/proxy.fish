function proxy
    set -l PROXY_HOST 127.0.0.1
    set -l PROXY_HTTP_PORT 10808
    set -l PROXY_SOCKS_PORT 10809

    set http_proxy_addr http://$PROXY_HOST:$PROXY_HTTP_PORT
    set socks_proxy_addr socks5h://$PROXY_HOST:$PROXY_SOCKS_PORT

    switch $argv[1]

    case on o
        set -gx HTTP_PROXY $http_proxy_addr
        set -gx HTTPS_PROXY $http_proxy_addr
        set -gx ALL_PROXY $socks_proxy_addr
        set -gx http_proxy $HTTP_PROXY
        set -gx https_proxy $HTTPS_PROXY
        set -gx all_proxy $ALL_PROXY

        proxy status
        proxy test

    case off x
        set -e HTTP_PROXY
        set -e HTTPS_PROXY
        set -e ALL_PROXY
        set -e http_proxy
        set -e https_proxy
        set -e all_proxy

        echo "代理已关闭"


    case status s
        if set -q ALL_PROXY
            echo "状态：已开启"
            echo "HTTP_PROXY  = $HTTP_PROXY"
            echo "HTTPS_PROXY = $HTTPS_PROXY"
            echo "ALL_PROXY   = $ALL_PROXY"
        else
            echo "状态：已关闭"
        end

    case test t
        echo "测试连接..."
        if curl \
            -I \
            --max-time 5 \
            https://www.google.com \
            >/dev/null 2>&1

            echo "正常"
        else
            echo "异常"
        end


    case '*'
        echo "
用法:
  proxy on|o
  proxy off|x
  proxy status|s
  proxy test|t
"
    end
end
