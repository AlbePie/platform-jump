def apply_friction():
    global x_vel, y_vel
    x_vel = x_vel * 0.9
    y_vel = y_vel * 0.9
def move_lr():
    global x_vel
    if controller.left.is_pressed():
        x_vel += -1
    elif controller.right.is_pressed():
        x_vel += 1
def player_reset():
    global play, x_vel, y_vel, ground, ceiling
    play.x = 30
    play.y = 80
    x_vel, y_vel = 0, 0
    ground, ceiling = False, False
def show_level_text():
    global level_texts, level
    level_text = level_texts[level]
    if level_text:
        game.show_long_text(level_text, DialogLayout.TOP)
        if level == 0:
            game.show_long_text("You advance by being in the left edge", DialogLayout.TOP)
def next_level(reached_by_player):
    global level, pos, level_blocks, block_type, levels, \
    level_counter, playing, lava_type, level_texts, trampoline_type
    player_reset()
    sprites.destroy_all_sprites_of_kind(block_type)
    sprites.destroy_all_sprites_of_kind(lava_type)
    sprites.destroy_all_sprites_of_kind(trampoline_type)
    level += 1 if reached_by_player else 0
    level_counter.count = level + 1
    if level >= levels.length:
        game.set_game_over_message(True, "YOU WIN")
        music.stop_all_sounds()
        playing = False
        game.game_over(True)
    if reached_by_player:
        next_level_sound = music.create_song(assets.song("""level_win"""))
        music.play(next_level_sound, music.PlaybackMode.IN_BACKGROUND)
    level_data = levels[level]
    pos = [0, 0]
    for line in level_data:
        pos[0] = 0
        for block in line:
            coord_x = pos[0] * 10 + 5
            coord_y = pos[1] * 10 + 5
            if block == "a":
                pass
            else:
                if block == "b":
                    sprite= sprites.create(assets.image("""l_block"""),
                    block_type)
                elif block == "l":
                    sprite = sprites.create(assets.image("""l_lava"""),
                    lava_type)
                elif block == "t":
                    sprite = sprites.create(assets.image("""l_trampoline_upper_left"""),
                    trampoline_type)
                elif block == "r":
                    sprite = sprites.create(assets.image("""l_trampoline_upper_right"""),
                    trampoline_type)
                elif block == "m":
                    sprite = sprites.create(assets.image("""l_trampoline_bottom_left"""),
                    trampoline_type)
                elif block == "p":
                    sprite = sprites.create(assets.image("""l_trampoline_bottom_right"""),
                    trampoline_type)
                sprite.x = coord_x
                sprite.y = coord_y
                level_blocks.push(sprite)
            pos[0] += 1
        pos[1] += 1
    if reached_by_player:
        show_level_text()
def Level(data: str, text:str):
    global level_texts
    level_texts.push(text)
    return data.split("\n")
def check_lr_max():
    global x_vel
    if x_vel > max_speed:
        x_vel = max_speed
    if x_vel < max_speed * -1:
        x_vel = max_speed * -1
def play_song(show_text=False):
    global playing
    basscleff = music.create_song(assets.song("""basscleff"""))
    basscleff_volume = 100

    if playing:
        music.set_volume(basscleff_volume)
        music.play(basscleff, music.PlaybackMode.LOOPING_IN_BACKGROUND)
        if show_text:
            show_level_text()
            show_text = False
    else:
        return

