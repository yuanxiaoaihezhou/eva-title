# 福音战士标题生成器 Python版本

Python单文件版本的福音战士标题生成器，支持生成EVA风格的标题图片。

## 功能特性

- ✅ 单文件Python程序，易于使用
- ✅ 支持多种布局模板（e1, e25, air等）
- ✅ 支持多种配色方案（黑底白字、白底黑字、黑底红字等）
- ✅ 支持多种输出比例：4:3, 16:9, 3:3, 5:4, 3:2, **1:2 (824×1648)**
- ✅ 支持图像效果：模糊、噪点、锐化
- ✅ 命令行界面，易于集成到其他工具

## 安装依赖

```bash
pip install -r requirements.txt
```

或者直接安装Pillow：

```bash
pip install Pillow
```

## 使用方法

### 基本用法

```bash
# 生成默认的标题卡
python3 eva_title_generator.py -t "使徒" "襲来" "第壱話" -o output.png

# 使用e25布局
python3 eva_title_generator.py -t "終わる世界" "第弐拾伍話" -l e25 -o output.png

# 生成air风格，使用1:2比例（824×1648尺寸）
python3 eva_title_generator.py -t "air" -l air -r 1:2 -s 824 -o output.png

# 使用白底黑字配色，添加模糊和噪点效果
python3 eva_title_generator.py -t "Hello" "World" -p wb --blur --noise -o output.png
```

### 参数说明

```
-t, --texts          文字内容（可以多个，用空格分隔）
-o, --output         输出文件路径（默认：eva_title.png）
-l, --layout         布局模板（可选：e1, e25, air，默认：e1）
-p, --plan           配色方案（可选：bw, wb, br, rw, by, yb，默认：bw）
-r, --ratio          输出比例（可选：4:3, 16:9, 3:3, 5:4, 3:2, 1:2，默认：4:3）
-s, --size           基准尺寸（像素，默认：480；1:2竖版时指定宽度，其他时指定高度）
--blur               启用模糊效果
--noise              启用噪点效果
--sharpen            启用锐化效果
```

### 布局模板 (Layout)

- **e1**: 第壱話风格（使徒、襲来）- 垂直+水平组合
- **e25**: 第弐拾伍話风格（終わる世界）- 居中大字
- **air**: Air风格 - 带边框

### 配色方案 (Color Plan)

- **bw**: 黑底白字（默认）
- **wb**: 白底黑字
- **br**: 黑底红字
- **rw**: 红底白字
- **by**: 黑底黄字
- **yb**: 黄底黑字

### 输出比例 (Aspect Ratio)

- **4:3**: 标准4:3比例（640×480等）
- **16:9**: 宽屏16:9比例（853×480等）
- **3:3**: 正方形1:1比例（480×480等）
- **5:4**: 5:4比例（600×480等）
- **3:2**: 3:2比例（720×480等）
- **1:2**: 1:2比例（**824×1648，竖版长图**）

### 824×1648尺寸说明

要生成824×1648尺寸的图片（宽824，高1648，1:2竖版比例），使用以下参数：

```bash
python3 eva_title_generator.py -t "你的文字" -r 1:2 -s 824 -o output.png
```

这将生成宽度为824像素、高度为1648像素的竖版图片。

## 示例

### 生成经典EVA标题

```bash
# 第壱話 使徒、襲来
python3 eva_title_generator.py -t "使徒" "襲来" "第壱話" -o eva_e1.png

# 第弐拾伍話 終わる世界
python3 eva_title_generator.py -t "終わる世界" "第弐拾伍話" -l e25 -o eva_e25.png

# Air标题，1:2比例（824×1648）
python3 eva_title_generator.py -t "air" -l air -r 1:2 -s 824 -o eva_air_1x2.png
```

### 使用特殊效果

```bash
# 带模糊和噪点效果
python3 eva_title_generator.py -t "測試" "文字" --blur --noise -o test_effects.png

# 白底黑字配色 + 锐化
python3 eva_title_generator.py -t "白黑" "標題" -p wb --sharpen -o test_wb.png
```

### 不同比例示例

```bash
# 16:9宽屏
python3 eva_title_generator.py -t "宽屏" "标题" -r 16:9 -o test_16x9.png

# 正方形
python3 eva_title_generator.py -t "正方形" -r 3:3 -o test_square.png

# 1:2比例（824×1648竖版）
python3 eva_title_generator.py -t "长条形" -r 1:2 -s 824 -o test_1x2.png
```

## 查看帮助

```bash
python3 eva_title_generator.py --help
```

## 注意事项

1. **字体**: 程序会尝试使用系统中的字体（MatissePro-EB, Arial Unicode MS, Microsoft YaHei等），如果没有找到合适的字体，会使用默认字体。建议安装Matisse-EB字体以获得最佳效果。

2. **中文支持**: 确保系统安装了支持中文的字体。

3. **输出格式**: 当前仅支持PNG格式输出。

4. **尺寸计算**: 
   - 对于横版或正方形比例（≥1，如4:3, 16:9），`-s`参数指定高度，宽度自动计算
   - 对于竖版比例（<1，如1:2），`-s`参数指定宽度，高度自动计算
   - 例如：`-r 1:2 -s 824` 将生成 824×1648 的图片

## 与Web版本的区别

Python版本是原Web版本的简化实现：

- ✅ 保留了核心布局和配色功能
- ✅ 新增了1:2比例支持（满足824×1648需求，宽824×高1648）
- ✅ 单文件实现，无需浏览器
- ⚠️ 仅实现了主要的3个布局模板（e1, e25, air）
- ⚠️ 字体效果可能与Web版本略有不同（取决于系统字体）
- ⚠️ 不支持字体在线加载

## 开发

本程序是单文件Python实现，所有代码都在 `eva_title_generator.py` 中，便于修改和扩展。

主要类结构：
- `EvaConfig`: 配置管理
- `EvaTextRenderer`: 文字渲染
- `LayoutE1`, `LayoutE25`, `LayoutAir`: 布局渲染器
- `EvaLayoutManager`: 布局管理器
- `EvaTitleGenerator`: 主生成器

## 许可证

本项目基于原Web版本的eva-title项目，字体授权请参考原项目说明。

---

原项目: https://github.com/itorr/eva-title
