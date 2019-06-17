import arcade
from platform import system
import typing
import pyglet
import random
from arcade.monkey_patch_pyglet import *


class Sound:

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.player = pyglet.media.load(file_name)

    def play(self):
        if self.player.is_queued:
            player = pyglet.media.load(self.file_name)
            player.play()
        else:
            self.player.play()
class PlaysoundException(Exception):
    pass



def _load_sound_library():
    """
    Special code for Windows so we grab the proper avbin from our directory.
    Otherwise hope the correct package is installed.
    """

    # lazy loading
    if not _load_sound_library._sound_library_loaded:
        _load_sound_library._sound_library_loaded = True
    else:
        return

    import pyglet_ffmpeg2
    pyglet_ffmpeg2.load_ffmpeg()


# Initialize static function variable
_load_sound_library._sound_library_loaded = False


def load_sound(file_name: str):
    """
    Load a sound. Support for .wav files. If ffmpeg is available, will work
    with ogg and mp3 as well.

    :param str file_name: Name of the sound file to load.

    :returns: Sound object
    :rtype: Sound
    """

    try:
        sound = Sound(file_name)
        return sound
    except Exception as e:
        print("Unable to load {str}.", e)
        return None


def play_sound(sound: Sound):
    """
    Play a sound.

    :param Sound sound: Sound loaded by load_sound. Do NOT use a string here for the filename.
    """
    if sound is None:
        print("Unable to play sound, no data passed in.")
    elif isinstance(sound, str):
        raise Exception("Error, passed in a string as a sound. Make sure to use load_sound first, and use that result in play_sound.")
    try:
        sound.play()
    except Exception as e:
        print("Error playing sound.", e)



def stop_sound(sound: pyglet.media.Source):
    """
    Stop a sound that is currently playing.

    :param sound:
    """
    sound.pause()


_load_sound_library()

WIDTH = 1280
HEIGHT = 720
my_button = [700, 50, 565, 111]
button_1=[620, 395, 200,230]
button_2=[830, 395, 200,230]
button_3=[1040, 395, 200,230]
button_4=[620, 155, 200,230]
button_5=[830, 155, 200,230]
SPRITE_SCALING = 0.5

RECT_WIDTH = 150
RECT_HEIGHT = 50

pickaxe_x = 20
delta_angle = -1
timer=0
battle_start_sound=0
explosion_timer=1

center_x = 100      # Initial x position
center_y = 50       # Initial y position
delta_x = 10       # change in x
delta_y = 15
# change in y

battle=0
start_screen=1
formation_select=-1
start_battle=0
display_ships=0
enemy_location=[0, 0, 0, 0, 0, 0]
display_form=0
attacking_ship=0
x_ship=0
airattack=0
target_select=0
count=0
count2=0
countdmg=0
selection=0
music_timer=1
damage_timer=0
enemy_target=0
turn=0

plane_x=0
plane_y=0
torp_x=0
torp_y=0
launch_x=0
launch_y=0
form_screen=0
start_timer=0
attack_timer=0
ship_damage=1
crit_status=0
enemy_turn=0
enemy_attack_timer=0
x_enemy_ship=0
ship=0
win=0
finish_timer=0

form_dmg=[1, 0.8, 0.7, 0.75, 0.60]
form_aa=[1, 1.2, 1.6, 1, 1]
baim=[1, 1.2, 1, 1.2, 1.2]
torpaim=[1, 0.8, 0.4, 0.6, 0.3]
fs=[0.45, 0.6, 0.75, 0.6, 0.6]

enemy_maxhp=[150, 80, 60, 40, 20, 20]
enemy_hp=[150, 80, 60, 40, 20, 20]
maxhp=[30, 75, 30, 77, 50, 42]
hp=[30, 75, 30, 77, 50, 42]
dmg=[53, 131, 50, 82, 66, 60]
aa=[49, 66, 46, 55, 45, 23]

enemy_dmg=[140, 100, 82, 60, 50, 50]

torp=[77, 0, 86, 0, 0, 41]
arm=[49, 89, 49, 70, 39, 89]
scale=[656, 400, 660, 480, 405, 528]

kantai=load_sound("kancolle_music.mp3")

def on_update(delta_time):

    #plays music in a loop
    global music_timer
    global kantai
    if music_timer==1:
        play_sound(kantai)
    if music_timer==4200:
        music_timer=0
    music_timer+=1

