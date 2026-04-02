import os
import re

def fix_all_htmls():
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root or 'solar-system' in root:
            continue
            
        images_dir = os.path.join(root, 'IMAGES')
        local_images = []
        if os.path.isdir(images_dir):
            local_images = os.listdir(images_dir)
            
        for file in files:
            if not file.endswith('.html'):
                continue
                
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix hardcoded localhost paths anywhere
            content = re.sub(r'http://localhost:8000/p\d\d/IMAGES/', './IMAGES/', content)

            # Look for script blocks that use isLocal and inject an image
            # They usually look like img.setAttribute('src', src);
            script_pattern = re.compile(r"<script>[\s\S]*?isLocal[\s\S]*?</script>")
            
            # Before removing scripts, we need to make sure any <img> tag with just an id gets a src.
            # E.g. <img id="forest" crossorigin="anonymous">
            # We will replace them with the first available local image if they are missing a src
            # or specifically we know forest is Moving_Forest_1050_700.webp
            
            # Simple replace: add a temporary src if missing
            def img_src_injector(match):
                tag = match.group(0)
                if 'src=' not in tag:
                    # check if id has a hint
                    img_id = re.search(r'id="([^"]+)"', tag)
                    src_file = None
                    if img_id:
                        img_id = img_id.group(1).lower()
                        if 'forest' in img_id and 'Moving_Forest_1050_700.webp' in local_images:
                            src_file = 'Moving_Forest_1050_700.webp'
                        elif 'nebula' in img_id and 'heic2007a.jpg' in local_images:
                            src_file = 'heic2007a.jpg'
                    
                    if not src_file and local_images:
                        src_file = local_images[0]
                        
                    if src_file:
                        return tag.replace('>', f' src="./IMAGES/{src_file}">')
                return tag
                
            content = re.sub(r'<img[^>]+>', img_src_injector, content)
            
            # Now remove the problematic script blocks
            content = script_pattern.sub("", content)
            
            # Replace any wikimedia links that STILL exist in src= tags
            def wikimedia_replacer(match):
                tag = match.group(0)
                if 'wikimedia.org' in tag and local_images:
                    # just pick the first valid background we have locally
                    src_file = local_images[0]
                    # if there is a .webp, prioritize it or .jpg
                    for img in local_images:
                        if img.endswith('.jpg') or img.endswith('.webp'):
                            src_file = img
                            break
                    tag = re.sub(r'src="[^"]+"', f'src="./IMAGES/{src_file}"', tag)
                return tag
            
            content = re.sub(r'<(?:a-sky|img|a-sphere|a-box|a-entity)[^>]+src="[^"]+"[^>]*>', wikimedia_replacer, content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

fix_all_htmls()
print("Fixed HTML files completely!")
