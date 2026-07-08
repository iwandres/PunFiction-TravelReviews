import os
import shutil
import math
from PIL import Image, ImageDraw

# Define directories
src_dir = 'assets/stamps/'
dest_dir = 'c:/Users/iwand/.antigravity/Projects/PunFiction-BoxOffice/travelreviews/assets/stamps/'

# Create directories if they do not exist
os.makedirs(src_dir, exist_ok=True)
os.makedirs(dest_dir, exist_ok=True)

# Helper to draw a circle stamp border
def draw_base_stamp(draw, color, shape='circle'):
    if shape == 'circle':
        # Outer thick border
        draw.ellipse([15, 15, 235, 235], outline=color, width=4)
        # Inner thin border
        draw.ellipse([25, 25, 225, 225], outline=color, width=1.5)
        # Add some stars or dots in the border area
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            x = 125 + 95 * math.cos(angle)
            y = 125 + 95 * math.sin(angle)
            draw.ellipse([x-2, y-2, x+2, y+2], fill=color)
    elif shape == 'scallop':
        # Draw a scalloped border
        num_scallops = 24
        for i in range(num_scallops):
            angle = i * (2 * math.pi / num_scallops)
            x = 125 + 105 * math.cos(angle)
            y = 125 + 105 * math.sin(angle)
            draw.ellipse([x-10, y-10, x+10, y+10], fill=color)
        # Clear the inside
        draw.ellipse([30, 30, 220, 220], fill=(0,0,0,0))
        # Draw inner ring
        draw.ellipse([32, 32, 218, 218], outline=color, width=3)
        draw.ellipse([40, 40, 210, 210], outline=color, width=1)
    elif shape == 'diamond':
        # Draw a diamond shaped stamp
        draw.polygon([(125, 15), (235, 125), (125, 235), (15, 125)], outline=color, width=4)
        draw.polygon([(125, 25), (225, 125), (125, 225), (25, 125)], outline=color, width=1.5)

# 1. ANCIENT RUINS: stamp_ancient_pyramid.png
def make_ancient_pyramid():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (135, 54, 0, 255) # Sienna Brown #873600
    draw_base_stamp(draw, color, 'scallop')
    # Draw Pyramid
    draw.polygon([(125, 75), (65, 165), (125, 165)], fill=color) # Left side
    draw.polygon([(125, 75), (125, 165), (185, 165)], outline=color, fill=(0,0,0,0), width=2) # Right side (wireframe/shaded)
    # Shading lines on the right side
    for y in range(85, 165, 10):
        w = int((y - 75) * 60 / 90)
        draw.line([(125, y), (125 + w, y)], fill=color, width=2)
    # Horizon line
    draw.line([(55, 165), (195, 165)], fill=color, width=3)
    img.save(os.path.join(src_dir, 'stamp_ancient_pyramid.png'))

# 2. ANCIENT RUINS: stamp_ancient_temple.png
def make_ancient_temple():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (135, 54, 0, 255) # Sienna Brown #873600
    draw_base_stamp(draw, color, 'circle')
    # Draw Greek Temple
    # Roof (Triangle)
    draw.polygon([(125, 70), (70, 95), (180, 95)], fill=color)
    # Architrave (beam)
    draw.rectangle([75, 95, 175, 103], fill=color)
    # Columns (4 columns)
    cols = [80, 107, 137, 163]
    for x in cols:
        draw.rectangle([x, 103, x+7, 155], fill=color)
    # Base (Steps)
    draw.rectangle([65, 155, 185, 163], fill=color)
    draw.rectangle([60, 163, 190, 172], fill=color)
    img.save(os.path.join(src_dir, 'stamp_ancient_temple.png'))

