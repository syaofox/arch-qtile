from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
import shutil


mod = "mod4"
terminal = guess_terminal()

myTerm = "alacritty"      # My terminal of choice


def columns_grow_current(qtile):
    layout = qtile.current_layout
    if getattr(layout, "name", "") != "columns":
        return
    if len(layout.columns) < 2:
        return
    amount = getattr(layout, "grow_amount", 10)
    left = layout.columns[0]
    right = layout.columns[1]
    if right.width <= amount:
        return
    left.width += amount
    right.width -= amount
    layout.group.layout_all()


def columns_shrink_current(qtile):
    layout = qtile.current_layout
    if getattr(layout, "name", "") != "columns":
        return
    if len(layout.columns) < 2:
        return
    amount = getattr(layout, "grow_amount", 10)
    left = layout.columns[0]
    right = layout.columns[1]
    if left.width <= amount:
        return
    left.width -= amount
    right.width += amount
    layout.group.layout_all()


keys = [
    Key([mod], "h", lazy.layout.left(), desc="移动焦点到左边"),
    Key([mod], "l", lazy.layout.right(), desc="移动焦点到右边"),
    Key([mod], "j", lazy.layout.down(), desc="移动焦点到下边"),
    Key([mod], "k", lazy.layout.up(), desc="移动焦点到上边"),
    Key([mod], "d", lazy.layout.next(), desc="移动窗口焦点到其他窗口"),
    # 改变窗口大小
    Key([mod], "period", lazy.function(columns_grow_current), desc="放大当前窗口"),
    Key([mod], "comma", lazy.function(columns_shrink_current), desc="缩小当前窗口"),
    # 移动窗口
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="移动窗口到左边"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="移动窗口到右边"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="移动窗口到下边"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="移动窗口到上边"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="放大窗口到左边"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="放大窗口到右边"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="放大窗口到下边"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="放大窗口到上边"),
    Key([mod], "n", lazy.layout.normalize(), desc="重置所有窗口大小"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="切换分割和非分割",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="启动终端"),
    Key([mod], "w", lazy.spawn("bash -c 'export LANGUAGE=zh_CN.UTF-8 && brave-browser &'"), desc="启动浏览器"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="切换布局"),
    Key([mod], "q", lazy.window.kill(), desc="关闭焦点窗口"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="焦点窗口切换全屏",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="焦点窗口切换浮动"),
    Key([mod], "e", lazy.spawn("thunar"), desc="打开文件管理器"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="重新加载配置"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="关闭 Qtile"),
    Key([mod], "Space", lazy.spawn("rofi -show drun -show-icons"), desc='启动启动器'),
    Key(
        [mod], 
        "a",
        lazy.spawn('sh -c "maim -s | xclip -selection clipboard -t image/png -i"'),
        desc="截图"
    ),
    Key([mod], "p", lazy.spawn("sh -c 'gpick -p'"), desc="选择颜色并复制到剪贴板"),

]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


group_definitions = [
    ("1", {"label": ""}),
    ("2", {"label": "", "matches": [Match(wm_class="brave-browser")]}),
    ("3", {"label": "", "matches": [Match(wm_class="cursor")]}),
    ("4", {}),
    ("5", {}),
    ("6", {}),
    ("7", {}),
    ("8", {}),
    ("9", {"label": "", "matches": [Match(wm_class="io.github.celluloid_player.Celluloid")]}),
]

groups = [Group(name, **params) for name, params in group_definitions]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            # Key(
            #     [mod, "shift"],
            #     i.name,
            #     lazy.window.togroup(i.name, switch_group=True),
            #     desc=f"Switch to & move focused window to group {i.name}",
            # ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                desc="将焦点窗口移动到组 {}".format(i.name)),
        ]
    )

colors = [
    ["#1a1b26", "#1a1b26"],  # bg        (primary.background)
    ["#a9b1d6", "#a9b1d6"],  # fg        (primary.foreground)
    ["#32344a", "#32344a"],  # color01   (normal.black)
    ["#f7768e", "#f7768e"],  # color02   (normal.red)
    ["#9ece6a", "#9ece6a"],  # color03   (normal.green)
    ["#e0af68", "#e0af68"],  # color04   (normal.yellow)
    ["#7aa2f7", "#7aa2f7"],  # color05   (normal.blue)
    ["#ad8ee6", "#ad8ee6"],  # color06   (normal.magenta)
    ["#0db9d7", "#0db9d7"],  # color15   (bright.cyan)
    ["#444b6a", "#444b6a"]   # color[9]  (bright.black)
]

# helper in case your colors are ["#hex", "#hex"]
def C(x): return x[0] if isinstance(x, (list, tuple)) else x


def make_sep(padding: int = 8):
    return widget.Sep(linewidth=1, padding=padding, foreground=colors[9])


