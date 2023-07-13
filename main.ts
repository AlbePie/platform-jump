function apply_friction() {
    
    x_vel = x_vel * 0.9
    y_vel = y_vel * 0.9
}

function move_lr() {
    
    if (controller.left.isPressed()) {
        x_vel += -1
    } else if (controller.right.isPressed()) {
        x_vel += 1
    }
    
}

function player_reset() {
    
    play.x = 30
    play.y = 80
    let ___tempvar10 = [0, 0]
    x_vel = ___tempvar10[0]
    y_vel = ___tempvar10[1]
    let ___tempvar11 = [false, false]
    ground = ___tempvar11[0]
    ceiling = ___tempvar11[1]
}

function show_level_text() {
    
    let level_text = level_texts[level]
    if (level_text) {
        game.showLongText(level_text, DialogLayout.Top)
        if (level == 0) {
            game.showLongText("You advance by being in the left edge", DialogLayout.Top)
        }
        
    }
    
}

function next_level(reached_by_player: boolean) {
    let next_level_sound: music.Playable;
    let coord_x: number;
    let coord_y: number;
    let sprite: Sprite;
    
    player_reset()
    sprites.destroyAllSpritesOfKind(block_type)
    sprites.destroyAllSpritesOfKind(lava_type)
    level += reached_by_player ? 1 : 0
    level_counter.count = level + 1
    if (level >= levels.length) {
        game.setGameOverMessage(true, "YOU WIN")
        music.stopAllSounds()
        playing = false
        game.gameOver(true)
    }
    
    if (reached_by_player) {
        next_level_sound = music.createSong(assets.song`level_win`)
        music.play(next_level_sound, music.PlaybackMode.InBackground)
    }
    
    let level_data = levels[level]
    pos = [0, 0]
    for (let line of level_data) {
        pos[0] = 0
        for (let block of line) {
            coord_x = pos[0] * 10 + 5
            coord_y = pos[1] * 10 + 5
            if (block == "a") {
                
            } else {
                if (block == "b") {
                    sprite = sprites.create(assets.image`l_block`, block_type)
                } else if (block == "l") {
                    sprite = sprites.create(assets.image`l_lava`, lava_type)
                } else if (block == "t") {
                    sprite = sprites.create(assets.image`l_trampoline_upper_left`, trampoline_type)
                } else if (block == "r") {
                    sprite = sprites.create(assets.image`l_trampoline_upper_right`, trampoline_type)
                } else if (block == "m") {
                    sprite = sprites.create(assets.image`l_trampoline_bottom_left`, trampoline_type)
                } else if (block == "p") {
                    sprite = sprites.create(assets.image`l_trampoline_bottom_right`, trampoline_type)
                }
                
                sprite.x = coord_x
                sprite.y = coord_y
                level_blocks.push(sprite)
            }
            
            pos[0] += 1
        }
        pos[1] += 1
    }
    if (reached_by_player) {
        show_level_text()
    }
    
}

function Level(data: string, text: string): string[] {
    
    level_texts.push(text)
    return data.split("\n")
}

function check_lr_max() {
    
    if (x_vel > max_speed) {
        x_vel = max_speed
    }
    
    if (x_vel < max_speed * -1) {
        x_vel = max_speed * -1
    }
    
}

function play_song(show_text: boolean = false) {
    
    let basscleff = music.createSong(assets.song`basscleff`)
    let basscleff_volume = 100
    if (playing) {
        music.setVolume(basscleff_volume)
        music.play(basscleff, music.PlaybackMode.LoopingInBackground)
        if (show_text) {
            show_level_text()
            show_text = false
        }
        
    } else {
        return
    }
    
}

