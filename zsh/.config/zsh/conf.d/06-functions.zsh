export PROXY_HOST=127.0.0.1
export PROXY_HTTP_PORT=10808
export PROXY_SOCKS_PORT=10809
proxy() {
    local http_proxy_addr="http://${PROXY_HOST}:${PROXY_HTTP_PORT}"
    local socks_proxy_addr="socks5h://${PROXY_HOST}:${PROXY_SOCKS_PORT}"

    case "$1" in
        on|o)
            # HTTP系工具
            export HTTP_PROXY="$http_proxy_addr"
            export HTTPS_PROXY="$http_proxy_addr"

            export http_proxy="$HTTP_PROXY"
            export https_proxy="$HTTPS_PROXY"

            # 支持SOCKS的工具优先使用
            export ALL_PROXY="$socks_proxy_addr"
            export all_proxy="$ALL_PROXY"

            proxy status
            proxy test
            ;;

        off|x)
            unset HTTP_PROXY HTTPS_PROXY ALL_PROXY
            unset http_proxy https_proxy all_proxy

            echo "代理已关闭"
            ;;

        status|s)
            if [[ -n "$ALL_PROXY" ]]; then
                cat <<EOF
状态：已开启
HTTP_PROXY  = ${HTTP_PROXY}
HTTPS_PROXY = ${HTTPS_PROXY}
ALL_PROXY   = ${ALL_PROXY}
EOF
            else
                echo "状态：已关闭"
            fi
            ;;

        test|t)
            printf "测试连接...\n"

            if curl \
                -I \
                --max-time 5 \
                https://www.google.com \
                >/dev/null 2>&1
            then
                echo "正常"
            else
                echo "异常"
            fi
            ;;

        *)
            cat <<EOF
用法:
  proxy on|o       开启代理
  proxy off|x      关闭代理
  proxy status|s   查看状态
  proxy test|t     测试连接
EOF
            ;;
    esac
}
