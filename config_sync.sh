#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
config_root="${script_dir}/config"

timestamp="$(date +"%Y%m%d-%H%M%S")"

log() {
  printf '[INFO] %s\n' "$*"
}

warn() {
  printf '[WARN] %s\n' "$*" >&2
}

ensure_dir() {
  local dir="$1"
  if [ ! -d "$dir" ]; then
    log "创建目录：$dir"
    mkdir -p "$dir"
  fi
}

backup_existing() {
  local target="$1"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    local backup="${target}.bak-${timestamp}"
    log "检测到现有文件/目录，移动到备份：$backup"
    mv "$target" "$backup"
  elif [ -L "$target" ]; then
    log "移除已有软链接：$target"
    rm -f "$target"
  fi
}

copy_rofi_power_menu() {
  local source_file="${config_root}/rofi/rofi-power-menu"
  local target_dir="${HOME}/.local/bin"
  local target_file="${target_dir}/rofi-power-menu"

  if [ ! -f "$source_file" ]; then
    warn "找不到源文件：$source_file"
    return 1
  fi

  ensure_dir "$target_dir"
  backup_existing "$target_file"

  log "复制 ${source_file} -> ${target_file}"
  install -m 0755 "$source_file" "$target_file"
}

link_config_dir() {
  local name="$1"
  local source_path="${config_root}/${name}"
  local target_path="${HOME}/.config/${name}"

  if [ ! -e "$source_path" ]; then
    warn "源路径不存在：$source_path，跳过"
    return
  fi

  ensure_dir "$(dirname "$target_path")"
  backup_existing "$target_path"

  log "创建软链接 ${target_path} -> ${source_path}"
  ln -s "$source_path" "$target_path"
}

main() {
  copy_rofi_power_menu

  local entries=(
    "alacritty"
    "fcitx5"
    "nvim"
    "picom"
    "qtile"
    "rofi"
    "walls"
  )

  for entry in "${entries[@]}"; do
    link_config_dir "$entry"
  done

  log "全部操作完成。"
}

main "$@"