def on_draw():
    arcade.start_render()
    global start_timer
    global form_screen
    global formation_select
    global display_ships
    global battle
    global airattack
    global attacking_ship
    global turn
    global enemy_turn
    global win

    # Draw in here...
    #arcade.draw_circle_filled(100, 100, 25, arcade.color.BLUE)
    arcade.start_render()
    # Draw in here...
    create_image("background.jpg", 0, 0, 1280, 720)

    #hides start screen when button is pressed
    if start_screen==1:
        create_image("start_screen.png", 0, 0, 1280, 720)

    if start_timer>0 and start_timer<=20:
        start_timer+=1
    if start_timer==20:
        form_screen=1

    if formation_select==0:
        create_image("select_form.png", 0, 0, 1280, 720)

    if formation_select>0:
        load_form_screen()


    if display_ships==1:
        show_ships()


    if battle==1:
        start_the_battle()


    if airattack==1:
        battle_turn()

    if enemy_turn==0:
        turn=attacking_ship
    else:
        turn=0
    for i in range(0, 5, 1):
        if enemy_hp[i]==0:
            enemy_dmg[i]=-999

    for i in range(0, 5, 1):
        if hp[i]==0:
            dmg[i]=-999

    if enemy_hp==[0, 0, 0, 0, 0, 0]:
        win=1
    elif hp==[1, 1, 1, 1, 1, 1]:
        win=-1


def attack(your_ship, enemy_ship):
    #calculates damage done to enemy ship

    global ship_damage
    global crit_status
    global display_form
    global damage_timer

    if damage_timer==1:
        ship_damage=dmg[your_ship-1]+random.randint(-5, 5)
        miss=random.randint(1, 100)
        crit=random.randint(1, 100)
        crit_status=0
        if miss>70*baim[display_form-1]:
            ship_damage=0
        elif crit<35:
            ship_damage*=5
            crit_status=1
        ship_damage//=5
    explosion(1050, 520-68*enemy_ship, ship_damage, enemy_ship, crit_status)


def enemy_attack(enemy_ship, your_ship):
    #calculates damage done to your ship

    global ship_damage
    global crit_status
    global display_form
    global damage_timer
    global enemy_dmg
    global enemy_attack_timer

    if enemy_attack_timer == 51:
        ship_damage = enemy_dmg[enemy_ship - 1] + random.randint(-5, 5)
        miss = random.randint(1, 100)
        crit = random.randint(1, 100)
        crit_status = 0
        if miss > 70:
            ship_damage = 0
        elif crit < 35:
            ship_damage *= 5
            crit_status = 1
        ship_damage //= 5
    if ship_damage>-11:
        explosion(135, 620 - 68 * your_ship, ship_damage, your_ship, crit_status)


def torp_launch():
    #launches torpedo at start of battle

    global torp_x
    global torp_y
    global launch_x
    global launch_y
    global count2
    if count2<30:
        create_image("torp.png", launch_x, launch_y, 60, 20)
    elif count2<60:
        torp_x+=(1320+launch_x)//300
        torp_y+=(enemy_location[1]+launch_y)//300
        image = arcade.load_texture("torpline.png", mirrored=False, scale=SPRITE_SCALING)
        arcade.draw_xywh_rectangle_textured(torp_x, torp_y, 200, 30, image, 15, 255, 1, 1)
    elif count2<95:
        explosion(torp_x+200, torp_y, 75, 2, 1)
    count2+=1

def air_raid(start, end):
    #lauches planes at start of battle

    global count
    global plane_x
    global plane_y
    y=600-68*start
    count+=1
    plane_x=count*1320//200
    plane_y=y+count*(enemy_location[end-1]-y)//200
    create_image("aircraft.png", plane_x, plane_y, 100, 100)
    create_image("aircraft.png", plane_x+40, plane_y+40, 100, 100)
    create_image("aircraft.png", plane_x-40, plane_y-40, 100, 100)