def get_kernel_version():
    try:
        return subprocess.check_output(["uname", "-r"], text=True).strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        return "kernel?"


def systray_widget():
    core = getattr(qtile, "core", None)
    if core and getattr(core, "name", None) == "x11":
        return widget.Systray(padding=6)
    return widget.Spacer(length=0)


def start_gnome_keyring():
    keyring_exec = shutil.which("gnome-keyring-daemon")
    if not keyring_exec:
        print("gnome-keyring-daemon 不存在，无法自动启动。")
        return

    try:
        keyring_result = subprocess.run(
            [keyring_exec, "--daemonize", "--start", "--components=pkcs11,secrets,ssh"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        print("gnome-keyring-daemon 启动超时。")
        return
    except subprocess.CalledProcessError as error:
        print(f"gnome-keyring-daemon 启动失败: {error}")
        return

    for line in keyring_result.stdout.splitlines():
        if "=" in line:
            key, value = line.strip().split("=", 1)
            os.environ[key] = value


def ensure_picom_running():
    try:
        picom_process = subprocess.run(
            ["pgrep", "picom"],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        picom_process = None

    if picom_process and picom_process.stdout:
        print("picom 已经在运行。")
        return

    picom_exec = shutil.which("picom")
    if not picom_exec:
        print("picom 不存在，无法自动启动。")
        return

    picom_config = os.path.expanduser("~/.config/picom/picom.conf")
    picom_cmd = [picom_exec]
    if os.path.isfile(picom_config):
        picom_cmd.extend(["--config", picom_config])

    try:
        subprocess.Popen(picom_cmd)
        print(f"已启动 picom: {' '.join(picom_cmd)}")
    except OSError as error:
        print(f"启动 picom 失败: {error}")


def ensure_fcitx_running():
    try:
        process = subprocess.run(
            ["pgrep", "fcitx5"],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        process = None

    if process and process.stdout:
        print("fcitx5 已经在运行。")
        return

    try:
        subprocess.Popen(["fcitx5", "-d"])
    except OSError as error:
        print(f"启动 fcitx5 失败: {error}")


def get_gpu_usage():
    try:
        output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            text=True,
        )
        usage = output.strip().splitlines()[0]
        return f"GPU: {usage}%"
    except (FileNotFoundError, subprocess.CalledProcessError, IndexError):
        return "GPU: n/a"


def get_gpu_memory():
    try:
        output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ],
            text=True,
        )
        used, total = output.strip().splitlines()[0].split(",")
        used = float(used.strip()) / 1024
        # total = float(total.strip()) / 1024
        return f"VRAM: {used:.2f}G"
        # return f"VRAM: {used:.2f}GiB/{total:.2f}GiB"
    except (FileNotFoundError, subprocess.CalledProcessError, IndexError, ValueError):
        return "VRAM: n/a"

layout_theme = {
    "border_width" : 1,
    "margin" : 1,
    "border_focus" : colors[6],
    "border_normal" : colors[0],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Propo Bold",
    # font="Ubuntu Bold",
    fontsize=14,
    padding=0,
    background=colors[0],
)


extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            widgets = [
                widget.Spacer(length = 8),
                widget.Image(
                    filename = "~/.config/qtile/icons/syaofox.png",
                    margin = 6,
                    scale = True,
                    # /home/syaofox/.local/bin/rofi-power-menu
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("rofi -show power-menu -modi 'power-menu:rofi-power-menu'")},
                ),
                widget.Prompt(
                    font = "Ubuntu Mono",
                    fontsize=14,
                    foreground = colors[1]
                ),
                widget.GroupBox(
                    fontsize = 16,
                    margin_y = 5,
                    margin_x = 5,
                    padding_y = 0,
                    padding_x = 2,
                    borderwidth = 3,
                    active = colors[8],
                    inactive = colors[9],
                    rounded = False,
                    highlight_color = colors[0],
                    highlight_method = "line",
                    this_current_screen_border = colors[7],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[7],
                    other_screen_border = colors[4],
                ),
                widget.TextBox(
                    text = '|',
                    font = "JetBrainsMono Nerd Font Propo Bold",
                    foreground = colors[9],
                    padding = 2,
                    fontsize = 14
                ),
                widget.CurrentLayout(
                    foreground = colors[1],
                    padding = 5
                ),
                widget.TextBox(
                    text = '|',
                    font = "JetBrainsMono Nerd Font Propo Bold",
                    foreground = colors[9],
                    padding = 2,
                    fontsize = 14
                ),
                widget.WindowName(
                    foreground = colors[6],
                    padding = 8,
                    max_chars = 40
                ),
                # make_sep(),
                widget.Net(
                    foreground = colors[5],
                    padding = 8,
                    format = 'Net: ↓{down:.1f}{down_suffix}/s ↑{up:.1f}{up_suffix}/s',
                    update_interval = 1,
                    use_bits = False,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e btop')},
                ),
                # widget.GenPollText(
                #     update_interval = 300,
                #     func = get_kernel_version,
                #     foreground = colors[3],
                #     padding = 8, 
                #     fmt = '{}',
                # ),
                make_sep(),
                # uv tool install qtile --with psutil
                widget.CPU(
                    foreground = colors[4],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e btop')},
                    format="CPU: {load_percent}%",
                ),
                make_sep(),
                widget.Memory(
                    foreground = colors[8],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e btop')},
                    measure_mem = 'G',
                    format = 'Mem: {MemUsed:.2f}{mm}',
                ),                
                make_sep(),
                widget.GenPollText(
                    update_interval = 5,
                    func = get_gpu_usage,
                    foreground = colors[3],
                    padding = 8,
                    fmt = '{}',
                ),
                make_sep(),
                widget.GenPollText(
                    update_interval = 5,
                    func = get_gpu_memory,
                    foreground = colors[6],
                    padding = 8,
                    fmt = '{}',
                ),
                make_sep(),
                widget.DF(
                    update_interval = 60,
                    foreground = colors[5],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-disk')},
                    partition = '/',
                    #format = '[{p}] {uf}{m} ({r:.0f}%)',
                    format = '{uf}{m} free',
                    fmt = 'Disk: {}',
                    visible_on_warn = False,
                ),
                make_sep(),
                widget.DF(
                    update_interval = 60,
                    foreground = colors[7],
                    padding = 8,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-disk')},
                    partition = '/mnt/data',
                    format = '{uf}{m} free',
                    fmt = 'Data: {}',
                    visible_on_warn = False,
                ),
                # sep,
                # widget.Battery(
                #     foreground=colors[6],           # pick a palette slot you like
                #     padding=8,
                #     update_interval=5,
                #     format='{percent:2.0%} {char} {hour:d}:{min:02d}',  # e.g. "73% ⚡ 1:45"
                #     fmt='Bat: {}',
                #     charge_char='',               # shown while charging
                #     discharge_char='',            # Nerd icon; use '-' if you prefer plain ascii
                #     full_char='✔',                 # when at/near 100%
                #     unknown_char='?',
                #     empty_char='!', 
                #     mouse_callbacks={
                #         'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e upower -i $(upower -e | grep BAT)'),
                #     },
                # ),
                make_sep(),
                widget.Volume(
                    foreground = colors[7],
                    padding = 8, 
                    fmt = 'Vol: {}',
                ),
                make_sep(),
                widget.Clock(
                    foreground = colors[8],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-date')},
                    ## Uncomment for date and time 
                    format = "%m-%d %H:%M",
                    ## Uncomment for time only
                    # format = "%I:%M %p",
                ),
                systray_widget(),
                widget.Spacer(length = 8),
            ],
            # 24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"],  # Borders are magenta
            margin=[0, 0, 1, 0], 
            size=30,
        ),
        wallpaper="/home/syaofox/.config/walls/eva.jpg",
        wallpaper_mode="fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    # 设置 fcitx5 输入法所需的环境变量
    os.environ["GTK_IM_MODULE"] = "fcitx"
    os.environ["QT_IM_MODULE"] = "fcitx"
    os.environ["XMODIFIERS"] = "@im=fcitx"

    start_gnome_keyring()