# 3. NATURAL WONDERS: stamp_natural_mountain.png
def make_natural_mountain():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (30, 132, 73, 255) # Forest Green #1E8449
    draw_base_stamp(draw, color, 'circle')
    # Draw Mountains
    # Back mountain
    draw.polygon([(125, 65), (65, 170), (185, 170)], fill=color)
    # Foreground left mountain
    draw.polygon([(90, 90), (45, 170), (135, 170)], fill=color)
    # Foreground right mountain
    draw.polygon([(160, 100), (110, 170), (210, 170)], fill=color)
    # Snowcaps (White overlays)
    draw.polygon([(125, 65), (110, 95), (140, 95)], fill=(255,255,255,255))
    draw.polygon([(90, 90), (80, 110), (100, 110)], fill=(255,255,255,255))
    draw.polygon([(160, 100), (150, 120), (170, 120)], fill=(255,255,255,255))
    # Ground lines
    draw.line([(40, 170), (210, 170)], fill=color, width=3)
    img.save(os.path.join(src_dir, 'stamp_natural_mountain.png'))

# 4. NATURAL WONDERS: stamp_natural_forest.png
def make_natural_forest():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (30, 132, 73, 255) # Forest Green #1E8449
    draw_base_stamp(draw, color, 'scallop')
    # Draw three pine trees
    def draw_tree(tx, ty, scale):
        # Trunk
        draw.rectangle([tx-3, ty, tx+3, ty+15*scale], fill=color)
        # Foliage layers
        draw.polygon([(tx, ty-30*scale), (tx-20*scale, ty-10*scale), (tx+20*scale, ty-10*scale)], fill=color)
        draw.polygon([(tx, ty-18*scale), (tx-23*scale, ty+2*scale), (tx+23*scale, ty+2*scale)], fill=color)
        draw.polygon([(tx, ty-5*scale), (tx-26*scale, ty+15*scale), (tx+26*scale, ty+15*scale)], fill=color)

    draw_tree(125, 145, 1.1)  # Center main tree
    draw_tree(85, 150, 0.8)   # Left tree
    draw_tree(165, 150, 0.8)  # Right tree
    # Base land line
    draw.line([(55, 170), (195, 170)], fill=color, width=3)
    img.save(os.path.join(src_dir, 'stamp_natural_forest.png'))

# 5. HISTORIC MONUMENTS: stamp_monument_tower.png
def make_monument_tower():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (183, 149, 11, 255) # Historic Gold #B7950B
    draw_base_stamp(draw, color, 'circle')
    # Draw Eiffel Tower style lattice tower
    # Base legs
    draw.polygon([(85, 185), (105, 185), (115, 125), (95, 125)], fill=color) # Left leg
    draw.polygon([(165, 185), (145, 185), (135, 125), (155, 125)], fill=color) # Right leg
    # Arch between legs
    draw.chord([98, 145, 152, 195], 180, 360, fill=(0,0,0,0), outline=color, width=3)
    # First deck platform
    draw.rectangle([92, 125, 158, 133], fill=color)
    # Mid section
    draw.polygon([(100, 125), (150, 125), (140, 85), (110, 85)], fill=color)
    draw.rectangle([106, 85, 144, 91], fill=color) # Second deck
    # Top spire
    draw.polygon([(112, 85), (138, 85), (125, 45)], fill=color)
    draw.line([(125, 45), (125, 33)], fill=color, width=3) # Spire tip
    img.save(os.path.join(src_dir, 'stamp_monument_tower.png'))

