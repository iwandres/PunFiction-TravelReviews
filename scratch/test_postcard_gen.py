import os
import random
import time
import json
from google import genai
from google.genai import types
from PIL import Image
import io

gemini_key = os.environ.get("GEMINI_API_KEY")
print("Key exists:", gemini_key is not None)

CLUES_FILE = 'backend/travelreviews_clues.json'
POSTCARDS_FILE = 'backend/travelreviews_postcards.json'

clues = json.load(open(CLUES_FILE))
postcards = json.load(open(POSTCARDS_FILE))

existing_clues_in_postcards = {p['clue_id'] for p in postcards}
approved_clues = [c for c in clues if c.get('status') == 'approved' and c['id'] not in existing_clues_in_postcards]

print("Awaiting postcards:", len(approved_clues))

styles_dict = {
    "cartoon": "Comical cartoon illustration, bold lines, bright vibrant colors, humorous caricature, white postcard border.",
    "watercolor": "Whimsical watercolor and ink sketch, detailed storybook style, soft textures, pastel colors, artistically detailed.",
    "retro": "Vintage 1950s travel poster style, retro flat vector design, bold colors, screen-printed poster aesthetic.",
    "wpa": "Old school vintage travel illustration style, rooted in 1930s WPA-era silk-screened travel posters and 1960s lithographs, featuring bold shapes, muted earthy color palettes, and hand-drawn typography.",
    "vintage": "Classic distressed linen texture vintage postcard style, hand-colored photo print aesthetic, 1930s travel style.",
    "pop-art": "Vibrant Pop Art style, bold outlines, screen print dot texture, retro comic book feel, high contrast colors."
}

client = genai.Client(api_key=gemini_key)

for i, c in enumerate(approved_clues[:15]):
    print(f"\n--- Clue {i+1}/{len(approved_clues)}: {c['pun_name']} (original: {c['original_name']}) ---")
    try:
        style_key = random.choice(list(styles_dict.keys()))
        style_prompt = styles_dict[style_key]
        
        prompt_gen = f"""
        Create a single-sentence descriptive text-to-image prompt for a parodied travel postcard based on the location pun "{c['pun_name']}" (derived from "{c['original_name']}").
        The prompt should describe a funny, comical scene matching this art style: "{style_prompt}".
        
        Return a JSON object exactly matching this schema:
        {{
          "image_prompt": "A description of the funny parodied scene."
        }}
        """
        
        print("Generating prompt...")
        prompt_res = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_gen,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        prompt_data = json.loads(prompt_res.text)
        image_prompt = prompt_data.get("image_prompt")
        print("Generated image prompt:", image_prompt)
        
        print("Generating image...")
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=f"{style_prompt} {image_prompt}".strip(),
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/png",
                aspect_ratio="4:3"
            )
        )
        print("Success! Number of images returned:", len(response.generated_images))
        time.sleep(1) # rate limit courtesy
    except Exception as e:
        print(f"FAILED for {c['pun_name']}: {e}")
