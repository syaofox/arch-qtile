
需要的包
intel-ucode 
base-devel ripgrep nodejs git  

bash-completion nfs-utils 
htop timeshift firefox 

picom
xclip
xwallpaper
maim
rofi

ttf-jetbrains-mono-nerd wqy-microhei noto-fonts-emoji 

gnome-keyring seahorse
xviewer xviewer-plugins
mpv
nemo-share nemo-fileroller nemo-media-columns

fcitx5 fcitx5-configtool fcitx5-gtk fcitx5-qt











步骤一：安装 Nemo 和 udisks2

首先，请确保您已经安装了 Nemo 和 udisks2。
Bash

# 1. 安装 Nemo 文件管理器（如果您尚未安装）
sudo pacman -S nemo

# 2. 安装 udisks2（磁盘管理服务）
sudo pacman -S udisks2

步骤二：安装必要的依赖包

为了让 udisks2 能够正确地处理挂载操作，并允许非 root 用户（即您自己）进行挂载，您通常还需要安装以下包：
Bash

# 3. 安装用于处理权限和 PolicyKit 认证的包
sudo pacman -S polkit

    PolicyKit (现在通常称为 polkit): 这是 Linux 系统中用于授权非特权用户执行特权操作（例如挂载磁盘）的框架。udisks2 会使用它来验证您的权限。

步骤三：启动和启用相关服务

udisks2 服务默认通常会在您安装它之后自动启动和启用，但为了确保万无一失，您可以检查并确认：
Bash

# 4. 检查 udisks2 服务的状态（可选）
systemctl status udisks2

# 5. 如果服务未运行，请启动它（通常不需要手动执行）
# sudo systemctl start udisks2

# 6. 如果服务未启用（即系统启动时不自动运行），请启用它（通常不需要手动执行）
# sudo systemctl enable udisks2

步骤四：将用户添加到存储组 (Storage Group)

虽然现代的 udisks2/PolicyKit 配置通常不需要这样做，但作为额外的保险措施，您可以确保您的用户属于 storage 组。
Bash

# 7. 将您的用户名添加到 storage 组
# 请将 <您的用户名> 替换为您实际的用户名
sudo gpasswd -a <您的用户名> storage