# 6. HISTORIC MONUMENTS: stamp_monument_statue.png
def make_monument_statue():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (183, 149, 11, 255) # Historic Gold #B7950B
    draw_base_stamp(draw, color, 'scallop')
    # Draw Statue on Pedestal (Statue of Liberty style)
    # Pedestal (steps)
    draw.rectangle([95, 160, 155, 175], fill=color)
    draw.rectangle([102, 140, 148, 160], fill=color)
    # Body/Robes
    draw.polygon([(112, 140), (138, 140), (132, 80), (118, 80)], fill=color)
    # Head & Crown
    draw.ellipse([120, 68, 130, 78], fill=color)
    draw.polygon([(118, 70), (132, 70), (125, 62)], fill=color) # crown rays
    # Raised Arm & Torch
    draw.line([(130, 95), (142, 65)], fill=color, width=4) # arm
    draw.ellipse([139, 58, 145, 65], fill=color) # torch
    draw.polygon([(137, 60), (147, 60), (142, 50)], fill=color) # flame
    # Left arm holding tablet
    draw.rectangle([112, 100, 118, 115], fill=color)
    img.save(os.path.join(src_dir, 'stamp_monument_statue.png'))

# 7. CASTLES_CATHEDRALS: stamp_castle_turret.png
def make_castle_turret():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (125, 60, 152, 255) # Royal Purple #7D3C98
    draw_base_stamp(draw, color, 'circle')
    # Draw Castle Turrets
    # Main Central Keep
    draw.rectangle([100, 100, 150, 170], fill=color)
    # Battlements on Keep
    draw.rectangle([96, 90, 154, 100], fill=color)
    for x in range(96, 154, 14):
        draw.rectangle([x+4, 84, x+10, 90], fill=color)
    # Arched door
    draw.ellipse([117, 145, 133, 170], fill=(255,255,255,255))
    draw.rectangle([117, 157, 133, 170], fill=(255,255,255,255))
    # Side turrets (narrower and taller)
    draw.rectangle([75, 75, 95, 170], fill=color)
    draw.polygon([(70, 75), (100, 75), (85, 45)], fill=color) # Cone roof left
    draw.rectangle([155, 75, 175, 170], fill=color)
    draw.polygon([(150, 75), (180, 75), (165, 45)], fill=color) # Cone roof right
    # Flag on left roof
    draw.line([(85, 45), (85, 30)], fill=color, width=2)
    draw.polygon([(85, 30), (95, 35), (85, 40)], fill=color)
    img.save(os.path.join(src_dir, 'stamp_castle_turret.png'))

# 8. CASTLES_CATHEDRALS: stamp_cathedral_window.png
def make_cathedral_window():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (125, 60, 152, 255) # Royal Purple #7D3C98
    draw_base_stamp(draw, color, 'scallop')
    # Draw Gothic Rose Window geometry
    cx, cy = 125, 125
    r = 60
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=3)
    draw.ellipse([cx-20, cy-20, cx+20, cy+20], outline=color, width=2)
    # Draw 12 spoke arches
    for i in range(12):
        angle = i * (2 * math.pi / 12)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        draw.line([(cx, cy), (x, y)], fill=color, width=2)
        
        # Draw small petal circles in the sections
        mid_angle = angle + (math.pi / 12)
        px = cx + 42 * math.cos(mid_angle)
        py = cy + 42 * math.sin(mid_angle)
        draw.ellipse([px-6, py-6, px+6, py+6], outline=color, width=1.5)
    img.save(os.path.join(src_dir, 'stamp_cathedral_window.png'))

# 9. BRIDGES_CANALS: stamp_bridge_arch.png
def make_bridge_arch():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (14, 102, 85, 255) # Deep Teal #0E6655
    draw_base_stamp(draw, color, 'circle')
    # Draw Arch Bridge
    # Water line/waves
    draw.line([(40, 160), (210, 160)], fill=color, width=2)
    for x in range(45, 205, 15):
        draw.arc([x, 158, x+12, 166], 0, 180, fill=color, width=2)
    # Bridge deck
    draw.rectangle([50, 120, 200, 130], fill=color)
    # Support piers & arches
    draw.rectangle([60, 130, 75, 160], fill=color)
    draw.rectangle([115, 130, 135, 160], fill=color)
    draw.rectangle([175, 130, 190, 160], fill=color)
    # Arches under deck
    draw.chord([75, 128, 115, 162], 180, 360, fill=(0,0,0,0), outline=color, width=4)
    draw.chord([135, 128, 175, 162], 180, 360, fill=(0,0,0,0), outline=color, width=4)
    img.save(os.path.join(src_dir, 'stamp_bridge_arch.png'))

