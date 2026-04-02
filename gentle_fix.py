import os
import re

def gentle_fix():
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root or 'solar-system' in root:
            continue
        for file in files:
            if not file.endswith('.html'):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            original = content
            
            # 1. Force isLocal to be true everywhere so it drops the wikimedia fallback
            content = content.replace("const isLocal = ['localhost','127.0.0.1','[::1]'].includes(location.hostname);", "const isLocal = true;")

            # 2. Fix the hardcoded http://localhost:8000 paths to be relative
            content = re.sub(r'http://localhost:8000/p\d\d/IMAGES/', './IMAGES/', content)

            # 3. For the specific files that don't even use isLocal fallback but hardcode Wikipedia URLs in JS
            content = content.replace("'https://upload.wikimedia.org/wikipedia/commons/4/4c/Rainbow_on_the_Azores_%E2%80%93_360%C2%B0_drone_shot.jpg'", "'./IMAGES/Moving_Forest_1050_700.webp'")
            content = content.replace('src="https://upload.wikimedia.org/wikipedia/commons/4/4c/Rainbow_on_the_Azores_%E2%80%93_360%C2%B0_drone_shot.jpg"', 'src="./IMAGES/Moving_Forest_1050_700.webp"')

            # Other ones in p02 over-XXX.html that just stick wikimedia stuff straight into <a-sky> 
            content = content.replace('https://upload.wikimedia.org/wikipedia/commons/2/23/Seattle_skyline_from_Kerry_Park.jpg', './IMAGES/Moving_Forest_1050_700.webp')
            content = content.replace('https://upload.wikimedia.org/wikipedia/commons/7/7d/Rainbow_on_the_Azores_%E2%80%93_360%C2%B0_drone_shot.jpg', './IMAGES/Moving_Forest_1050_700.webp')
            content = content.replace('https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Paris_-_Eiffelturm_und_Marsfeld2.jpg/1280px-Paris_-_Eiffelturm_und_Marsfeld2.jpg', './IMAGES/Moving_Forest_1050_700.webp')
            
            if original != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)

gentle_fix()
print("Gentle fix complete")