#    # 设置屏幕分辨率
#    try:
#        if not os.environ.get("WAYLAND_DISPLAY"):
#            subprocess.run(
#                ["xrandr", "-s", "1920x1080", "-r", "60"],
#                check=True,
#                timeout=5,
#            )
#    except FileNotFoundError:
#        print("xrandr 不存在，无法设置屏幕分辨率。")
#    except subprocess.TimeoutExpired:
#        print("设置屏幕分辨率超时。")
#    except subprocess.CalledProcessError as error:
#        print(f"设置屏幕分辨率失败: {error}")
#
#    # 启动 gnome-keyring 守护进程，并写入返回的环境变量
#    try:
#        keyring_result = subprocess.run(
#            ["/usr/bin/gnome-keyring-daemon", "--daemonize", "--start"],
#            check=True,
#            capture_output=True,
#            text=True,
#            timeout=5,
#        )
#
#        for line in keyring_result.stdout.splitlines():
#            if "=" in line:
#                key, value = line.strip().split("=", 1)
#                os.environ[key] = value
#
#    except FileNotFoundError:
#        print("gnome-keyring-daemon 不存在，无法自动启动。")
#    except subprocess.TimeoutExpired:
#        print("gnome-keyring-daemon 启动超时。")
#    except subprocess.CalledProcessError as error:
#        print(f"gnome-keyring-daemon 启动失败: {error}")

    ensure_fcitx_running()
    ensure_picom_running()
