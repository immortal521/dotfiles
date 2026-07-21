$env.config = {
    show_banner: false # 是否在启动时显示 Nushell 的欢迎横幅（true 为启用，false 为禁用）
    ls: {use_ls_colors: true, clickable_links: true}
    rm: {always_trash: false}
    table: {
        # 表格边框样式。可选值: basic, compact, compact_double, light, thin, with_love, rounded, reinforced, heavy, none 等
        mode: rounded
        # 索引列（行号）的显示模式："always" 总是显示，"never" 从不显示，"auto" 仅在数据本身含有 index 列时显示
        index_mode: always
        # 当命令返回空列表或空记录时，是否显式打印出 '[empty list]' 或 '[empty record]' 占位符
        show_empty: true
        # 表格每个单元格的左右内边距（空格数）
        padding: {left: 1, right: 1}
        # 当文本超出列宽时的裁剪/处理策略
        trim: {methodology: truncating, wrapping_try_keep_words: true, truncating_suffix: "..."}
        header_on_separator: false # 是否把表头文字直接嵌入到上方分割线/边框线中
        footer_inheritance: false # 当子表格足够大时，是否将页脚渲染在父表格中（高级嵌套表格选项）
        # abbreviated_row_count: 10 # 限制表格展示的最大行数，超过时隐藏中间部分，保留顶部和底部各几行（当前已注释）
    }
    error_style: "fancy" # 错误风格："fancy" 带有华丽的彩色和位置指针，"plain" 为纯文本（更适合屏幕阅读器等无障碍设备）

    # 控制当触发某种错误时，是否向终端打印错误信息
    display_errors: {exit_code: false, termination_signal: true}

    # 决定 shell 中日期时间的渲染格式。如果不配置，默认会“人性化”地显示为“a day ago（一天前）”等。
    datetime_format: {}
    explore: {
        status_bar_background: {fg: "#1D1F21", bg: "#C4C9C6"} # 底部状态栏的前景色与背景色
        command_bar_text: {fg: "#C4C9C6"} # 底部命令输入栏的文本颜色
        highlight: {fg: "black", bg: "yellow"} # 搜索匹配项的高亮颜色
        status: {
            error: {fg: "white", bg: "red"} # 状态栏报错时的颜色
            warn: {}
            info: {}
        }
        selected_cell: {bg: light_blue} # 当前选中的单元格背景色
    }

    # 历史记录
    history: {
        max_size: 100_000 # 历史记录最大保存条数（修改后需要重启 Session 才会生效）
        sync_on_enter: true # 每次敲回车时是否立即同步历史。开启后可在多个打开的终端窗口间实时共享历史记录。
        file_format: "sqlite" # 历史记录的存储格式："sqlite" 数据库格式，或 "plaintext" 纯文本格式
        isolation: false # 仅在 sqlite 格式下有效。true 表示开启历史隔离（各终端窗口的上下箭头只能翻看自己窗口的历史）；false 表示所有窗口混用、共享。
    }

    # 自动补全
    completions: {
        case_sensitive: false # 自动补全时是否区分大小写
        quick: true # 如果只剩下一个匹配项，是否自动直接选中并填入（false 则需要再次确认）
        partial: true # 是否允许只填入公共前缀（部分填充补全）
        algorithm: "prefix" # 补全匹配算法："prefix"（前缀匹配）或 "fuzzy"（模糊匹配）
        sort: "smart" # 排序规则："smart"（前缀匹配时按字母序，模糊匹配时按匹配度得分排序），或强制 "alphabetical"（全按字母序）
        external: {enable: true, max_results: 100, completer: null}
        use_ls_colors: true # 进行文件/路径补全时，提示菜单是否也根据 LS_COLORS 显示对应的文件颜色
    }
    filesize: {unit: "metric"}

    # 光标样式
    cursor_shape: {emacs: line, vi_insert: block, vi_normal: underscore}
    # color_config: $dark_theme # 终端色彩主题。这里绑定了预设的暗色主题 `$dark_theme`（也可以换成 `$light_theme` 或自定义记录）
    footer_mode: 25 # 表格页脚（重复显示表头）的触发模式。数字 25 表示：当表格行数超过 25 行时，才在底部显示页脚。
    float_precision: 2 # 数据表格中浮点数（小数）显示的保留位数
    buffer_editor: "nvim" # 按下 Ctrl+O 时，用来编辑当前长命令行缓冲区的文本编辑器（这里配置为 Neovim）。若不设，则找环境变量中的 VISUAL 或 EDITOR。
    use_ansi_coloring: true # 是否启用 ANSI 颜色代码输出
    bracketed_paste: true # 启用括号式粘贴（防止粘贴多行代码时直接触发执行，对 Windows 暂无效）
    edit_mode: emacs # 命令行文本编辑快捷键模式：emacs 模式（如 Ctrl+A 触网开头）或 vi 模式
    shell_integration: {
        osc2: true # 自动简化家目录路径、并在终端标签页/窗口标题上显示当前正在运行的命令
        osc7: true # 向终端实时汇报当前工作目录（CWD），方便你在终端开新标签页时能自动保持在当前目录下
        osc8: true # 与之前被弃用的 `ls.clickable_links` 类似，负责在表格中生成可点击的超链接
        osc9_9: false # ConEmu 终端特有的目录汇报协议。这里关闭。
        osc133: false # Final Term 协议。包含 A(提示符开始), B(提示符结束), C(执行前), D(执行后带退出码)。让现代终端精确识别命令与输出的边界。这里关闭。
        osc633: true # 类似 osc133，但专门用于 VS Code 的终端集成，能强化 VS Code 里的最近命令菜单和命令导航功能。
        reset_application_mode: true # 发送 `\x1b[?1l` 转义符，用于让 SSH 远程连接工作得更稳定。
    }
    render_right_prompt_on_last_line: false # 当你的右侧提示符（Right Prompt）是多行时，是否强制将其渲染在提示符的最后一行。
    use_kitty_protocol: false # 是否开启 Kitty 键盘高级增强协议（需要你的终端模拟器本身支持该协议）
    highlight_resolved_externals: false # 是否在 REPL 命令行中高亮那些通过 `which` 找到的外部系统命令
    recursion_limit: 50 # Nushell 允许脚本或函数递归调用的最大深度，超过 50 次将强行停止防死锁

    # 插件
    plugins: {}
    plugin_gc: {
        default: {
            enabled: true # 是否允许自动停止不活动的插件
            stop_after: 10sec # 某个插件闲置超过 10 秒后，将其后台进程杀掉
        }
        plugins: {}
    }

    # Hook
    hooks: {
        pre_prompt: [
            { null }
        ]
        pre_execution: [
            { null }
        ]
        env_change: {
            PWD: [
                {|before, after| null }
            ]
        }
        # 当管道产生输出准备打印在屏幕上时执行。这里表示：如果终端列宽 >= 100，使用 `table -e`（展开模式表格）展示，否则用普通 `table`。
        display_output: "if (term size).columns >= 100 { table -e } else { table }"
        command_not_found: { null }
    }
    menus: [
        {
            name: completion_menu
            only_buffer_difference: false
            marker: "| "
            type: {
                layout: columnar
                columns: 4
                col_width: 20 # Optional value. If missing all the screen width is used to calculate column width
                col_padding: 2
            }
            style: {
                text: green
                selected_text: {attr: r}
                description_text: yellow
                match_text: {attr: u}
                selected_match_text: {attr: ur}
            }
        }
        {
            name: ide_completion_menu
            only_buffer_difference: false
            marker: "| "
            type: {
                layout: ide
                min_completion_width: 0
                max_completion_width: 50
                max_completion_height: 10 # will be limited by the available lines in the terminal
                padding: 0
                border: true
                cursor_offset: 0
                description_mode: "prefer_right"
                min_description_width: 0
                max_description_width: 50
                max_description_height: 10
                description_offset: 1
                correct_cursor_pos: false
            }
            style: {
                text: green
                selected_text: {attr: r}
                description_text: yellow
                match_text: {attr: u}
                selected_match_text: {attr: ur}
            }
        }
        {
            name: history_menu
            only_buffer_difference: true
            marker: "? "
            type: {layout: list, page_size: 10}
            style: {text: green, selected_text: green_reverse, description_text: yellow}
        }
        {
            name: help_menu
            only_buffer_difference: true
            marker: "? "
            type: {
                layout: description
                columns: 4
                col_width: 20 # Optional value. If missing all the screen width is used to calculate column width
                col_padding: 2
                selection_rows: 4
                description_rows: 10
            }
            style: {text: green, selected_text: green_reverse, description_text: yellow}
        }
    ]
    keybindings: [
        {
            name: completion_menu
            modifier: none
            keycode: tab
            mode: [emacs vi_normal vi_insert]
            event: {
                until: [
                    {send: menu, name: completion_menu}
                    {send: menunext}
                    {edit: complete}
                ]
            }
        }
        {
            name: completion_previous_menu
            modifier: shift
            keycode: backtab
            mode: [emacs, vi_normal, vi_insert]
            event: {send: menuprevious}
        }
        {
            name: ide_completion_menu
            modifier: control
            keycode: space
            mode: [emacs vi_normal vi_insert]
            event: {
                until: [
                    {send: menu, name: ide_completion_menu}
                    {send: menunext}
                    {edit: complete}
                ]
            }
        }
        {
            name: history_menu
            modifier: control
            keycode: char_r
            mode: [emacs, vi_insert, vi_normal]
            event: {send: menu, name: history_menu}
        }
        {
            name: help_menu
            modifier: none
            keycode: f1
            mode: [emacs, vi_insert, vi_normal]
            event: {send: menu, name: help_menu}
        }
        {
            name: next_page_menu
            modifier: control
            keycode: char_x
            mode: emacs
            event: {send: menupagenext}
        }
        {
            name: undo_or_previous_page_menu
            modifier: control
            keycode: char_z
            mode: emacs
            event: {
                until: [
                    {send: menupageprevious}
                    {edit: undo}
                ]
            }
        }
        {
            name: escape
            modifier: none
            keycode: escape
            mode: [emacs, vi_normal, vi_insert]
            event: {send: esc} # NOTE: does not appear to work
        }
        {
            name: cancel_command
            modifier: control
            keycode: char_c
            mode: [emacs, vi_normal, vi_insert]
            event: {send: ctrlc}
        }
        {
            name: quit_shell
            modifier: control
            keycode: char_d
            mode: [emacs, vi_normal, vi_insert]
            event: {send: ctrld}
        }
        {
            name: clear_screen
            modifier: control
            keycode: char_l
            mode: [emacs, vi_normal, vi_insert]
            event: {send: clearscreen}
        }
        {
            name: search_history
            modifier: control
            keycode: char_q
            mode: [emacs, vi_normal, vi_insert]
            event: {send: searchhistory}
        }
        {
            name: open_command_editor
            modifier: control
            keycode: char_o
            mode: [emacs, vi_normal, vi_insert]
            event: {send: openeditor}
        }
        {
            name: move_up
            modifier: none
            keycode: up
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: menuup}
                    {send: up}
                ]
            }
        }
        {
            name: move_down
            modifier: none
            keycode: down
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: menudown}
                    {send: down}
                ]
            }
        }
        {
            name: move_left
            modifier: none
            keycode: left
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: menuleft}
                    {send: left}
                ]
            }
        }
        {
            name: move_right_or_take_history_hint
            modifier: none
            keycode: right
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: historyhintcomplete}
                    {send: menuright}
                    {send: right}
                ]
            }
        }
        {
            name: move_one_word_left
            modifier: control
            keycode: left
            mode: [emacs, vi_normal, vi_insert]
            event: {edit: movewordleft}
        }
        {
            name: move_one_word_right_or_take_history_hint
            modifier: control
            keycode: right
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: historyhintwordcomplete}
                    {edit: movewordright}
                ]
            }
        }
        {
            name: move_to_line_start
            modifier: none
            keycode: home
            mode: [emacs, vi_normal, vi_insert]
            event: {edit: movetolinestart}
        }
        {
            name: move_to_line_start
            modifier: control
            keycode: char_a
            mode: [emacs, vi_normal, vi_insert]
            event: {edit: movetolinestart}
        }
        {
            name: move_to_line_end_or_take_history_hint
            modifier: none
            keycode: end
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: historyhintcomplete}
                    {edit: movetolineend}
                ]
            }
        }
        {
            name: move_to_line_end_or_take_history_hint
            modifier: control
            keycode: char_e
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: historyhintcomplete}
                    {edit: movetolineend}
                ]
            }
        }
        {
            name: move_to_line_start
            modifier: control
            keycode: home
            mode: [emacs, vi_normal, vi_insert]
            event: {edit: movetolinestart}
        }
        {
            name: move_to_line_end
            modifier: control
            keycode: end
            mode: [emacs, vi_normal, vi_insert]
            event: {edit: movetolineend}
        }
        {
            name: move_down
            modifier: control
            keycode: char_n
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: menudown}
                    {send: down}
                ]
            }
        }
        {
            name: move_up
            modifier: control
            keycode: char_p
            mode: [emacs, vi_normal, vi_insert]
            event: {
                until: [
                    {send: menuup}
                    {send: up}
                ]
            }
        }
        {
            name: delete_one_character_backward
            modifier: none
            keycode: backspace
            mode: [emacs, vi_insert]
            event: {edit: backspace}
        }
        {
            name: delete_one_word_backward
            modifier: control
            keycode: backspace
            mode: [emacs, vi_insert]
            event: {edit: backspaceword}
        }
        {
            name: delete_one_character_forward
            modifier: none
            keycode: delete
            mode: [emacs, vi_insert]
            event: {edit: delete}
        }
        {
            name: delete_one_character_forward
            modifier: control
            keycode: delete
            mode: [emacs, vi_insert]
            event: {edit: delete}
        }
        {
            name: delete_one_character_backward
            modifier: control
            keycode: char_h
            mode: [emacs, vi_insert]
            event: {edit: backspace}
        }
        {
            name: delete_one_word_backward
            modifier: control
            keycode: char_w
            mode: [emacs, vi_insert]
            event: {edit: backspaceword}
        }
        {
            name: move_left
            modifier: none
            keycode: backspace
            mode: vi_normal
            event: {edit: moveleft}
        }
        {
            name: newline_or_run_command
            modifier: none
            keycode: enter
            mode: emacs
            event: {send: enter}
        }
        {
            name: move_left
            modifier: control
            keycode: char_b
            mode: emacs
            event: {
                until: [
                    {send: menuleft}
                    {send: left}
                ]
            }
        }
        {
            name: move_right_or_take_history_hint
            modifier: control
            keycode: char_f
            mode: emacs
            event: {
                until: [
                    {send: historyhintcomplete}
                    {send: menuright}
                    {send: right}
                ]
            }
        }
        {
            name: redo_change
            modifier: control
            keycode: char_g
            mode: emacs
            event: {edit: redo}
        }
        {
            name: undo_change
            modifier: control
            keycode: char_z
            mode: emacs
            event: {edit: undo}
        }
        {
            name: paste_before
            modifier: control
            keycode: char_y
            mode: emacs
            event: {edit: pastecutbufferbefore}
        }
        {
            name: cut_word_left
            modifier: control
            keycode: char_w
            mode: emacs
            event: {edit: cutwordleft}
        }
        {
            name: cut_line_to_end
            modifier: control
            keycode: char_k
            mode: emacs
            event: {edit: cuttolineend}
        }
        {
            name: cut_line_from_start
            modifier: control
            keycode: char_u
            mode: emacs
            event: {edit: cutfromstart}
        }
        {
            name: swap_graphemes
            modifier: control
            keycode: char_t
            mode: emacs
            event: {edit: swapgraphemes}
        }
        {
            name: move_one_word_left
            modifier: alt
            keycode: left
            mode: emacs
            event: {edit: movewordleft}
        }
        {
            name: move_one_word_right_or_take_history_hint
            modifier: alt
            keycode: right
            mode: emacs
            event: {
                until: [
                    {send: historyhintwordcomplete}
                    {edit: movewordright}
                ]
            }
        }
        {
            name: move_one_word_left
            modifier: alt
            keycode: char_b
            mode: emacs
            event: {edit: movewordleft}
        }
        {
            name: move_one_word_right_or_take_history_hint
            modifier: alt
            keycode: char_f
            mode: emacs
            event: {
                until: [
                    {send: historyhintwordcomplete}
                    {edit: movewordright}
                ]
            }
        }
        {
            name: delete_one_word_forward
            modifier: alt
            keycode: delete
            mode: emacs
            event: {edit: deleteword}
        }
        {
            name: delete_one_word_backward
            modifier: alt
            keycode: backspace
            mode: emacs
            event: {edit: backspaceword}
        }
        {
            name: delete_one_word_backward
            modifier: alt
            keycode: char_m
            mode: emacs
            event: {edit: backspaceword}
        }
        {
            name: cut_word_to_right
            modifier: alt
            keycode: char_d
            mode: emacs
            event: {edit: cutwordright}
        }
        {
            name: upper_case_word
            modifier: alt
            keycode: char_u
            mode: emacs
            event: {edit: uppercaseword}
        }
        {
            name: lower_case_word
            modifier: alt
            keycode: char_l
            mode: emacs
            event: {edit: lowercaseword}
        }
        {
            name: capitalize_char
            modifier: alt
            keycode: char_c
            mode: emacs
            event: {edit: capitalizechar}
        }
        {
            name: copy_selection
            modifier: control_shift
            keycode: char_c
            mode: emacs
            event: {edit: copyselection}
        }
        {
            name: cut_selection
            modifier: control_shift
            keycode: char_x
            mode: emacs
            event: {edit: cutselection}
        }
        {
            name: select_all
            modifier: control_shift
            keycode: char_a
            mode: emacs
            event: {edit: selectall}
        }
    ]
}