def explosion(x, y, damage, ship, crit):
    #shows explosion animation and does damage to ship

    global explosion_timer
    global hp
    global enemy_hp
    if damage>200:
        damage//=200
    if damage<0:
        damage=0
    if explosion_timer<26:
        create_image("explosion ("+str(explosion_timer)+").png", x, y, 200, 200)
    if explosion_timer==1:
        if crit==0:
            sound=load_sound("damage.ogg")
        else:
            sound=load_sound("critical_damage.ogg")
        play_sound(sound)

    if explosion_timer>0 and explosion_timer<26:
        if x<500:
            if damage!=0:
                if crit==0:
                    arcade.draw_text(str(int(damage)), x+80, y+30, arcade.color.RED, 30)
                else:
                    arcade.draw_text(str(int(damage)), x+80, y+30, arcade.color.YELLOW, 30)
                    arcade.draw_text("Critical Hit!", x+50, y, arcade.color.YELLOW, 30)
                if explosion_timer==5:
                    hp[ship-1]-=damage
            else:
                arcade.draw_text("miss", x+80, y+30, arcade.color.RED, 30)
        else:
            if damage!=0:
                if crit==0:
                    arcade.draw_text(str(damage), x+80, y+30, arcade.color.RED, 30)
                else:
                    arcade.draw_text(str(damage), x+80, y+30, arcade.color.YELLOW, 30)
                    arcade.draw_text("Critical Hit!", x+50, y, arcade.color.YELLOW, 30)
                if explosion_timer==5:
                    enemy_hp[ship-1]-=damage
                    if enemy_hp[ship-1]<0:
                        enemy_dmg[ship-1]=0
            else:
                arcade.draw_text("miss", x+80, y+30, arcade.color.RED, 30)


    if explosion_timer==36:
        explosion_timer=0
    explosion_timer+=1

def load_form_screen():
    #loads formation selection screen

    global battle_start_sound
    global timer
    global formation_select
    global start_battle
    global display_form
    global display_ships
    global form_screen

    form_screen = 0
    if battle_start_sound == 0:
        sound = load_sound("FubukiKai-Starting_A_Sortie.ogg")
        battle_start_sound = 1
        play_sound(sound)
        timer=1
    if timer <= 406 and timer >= 0:
        create_image("new_battle_anims(" + str(timer) + ").png", 0, 0, 1280, 720)
        if timer == 334:
            sound = load_sound("Akagi-Air_Battle.ogg")
            play_sound(sound)
        if timer == 120:
            sound = load_sound("FubukiKai-Battle_Start.ogg")
            play_sound(sound)
        timer += 1
    else:
        timer = 0
        start_battle = 1
        for i in range(5):
            dmg[i] *= form_dmg[formation_select - 1]
        for i in range(5):
            aa[i] *= form_aa[formation_select - 1]
        display_form = formation_select
        formation_select = -1
        display_ships = 1


def show_ships():
    #displays ships

    global battle
    global x_ship
    global hp
    global maxhp
    global enemy_hp
    global attacking_ship
    global enemy_location
    global x_enemy_ship
    global turn
    global enemy_turn
    global enemy_maxhp

    for i in range(1, 7, 1):
        if turn == i and enemy_turn==0:
            x_ship = 50
        else:
            x_ship = 0
        create_image("ship(" + str(i) + ").png", x_ship, 610 - 68 * i, 270, 65)

        if hp[i - 1] <= 1:
            hp[i - 1] = 1

        if hp[i - 1] <= maxhp[i - 1] // 4:
            arcade.draw_text("heavy", 170 + x_ship, 650 - 68 * i, arcade.color.RED, 20)
            arcade.draw_text("damage", 170 + x_ship, 620 - 68 * i, arcade.color.RED, 20)
        elif hp[i - 1] <= maxhp[i - 1] // 2:
            arcade.draw_text("medium", 170 + x_ship, 650 - 68 * i, arcade.color.ORANGE, 20)
            arcade.draw_text("damage", 170 + x_ship, 620 - 68 * i, arcade.color.ORANGE, 20)
        elif hp[i - 1] <= maxhp[i - 1]*3 // 4:
            arcade.draw_text("light", 170 + x_ship, 650 - 68 * i, arcade.color.YELLOW, 20)
            arcade.draw_text("damage", 170 + x_ship, 620 - 68 * i, arcade.color.YELLOW, 20)

        arcade.draw_text(str(int(hp[i - 1])) + "/" + str(maxhp[i - 1]), 285 + x_ship, 630 - 68 * i, arcade.color.WHITE, 20)

    for i in range(1, 7, 1):
        if attacking_ship == i and enemy_turn==1:
            x_enemy_ship = 50
        else:
            x_enemy_ship = 0
        create_image("Enemy" + str(i) + ".png", 1010-x_enemy_ship, 510 - 68 * i, 270, 65)
        enemy_location[i - 1] = 510 - 68 * i
        if enemy_hp[i - 1] <= 0:
            enemy_hp[i - 1] = 0
            arcade.draw_text("sunk", 1200 + x_enemy_ship, 520 - 68 * i, arcade.color.LIGHT_BLUE, 30)
        elif enemy_hp[i - 1] <= enemy_maxhp[i - 1] // 4:
            arcade.draw_text("heavy", 1170 + x_enemy_ship, 550 - 68 * i, arcade.color.RED, 20)
            arcade.draw_text("damage", 1170 + x_enemy_ship, 520 - 68 * i, arcade.color.RED, 20)

        elif enemy_hp[i - 1] <= enemy_maxhp[i - 1] // 2:
            arcade.draw_text("medium", 1170 + x_enemy_ship, 550 - 68 * i, arcade.color.ORANGE, 20)
            arcade.draw_text("damage", 1170 + x_enemy_ship, 520 - 68 * i, arcade.color.ORANGE, 20)

        elif enemy_hp[i - 1] <= enemy_maxhp[i - 1]*3 // 4:
            arcade.draw_text("light", 1170 + x_enemy_ship, 550 - 68 * i, arcade.color.YELLOW, 20)
            arcade.draw_text("damage", 1170 + x_enemy_ship, 520 - 68 * i, arcade.color.YELLOW, 20)

        arcade.draw_text(str(int(enemy_hp[i - 1])) + "/" + str(enemy_maxhp[i - 1]), 900-x_enemy_ship, 530 - 68 * i, arcade.color.WHITE, 20)
    battle = 1


