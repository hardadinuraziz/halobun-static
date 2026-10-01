import math
import os
import random
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

def make_cinemagraph(input_path, output_path, width=720, height=405, num_frames=36, fps=15):
    print(f"Loading {input_path}...")
    base_img = Image.open(input_path).convert('RGB')
    orig_w, orig_h = base_img.size

    # Crop to 16:9 ratio if needed
    target_ratio = width / height
    current_ratio = orig_w / orig_h
    if current_ratio > target_ratio:
        new_w = int(orig_h * target_ratio)
        offset = (orig_w - new_w) // 2
        base_img = base_img.crop((offset, 0, offset + new_w, orig_h))
    else:
        new_h = int(orig_w / target_ratio)
        offset = (orig_h - new_h) // 2
        base_img = base_img.crop((0, offset, orig_w, offset + new_h))

    # Base scale to slightly larger than target for ken-burns panning
    scale_factor = 1.08
    large_w = int(width * scale_factor)
    large_h = int(height * scale_factor)
    base_img = base_img.resize((large_w, large_h), Image.Resampling.LANCZOS)

    # Pre-generate floating particles / leaves
    random.seed(42)
    leaves = []
    for _ in range(14):
        leaves.append({
            'x_start': random.uniform(-50, width + 50),
            'y_start': random.uniform(-30, height - 50),
            'speed_x': random.uniform(25, 60),
            'speed_y': random.uniform(15, 45),
            'size': random.uniform(6, 14),
            'color': random.choice([(34, 197, 94), (74, 222, 128), (234, 179, 8), (250, 204, 21)]),
            'phase': random.uniform(0, 2 * math.pi)
        })

    frames = []
    max_pan_x = large_w - width
    max_pan_y = large_h - height

    for f in range(num_frames):
        t = f / num_frames
        rad = t * 2 * math.pi

        # 1. Subtle smooth camera drift (breathing zoom & pan)
        # Using sine and cosine to ensure seamless loop
        pan_x = int((math.sin(rad) * 0.5 + 0.5) * max_pan_x)
        pan_y = int((math.cos(rad) * 0.5 + 0.5) * max_pan_y)
        
        frame = base_img.crop((pan_x, pan_y, pan_x + width, pan_y + height)).copy()

        # 2. Dynamic sunlight rays shimmer & mist
        # We create an atmospheric lighting overlay
        sun_shimmer = math.sin(rad) * 0.08 + 1.0 # 0.92 to 1.08
        if sun_shimmer != 1.0:
            enhancer = ImageEnhance.Brightness(frame)
            frame = enhancer.enhance(sun_shimmer)

        # 3. Soft golden sunbeam ray overlay from top right (sunrise)
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # Sunbeam polygon from top right corner
        ray_intensity = int(35 + 20 * math.sin(rad))
        sun_x, sun_y = width * 0.85, 40
        # Draw 3 subtle radiant rays
        rays = [
            (width * 0.45, height, width * 0.65, height),
            (width * 0.2, height, width * 0.4, height),
            (0, height * 0.6, 0, height * 0.9),
        ]
        for rx1, ry1, rx2, ry2 in rays:
            draw_ov.polygon([(sun_x, sun_y), (rx1, ry1), (rx2, ry2)], fill=(254, 240, 138, ray_intensity // 2))

        # 4. Animated drifting mist / fog layer across valley
        mist_offset_x = (math.sin(rad) * 30)
        mist_y = int(height * 0.35 + math.cos(rad) * 6)
        draw_ov.ellipse([
            -50 + mist_offset_x, mist_y - 25,
            width * 0.75 + mist_offset_x, mist_y + 35
        ], fill=(255, 255, 255, int(18 + 10 * math.sin(rad))))

        # 5. Floating leaves & golden pollen motes
        for lf in leaves:
            # Wrap around positions
            cur_x = (lf['x_start'] + t * lf['speed_x']) % (width + 60) - 30
            cur_y = (lf['y_start'] + t * lf['speed_y'] + math.sin(rad + lf['phase']) * 15) % (height + 40) - 20
            
            # Leaf flutter rotation
            sz = lf['size']
            rot = (t * 360 + lf['phase'] * 50) % 360
            angle_rad = math.radians(rot)
            
            # Draw rotated leaf polygon
            dx = math.cos(angle_rad) * sz
            dy = math.sin(angle_rad) * (sz * 0.5)
            draw_ov.ellipse([cur_x - abs(dx), cur_y - abs(dy), cur_x + abs(dx), cur_y + abs(dy)],
                            fill=(*lf['color'], 180))
            # Leaf shine
            draw_ov.point((int(cur_x), int(cur_y)), fill=(255, 255, 255, 220))

        # Composite overlay
        frame.paste(overlay, (0, 0), overlay)

        # Convert to P mode with adaptive palette for crisp small GIF
        frame_p = frame.convert('P', palette=Image.Palette.ADAPTIVE, colors=192)
        frames.append(frame_p)

    duration_ms = int(1000 / fps)
    print(f"Saving animated GIF to {output_path} ({num_frames} frames)...")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=True
    )
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Done! {output_path} is {file_size_mb:.2f} MB")

if __name__ == '__main__':
    # 1. Panoramic Landscape
    make_cinemagraph(
        'images/nature_landscape_bg.jpg',
        'images/nature_landscape_animated.gif',
        width=720, height=405, num_frames=30, fps=12
    )
    # 2. Greenhouse Foliage
    make_cinemagraph(
        'images/greenhouse_foliage_bg.jpg',
        'images/greenhouse_foliage_animated.gif',
        width=720, height=405, num_frames=30, fps=12
    )
