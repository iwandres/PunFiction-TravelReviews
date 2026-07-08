import os
import random
import time
import json
import re
import io
from google import genai
from google.genai import types
from PIL import Image

DIR_PATH = 'backend'
PROJECT_ROOT = '.'
CLUES_FILE = os.path.join(DIR_PATH, 'travelreviews_clues.json')
POSTCARDS_FILE = os.path.join(DIR_PATH, 'travelreviews_postcards.json')

if os.path.exists(os.path.join(PROJECT_ROOT, 'travelreviews')):
    CARTOONS_DIR = os.path.join(PROJECT_ROOT, 'travelreviews', 'assets', 'cartoons')
else:
    CARTOONS_DIR = os.path.join(PROJECT_ROOT, 'assets', 'cartoons')
os.makedirs(CARTOONS_DIR, exist_ok=True)

gemini_key = os.environ.get("GEMINI_API_KEY")
if not gemini_key:
    print("Error: GEMINI_API_KEY environment variable missing.")
    exit(1)

styles_dict = {
    "cartoon": "Comical cartoon illustration, bold lines, bright vibrant colors, humorous caricature, white postcard border.",
    "watercolor": "Whimsical watercolor and ink sketch, detailed storybook style, soft textures, pastel colors, artistically detailed.",
    "retro": "Vintage 1950s travel poster style, retro flat vector design, bold colors, screen-printed poster aesthetic.",
    "wpa": "Old school vintage travel illustration style, rooted in 1930s WPA-era silk-screened travel posters and 1960s lithographs, featuring bold shapes, muted earthy color palettes, and hand-drawn typography.",
    "vintage": "Classic distressed linen texture vintage postcard style, hand-colored photo print aesthetic, 1930s travel style.",
    "pop-art": "Vibrant Pop Art style, bold outlines, screen print dot texture, retro comic book feel, high contrast colors."
}

def load_json(filepath, default_val=None):
    if default_val is None:
        default_val = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
    return default_val

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving {filepath}: {e}")

clues = load_json(CLUES_FILE, [])
postcards = load_json(POSTCARDS_FILE, [])

existing_clues_in_postcards = {p['clue_id'] for p in postcards}
approved_clues = [c for c in clues if c.get('status') == 'approved' and c['id'] not in existing_clues_in_postcards]

print(f"Total approved clues awaiting postcards: {len(approved_clues)}")

client = genai.Client(api_key=gemini_key)
generated_count = 0

for c in approved_clues:
    print(f"\n--- Processing '{c['pun_name']}' ({c['id']}) ---")
    try:
        style_key = random.choice(list(styles_dict.keys()))
        style_prompt = styles_dict[style_key]
        
        prompt_gen = f"""
        Create a single-sentence descriptive text-to-image prompt for a parodied travel postcard based on the location pun "{c['pun_name']}" (derived from "{c['original_name']}").
        The prompt should describe a funny, comical scene matching this art style: "{style_prompt}".
        Example for "The Grand Crayon":
        "A giant yellow crayon laying inside the rocky Grand Canyon, comical cartoon illustration."
        
        Return a JSON object exactly matching this schema:
        {{
          "image_prompt": "A giant yellow crayon laying inside the rocky Grand Canyon, comical cartoon illustration."
        }}
        """
        
        prompt_res = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_gen,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        prompt_data = json.loads(prompt_res.text)
        image_prompt = prompt_data.get("image_prompt", f"A funny cartoon of {c['pun_name']}, comical illustration.")
        
        safe_filename = c['pun_name'].lower().replace(' ', '_').replace('-', '_').replace(':', '')
        safe_filename = re.sub(r'[^a-z0-9_]', '', safe_filename) + f"_{int(time.time())}.png"
        image_path = f"/assets/cartoons/{safe_filename}"
        local_image_path = os.path.join(CARTOONS_DIR, safe_filename)
        
        print(f"Generating image in style '{style_key}' using imagen-4.0-generate-001...")
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=f"{style_prompt} {image_prompt}".strip(),
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/png",
                aspect_ratio="4:3"
            )
        )
        
        saved_image = False
        for generated_image in response.generated_images:
            image_bytes = generated_image.image.image_bytes
            image = Image.open(io.BytesIO(image_bytes))
            image.save(local_image_path)
            print(f"Saved image to: {local_image_path}")
            saved_image = True
            break
            
        if not saved_image:
            raise Exception("No image returned from Imagen API.")
            
        # Re-load postcards to avoid overwriting concurrent edits
        postcards = load_json(POSTCARDS_FILE, [])
        postcard_entry = {
            "id": f"postcard_{c['id']}_{int(time.time())}",
            "clue_id": c['id'],
            "pun_name": c['pun_name'],
            "original_name": c['original_name'],
            "image_prompt": image_prompt,
            "image_path": image_path,
            "art_style": style_key,
            "owner_response": c['owner_response'],
            "page_theme": c.get('page_theme', 'road_trip'),
            "status": "pending"
        }
        postcards.append(postcard_entry)
        save_json(POSTCARDS_FILE, postcards)
        generated_count += 1
        print(f"Postcard saved successfully. Total generated so far: {generated_count}")
        
        # Sleep to avoid rate limiting
        time.sleep(2)
        
    except Exception as e:
        print(f"Error generating postcard for {c['pun_name']}: {e}")
        # Sleep a bit longer on error
        time.sleep(5)

print(f"\nDone! Generated {generated_count} postcards.")
