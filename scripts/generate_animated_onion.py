import math
import os
from PIL import Image, ImageDraw

def create_onion_animation():
    os.makedirs('images', exist_ok=True)
    width, height = 480, 480
    num_frames = 48
    frames = []

    cx = width // 2
    soil_y = 390
    bulb_y = soil_y - 45

    # Water droplet trajectories
    drops_config = [
        (0.00, 140, 115, 230, 310, 8),
        (0.18, 150, 125, 205, 270, 7),
        (0.36, 160, 120, 260, 335, 9),
        (0.54, 145, 110, 240, 380, 7),
        (0.72, 155, 122, 220, 300, 8),
        (0.88, 165, 130, 250, 375, 6),
    ]

    # Sparkling sunlight motes
    sparkles = [
        (265, 315, -50, 20, 4),
        (205, 290, -70, -25, 5),
        (285, 250, -60, 15, 4),
        (185, 335, -45, -15, 4),
        (245, 210, -55, 10, 4),
        (300, 160, -40, 18, 3),
    ]

    for f in range(num_frames):
        t = f / num_frames
        t_rad = t * 2 * math.pi
        
        # Transparent canvas RGBA
        im = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)

        # 1. Soil Mound (Rich organic volcanic earth)
        soil_points = [
            (100, soil_y + 15),
            (150, soil_y - 10),
            (200, soil_y - 20),
            (cx, soil_y - 24),
            (280, soil_y - 20),
            (330, soil_y - 10),
            (380, soil_y + 15),
            (360, soil_y + 36),
            (240, soil_y + 44),
            (120, soil_y + 36),
        ]
        draw.polygon(soil_points, fill=(62, 39, 35, 255))
        draw.arc([130, soil_y - 24, 350, soil_y + 22], start=190, end=350, fill=(93, 64, 55, 255), width=4)

        # Root hairs spreading into soil
        roots = [
            [(cx - 20, bulb_y + 35), (cx - 45, soil_y + 10), (cx - 65, soil_y + 28)],
            [(cx - 10, bulb_y + 38), (cx - 20, soil_y + 18), (cx - 25, soil_y + 38)],
            [(cx, bulb_y + 40), (cx + 2, soil_y + 22), (cx + 5, soil_y + 42)],
            [(cx + 12, bulb_y + 38), (cx + 25, soil_y + 18), (cx + 38, soil_y + 38)],
            [(cx + 22, bulb_y + 35), (cx + 50, soil_y + 12), (cx + 70, soil_y + 26)],
        ]
        for r_pts in roots:
            draw.line([r_pts[0], r_pts[1]], fill=(226, 232, 240, 180), width=2)
            draw.line([r_pts[1], r_pts[2]], fill=(203, 213, 225, 140), width=1)

        # Soil pebbles
        pebbles = [
            (160, soil_y + 6, 8, 5), (300, soil_y + 9, 7, 4),
            (225, soil_y + 15, 10, 6), (335, soil_y + 12, 6, 4),
            (140, soil_y + 19, 7, 5)
        ]
        for px, py, pw, ph in pebbles:
            draw.ellipse([px, py, px + pw, py + ph], fill=(46, 27, 22, 240))

        # 2. Shallot Bulb Clusters (Umbi Bawang Merah - Rich Crimson Red & Purple)
        bulb_breath = math.sin(t_rad) * 1.5
        
        # Left cluster bulb (clove)
        l_bx, l_by = cx - 22, bulb_y + 5
        draw.ellipse([l_bx - 20, l_by - 22, l_bx + 20, l_by + 28], fill=(159, 18, 57, 255))
        draw.ellipse([l_bx - 16, l_by - 18, l_bx + 16, l_by + 24], fill=(190, 24, 93, 255))
        # Longitudinal striations (garis bawang)
        draw.arc([l_bx - 18, l_by - 20, l_bx + 18, l_by + 26], start=210, end=330, fill=(244, 63, 94, 200), width=2)
        draw.arc([l_bx - 10, l_by - 20, l_bx + 10, l_by + 26], start=210, end=330, fill=(251, 113, 133, 160), width=2)

        # Right cluster bulb (clove)
        r_bx, r_by = cx + 24, bulb_y + 6
        draw.ellipse([r_bx - 19, r_by - 20, r_bx + 19, r_by + 27], fill=(136, 19, 55, 255))
        draw.ellipse([r_bx - 15, r_by - 17, r_bx + 15, r_by + 23], fill=(159, 18, 57, 255))
        draw.arc([r_bx - 16, r_by - 18, r_bx + 16, r_by + 25], start=210, end=330, fill=(244, 63, 94, 200), width=2)

        # Central Main Shallot Bulb
        m_bw = 28 + int(bulb_breath)
        m_bh = 38 + int(bulb_breath)
        draw.ellipse([cx - m_bw, bulb_y - 20, cx + m_bw, bulb_y + m_bh], fill=(112, 26, 117, 255))
        draw.ellipse([cx - m_bw + 2, bulb_y - 18, cx + m_bw - 2, bulb_y + m_bh - 2], fill=(159, 18, 57, 255))
        draw.ellipse([cx - m_bw + 5, bulb_y - 15, cx + m_bw - 5, bulb_y + m_bh - 5], fill=(190, 24, 93, 255))
        # Characteristic white-pink longitudinal veins of shallot
        draw.arc([cx - m_bw + 7, bulb_y - 16, cx + m_bw - 7, bulb_y + m_bh - 4], start=200, end=340, fill=(253, 164, 175, 230), width=2)
        draw.arc([cx - m_bw + 14, bulb_y - 16, cx + m_bw - 14, bulb_y + m_bh - 4], start=200, end=340, fill=(254, 205, 211, 240), width=2)
        draw.arc([cx - 4, bulb_y - 16, cx + 4, bulb_y + m_bh - 4], start=200, end=340, fill=(255, 228, 230, 255), width=2)
        # Glossy sheen
        draw.ellipse([cx - 10, bulb_y - 2, cx - 2, bulb_y + 14], fill=(255, 255, 255, 110))

        # Green Neck collar transitioning to foliage shoots
        draw.ellipse([cx - 9, bulb_y - 24, cx + 9, bulb_y - 14], fill=(132, 204, 22, 255))

        # 3. Slender Tubular Shallot Leaves / Shoots (Daun Bawang Merah Berongga)
        # Each stalk has an individual sway phase for natural fluid motion
        stalks = [
            # (base_offset_x, angle_deg, length, phase_offset, sway_amp, color_outer, color_inner, width)
            (-12, -22, 175, 0.4, 14, (21, 128, 61), (74, 222, 128), 5),  # far left
            (-6, -11, 220, 0.2, 11, (22, 163, 74), (134, 239, 172), 6),  # mid left
            (0,    0, 255, 0.0,  9, (34, 197, 94), (187, 247, 208), 7),  # center tall shoot
            (6,   12, 215, 0.6, 12, (22, 163, 74), (134, 239, 172), 6),  # mid right
            (12,  24, 170, 0.8, 15, (21, 128, 61), (74, 222, 128), 5),  # far right
        ]

        for bx_off, ang_base, slen, phase, amp, col_out, col_in, sw in stalks:
            sway_ang = ang_base + math.sin(t_rad + phase * 2 * math.pi) * amp
            sway_rad = math.radians(sway_ang)
            
            # Bezier curve for natural curved onion leaf
            p0 = (cx + bx_off, bulb_y - 20)
            ctrl = (
                cx + bx_off + math.sin(sway_rad * 0.7) * (slen * 0.55),
                p0[1] - math.cos(sway_rad * 0.7) * (slen * 0.55)
            )
            p1 = (
                cx + bx_off + math.sin(sway_rad) * slen,
                p0[1] - math.cos(sway_rad) * slen
            )

            # Sample points along the tubular shoot
            pts = []
            steps = 24
            for s in range(steps + 1):
                st = s / float(steps)
                # Quadratic bezier
                x = (1 - st)**2 * p0[0] + 2 * (1 - st) * st * ctrl[0] + st**2 * p1[0]
                y = (1 - st)**2 * p0[1] + 2 * (1 - st) * st * ctrl[1] + st**2 * p1[1]
                pts.append((x, y))

            for k in range(len(pts) - 1):
                # Taper towards the slender tip
                w_cur = max(2, int(sw * (1.0 - (k / len(pts)) * 0.65)))
                draw.line([pts[k], pts[k+1]], fill=(*col_out, 255), width=w_cur)
                # Longitudinal highlight ridge
                draw.line([
                    (pts[k][0] - 1, pts[k][1]),
                    (pts[k+1][0] - 1, pts[k+1][1])
                ], fill=(*col_in, 200), width=max(1, w_cur - 2))

            # Dewdrop on middle and center stalks
            if abs(ang_base) < 15:
                dew_idx = int(len(pts) * 0.45)
                dw_pt = pts[dew_idx]
                draw.ellipse([dw_pt[0] - 3, dw_pt[1] - 3, dw_pt[0] + 3, dw_pt[1] + 3], fill=(56, 189, 248, 240))
                draw.point((int(dw_pt[0] - 1), int(dw_pt[1] - 1)), fill=(255, 255, 255, 255))

        # 4. Gardener's Watering Can (Golden / Brass)
        can_tilt = math.sin(t_rad) * 4
        can_base_x = 75
        can_base_y = 110 + int(math.cos(t_rad) * 3)

        # Handle
        draw.arc([can_base_x - 35, can_base_y - 20, can_base_x + 15, can_base_y + 40], start=100, end=270, fill=(202, 138, 4, 255), width=6)
        draw.arc([can_base_x - 35, can_base_y - 20, can_base_x + 15, can_base_y + 40], start=100, end=270, fill=(254, 240, 138, 200), width=2)
        # Top Arch Handle
        draw.arc([can_base_x, can_base_y - 45, can_base_x + 60, can_base_y + 5], start=180, end=360, fill=(202, 138, 4, 255), width=5)

        # Body
        draw.polygon([
            (can_base_x, can_base_y),
            (can_base_x + 65, can_base_y),
            (can_base_x + 58, can_base_y + 46),
            (can_base_x + 6, can_base_y + 46)
        ], fill=(234, 179, 8, 255))
        # Body highlight
        draw.line([(can_base_x + 8, can_base_y + 6), (can_base_x + 56, can_base_y + 6)], fill=(254, 240, 138, 240), width=3)
        draw.line([(can_base_x + 12, can_base_y + 40), (can_base_x + 52, can_base_y + 40)], fill=(161, 98, 7, 240), width=3)

        # Spout & Rose
        spout_start = (can_base_x + 55, can_base_y + 26)
        spout_end = (can_base_x + 95, can_base_y + 12)
        draw.line([spout_start, spout_end], fill=(234, 179, 8, 255), width=8)
        draw.line([spout_start, spout_end], fill=(254, 240, 138, 200), width=2)
        
        # Rose Head (Showerhead)
        rose_x, rose_y = spout_end[0] + 5, spout_end[1] - 2
        draw.ellipse([rose_x - 4, rose_y - 10, rose_x + 8, rose_y + 10], fill=(202, 138, 4, 255))
        draw.ellipse([rose_x - 2, rose_y - 8, rose_x + 6, rose_y + 8], fill=(250, 204, 21, 255))

        # 5. Falling Crystal Water Droplets & Soil Impact Ripples
        for frac, sx, sy, ex, ey, sz in drops_config:
            drop_t = (t + frac) % 1.0
            cur_x = sx + drop_t * (ex - sx)
            cur_y = sy + (drop_t ** 1.6) * (ey - sy)

            if drop_t < 0.88:
                # Droplet teardrop in flight
                draw.ellipse([cur_x - sz//2, cur_y - sz, cur_x + sz//2, cur_y + sz//2], fill=(56, 189, 248, 230))
                draw.point((int(cur_x - 1), int(cur_y - 2)), fill=(255, 255, 255, 255))
            else:
                # Water impact ripple expanding on soil/bulb
                splash_t = (drop_t - 0.88) / 0.12
                r_w = int(splash_t * 24)
                r_h = int(splash_t * 9)
                alpha = int(255 * (1.0 - splash_t))
                if alpha > 0 and r_w > 2:
                    draw.ellipse([ex - r_w, ey - r_h, ex + r_w, ey + r_h], outline=(125, 211, 252, alpha), width=2)

        # 6. Golden Nutrient & Sun Motes (Floating gently upwards)
        for sp_x, sp_y, drift_y, drift_x, rad in sparkles:
            sp_t = (t + sp_x * 0.003) % 1.0
            px = sp_x + math.sin(sp_t * 2 * math.pi) * drift_x
            py = sp_y + sp_t * drift_y
            sp_alpha = int(220 * math.sin(sp_t * math.pi))
            if sp_alpha > 30:
                # 4-point star
                draw.line([(px - rad, py), (px + rad, py)], fill=(254, 240, 138, sp_alpha), width=2)
                draw.line([(px, py - rad), (px, py + rad)], fill=(254, 240, 138, sp_alpha), width=2)
                draw.point((int(px), int(py)), fill=(255, 255, 255, sp_alpha))

        # 7. Convert to transparent GIF frame
        alpha = im.split()[3]
        im_rgb = im.convert('RGB')
        im_p = im_rgb.convert('P', palette=Image.Palette.ADAPTIVE, colors=254)
        mask = Image.eval(alpha, lambda a: 255 if a < 64 else 0)
        im_p.paste(255, mask)
        im_p.info['transparency'] = 255
        frames.append(im_p)

    out_path = 'images/halobun_onion_animation.gif'
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=42, # ~24 fps smooth
        loop=0,
        disposal=2
    )
    print(f"Onion animation saved to {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == '__main__':
    create_onion_animation()
