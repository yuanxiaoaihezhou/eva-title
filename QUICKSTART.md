# 快速开始指南

## 一键安装和使用

```bash
# 1. 安装依赖
pip install Pillow

# 2. 生成824×1648竖版图片（最常用）
python3 eva_title_generator.py -t "air" -l air -r 1:2 -s 824 -o output.png
```

## 常用命令速查

```bash
# 基础用法
python3 eva_title_generator.py -t "你的文字" -o output.png

# 824×1648竖版（重点）
python3 eva_title_generator.py -t "你的文字" -r 1:2 -s 824 -o output.png

# E1布局（使徒、襲来风格）
python3 eva_title_generator.py -t "使徒" "襲来" "第壱話" -l e1 -r 1:2 -s 824 -o output.png

# E25布局（終わる世界风格）
python3 eva_title_generator.py -t "終わる世界" "第弐拾伍話" -l e25 -r 1:2 -s 824 -o output.png

# Air布局（带边框）
python3 eva_title_generator.py -t "air" -l air -r 1:2 -s 824 -o output.png

# 白底黑字
python3 eva_title_generator.py -t "文字" -p wb -r 1:2 -s 824 -o output.png

# 带效果
python3 eva_title_generator.py -t "文字" -r 1:2 -s 824 --blur --noise -o output.png
```

## 参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `-t` | 文字内容（必需） | `-t "使徒" "襲来"` |
| `-o` | 输出文件 | `-o output.png` |
| `-l` | 布局 (e1/e25/air) | `-l e25` |
| `-p` | 配色 (bw/wb/br/rw/by/yb) | `-p wb` |
| `-r` | 比例 (**1:2**为824×1648) | `-r 1:2` |
| `-s` | 尺寸（1:2时为宽度） | `-s 824` |
| `--blur` | 模糊效果 | `--blur` |
| `--noise` | 噪点效果 | `--noise` |
| `--sharpen` | 锐化效果 | `--sharpen` |

## 查看完整帮助

```bash
python3 eva_title_generator.py --help
```

## 更多文档

- **README_PYTHON.md** - 完整文档
- **USAGE_EXAMPLES.md** - 详细示例
- **PROJECT_SUMMARY.md** - 项目总结
