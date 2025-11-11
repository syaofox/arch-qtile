#!/bin/bash

# --- Arch Linux 软件包安装脚本 ---

# 检查是否以 root 身份运行，pacman 需要 sudo
if [ "$EUID" -ne 0 ]; then
  echo "请使用 'sudo bash install_packages.sh' 运行此脚本"
  exit
fi

# 1. 定义软件包列表
PACKAGES=(
    # --- 核心系统/开发/微码 ---
    intel-ucode        # Intel CPU 微码 (如果是 AMD 请替换为 amd-ucode)
    base-devel         # 编译环境核心工具 (包含 gcc, make 等)
    xorg-xrandr       # 显示器管理工具
    git                # Git 版本控制
    neovim             # 文本编辑器
    nodejs             # JavaScript 运行时
    ripgrep            # 快速代码搜索工具
    python-psutil      # Python 进程监控工具

    # --- 基础工具/效率/系统管理 ---
    alacritty          # 终端模拟器
    bash-completion    # bash 命令行自动补全
    nfs-utils          # 支持 NFS 网络文件系统
    htop               # 交互式进程查看器
    btop               # 交互式系统监控工具
    timeshift          # 系统快照和恢复工具
    # firefox            # 网页浏览器

    # --- 窗口管理器/工具 (适用于 Qtile) ---
    picom              # 合成器 (Compositor)
    xclip              # X 剪贴板命令行工具
    gpick              # 颜色选择器
    # xwallpaper         # 设置 X 桌面壁纸
    maim               # 截图工具
    rofi               # 应用程序启动器/窗口切换器
    # gvfs               # 虚拟文件系统
    pavucontrol        # 音量控制
   
    # --- 字体 ---
    ttf-jetbrains-mono-nerd # JetBrains Mono Nerd 字体
    wqy-microhei       # 文泉驿微米黑
    noto-fonts-emoji   # Noto Emoji 字体 (确保能显示彩色表情)

    # --- 文件管理器/多媒体/安全 ---
    nemo               # Nemo 文件管理器 (核心包)
    nemo-share         # Nemo 分享插件
    nemo-fileroller    # Nemo 归档管理器插件
    udisks2            # udisks2 
    tumbler            # 图像查看器插件
    # nemo-media-columns # Nemo 媒体列插件
    # xviewer            # 图像查看器
    # xviewer-plugins    # 图像查看器插件
    mpv                # 媒体播放器
    gnome-keyring      # 密钥管理服务
    seahorse           # 密钥和密码管理工具 (GNOME Keyring 的图形化界面)

    # --- 输入法 (Fcitx 5) ---
    fcitx5             # Fcitx 5 核心框架
    fcitx5-configtool  # Fcitx 5 图形配置工具
    fcitx5-gtk         # GTK 应用程序集成
    fcitx5-qt          # Qt 应用程序集成
    fcitx5-chinese-addons      # Fcitx 5 官方拼音输入法引擎
)

configure_git_identity() {
  local target_user="${SUDO_USER:-root}"

  if ! command -v git >/dev/null 2>&1; then
    echo "git 未安装，跳过全局账号配置。"
    return
  fi

  local git_runner=(git)
  if [ "$target_user" != "root" ]; then
    git_runner=(sudo -u "$target_user" git)
  fi

  if ! "${git_runner[@]}" config --global user.name >/dev/null 2>&1; then
    "${git_runner[@]}" config --global user.name "syaofox"
    echo "已为用户 $target_user 设置 git user.name=syaofox"
  fi

  if ! "${git_runner[@]}" config --global user.email >/dev/null 2>&1; then
    "${git_runner[@]}" config --global user.email "syaofox@gmail.com"
    echo "已为用户 $target_user 设置 git user.email=syaofox@gmail.com"
  fi
}

# 2. 确认安装并执行
echo "即将安装以下软件包和包组: ${PACKAGES[@]}"
echo "-------------------------------------"
sleep 2

# 使用 pacman -S 安装所有包
pacman -S "${PACKAGES[@]}"

# 3. 检查安装结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 所有软件包安装完成。下一步："
    configure_git_identity
    echo "1. 配置 Fcitx 5 环境变量 (参考之前的指导)。"
    echo "2. 配置 picom, rofi, xwallpaper, Qtile 等工具。"
    echo "3. 重启或重新登录以加载新的配置和微码。"
else
    echo ""
    echo "❌ 软件包安装过程中发生错误。请检查 pacman 的输出信息。"
fi