# 10. BRIDGES_CANALS: stamp_nautical_anchor.png
def make_nautical_anchor():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (14, 102, 85, 255) # Deep Teal #0E6655
    draw_base_stamp(draw, color, 'diamond')
    # Draw Anchor
    cx, cy = 125, 130
    # Center shank (vertical line)
    draw.line([(cx, cy-60), (cx, cy+50)], fill=color, width=6)
    # Stock (horizontal bar near top)
    draw.line([(cx-35, cy-40), (cx+35, cy-40)], fill=color, width=5)
    # Crown ring at top
    draw.ellipse([cx-15, cy-80, cx+15, cy-50], outline=color, width=5)
    # Curved arms
    draw.arc([cx-50, cy+10, cx+50, cy+70], 0, 180, fill=color, width=6)
    # Flukes (triangles on ends of curve)
    draw.polygon([(cx-50, cy+32), (cx-58, cy+40), (cx-42, cy+45)], fill=color)
    draw.polygon([(cx+50, cy+32), (cx+58, cy+40), (cx+42, cy+45)], fill=color)
    img.save(os.path.join(src_dir, 'stamp_nautical_anchor.png'))

# 11. STREETS_SQUARES: stamp_street_lamp.png
def make_street_lamp():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (186, 74, 0, 255) # Terracotta Orange #BA4A00
    draw_base_stamp(draw, color, 'circle')
    # Draw Vintage Street Lamp
    cx = 125
    # Pole
    draw.line([(cx, 75), (cx, 185)], fill=color, width=5)
    draw.rectangle([cx-10, 175, cx+10, 185], fill=color) # base
    # Decorative arms/scrollwork
    draw.arc([cx-25, 75, cx+25, 105], 180, 360, fill=color, width=3)
    # Central Lantern
    draw.polygon([(cx-12, 70), (cx+12, 70), (cx+8, 48), (cx-8, 48)], fill=color) # Cap
    draw.polygon([(cx-10, 70), (cx+10, 70), (cx+6, 95), (cx-6, 95)], outline=color, fill=(0,0,0,0), width=3) # glass cage
    draw.line([(cx, 95), (cx, 110)], fill=color, width=4) # bottom post support
    draw.ellipse([cx-4, 80, cx+4, 88], fill=color) # light bulb
    img.save(os.path.join(src_dir, 'stamp_street_lamp.png'))

# 12. STREETS_SQUARES: stamp_vintage_car.png
def make_vintage_car():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (186, 74, 0, 255) # Terracotta Orange #BA4A00
    draw_base_stamp(draw, color, 'scallop')
    # Draw Retro Car Silhouette
    # Wheels
    draw.ellipse([80, 150, 105, 175], fill=color)
    draw.ellipse([145, 150, 170, 175], fill=color)
    draw.ellipse([87, 157, 98, 168], fill=(255,255,255,255))
    draw.ellipse([152, 157, 163, 168], fill=(255,255,255,255))
    # Car Body
    draw.polygon([
        (60, 155), (190, 155), (190, 135), (175, 135),
        (160, 115), (110, 115), (95, 135), (60, 135)
    ], fill=color)
    # Windshield/Window cutout (White shape)
    draw.polygon([
        (102, 118), (123, 118), (123, 132), (105, 132)
    ], fill=(255,255,255,255))
    draw.polygon([
        (127, 118), (155, 118), (163, 132), (127, 132)
    ], fill=(255,255,255,255))
    # Bumpers
    draw.rectangle([50, 148, 62, 154], fill=color)
    draw.rectangle([188, 148, 200, 154], fill=color)
    img.save(os.path.join(src_dir, 'stamp_vintage_car.png'))

