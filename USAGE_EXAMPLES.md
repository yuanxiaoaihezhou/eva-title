# 福音战士标题生成器 - 使用示例

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 基本使用

#### 生成默认标题（e1布局，黑底白字）
```bash
python3 eva_title_generator.py -t "使徒" "襲来" "第壱話" -o output.png
```

#### 生成824×1648竖版图片（重要！）
```bash
python3 eva_title_generator.py -t "air" -l air -r 1:2 -s 824 -o output_824x1648.png
```

生成的图片尺寸为：**宽824像素 × 高1648像素**

## 详细示例

### 不同布局

#### E1布局（第壱話风格）
```bash
# 标准4:3比例
python3 eva_title_generator.py -t "使徒" "襲来" "第壱話" -l e1 -o e1_standard.png

# 824×1648竖版
python3 eva_title_generator.py -t "使徒" "襲来" "第壱話" -l e1 -r 1:2 -s 824 -o e1_portrait.png
```

#### E25布局（第弐拾伍話风格）
```bash
# 标准4:3比例
python3 eva_title_generator.py -t "終わる世界" "第弐拾伍話" -l e25 -o e25_standard.png

# 824×1648竖版
python3 eva_title_generator.py -t "終わる世界" "第弐拾伍話" -l e25 -r 1:2 -s 824 -o e25_portrait.png
```

#### Air布局
```bash
# 标准4:3比例
python3 eva_title_generator.py -t "air" -l air -o air_standard.png

# 824×1648竖版
python3 eva_title_generator.py -t "air" -l air -r 1:2 -s 824 -o air_portrait.png
```

### 不同配色方案

```bash
# 黑底白字（默认）
python3 eva_title_generator.py -t "黑底" "白字" -p bw -r 1:2 -s 824 -o color_bw.png

# 白底黑字
python3 eva_title_generator.py -t "白底" "黑字" -p wb -r 1:2 -s 824 -o color_wb.png

# 黑底红字
python3 eva_title_generator.py -t "黑底" "红字" -p br -r 1:2 -s 824 -o color_br.png

# 红底白字
python3 eva_title_generator.py -t "红底" "白字" -p rw -r 1:2 -s 824 -o color_rw.png

# 黑底黄字
python3 eva_title_generator.py -t "黑底" "黄字" -p by -r 1:2 -s 824 -o color_by.png

# 黄底黑字
python3 eva_title_generator.py -t "黄底" "黑字" -p yb -r 1:2 -s 824 -o color_yb.png
```

### 不同比例

```bash
# 4:3 标准比例
python3 eva_title_generator.py -t "测试" -r 4:3 -s 480 -o ratio_4_3.png

# 16:9 宽屏
python3 eva_title_generator.py -t "测试" -r 16:9 -s 480 -o ratio_16_9.png

# 3:3 正方形
python3 eva_title_generator.py -t "测试" -r 3:3 -s 480 -o ratio_3_3.png

# 1:2 竖版（824×1648）
python3 eva_title_generator.py -t "测试" -r 1:2 -s 824 -o ratio_1_2.png
```

### 添加效果

```bash
# 添加模糊效果
python3 eva_title_generator.py -t "模糊" "效果" -r 1:2 -s 824 --blur -o effect_blur.png

# 添加噪点效果
python3 eva_title_generator.py -t "噪点" "效果" -r 1:2 -s 824 --noise -o effect_noise.png

# 添加锐化效果
python3 eva_title_generator.py -t "锐化" "效果" -r 1:2 -s 824 --sharpen -o effect_sharpen.png

# 组合多个效果
python3 eva_title_generator.py -t "多重" "效果" -r 1:2 -s 824 --blur --noise -o effect_combined.png
```

### 实用组合示例

#### 经典EVA风格（824×1648）
```bash
python3 eva_title_generator.py -t "使徒" "襲来" "第壱話" -l e1 -p bw -r 1:2 -s 824 --noise -o classic_eva.png
```

#### 现代清晰风格
```bash
python3 eva_title_generator.py -t "現代" "風格" -l e25 -p wb -r 1:2 -s 824 --sharpen -o modern_clean.png
```

#### 复古效果
```bash
python3 eva_title_generator.py -t "復古" "效果" -l air -p br -r 1:2 -s 824 --blur --noise -o retro_style.png
```

## 批量生成脚本示例

创建一个shell脚本来批量生成多个标题：

```bash
#!/bin/bash
# batch_generate.sh

# 生成一系列EVA标题
python3 eva_title_generator.py -t "使徒" "襲来" "第壱話" -r 1:2 -s 824 -o ep01.png
python3 eva_title_generator.py -t "見知らぬ、天井" "第弐話" -r 1:2 -s 824 -o ep02.png
python3 eva_title_generator.py -t "鳴らない、電話" "第参話" -r 1:2 -s 824 -o ep03.png
python3 eva_title_generator.py -t "雨、逃げ出した後" "第四話" -r 1:2 -s 824 -o ep04.png

echo "批量生成完成！"
```

## 常见问题

### Q: 如何确认生成的图片是824×1648？
A: 使用以下命令检查：
```bash
python3 -c "from PIL import Image; img = Image.open('output.png'); print(f'尺寸: {img.size[0]}×{img.size[1]}')"
```

### Q: 字体显示不正确怎么办？
A: 
1. 安装Matisse-EB字体以获得最佳效果
2. 或安装其他中文字体（Arial Unicode MS, Microsoft YaHei等）
3. 程序会自动尝试多个字体并回退到默认字体

### Q: 如何修改默认字体？
A: 编辑`eva_title_generator.py`文件中的`font_names`列表，添加你的字体名称

### Q: 可以生成其他尺寸吗？
A: 可以！使用`-s`参数指定基准尺寸：
- 对于1:2比例：`-r 1:2 -s 400` 生成400×800
- 对于1:2比例：`-r 1:2 -s 1000` 生成1000×2000
- 对于4:3比例：`-r 4:3 -s 600` 生成800×600

## 查看完整帮助

```bash
python3 eva_title_generator.py --help
```