let playing = true
let level_counter = sevenseg.createCounter(SegmentStyle.Thick, SegmentScale.Full, 2)
let level_blocks : Sprite[] = []
let map_coord_y = 0
let map_coord_x = 0
let divider = 0
let y_vel = 0
let x_vel = 0
let level = -1
let max_speed = 0
let pos : number[] = []
let lines : number[] = []
let gravity = 0.2
scene.setBackgroundImage(sprites.background.cityscape)
let play = sprites.create(assets.image`player`, SpriteKind.Player)
let block_type = SpriteKind.create()
let lava_type = SpriteKind.create()
let trampoline_type = SpriteKind.create()
max_speed = 8
let level_texts : string[] = []
let levels = [Level(`aaaaaaaaaaaaaaaa
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
bbbbbbbbbbbbbbbb`, "You can move with left and right"), Level(`aaaaaaaaaaaaaaaa
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
bbbbbbbbbbbbbbbb`, "You jump by pressing up or A"), Level(`aaaaaaaaaaaaaaaa
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
bbbbbbbbbbbbbbbb`, "Parkour!"), Level(`aaaaaaaaaaaaaaaa
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
bbbbbbbbbbbbbbbb`, "If you die, you have to play the level again"), Level(`aaaaaaaaaaaaaabb
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
bbbbbbbbbbbbbbbb`, "Jump from the upper block"), Level(`aaaaaaaaaaaaaaaa
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
bbbbbbbbbbbbbbbb`, "The trampoline boosts you up")]
level = 0
next_level(false)
let ground = false
let ceiling = false
let trampoline = 0
function move_x(value: number) {
    
    divider = 4
    play.x += value / divider
    check(value, 0)
}

function boost_up() {
    let trampoline_sound: music.Playable;
    
    if (trampoline >= 1) {
        y_vel = -10
        play.startEffect(effects.spray, 200)
        if (trampoline == 1) {
            music.setVolume(40)
            trampoline_sound = music.createSong(assets.song`trampoline_sound`)
            music.play(trampoline_sound, music.PlaybackMode.InBackground)
        }
        
    }
    
}

function move_y(value: number) {
    
    play.y += value
    let ___tempvar5 = [false, false]
    ground = ___tempvar5[0]
    ceiling = ___tempvar5[1]
    if (check(0, value)) {
        if (value > 0) {
            ground = true
        } else if (value < 0) {
            ceiling = true
        }
        
        y_vel = 0
    }
    
}

function check(x: number, y: number, stack: number = 0): boolean {
    let lose_sound: music.Playable;
    let death_effect: Sprite;
    
    let go_back = false
    let was_in_trampoline = false
    for (let block of level_blocks) {
        if (play.overlapsWith(block) && block.kind() == trampoline_type) {
            was_in_trampoline = true
        } else if (play.overlapsWith(block) && block.kind() == lava_type) {
            music.setVolume(80)
            lose_sound = music.createSong(assets.song`level_lose`)
            music.play(lose_sound, music.PlaybackMode.InBackground)
            death_effect = sprites.create(img`
                .
            `)
            death_effect.x = play.x
            death_effect.y = play.y
            player_reset()
            for (let i = 0; i < 5; i++) {
                death_effect.startEffect(effects.fountain, 500)
            }
            sprites.destroy(death_effect)
        } else if (play.overlapsWith(block) && block.kind() == block_type || play.x < 8) {
            go_back = true
        }
        
    }
    if (was_in_trampoline) {
        trampoline += 1
        boost_up()
    } else {
        trampoline = 0
        console.log(trampoline)
    }
    
    if (go_back) {
        play.x -= 0.5 * Math.sign(x)
        play.y -= 0.5 * Math.sign(y)
        if (!(stack == 63)) {
            check(x, y, stack + 1)
        } else {
            
        }
        
        return true
    }
    
    return false
}

game.onUpdate(function on_on_update() {
    let jump_sound: music.Playable;
    
    if (!playing) {
        return
    }
    
    move_lr()
    check_lr_max()
    apply_friction()
    move_x(x_vel)
    y_vel += gravity
    if (controller.up.isPressed() || controller.A.isPressed()) {
        if (ground) {
            y_vel = -6
            for (let i = 0; i < 3; i++) {
                play.startEffect(effects.spray, 200)
            }
            music.setVolume(80)
            jump_sound = music.createSong(assets.song`jump`)
            music.play(jump_sound, music.PlaybackMode.InBackground)
        }
        
    }
    
    move_y(y_vel)
    if (play.x > scene.screenWidth()) {
        next_level(true)
    }
    
})
play_song(true)