def start_the_battle():
    #launches attack at start of battle

    global airattack
    global timer
    global launch_x
    global launch_y
    global torp_x
    global torp_y
    global attacking_ship

    image = arcade.load_texture("Form" + str(display_form) + ".png", mirrored=False, scale=SPRITE_SCALING)
    arcade.draw_xywh_rectangle_textured(50, 50, 125, 125, image, 90, 255, 1, 1)
    if airattack == 0:
        if timer <= 199:
            air_raid(4, 2)
            air_raid(5, 2)
            timer += 1
            if timer == 50:
                launch_x = torp_x = plane_x
                launch_y = torp_y = plane_y
            if timer > 50:
                torp_launch()
        else:
            airattack = 1
            timer = 0
            attacking_ship = 0


def battle_turn():
    #allows you and the enemy to attack

    global timer
    global selection
    global attacking_ship
    global target_select
    global attack_timer
    global enemy_turn
    global enemy_attack_timer
    global ship
    global win

    if win==0:
        if timer==0:
            attacking_ship += 1
            if attacking_ship>6 or attacking_ship<1:
                attacking_ship = 1

        if timer == 50:
            if enemy_turn==0:
                selection = 1
                if hp[attacking_ship-1]==1:
                    enemy_turn=1
            timer+=1
        elif timer==51:

            if target_select > 0:
                if attack_timer<50:
                    create_image(str(attacking_ship)+".png", -500, -700, 1400, 1400)
                if attack_timer == 5:
                    ship_voice = load_sound("attack" + str(attacking_ship) + ".ogg")
                    play_sound(ship_voice)
                if attacking_ship == 4 or attacking_ship == 5:
                    air_battle()
                else:
                    attack_anims()
                if attacking_ship==7:
                    attacking_ship=1

            if enemy_turn == 1:
                enemy_fire()

        else:
            timer += 1
    elif win==1:
        victory()
    elif win==-1:
        lost()


def victory():
    #win screen

    create_image("victory.png", 0, 0, 1280, 720)
    arcade.draw_text("Victory", 500, 650, arcade.color.YELLOW, 60)

def lost():
    #lose screen
    create_image("defeat.png", 0, 0, 1280, 720)
    arcade.draw_text("Defeat", 500, 650, arcade.color.RED, 60)

def air_battle():
    #animations for air attacks

    global attack_timer
    global damage_timer
    global target_select
    global explosion_timer
    global enemy_turn
    global count
    global attacking_ship
    global turn
    global timer

    attack_timer += 1
    if attack_timer == 5:
        count = 0
    if attack_timer < 105 and attack_timer > 5:
        air_raid(attacking_ship, target_select)
    if attack_timer > 100 and attack_timer < 135:
        damage_timer += 1
        attack(attacking_ship, target_select)
    if attack_timer >= 140:
        explosion_timer = 1
        target_select = 0
        attack_timer = 0
        damage_timer = 0
        ship=attacking_ship-1
        if ship==-1:
            ship=5
        if enemy_hp[ship]>0:
            enemy_turn = 1
        else:
            timer=0

    count += 1


def attack_anims():
    #animations for normal attacks
    global attack_timer
    global damage_timer
    global target_select
    global attacking_ship
    global explosion_timer
    global enemy_turn
    global turn
    global timer

    attack_timer += 1

    if attack_timer > 50 and attack_timer < 85:
        damage_timer += 1
        attack(attacking_ship, target_select)
    if attack_timer == 90:
        explosion_timer = 1
        target_select = 0
        attack_timer = 0
        damage_timer = 0
        ship = attacking_ship - 1
        if ship == -1:
            ship = 5
        if enemy_hp[ship] > 0:
            enemy_turn = 1
        else:
            timer=0



