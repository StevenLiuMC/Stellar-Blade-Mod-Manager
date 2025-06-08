from PIL import Image
img = Image.open('icon.png')
img.save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])