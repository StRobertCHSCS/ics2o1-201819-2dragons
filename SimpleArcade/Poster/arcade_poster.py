import arcade

WIDTH = 1280
HEIGHT = 720
my_button = [500, 50, 300, 100]
SPRITE_SCALING = 0.5

RECT_WIDTH = 150
RECT_HEIGHT = 50

center_x = 20      # Initial x position
delta_x = -1     # change in x


def on_update(delta_time):
    global center_x, center_y
    global delta_x, delta_y

    center_x += delta_x

    # Figure out if we hit the edge and need to reverse.
    if center_x < -20 or center_x >40:
        delta_x *= -1

def on_draw():
    arcade.start_render()
    # Draw in here...
    #arcade.draw_circle_filled(100, 100, 25, arcade.color.BLUE)
    arcade.start_render()
    # Draw in here...

    create_image("dirt.png", 0, -20, 1280, 740)
    create_image("kancolle_button.jpg", my_button[0],my_button[1],my_button[2],my_button[3])
    create_image("minecraft_logo.png", 450, 450, 400, 250)
    start_x = 300
    start_y = 400
    arcade.draw_text("The game you need to play during school", start_x, start_y, arcade.color.WHITE, 30, font_name='GARA')
    draw_minecraft_images(0)
    draw_minecraft_images(300)
    draw_minecraft_images(600)

def draw_minecraft_images(x):
    create_image("player.png", x+250, 200, 150, 200)
    create_image("ore.png", x+350, 200, 100, 100)
    create_pickaxe(x+220)


def create_image(texture, x, y, wid, ht):
    image = arcade.load_texture(texture, mirrored=False, scale=SPRITE_SCALING)
    arcade.draw_xywh_rectangle_textured(x, y, wid, ht, image, 0, 255, 1, 1)


def create_pickaxe(x):
    image = arcade.load_texture("pickaxe.png", mirrored=False, scale=SPRITE_SCALING)
    arcade.draw_xywh_rectangle_textured(x, 200, 150, 150, image, center_x, 255, 1, 1)


def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    # unpack the button list into readable? variables.
    my_button_x, my_button_y, my_button_w, my_button_h = my_button

    # Need to check all four limits of the button.
    if x > my_button_x and x < my_button_x + my_button_w and y > my_button_y and y < my_button_y + my_button_h:
        print("www.minecraft.net")
    else:
        pass
        #print("not clicked")


def setup():
    arcade.open_window(WIDTH, HEIGHT, "Minecraft マインクラフト")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press

    arcade.run()


if __name__ == '__main__':
    setup()