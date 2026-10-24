import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def ease_in_out_cubic(x):
    return 4 * x * x * x if x < 0.5 else 1 - pow(-2 * x + 2, 3) / 2

def ease_out_back(x):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2)

def main():
    im1_path = r"C:\Users\91821\.gemini\antigravity\brain\215bc613-f23d-4a7f-acc3-b6b9248c3a45\.user_uploaded\media_1792823201183.jpg"
    im2_path = r"C:\Users\91821\.gemini\antigravity\brain\215bc613-f23d-4a7f-acc3-b6b9248c3a45\.user_uploaded\media_1792825476575.jpg"
    out_dir = r"C:\Users\91821\.gemini\antigravity\scratch\lecturelens\frontend\public\sequence"
    os.makedirs(out_dir, exist_ok=True)

    base1 = Image.open(im1_path).convert("RGBA")
    W, H = base1.size  # 1024, 576
    bg_color = (5, 5, 5, 255)

    # Prepare im2 (waving robot) aligned to (1024, 576)
    im2 = Image.open(im2_path).convert("RGBA")
    s2 = 1.54
    im2_s = im2.resize((int(im2.width * s2), int(im2.height * s2)), Image.Resampling.LANCZOS)
    
    # Feathered mask for im2 to eliminate any edge artifacts and blend into #050505
    mask2 = Image.new("L", im2_s.size, 0)
    d_m2 = ImageDraw.Draw(mask2)
    # Generous oval & rect covering the robot, feathering the edges
    d_m2.ellipse([320, 10, 960, 560], fill=255)
    d_m2.rectangle([400, 20, 920, 510], fill=255)
    mask2 = mask2.filter(ImageFilter.GaussianBlur(30))
    im2_s.putalpha(mask2)

    # Composite aligned im2 onto void canvas
    waving_full = Image.new("RGBA", (W, H), bg_color)
    waving_full.alpha_composite(im2_s, (-44, 19))

    # Cut out distinct anatomical sections from im1 for exploded view
    # 1. Head
    head_box = (360, 45, 640, 240)
    head_crop = base1.crop(head_box)
    head_mask = Image.new("L", (head_box[2]-head_box[0], head_box[3]-head_box[1]), 0)
    draw_hm = ImageDraw.Draw(head_mask)
    draw_hm.rounded_rectangle([15, 15, head_mask.width-15, head_mask.height-15], radius=60, fill=255)
    head_mask = head_mask.filter(ImageFilter.GaussianBlur(8))
    head_crop.putalpha(head_mask)

    # 2. Chest Panel / Screen
    chest_box = (435, 275, 560, 480)
    chest_crop = base1.crop(chest_box)
    chest_mask = Image.new("L", (chest_box[2]-chest_box[0], chest_box[3]-chest_box[1]), 0)
    draw_cm = ImageDraw.Draw(chest_mask)
    draw_cm.rounded_rectangle([8, 8, chest_mask.width-8, chest_mask.height-8], radius=25, fill=255)
    chest_mask = chest_mask.filter(ImageFilter.GaussianBlur(6))
    chest_crop.putalpha(chest_mask)

    # 3. Left Arm (viewer's left)
    larm_box = (270, 275, 380, 576)
    larm_crop = base1.crop(larm_box)
    larm_mask = Image.new("L", (larm_box[2]-larm_box[0], larm_box[3]-larm_box[1]), 0)
    draw_lm = ImageDraw.Draw(larm_mask)
    draw_lm.rounded_rectangle([10, 10, larm_mask.width-10, larm_mask.height-10], radius=35, fill=255)
    larm_mask = larm_mask.filter(ImageFilter.GaussianBlur(6))
    larm_crop.putalpha(larm_mask)

    # 4. Right Arm (viewer's right)
    rarm_box = (630, 275, 745, 576)
    rarm_crop = base1.crop(rarm_box)
    rarm_mask = Image.new("L", (rarm_box[2]-rarm_box[0], rarm_box[3]-rarm_box[1]), 0)
    draw_rm = ImageDraw.Draw(rarm_mask)
    draw_rm.rounded_rectangle([10, 10, rarm_mask.width-10, rarm_mask.height-10], radius=35, fill=255)
    rarm_mask = rarm_mask.filter(ImageFilter.GaussianBlur(6))
    rarm_crop.putalpha(rarm_mask)

    # Extract waving hand & forearm from waving_full for live oscillation
    hand_box = (720, 20, 930, 260)
    waving_hand = waving_full.crop(hand_box)
    hand_mask = Image.new("L", (hand_box[2]-hand_box[0], hand_box[3]-hand_box[1]), 0)
    d_hm = ImageDraw.Draw(hand_mask)
    d_hm.rounded_rectangle([10, 10, hand_mask.width-10, hand_mask.height-10], radius=40, fill=255)
    hand_mask = hand_mask.filter(ImageFilter.GaussianBlur(10))
    waving_hand.putalpha(hand_mask)

    # Base without the waving forearm for isolated hand rotation
    waving_body = waving_full.copy()
    d_wb = ImageDraw.Draw(waving_body)
    d_wb.rectangle([740, 40, 920, 250], fill=bg_color)
    waving_body = waving_body.filter(ImageFilter.GaussianBlur(2))

    total_frames = 120
    print(f"Generating {total_frames} cinematic frames into {out_dir}...")

    for i in range(total_frames):
        frame = Image.new("RGBA", (W, H), bg_color)

        # Subtle radial blue glow behind robot
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_glow = ImageDraw.Draw(glow)
        center_x, center_y = W // 2, H // 2 + 30
        glow_alpha = int(28 + 14 * math.sin(i * 0.08))
        draw_glow.ellipse(
            [center_x - 300, center_y - 240, center_x + 300, center_y + 240],
            fill=(0, 80, 255, glow_alpha)
        )
        glow = glow.filter(ImageFilter.GaussianBlur(60))
        frame.alpha_composite(glow)

        idle_dy = int(math.sin(i * 0.1) * 3)

        # =============================================================
        # PHASE 1: HERO ASSEMBLED (Frames 0 - 18)
        # =============================================================
        if i <= 18:
            f_robot = base1.copy()
            draw_fr = ImageDraw.Draw(f_robot)
            dot_alpha = int(180 + 75 * math.sin(i * 0.35))
            draw_fr.ellipse([493, 497, 507, 511], fill=(0, 214, 255, dot_alpha))
            frame.alpha_composite(f_robot, (0, idle_dy))

        # =============================================================
        # PHASE 2: SEPARATION / DISASSEMBLY (Frames 19 - 45)
        # =============================================================
        elif 19 <= i <= 45:
            p = (i - 18) / 27.0
            e = ease_in_out_cubic(p)

            head_dy = int(-55 * e)
            chest_dy = int(22 * e)
            chest_scale = 1.0 + 0.10 * e
            larm_dx = int(-50 * e)
            rarm_dx = int(50 * e)

            # Draw background torso
            frame.alpha_composite(base1, (0, idle_dy))

            # Quantum Core behind chest panel
            core_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw_core = ImageDraw.Draw(core_layer)
            core_cx, core_cy = 495, 375 + idle_dy
            core_rad = int(28 * e)
            if core_rad > 2:
                draw_core.ellipse(
                    [core_cx - core_rad, core_cy - core_rad, core_cx + core_rad, core_cy + core_rad],
                    fill=(0, 180, 255, int(180 * e)),
                    outline=(0, 235, 255, int(240 * e)),
                    width=2
                )
                draw_core.ellipse(
                    [core_cx - 8, core_cy - 8, core_cx + 8, core_cy + 8],
                    fill=(255, 255, 255, int(230 * e))
                )
                for angle in range(0, 360, 45):
                    rad = math.radians(angle + i * 3)
                    tx1 = core_cx + int((core_rad + 8) * math.cos(rad))
                    ty1 = core_cy + int((core_rad + 8) * math.sin(rad))
                    tx2 = core_cx + int((core_rad + 18) * math.cos(rad))
                    ty2 = core_cy + int((core_rad + 18) * math.sin(rad))
                    draw_core.line([tx1, ty1, tx2, ty2], fill=(0, 214, 255, int(150 * e)), width=1)
            frame.alpha_composite(core_layer)

            # Blueprint lines
            hud_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw_hud = ImageDraw.Draw(hud_layer)
            draw_hud.line([500, 205 + idle_dy, 500, 205 + idle_dy + head_dy], fill=(0, 214, 255, int(180 * e)), width=2)
            draw_hud.line([520, 205 + idle_dy, 520, 205 + idle_dy + head_dy], fill=(0, 214, 255, int(180 * e)), width=2)
            draw_hud.line([330 + larm_dx, 330 + idle_dy, 330, 330 + idle_dy], fill=(0, 214, 255, int(140 * e)), width=1)
            draw_hud.rectangle([328 + larm_dx, 328 + idle_dy, 332 + larm_dx, 332 + idle_dy], fill=(0, 235, 255, int(200 * e)))
            draw_hud.line([680, 330 + idle_dy, 680 + rarm_dx, 330 + idle_dy], fill=(0, 214, 255, int(140 * e)), width=1)
            draw_hud.rectangle([678 + rarm_dx, 328 + idle_dy, 682 + rarm_dx, 332 + idle_dy], fill=(0, 235, 255, int(200 * e)))
            frame.alpha_composite(hud_layer)

            # Displaced limbs
            frame.alpha_composite(larm_crop, (larm_box[0] + larm_dx, larm_box[1] + idle_dy))
            frame.alpha_composite(rarm_crop, (rarm_box[0] + rarm_dx, rarm_box[1] + idle_dy))
            frame.alpha_composite(head_crop, (head_box[0], head_box[1] + idle_dy + head_dy))

            cw = int(chest_crop.width * chest_scale)
            ch = int(chest_crop.height * chest_scale)
            scaled_chest = chest_crop.resize((cw, ch), Image.Resampling.LANCZOS)
            cx_pos = chest_box[0] - (cw - chest_crop.width) // 2
            cy_pos = chest_box[1] + idle_dy + chest_dy
            frame.alpha_composite(scaled_chest, (cx_pos, cy_pos))

        # =============================================================
        # PHASE 3: PEAK FLOATING TECHNICAL DIAGRAM (Frames 46 - 75)
        # =============================================================
        elif 46 <= i <= 75:
            f_time = (i - 46) * 0.15
            float_y = int(math.sin(f_time) * 4)
            float_h = int(math.cos(f_time) * 3)

            head_dy = -55 + float_h
            chest_dy = 22 + float_y
            chest_scale = 1.10
            larm_dx = -52 + float_y
            rarm_dx = 52 - float_y

            frame.alpha_composite(base1, (0, idle_dy))

            core_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw_core = ImageDraw.Draw(core_layer)
            core_cx, core_cy = 495, 375 + idle_dy

            draw_core.ellipse([core_cx - 40, core_cy - 40, core_cx + 40, core_cy + 40], outline=(0, 160, 255, 90), width=1)
            draw_core.ellipse([core_cx - 28, core_cy - 28, core_cx + 28, core_cy + 28], fill=(0, 170, 255, 170), outline=(0, 235, 255, 240), width=2)
            draw_core.ellipse([core_cx - 9, core_cy - 9, core_cx + 9, core_cy + 9], fill=(255, 255, 255, 240))

            for angle in range(0, 360, 30):
                rad = math.radians(angle + i * 3)
                tx1 = core_cx + int(32 * math.cos(rad))
                ty1 = core_cy + int(32 * math.sin(rad))
                tx2 = core_cx + int(38 * math.cos(rad))
                ty2 = core_cy + int(38 * math.sin(rad))
                draw_core.line([tx1, ty1, tx2, ty2], fill=(0, 214, 255, 180), width=1)
            frame.alpha_composite(core_layer)

            hud_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw_hud = ImageDraw.Draw(hud_layer)
            draw_hud.line([head_box[0] - 80, head_box[1] + head_dy + 40, head_box[0] + 20, head_box[1] + head_dy + 40], fill=(0, 214, 255, 160), width=1)
            draw_hud.rectangle([head_box[0] - 83, head_box[1] + head_dy + 38, head_box[0] - 77, head_box[1] + head_dy + 42], fill=(0, 214, 255, 220))
            draw_hud.line([330 + larm_dx, 330 + idle_dy, 330, 330 + idle_dy], fill=(0, 214, 255, 140), width=1)
            draw_hud.line([680, 330 + idle_dy, 680 + rarm_dx, 330 + idle_dy], fill=(0, 214, 255, 140), width=1)

            # Torso grid
            for gy in range(260, 480, 30):
                draw_hud.line([440, gy + idle_dy, 550, gy + idle_dy], fill=(0, 214, 255, 25), width=1)
            for gx in range(450, 550, 25):
                draw_hud.line([gx, 260 + idle_dy, gx, 480 + idle_dy], fill=(0, 214, 255, 25), width=1)

            frame.alpha_composite(hud_layer)

            frame.alpha_composite(larm_crop, (larm_box[0] + larm_dx, larm_box[1] + idle_dy))
            frame.alpha_composite(rarm_crop, (rarm_box[0] + rarm_dx, rarm_box[1] + idle_dy))
            frame.alpha_composite(head_crop, (head_box[0], head_box[1] + idle_dy + head_dy))

            cw = int(chest_crop.width * chest_scale)
            ch = int(chest_crop.height * chest_scale)
            scaled_chest = chest_crop.resize((cw, ch), Image.Resampling.LANCZOS)
            cx_pos = chest_box[0] - (cw - chest_crop.width) // 2
            cy_pos = chest_box[1] + idle_dy + chest_dy
            frame.alpha_composite(scaled_chest, (cx_pos, cy_pos))

        # =============================================================
        # PHASE 4: MAGNETIC REASSEMBLY (Frames 76 - 94)
        # =============================================================
        elif 76 <= i <= 94:
            p = 1.0 - (i - 75) / 19.0
            e = ease_in_out_cubic(p)

            head_dy = int(-55 * e)
            chest_dy = int(22 * e)
            chest_scale = 1.0 + 0.10 * e
            larm_dx = int(-50 * e)
            rarm_dx = int(50 * e)

            frame.alpha_composite(base1, (0, idle_dy))

            if e > 0.1:
                core_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                draw_core = ImageDraw.Draw(core_layer)
                core_cx, core_cy = 495, 375 + idle_dy
                rad = int(24 * e)
                draw_core.ellipse([core_cx - rad, core_cy - rad, core_cx + rad, core_cy + rad], fill=(0, 180, 255, int(150 * e)))
                frame.alpha_composite(core_layer)

            frame.alpha_composite(larm_crop, (larm_box[0] + larm_dx, larm_box[1] + idle_dy))
            frame.alpha_composite(rarm_crop, (rarm_box[0] + rarm_dx, rarm_box[1] + idle_dy))
            frame.alpha_composite(head_crop, (head_box[0], head_box[1] + idle_dy + head_dy))

            cw = int(chest_crop.width * chest_scale)
            ch = int(chest_crop.height * chest_scale)
            scaled_chest = chest_crop.resize((cw, ch), Image.Resampling.LANCZOS)
            cx_pos = chest_box[0] - (cw - chest_crop.width) // 2
            cy_pos = chest_box[1] + idle_dy + chest_dy
            frame.alpha_composite(scaled_chest, (cx_pos, cy_pos))

            # Snap latch flash
            if 89 <= i <= 94:
                snap_p = (i - 89) / 5.0
                flash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                draw_flash = ImageDraw.Draw(flash)
                alpha = int(140 * (1.0 - snap_p))
                draw_flash.ellipse([460, 340, 530, 410], fill=(0, 214, 255, alpha))
                flash = flash.filter(ImageFilter.GaussianBlur(15))
                frame.alpha_composite(flash)

        # =============================================================
        # PHASE 5: REASSEMBLED WAVE HELLO (Frames 95 - 119)
        # Featuring user-uploaded media_1792825476575.jpg
        # =============================================================
        else:
            w_idx = i - 95  # 0 to 24

            if w_idx < 10:
                # Smooth morph/transition from base1 (neutral) to waving_full (arm raised)
                blend_t = w_idx / 10.0
                # Base1 assembled frame
                f_base1 = base1.copy()
                d_b1 = ImageDraw.Draw(f_base1)
                d_b1.ellipse([493, 497, 507, 511], fill=(0, 214, 255, 230))

                # Blend between base1 and waving_full
                blended = Image.blend(f_base1, waving_full, blend_t)
                frame.alpha_composite(blended, (0, idle_dy))

                # Arm raise cyan energy sweep
                sweep = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                draw_sw = ImageDraw.Draw(sweep)
                sw_alpha = int(90 * math.sin(blend_t * math.pi))
                draw_sw.line([680, 420 + idle_dy, 780, 200 + idle_dy], fill=(0, 214, 255, sw_alpha), width=3)
                sweep = sweep.filter(ImageFilter.GaussianBlur(8))
                frame.alpha_composite(sweep)

            else:
                # Fully into Waving Robot (w_idx >= 10, frames 105 to 119)
                wave_t = w_idx - 10
                # Natural sinusoidal hand wave rotation
                wave_angle = math.sin(wave_t * 0.75) * 7.5

                # Draw waving body base
                frame.alpha_composite(waving_body, (0, idle_dy))

                # Rotate the waving hand around elbow/wrist pivot (x: ~790, y: ~180 in canvas coords)
                rotated_hand = waving_hand.rotate(-wave_angle, resample=Image.Resampling.BICUBIC, expand=True)
                # Position rotated hand centered on original hand_box
                r_w, r_h = rotated_hand.size
                orig_cx = hand_box[0] + waving_hand.width // 2
                orig_cy = hand_box[1] + waving_hand.height // 2 + idle_dy
                hand_x = orig_cx - r_w // 2
                hand_y = orig_cy - r_h // 2
                frame.alpha_composite(rotated_hand, (hand_x, hand_y))

                # Friendly pulsing glow on chest display and eyes
                friendly_pulse = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                draw_fp = ImageDraw.Draw(friendly_pulse)
                p_alpha = int(40 + 20 * math.sin(wave_t * 0.5))
                # Chest screen glow
                draw_fp.ellipse([440, 270 + idle_dy, 560, 470 + idle_dy], fill=(0, 180, 255, p_alpha))
                # Eyes warmth
                draw_fp.ellipse([460, 110 + idle_dy, 540, 150 + idle_dy], fill=(0, 220, 255, int(p_alpha * 0.8)))
                friendly_pulse = friendly_pulse.filter(ImageFilter.GaussianBlur(18))
                frame.alpha_composite(friendly_pulse)

        # Convert to RGB and save JPEG
        final_rgb = frame.convert("RGB")
        frame_name = f"frame_{i:03d}.jpg"
        final_rgb.save(os.path.join(out_dir, frame_name), "JPEG", quality=88, optimize=True)

    print("Successfully generated all 120 sequence frames!")

if __name__ == "__main__":
    main()