playing = True
level_counter = sevenseg.create_counter(SegmentStyle.Thick, SegmentScale.Full, 2)
level_blocks:List[Sprite] = []
map_coord_y = 0
map_coord_x = 0
divider = 0
y_vel = 0
x_vel = 0
level = -1
max_speed = 0
pos: List[number] = []
lines: List[number] = []
gravity = 0.2
scene.set_background_image(sprites.background.cityscape)
play = sprites.create(assets.image("""player"""), SpriteKind.player)
block_type = SpriteKind.create()
lava_type = SpriteKind.create()
trampoline_type = SpriteKind.create()
max_speed = 8
level_texts:List[string] = []
levels = [Level("""aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb""", "You can move with left and right"), Level("""aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaabbaa
aaaaaaaaaaaabbaa
aaaaaaaaaaaabbaa
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb""", "You jump by pressing up or A"), Level("""aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaabbbb
aaaaabaaaaaaabbb
aaaaabbaaaaaaabb
aaaaaaaaaaaaaabb
aaaaaaaaaabbaabb
aaaaaaaaaabbaabb
aaaaaaaaaaaaaabb
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb""", "Parkour!"), Level("""aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaabaaaaaaba
aaaaaabbllllllbb
bbbbbbbbllllllbb
bbbbbbbbbbbbbbbb""", "If you die, you have to play the level again"), Level("""aaaaaaaaaaaaaabb
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaabbb
aaaaaaabbaaaaabb
aaaaaaaaaaaaaabb
aaaaaaaaaaaaaabb
aaaaaaaaaaaaabbb
aaaaaaabbaaabbbb
babbaaaaaaaaaabb
blllllllllllllbb
bbbbbbbbbbbbbbbb""", "Jump from the upper block"), Level("""aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaabb
aaaaaaaaaaaaaabb
aaaaaaaaaaaaaabb
aaaaaaaaaaaaaabb
aaaaaaaaaatraabb
aaaaaaaaaampaabb
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb""", "The trampoline boosts you up"), Level("""aaaaaaaaaaaaaaaa
aaaaaaaaabaaaaaa
aaaaaaaabblllb
aaaaaaabbblllbbb
aaaaaabbbbbbbbbb
aaaaaaaaaabaaabb
aaaaaaaaaaabaabb
aaaaatraaaaababb
aaaaampaaaaaabbb
bbbbbbbaaaaaaabb
blllllllllllllbb
bbbbbbbbbbbbbbbb""", "That's all from me, from now on you will continue playing alone"), Level("""aaaaaaaaaaaaaabb
aaaaaaaaaaaaaaab
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaabbbbbbbbbbb
aaaaaaaaaabaaabb
aaaaaaaaaaabaabb
aaaaaaaaaaaababb
aaaaatraaaaaabbb
aaaaampaaaaaaabb
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb""", ""), Level("""aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
llllllllllllllll
llllllllllllllll
aaaaaaaaaabbaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaatraaaaaa
aaaaaaaampaaaaaa
babbaaabbbbbaaab
bllllllllllllllb
bbbbbbbbbbbbbbbb""", ""), Level("""aaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaalbbbbbbbblllb
traaaaaaaaaaaaab
mpaaaaaaaaaaaaab
bbbbbbbbbbaaaaab
aaaaaaaaaaaaaaab
aaaaaaaaaaaaaaab
aaaaaaaaaaaaaaab
baaaaaaaabaatrab
blbblllbbbaampab
bbbbbbbbbbbbbbbb""", "")]
level = 0
next_level(False)
ground:bool = False
ceiling:bool = False
trampoline:number = 0

def on_on_update():
    global y_vel, map_coord_x, map_coord_y, ground, playing, trampoline
    if not playing:
        return
    move_lr()
    check_lr_max()
    apply_friction()
    move_x(x_vel)
    y_vel += gravity
    if controller.up.is_pressed() or controller.A.is_pressed():
        if ground:
            y_vel = -6
            for i in range(3):
                play.start_effect(effects.spray, 200)
            music.set_volume(80)
            jump_sound = music.create_song(assets.song("""jump"""))
            music.play(jump_sound, \
            music.PlaybackMode.IN_BACKGROUND)
    move_y(y_vel)

    if play.x > scene.screen_width():
        next_level(True)

def move_x(value):
    global divider
    divider = 4
    play.x += value / divider
    check(value, 0)

def boost_up():
    global y_vel, trampoline, play
    if trampoline >= 1:
        y_vel = -10
        play.start_effect(effects.spray, 200)
        if trampoline == 1:
            music.set_volume(40)
            trampoline_sound = music.create_song(assets.song("""trampoline_sound"""))
            music.play(trampoline_sound, \
            music.PlaybackMode.IN_BACKGROUND)

def move_y(value):
    global ground, ceiling, y_vel
    play.y += value

    ground, ceiling = False, False

    if check(0, value):
        if value > 0:
            ground = True
        elif value < 0:
            ceiling = True
        y_vel = 0

def check(x, y, stack = 0):
    global level_blocks, play, block_type, trampoline, trampoline_type
    go_back = play.x < 8
    was_in_trampoline = False
    for block in level_blocks:
        if Math.abs(block.x - play.x) > 16 or \
            Math.abs(block.y - play.y) > 16 or \
            not play.overlaps_with(block):
            continue
        if block.kind() == trampoline_type:
            was_in_trampoline = True
        elif block.kind() == lava_type:
            music.set_volume(80)
            lose_sound = music.create_song(assets.song("""level_lose"""))
            music.play(lose_sound, \
            music.PlaybackMode.IN_BACKGROUND)
            death_effect = sprites.create(img("""
                .
            """))
            death_effect.x = play.x
            death_effect.y = play.y
            player_reset()
            for i in range(5):
                death_effect.start_effect(effects.fountain, 500)
            sprites.destroy(death_effect)
        elif block.kind() == block_type:
            go_back = True
    
    if was_in_trampoline:
        trampoline += 1
        boost_up()
    else:
        trampoline = 0
    if go_back:
        play.x -= 0.5 * Math.sign(x)
        play.y -= 0.5 * Math.sign(y)
        if not stack == 63:
            check(x, y, stack + 1)
        else:
            pass
        return True

    return False

game.on_update(on_on_update)

play_song(True)