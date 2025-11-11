#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
福音战士标题生成器 - Evangelion Title Card Generator
Single-file Python implementation
"""

import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math


class EvaConfig:
    """Configuration for Eva title generation"""
    
    # Color schemes
    WHITE_COLOR = (228, 224, 232)
    BLACK_COLOR = (3, 2, 1)
    ORANGE_COLOR = (255, 165, 0, 153)
    
    # Output ratios
    OUTPUT_RATIOS = {
        '4:3': 1.334,
        '16:9': 1.778,
        '3:3': 1.0,
        '5:4': 1.25,
        '3:2': 1.5,
        '1:2': 0.5,  # 824×1648 support (824/1648 = 0.5, width:height)
    }
    
    # Color plans
    COLOR_PLANS = {
        'bw': {'font': WHITE_COLOR, 'bg': BLACK_COLOR, 'shadow': ORANGE_COLOR},
        'wb': {'font': BLACK_COLOR, 'bg': WHITE_COLOR, 'shadow': (255, 165, 255, 51)},
        'br': {'font': (221, 0, 0), 'bg': (24, 0, 0), 'shadow': (255, 0, 0, 128)},
        'rw': {'font': WHITE_COLOR, 'bg': (145, 11, 11), 'shadow': (255, 120, 120, 179)},
        'by': {'font': (231, 114, 37), 'bg': (20, 2, 2), 'shadow': (231, 120, 0, 128)},
        'yb': {'font': (20, 2, 2), 'bg': (231, 114, 5), 'shadow': (231, 120, 0, 128)},
    }


class EvaTextRenderer:
    """Handles text rendering for Eva titles"""
    
    def __init__(self, config):
        self.config = config
        self.default_font_size = 240
        self.font_cache = {}
        
    def get_font(self, size):
        """Get font with caching"""
        if size not in self.font_cache:
            try:
                # Try to load system fonts or fallback to default
                font_names = [
                    'MatissePro-EB',
                    'Arial Unicode MS',
                    'Microsoft YaHei',
                    'SimHei',
                    'DejaVuSans'
                ]
                
                for font_name in font_names:
                    try:
                        self.font_cache[size] = ImageFont.truetype(font_name, size)
                        break
                    except:
                        continue
                
                if size not in self.font_cache:
                    # Fallback to default font
                    self.font_cache[size] = ImageFont.load_default()
            except Exception as e:
                print(f"Warning: Could not load font, using default: {e}")
                self.font_cache[size] = ImageFont.load_default()
        
        return self.font_cache[size]
    
    def measure_text(self, text, font_size):
        """Measure text dimensions"""
        font = self.get_font(font_size)
        dummy_img = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    
    def create_text_image(self, text, font_size, color, shadow_color=None, shadow_blur=10):
        """Create an image with text"""
        if not text:
            return Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        
        font = self.get_font(font_size)
        
        # Measure text
        dummy_img = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0] + 40
        height = bbox[3] - bbox[1] + 40
        
        # Create image with padding for shadow
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw shadow if enabled
        if shadow_color:
            shadow_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_img)
            shadow_draw.text((20, 20), text, font=font, fill=shadow_color)
            shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(shadow_blur))
            img = Image.alpha_composite(img, shadow_img)
            draw = ImageDraw.Draw(img)
        
        # Draw text
        draw.text((20, 20), text, font=font, fill=color)
        
        return img
    
    def create_vertical_text_image(self, text, font_size, color, shadow_color=None):
        """Create vertical text image"""
        if not text:
            return Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        
        chars = list(text)
        char_images = []
        max_width = 0
        
        for char in chars:
            char_img = self.create_text_image(char, font_size, color, shadow_color)
            char_images.append(char_img)
            if char_img.width > max_width:
                max_width = char_img.width
        
        # Calculate total height
        total_height = sum(img.height for img in char_images)
        
        # Create final image
        result = Image.new('RGBA', (max_width, total_height), (0, 0, 0, 0))
        
        y_offset = 0
        for char_img in char_images:
            x_offset = (max_width - char_img.width) // 2
            result.paste(char_img, (x_offset, y_offset), char_img)
            y_offset += char_img.height
        
        return result


class LayoutE1:
    """第壱話 使徒、襲来 layout"""
    
    @staticmethod
    def render(canvas, texts, renderer, colors, dimensions):
        width, height = dimensions
        padding = height // 24
        font_size = height // 2
        
        text_a = texts[0] if len(texts) > 0 else "使徒"
        text_b = texts[1] if len(texts) > 1 else "襲来"
        sub_text = texts[2] if len(texts) > 2 else ""
        
        # Create vertical text for first part
        vertical_img = renderer.create_vertical_text_image(
            text_a, font_size, colors['font'], colors['shadow']
        )
        
        # Create horizontal text for second part
        horizontal_img = renderer.create_text_image(
            text_b, font_size, colors['font'], colors['shadow']
        )
        
        # Create comma
        comma_img = renderer.create_text_image(
            '、', font_size, colors['font'], colors['shadow']
        )
        
        # Composite the title
        if sub_text:
            sub_img = renderer.create_text_image(
                sub_text, int(font_size * 0.4), colors['font'], colors['shadow']
            )
            # Paste subtitle
            sub_height = int(height * 0.19)
            sub_width = int(sub_height * sub_img.width / sub_img.height)
            sub_img = sub_img.resize((sub_width, sub_height), Image.Resampling.LANCZOS)
            canvas.paste(sub_img, (padding, padding), sub_img)
            
            # Adjust main title position
            title_top = padding + sub_height
            title_height = height - padding * 2 - sub_height
        else:
            title_height = height - padding * 2
            title_top = padding
        
        # Scale and paste vertical text
        v_height = title_height
        v_width = int(v_height * vertical_img.width / vertical_img.height)
        vertical_img = vertical_img.resize((v_width, v_height), Image.Resampling.LANCZOS)
        canvas.paste(vertical_img, (padding, title_top), vertical_img)
        
        # Paste comma
        comma_width = int(v_width * 0.3)
        comma_height = int(comma_width * comma_img.height / comma_img.width)
        comma_img = comma_img.resize((comma_width, comma_height), Image.Resampling.LANCZOS)
        canvas.paste(comma_img, (padding + v_width - 20, title_top + v_height - comma_height), comma_img)
        
        # Paste horizontal text
        h_height = int(font_size * 0.8)
        h_width = int(h_height * horizontal_img.width / horizontal_img.height)
        horizontal_img = horizontal_img.resize((h_width, h_height), Image.Resampling.LANCZOS)
        canvas.paste(horizontal_img, 
                    (int(padding + v_width * 1.3), title_top + v_height - h_height),
                    horizontal_img)


class LayoutE25:
    """第弐拾伍話 終わる世界 layout"""
    
    @staticmethod
    def render(canvas, texts, renderer, colors, dimensions):
        width, height = dimensions
        padding = height // 24
        font_size = height // 2
        
        text = texts[0] if len(texts) > 0 else "終わる世界"
        sub_text = texts[1] if len(texts) > 1 else ""
        
        # Create main text
        text_img = renderer.create_text_image(
            text, font_size, colors['font'], colors['shadow']
        )
        
        # Scale and position in center
        text_width = int(width * 0.6)
        text_height = int(height * 0.25)
        text_img = text_img.resize((text_width, text_height), Image.Resampling.LANCZOS)
        
        text_x = int(width * 0.2)
        text_y = int(height * 0.44)
        canvas.paste(text_img, (text_x, text_y), text_img)
        
        # Add subtitle if present
        if sub_text:
            sub_img = renderer.create_text_image(
                sub_text, int(font_size * 0.4), colors['font'], colors['shadow']
            )
            sub_height = int(height * 0.12)
            sub_width = int(sub_height * sub_img.width / sub_img.height * 0.8)
            sub_img = sub_img.resize((sub_width, sub_height), Image.Resampling.LANCZOS)
            
            sub_x = (width - sub_width) // 2
            sub_y = int(height * 0.26)
            canvas.paste(sub_img, (sub_x, sub_y), sub_img)


class LayoutAir:
    """Air layout"""
    
    @staticmethod
    def render(canvas, texts, renderer, colors, dimensions):
        width, height = dimensions
        padding = height // 24
        font_size = height // 2
        
        text = texts[0] if len(texts) > 0 else "air"
        
        # Create text
        text_img = renderer.create_text_image(
            text, font_size, colors['font'], colors['shadow']
        )
        
        # Scale text
        text_height = int(height * 0.2)
        text_width = min(int(text_height * text_img.width / text_img.height), int(width * 0.8))
        text_img = text_img.resize((text_width, text_height), Image.Resampling.LANCZOS)
        
        # Center text
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        canvas.paste(text_img, (text_x, text_y), text_img)
        
        # Draw border
        draw = ImageDraw.Draw(canvas)
        border_width = padding // 2
        rect_width = text_width + padding * 2
        rect_height = text_height + padding
        rect_x = (width - rect_width) // 2
        rect_y = (height - rect_height) // 2
        
        draw.rectangle(
            [(rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height)],
            outline=colors['font'],
            width=border_width
        )


class EvaLayoutManager:
    """Manages different layout templates"""
    
    LAYOUTS = {
        'e1': {'name': '第壱話 使徒、襲来', 'renderer': LayoutE1},
        'e25': {'name': '第弐拾伍話 終わる世界', 'renderer': LayoutE25},
        'air': {'name': 'air', 'renderer': LayoutAir},
    }
    
    @staticmethod
    def get_layout(layout_id):
        """Get layout renderer by ID"""
        return EvaLayoutManager.LAYOUTS.get(layout_id, EvaLayoutManager.LAYOUTS['e1'])


class EvaTitleGenerator:
    """Main generator class"""
    
    def __init__(self, width=640, height=480, layout='e1', plan='bw', 
                 blur=False, noise=False, sharpen=False, output_ratio='4:3'):
        
        self.config = EvaConfig()
        
        # Calculate dimensions based on output ratio
        # ratio_value is width/height
        ratio_value = self.config.OUTPUT_RATIOS.get(output_ratio, 1.334)
        if ratio_value >= 1:
            # Landscape or square: height is base, calculate width
            self.height = height
            self.width = int(height * ratio_value)
        else:
            # Portrait: width is base, calculate height
            self.width = width
            self.height = int(width / ratio_value)
        
        self.layout_id = layout
        self.color_plan = plan
        self.blur = blur
        self.noise = noise
        self.sharpen = sharpen
        
        self.renderer = EvaTextRenderer(self.config)
        
    def apply_effects(self, image):
        """Apply post-processing effects"""
        
        # Blur effect
        if self.blur:
            image = image.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Sharpen effect
        if self.sharpen:
            image = image.filter(ImageFilter.SHARPEN)
        
        # Noise effect
        if self.noise:
            pixels = image.load()
            width, height = image.size
            for y in range(height):
                for x in range(width):
                    if random.random() < 0.1:
                        r, g, b, a = pixels[x, y]
                        noise = random.randint(-20, 20)
                        r = max(0, min(255, r + noise))
                        g = max(0, min(255, g + noise))
                        b = max(0, min(255, b + noise))
                        pixels[x, y] = (r, g, b, a)
        
        return image
    
    def generate(self, texts):
        """Generate title card with given texts"""
        
        # Get colors
        colors = self.config.COLOR_PLANS.get(self.color_plan, self.config.COLOR_PLANS['bw'])
        
        # Create base canvas
        canvas = Image.new('RGBA', (self.width, self.height), colors['bg'])
        
        # Get layout renderer
        layout = EvaLayoutManager.get_layout(self.layout_id)
        
        # Render layout
        layout['renderer'].render(
            canvas, texts, self.renderer, colors, (self.width, self.height)
        )
        
        # Apply effects
        canvas = self.apply_effects(canvas)
        
        # Convert to RGB for saving
        if canvas.mode == 'RGBA':
            background = Image.new('RGB', canvas.size, colors['bg'][:3])
            background.paste(canvas, mask=canvas.split()[3])
            canvas = background
        
        return canvas


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description='福音战士标题生成器 - Evangelion Title Card Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t "使徒" "襲来" "第壱話" -o output.png
  %(prog)s -t "終わる世界" "第弐拾伍話" -l e25 -o output.png
  %(prog)s -t "air" -l air -r 1:2 -s 824 -o output.png
  %(prog)s -t "Hello" "World" -p wb --blur --noise -o output.png

Available layouts: e1, e25, air
Available color plans: bw (black/white), wb (white/black), br (black/red), rw (red/white), by (black/yellow), yb (yellow/black)
Available output ratios: 4:3, 16:9, 3:3, 5:4, 3:2, 1:2 (824×1648)
        """
    )
    
    parser.add_argument('-t', '--texts', nargs='+', required=True,
                       help='Text strings for the title (multiple strings supported)')
    parser.add_argument('-o', '--output', default='eva_title.png',
                       help='Output file path (default: eva_title.png)')
    parser.add_argument('-l', '--layout', default='e1',
                       choices=['e1', 'e25', 'air'],
                       help='Layout template (default: e1)')
    parser.add_argument('-p', '--plan', default='bw',
                       choices=['bw', 'wb', 'br', 'rw', 'by', 'yb'],
                       help='Color plan (default: bw)')
    parser.add_argument('-r', '--ratio', default='4:3',
                       choices=['4:3', '16:9', '3:3', '5:4', '3:2', '1:2'],
                       help='Output aspect ratio (default: 4:3, 1:2 for 824×1648)')
    parser.add_argument('-s', '--size', type=int, default=480,
                       help='Base size in pixels (width for 1:2 portrait ratio, height for others)')
    parser.add_argument('--blur', action='store_true',
                       help='Apply blur effect')
    parser.add_argument('--noise', action='store_true',
                       help='Apply noise effect')
    parser.add_argument('--sharpen', action='store_true',
                       help='Apply sharpen effect')
    
    args = parser.parse_args()
    
    # Create generator
    # For portrait ratio (1:2), use width parameter; for others use height
    if args.ratio == '1:2':
        generator = EvaTitleGenerator(
            width=args.size,
            layout=args.layout,
            plan=args.plan,
            blur=args.blur,
            noise=args.noise,
            sharpen=args.sharpen,
            output_ratio=args.ratio
        )
    else:
        generator = EvaTitleGenerator(
            height=args.size,
            layout=args.layout,
            plan=args.plan,
            blur=args.blur,
            noise=args.noise,
            sharpen=args.sharpen,
            output_ratio=args.ratio
        )
    
    # Generate image
    print(f"Generating Eva title card...")
    print(f"  Texts: {args.texts}")
    print(f"  Layout: {args.layout}")
    print(f"  Color plan: {args.plan}")
    print(f"  Output ratio: {args.ratio}")
    print(f"  Size: {generator.width}×{generator.height}")
    print(f"  Effects: blur={args.blur}, noise={args.noise}, sharpen={args.sharpen}")
    
    image = generator.generate(args.texts)
    
    # Save image
    image.save(args.output, 'PNG')
    print(f"\n✓ Title card saved to: {args.output}")


if __name__ == '__main__':
    main()
