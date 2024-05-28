# import os
# import pygame
# import pygame_gui
# from pygame_gui.elements import UISelectionList
#
# pygame.init()
#
# display = pygame.display.set_mode((800, 600))
# manager = pygame_gui.UIManager((800, 600))
# video_data = os.listdir('static')
# selectionlist = UISelectionList(pygame.Rect(10, 50, 174, 400),
#                        video_data,
#                        manager,
#                        allow_multi_select=False)
#
# clock = pygame.time.Clock()
#
# background = pygame.Surface((800, 600))
# background.fill(manager.get_theme().get_colour('dark_bg'))
#
# is_running = True
# while is_running:
#     time_delta = clock.tick(60) / 1000.0
#     for event in pygame.event.get():
#         if event.type != 1024:
#             print(event)
#         if event.type == pygame.QUIT:
#             is_running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.dict['button'] == 3:
#                 if selectionlist.hover_point(*pygame.mouse.get_pos()):
#                     print(555)
#
#         manager.process_events(event)
#
#     manager.update(time_delta)
#
#     display.blit(background, (0, 0))
#     manager.draw_ui(display)
#
#     pygame.display.update()


from flask import Flask, render_template

app = Flask(__name__)

# List of folder names
folders = ['xxx1', 'xxx2', 'xxx3']

@app.route('/')
def index():
    return render_template('index.html', folders=folders)

@app.route('/click/<folder>')
def image_click(folder):
    # Here you can run any function you want based on the image clicked.
    print(f'Image from folder {folder} clicked!')
    return f'Image from folder {folder} clicked!'

if __name__ == '__main__':
    app.run(debug=True)