# 13. MODERN_SKYSCRAPERS: stamp_modern_skyline.png
def make_modern_skyline():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (27, 79, 114, 255) # Midnight Blue #1B4F72
    draw_base_stamp(draw, color, 'circle')
    # Draw Skyscrapers
    # Building 1 (Tall center)
    draw.rectangle([110, 60, 140, 175], fill=color)
    draw.polygon([(110, 60), (140, 60), (125, 40)], fill=color) # Spire roof
    draw.line([(125, 40), (125, 25)], fill=color, width=2) # Spire tip
    # Building 2 (Left angular)
    draw.polygon([(70, 95), (105, 75), (105, 175), (70, 175)], fill=color)
    # Building 3 (Right blocky)
    draw.rectangle([145, 80, 180, 175], fill=color)
    # Building 4 (Far left small)
    draw.rectangle([50, 120, 67, 175], fill=color)
    # Building 5 (Far right small)
    draw.rectangle([183, 110, 198, 175], fill=color)
    # Tiny window dots (white)
    window_cols = [77, 87, 116, 124, 132, 152, 162, 172]
    for x in window_cols:
        for y in range(100, 170, 15):
            # Only draw if inside building bounds
            if x < 105 and y < 85: continue
            if x > 145 and y < 90: continue
            if x > 110 and x < 140 and y < 70: continue
            draw.rectangle([x, y, x+3, y+4], fill=(255,255,255,255))
    img.save(os.path.join(src_dir, 'stamp_modern_skyline.png'))

# 14. MODERN_SKYSCRAPERS: stamp_modern_jet.png
def make_modern_jet():
    img = Image.new('RGBA', (250, 250), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    color = (27, 79, 114, 255) # Midnight Blue #1B4F72
    draw_base_stamp(draw, color, 'diamond')
    # Draw modern swept-wing jet outline/silhouette at a 45-degree angle
    cx, cy = 125, 125
    # Center fuselage
    draw.polygon([
        (cx-50, cy+50), (cx+50, cy-50), # tail to nose
        (cx+45, cy-38), (cx-38, cy+45)  # side widths
    ], fill=color)
    # Nose cone
    draw.polygon([(cx+40, cy-48), (cx+52, cy-52), (cx+48, cy-40)], fill=color)
    # Main wings (swept back)
    draw.polygon([
        (cx-5, cy+5), # center root
        (cx-45, cy-45), # left wingtip
        (cx-25, cy-15)  # swept back point
    ], fill=color)
    draw.polygon([
        (cx-5, cy+5), # center root
        (cx+45, cy+45), # right wingtip
        (cx+15, cy+25)  # swept back point
    ], fill=color)
    # Tail wings
    draw.polygon([
        (cx-38, cy+38), (cx-58, cy+25), (cx-45, cy+33)
    ], fill=color)
    draw.polygon([
        (cx-38, cy+38), (cx-25, cy+58), (cx-33, cy+45)
    ], fill=color)
    img.save(os.path.join(src_dir, 'stamp_modern_jet.png'))

# Generate all 14 stamps
make_ancient_pyramid()
make_ancient_temple()
make_natural_mountain()
make_natural_forest()
make_monument_tower()
make_monument_statue()
make_castle_turret()
make_cathedral_window()
make_bridge_arch()
make_nautical_anchor()
make_street_lamp()
make_vintage_car()
make_modern_skyline()
make_modern_jet()

print("Generated 14 vector travel stamps successfully.")

# Copy all new stamps to the BoxOffice travelreviews/assets/stamps/ directory
files = os.listdir(src_dir)
copied_count = 0
for f in files:
    if f.startswith('stamp_'):
        shutil.copyfile(os.path.join(src_dir, f), os.path.join(dest_dir, f))
        copied_count += 1

print(f"Successfully copied {copied_count} stamp files to BoxOffice repository.")
