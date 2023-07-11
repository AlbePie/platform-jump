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
    global play, x_vel, y_vel
    play.x = 30
    play.y = 80
    x_vel = 0
    y_vel = 0
def next_level():
    global level, pos, level_blocks, block_type, levels, level_counter
    player_reset()
    sprites.destroy_all_sprites_of_kind(block_type)
    level += 1
    level_counter.count = level + 1
    if level >= levels.length:
        game.set_game_over_message(True, "YOU WIN")
        game.game_over(True)
    level_data = levels[level]
    pos = [0, 0]
    for line in level_data:
        pos[0] = 0
        for block in line:
            coord_x = pos[0] * 10 + 5
            coord_y = pos[1] * 10 + 5
            if block == "a":
                pass
            elif block == "b":
                block_sprite = sprites.create(img("""
                    f f f f f f f f f f
                    f f f f f f f f f f
                    f f f f f f f f f f
                    f f f f f f f f f f
                    f f f f f f f f f f
                    f f f f f f f f f f
                    f f f f f f f f f f
                    f f f f f f f f f f
                    f f f f f f f f f f
                    f f f f f f f f f f
                """),
                    block_type)
                block_sprite.x = coord_x
                block_sprite.y = coord_y
                level_blocks.push(block_sprite)
            pos[0] += 1
        pos[1] += 1
def Level(data: str):
    return data.split("\n")
def check_lr_max():
    global x_vel
    if x_vel > max_speed:
        x_vel = max_speed
    if x_vel < max_speed * -1:
        x_vel = max_speed * -1
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
max_speed = 8
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
bbbbbbbbbbbbbbbb"""), Level("""aaaaaaaaaaaaaaaa
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
bbbbbbbbbbbbbbbb""")]
level = -1
next_level()
ground:bool = False
ceiling:bool = False

def on_on_update():
    global y_vel, map_coord_x, map_coord_y, ground
    move_lr()
    check_lr_max()
    apply_friction()
    move_x(x_vel)
    y_vel += gravity
    if controller.up.is_pressed() or controller.A.is_pressed():
        if ground:
            y_vel = -6
            play.start_effect(effects.spray, 200)
    move_y(y_vel)

    if play.x > scene.screen_width():
        next_level()

def move_x(value):
    global divider
    divider = 4
    play.x += value / divider
    check(value, 0)

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
    global level_blocks, play, block_type
    for block in level_blocks:
        if play.overlaps_with(block) and block.kind() == block_type \
         or play.x < 8:
            play.x -= x / 4
            play.y -= y / 4
            if not stack == 63:
                check(x, y, stack + 1)
            else:
                pass
            return True
    return False

game.on_update(on_on_update)
