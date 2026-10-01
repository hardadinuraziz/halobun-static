import math
import os
from PIL import Image, ImageDraw

def create_sprout_animation():
    os.makedirs('images', exist_ok=True)
    width, height = 480, 480
    num_frames = 48
    frames = []

    # Parameters
    cx = width // 2
    soil_y = 390
    
    # Droplets configuration: (spawn_offset_fraction, start_x, start_y, end_x, end_y, size)
    drops_config = [
        (0.00, 150, 120, 230, 310, 8),
        (0.18, 160, 130, 210, 260, 7),
        (0.36, 170, 125, 255, 330, 9),
        (0.54, 155, 115, 235, 385, 7),
        (0.72, 165, 128, 220, 290, 8),
        (0.88, 175, 135, 248, 380, 6),
    ]

    # Sparkle particles (drifting up)
    sparkles = [
        (260, 320, -50, 20, 4),
        (210, 300, -70, -25, 5),
        (280, 260, -60, 15, 3),
        (190, 340, -45, -15, 4),
        (240, 230, -55, 10, 4),
    ]

    for f in range(num_frames):
        t = f / num_frames
        t_rad = t * 2 * math.pi
        
        # Transparent canvas RGBA
        im = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)

        # 1. Soil Mound (Rich fertile earth)
        soil_points = [
            (110, soil_y + 15),
            (160, soil_y - 12),
            (210, soil_y - 22),
            (cx, soil_y - 26),
            (270, soil_y - 23),
            (320, soil_y - 14),
            (370, soil_y + 15),
            (350, soil_y + 35),
            (240, soil_y + 42),
            (130, soil_y + 35),
        ]
        # Soil base shadow & body
        draw.polygon(soil_points, fill=(78, 52, 34, 255))
        # Soil highlight curves
        draw.arc([140, soil_y - 25, 340, soil_y + 20], start=190, end=350, fill=(115, 77, 48, 255), width=4)
        # Small pebble/organic texture
        pebbles = [
            (180, soil_y + 5, 8, 5), (290, soil_y + 8, 7, 4),
            (230, soil_y + 14, 10, 6), (325, soil_y + 10, 6, 4),
            (150, soil_y + 18, 7, 5)
        ]
        for px, py, pw, ph in pebbles:
            draw.ellipse([px, py, px + pw, py + ph], fill=(60, 40, 25, 230))

        # 2. Plant Sway Dynamics
        sway = math.sin(t_rad) * 9
        sway_secondary = math.cos(t_rad) * 4
        stem_top_x = cx + sway
        stem_top_y = 230 + abs(sway) * 0.4
        stem_mid_x = cx + sway * 0.45
        stem_mid_y = 310

        # Draw stem (thick curved green stem)
        stem_width = 8
        stem_pts = []
        for step in range(30):
            st = step / 29.0
            # quadratic bezier from (cx, soil_y - 24) to (stem_top_x, stem_top_y) via (stem_mid_x, stem_mid_y)
            bx = (1 - st)**2 * cx + 2 * (1 - st) * st * stem_mid_x + st**2 * stem_top_x
            by = (1 - st)**2 * (soil_y - 24) + 2 * (1 - st) * st * stem_mid_y + st**2 * stem_top_y
            stem_pts.append((bx, by))
        
        for k in range(len(stem_pts) - 1):
            w = int(stem_width * (1.0 - k * 0.015))
            draw.line([stem_pts[k], stem_pts[k+1]], fill=(34, 197, 94, 255), width=max(4, w))
            # subtle inner highlight
            draw.line([(stem_pts[k][0]-1, stem_pts[k][1]), (stem_pts[k+1][0]-1, stem_pts[k+1][1])], fill=(74, 222, 128, 255), width=2)

        # 3. Left Leaf (Main mature leaf)
        left_angle = -0.55 + (sway * 0.02)
        leaf_l_base = stem_pts[14]
        # Draw left leaf as polygon with curved profile
        ll_len = 70
        ll_tip_x = leaf_l_base[0] - math.cos(left_angle) * ll_len
        ll_tip_y = leaf_l_base[1] + math.sin(left_angle) * ll_len - 10
        ll_ctrl_x1 = leaf_l_base[0] - 40
        ll_ctrl_y1 = leaf_l_base[1] - 40
        ll_ctrl_x2 = leaf_l_base[0] - 35
        ll_ctrl_y2 = leaf_l_base[1] + 15
        
        leaf_l_pts = [
            leaf_l_base,
            (ll_ctrl_x1, ll_ctrl_y1),
            (ll_tip_x, ll_tip_y),
            (ll_ctrl_x2, ll_ctrl_y2),
        ]
        draw.polygon(leaf_l_pts, fill=(22, 163, 74, 255))
        # Top highlight half of leaf
        draw.polygon([leaf_l_base, (ll_ctrl_x1, ll_ctrl_y1), (ll_tip_x, ll_tip_y)], fill=(34, 197, 94, 255))
        # Leaf central vein
        draw.line([leaf_l_base, (ll_tip_x, ll_tip_y)], fill=(134, 239, 172, 255), width=2)

        # 4. Right Leaf (Slightly larger, catching water)
        right_angle = -0.45 - (sway * 0.025)
        leaf_r_base = stem_pts[18]
        lr_len = 85
        lr_tip_x = leaf_r_base[0] + math.cos(right_angle) * lr_len
        lr_tip_y = leaf_r_base[1] + math.sin(right_angle) * lr_len - 5
        lr_ctrl_x1 = leaf_r_base[0] + 45
        lr_ctrl_y1 = leaf_r_base[1] - 45
        lr_ctrl_x2 = leaf_r_base[0] + 45
        lr_ctrl_y2 = leaf_r_base[1] + 18
        
        leaf_r_pts = [
            leaf_r_base,
            (lr_ctrl_x1, lr_ctrl_y1),
            (lr_tip_x, lr_tip_y),
            (lr_ctrl_x2, lr_ctrl_y2),
        ]
        draw.polygon(leaf_r_pts, fill=(21, 128, 61, 255))
        # Top highlight half
        draw.polygon([leaf_r_base, (lr_ctrl_x1, lr_ctrl_y1), (lr_tip_x, lr_tip_y)], fill=(34, 197, 94, 255))
        # Leaf vein
        draw.line([leaf_r_base, (lr_tip_x, lr_tip_y)], fill=(134, 239, 172, 255), width=2)

        # Dewdrop on right leaf
        dew_progress = (t + 0.3) % 1.0
        dew_x = leaf_r_base[0] + 25 + dew_progress * 25
        dew_y = leaf_r_base[1] - 12 + dew_progress * 15
        draw.ellipse([dew_x - 3, dew_y - 3, dew_x + 3, dew_y + 3], fill=(186, 230, 253, 240))
        draw.point((dew_x - 1, dew_y - 1), fill=(255, 255, 255, 255))

        # 5. Top Fresh Bud / Young Leaflet
        top_base = (stem_top_x, stem_top_y)
        tb_angle = (sway * 0.04)
        top_tip_x = stem_top_x + math.sin(tb_angle) * 35
        top_tip_y = stem_top_y - 38
        draw.polygon([
            top_base,
            (stem_top_x - 12, stem_top_y - 20),
            (top_tip_x, top_tip_y),
            (stem_top_x + 10, stem_top_y - 20),
        ], fill=(74, 222, 128, 255))
        draw.line([top_base, (top_tip_x, top_tip_y)], fill=(187, 247, 208, 255), width=2)

        # 6. Watering Can (Top Left) with Gentle Floating Animation
        can_bob = math.sin(t_rad) * 4
        can_tilt = math.sin(t_rad) * 0.05
        # Can body
        cb_x = 100
        cb_y = 90 + can_bob
        # Can main container (golden yellow)
        draw.rounded_rectangle([cb_x - 45, cb_y - 25, cb_x + 25, cb_y + 30], radius=12, fill=(234, 179, 8, 255), outline=(202, 138, 4, 255), width=3)
        # Can highlight
        draw.line([cb_x - 35, cb_y - 15, cb_x + 15, cb_y - 15], fill=(253, 224, 71, 255), width=3)
        # Can Handle
        draw.arc([cb_x - 70, cb_y - 30, cb_x - 30, cb_y + 25], start=100, end=270, fill=(202, 138, 4, 255), width=6)
        draw.arc([cb_x - 70, cb_y - 30, cb_x - 30, cb_y + 25], start=100, end=270, fill=(234, 179, 8, 255), width=3)
        # Can Spout
        spout_start = (cb_x + 20, cb_y + 10)
        spout_end = (cb_x + 65, cb_y - 5)
        draw.line([spout_start, spout_end], fill=(202, 138, 4, 255), width=10)
        draw.line([spout_start, spout_end], fill=(250, 204, 21, 255), width=6)
        # Shower rose/sprinkler head
        head_x, head_y = spout_end[0] + 5, spout_end[1] + 5
        draw.ellipse([head_x - 8, head_y - 12, head_x + 12, head_y + 12], fill=(217, 119, 6, 255), outline=(250, 204, 21, 255), width=2)
        # Sprinkler holes
        draw.point((head_x, head_y - 4), fill=(254, 240, 138, 255))
        draw.point((head_x + 4, head_y), fill=(254, 240, 138, 255))
        draw.point((head_x, head_y + 4), fill=(254, 240, 138, 255))

        # 7. Animated Water Droplets
        for spawn_offset, sx, sy, ex, ey, sz in drops_config:
            drop_t = (t + spawn_offset) % 1.0
            # Drop falls from head_x, head_y down to ex, ey
            cur_x = head_x + drop_t * (ex - head_x)
            # Quadratic acceleration for natural gravity
            cur_y = head_y + (drop_t ** 1.6) * (ey - head_y)
            
            if drop_t < 0.88:
                # Droplet in flight (teardrop)
                d_len = sz * 1.5
                draw.ellipse([cur_x - sz//2, cur_y - sz, cur_x + sz//2, cur_y + sz//2], fill=(56, 189, 248, 230))
                # highlight shine
                draw.point((int(cur_x - 1), int(cur_y - 2)), fill=(255, 255, 255, 255))
            else:
                # Splash impact ripple ring!
                splash_t = (drop_t - 0.88) / 0.12
                r_w = int(splash_t * 22)
                r_h = int(splash_t * 8)
                alpha = int(255 * (1.0 - splash_t))
                if alpha > 0 and r_w > 2:
                    draw.ellipse([ex - r_w, ey - r_h, ex + r_w, ey + r_h], outline=(125, 211, 252, alpha), width=2)

        # 8. Sparkles & Sun Rays / Pollen Motes (Golden drift)
        for sp_x, sp_y, drift_y, drift_x, rad in sparkles:
            sp_t = (t + sp_x * 0.003) % 1.0
            px = sp_x + math.sin(sp_t * 2 * math.pi) * drift_x
            py = sp_y + sp_t * drift_y
            sp_alpha = int(220 * math.sin(sp_t * math.pi))
            if sp_alpha > 30:
                # 4-point star sparkle
                draw.line([(px - rad, py), (px + rad, py)], fill=(254, 240, 138, sp_alpha), width=2)
                draw.line([(px, py - rad), (px, py + rad)], fill=(254, 240, 138, sp_alpha), width=2)
                draw.point((int(px), int(py)), fill=(255, 255, 255, sp_alpha))

        # 9. Clean Transparency Conversion
        # We preserve pure transparency with index 0
        alpha = im.split()[3]
        # Quantize to adaptive 255 colors
        im_rgb = im.convert('RGB')
        im_p = im_rgb.convert('P', palette=Image.Palette.ADAPTIVE, colors=254)
        
        # Transparent mask where alpha < 64
        mask = Image.eval(alpha, lambda a: 255 if a < 64 else 0)
        im_p.paste(255, mask)
        im_p.info['transparency'] = 255
        frames.append(im_p)

    out_path = 'images/halobun_sprout_animation.gif'
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=42, # ~24 fps smooth
        loop=0,
        disposal=2
    )
    print(f"Animation saved to {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == '__main__':
    create_sprout_animation()