def enemy_fire():
    #animations and target selection for enemy attacks
    global enemy_attack_timer
    global enemy_target
    global enemy_turn
    global attacking_ship
    global timer

    if enemy_attack_timer==1:
        flagship = 0
        while True:
            enemy_target = random.randint(1 + flagship, 6)
            if hp[enemy_target - 1] > 1:
                if enemy_target == 1:
                    if random.randint(1, 100) > fs[display_form-1]:
                        break
                    else:
                        flagship = 1
                else:
                    break
            if hp==[1, 1, 1, 1, 1, 1]:
                break
    if enemy_attack_timer > 50 and enemy_attack_timer < 85:
        enemy_attack(attacking_ship, enemy_target)
    elif enemy_attack_timer==85:
        enemy_attack_timer=0
        enemy_turn=0
        timer=0
    enemy_attack_timer+= 1


def create_image(texture, x, y, wid, ht):
    #creats an image
    try:
        image = arcade.load_texture(texture, mirrored=False, scale=SPRITE_SCALING)
        arcade.draw_xywh_rectangle_textured(x, y, wid, ht, image, 0, 255, 1, 1)
    except:
        pass


def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    #input

    global form_screen
    global start_screen
    global formation_select
    global battle
    global target_select
    global selection
    global start_timer
    global attacking_ship
    global hp

    # unpack the button list into readable? variables.
    my_button_x, my_button_y, my_button_w, my_button_h = my_button
    my_button_1_x, my_button_1_y, my_button_1_w, my_button_1_h = button_1
    my_button_2_x, my_button_2_y, my_button_2_w, my_button_2_h = button_2
    my_button_3_x, my_button_3_y, my_button_3_w, my_button_3_h = button_3
    my_button_4_x, my_button_4_y, my_button_4_w, my_button_4_h = button_4
    my_button_5_x, my_button_5_y, my_button_5_w, my_button_5_h = button_5

    #check if start button is pressed
    if x > my_button_x and x < my_button_x + my_button_w and y > my_button_y and y < my_button_y + my_button_h:
        if start_screen==1:
            start_screen=0
            formation_select=0
            start_timer+=1

    #get formation selection
    if(form_screen==1):
        if x > my_button_1_x and x < my_button_1_x + my_button_1_w and y > my_button_1_y and y < my_button_1_y + my_button_1_h:
            formation_select=1

        if x > my_button_2_x and x < my_button_2_x + my_button_2_w and y > my_button_2_y and y < my_button_2_y + my_button_2_h:
            formation_select=2

        if x > my_button_3_x and x < my_button_3_x + my_button_3_w and y > my_button_3_y and y < my_button_3_y + my_button_3_h:
            formation_select=3
        if x > my_button_4_x and x < my_button_4_x + my_button_4_w and y > my_button_4_y and y < my_button_4_y + my_button_4_h:
            formation_select=4
        if x > my_button_5_x and x < my_button_5_x + my_button_5_w and y > my_button_5_y and y < my_button_5_y + my_button_5_h:
            formation_select=5

    #get target selection
    if selection==1 and target_select==0 and hp[attacking_ship-1]>1:
        if x > 1010 and x < 1010+270 and y > enemy_location[0] and y < enemy_location[0]+65 and enemy_hp[0]>0:
            target_select=1
            selection=0

        if x > 1010 and x < 1010+270 and y > enemy_location[1] and y < enemy_location[1]+65 and enemy_hp[1]>0:
            target_select=2
            selection=0

        if x > 1010 and x < 1010+270 and y > enemy_location[2] and y < enemy_location[2]+65 and enemy_hp[2]>0:
            target_select=3
            selection=0

        if x > 1010 and x < 1010+270 and y > enemy_location[3] and y < enemy_location[3]+65 and enemy_hp[3]>0:
            target_select=4
            selection=0

        if x > 1010 and x < 1010+270 and y > enemy_location[4] and y < enemy_location[4]+65 and enemy_hp[4]>0:
            target_select=5
            selection=0

        if x > 1010 and x < 1010+270 and y > enemy_location[5] and y < enemy_location[5]+65 and enemy_hp[5]>0:
            target_select=6
            selection=0




def setup():
    arcade.open_window(WIDTH, HEIGHT, "Python Kancolle")
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
