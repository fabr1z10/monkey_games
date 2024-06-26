import monkey
from . import data
from . import settings
from . import ui
from . import factory

def makeText(id, pal):
    msg = monkey.Text('text', 'c64', data.strings[id], pal=pal)
    msg.set_position(0, 200, 0)
    return msg

def disable_ui():
    monkey.get_node(settings.id_ui).state = monkey.NodeState.INACTIVE
    settings.ui_enabled = False

def enable_ui():
    monkey.get_node(settings.id_ui).state = monkey.NodeState.ACTIVE
    settings.ui_enabled = True


def walkToItem(script, *args):
    item_info = data.getItem(args[0])
    walkto = item_info.get('walk_to', None)
    if not walkto:
        node = monkey.get_node(data.tag_to_id[args[0]])
        walkto = (node.x, node.y)
    walkdir = item_info.get('walk_dir', None)
    script.add(monkey.actions.Walk(data.tag_to_id['player'], walkto))
    if walkdir:
        script.add(monkey.actions.Turn(data.tag_to_id['player'], walkdir))

def walkToCharacter(script, *args):
    idp = data.tag_to_id['player']
    node = monkey.get_node(data.tag_to_id[args[0]])
    player = monkey.get_node(idp)
    if player.x > node.x:
        script.add(monkey.actions.Walk(idp, (node.x + 30, node.y)))
    script.add(monkey.actions.Turn(data.tag_to_id['player'], 'w'))


def addToInventory(item):
    def f():
        inv = data.inventory[settings.characters[settings.player]]
        if item in inv:
            return
        monkey.get_node(data.tag_to_id[item]).remove()
        data.inventory[settings.characters[settings.player]].append(item)
        ui.refresh_inventory()
    return f



def addText(msg):
    def f():
        textNode = monkey.get_node(settings.id_msg)
        textNode.add(msg)
    return f

def message(script, x, pal):
    msg = makeText(x, pal)
    script.add(monkey.actions.CallFunc(addText(msg)))
    script.add(monkey.actions.Delay(1))
    script.add(monkey.actions.CallFunc(lambda: msg.remove()))

def goto_room(room, pos, dir):
    def f():
        p = data.getItem(settings.characters[settings.player])
        p['room'] = room
        p['pos'] = pos
        p['direction'] = dir
        settings.room = room
        monkey.close_room()
    return f

def cut_scene(room, script):
    def f():
        settings.room = room
        settings.start_script = script
        monkey.close_room()
    return f

def kolpo(x):
    player = monkey.get_node(data.tag_to_id['player'])
    if abs(player.y-x.node.y) > 1.0:
        x.goto([x.node.x, player.y])


def say(script, *args):
    sayc(script, 'player', *args)
    # id = data.tag_to_id['player']
    # script.add(monkey.actions.CallFunc(lambda: monkey.get_node(id).sendMessage(id="animate", anim="talk")))
    # for x in args:
    #     message(script, x)
    # script.add(monkey.actions.CallFunc(lambda: monkey.get_node(id).sendMessage(id="animate", anim="quiet")))

def sayc(script, *args):
    id = data.tag_to_id[args[0]]
    cid = settings.characters[settings.player] if args[0] == 'player' else args[0]
    pal = data.items['items'][cid]['text_color']
    script.add(monkey.actions.CallFunc(lambda: monkey.get_node(id).sendMessage(id="animate", anim="talk")))
    for x in args[1:]:
        message(script, x, pal)
    script.add(monkey.actions.CallFunc(lambda: monkey.get_node(id).sendMessage(id="animate", anim="quiet")))

def saycn(script, *args):
    id = data.tag_to_id[args[0]]
    cid = settings.characters[settings.player] if args[0] == 'player' else args[0]
    pal = data.items['items'][cid]['text_color']
    for x in args[1:]:
        message(script, x, pal)

def talk_char(script, *args):
    id = data.tag_to_id[args[0]]
    script.add(monkey.actions.Animate(id=id, anim=args[1]))
    for x in args[3:]:
        message(script, x)
    script.add(monkey.actions.Animate(id=id, anim=args[2]))



def _read(script):
    say(script, 24)

def _push(script):
    say(script, 25)

def _open(script):
    say(script, 26)

def _close(script):
    say(script, 27)

def _pickup(script):
    say(script, 75)

def pickup(script, item, callback=None):
    data.getItem(item)['active'] = False
    script.add(monkey.actions.CallFunc(addToInventory(item)))
    if callback:
        globals()[callback](script)




_pull = _push
_turnon = _close
_turnoff = _close
_use = _close



def change_room(script, *args):
    script.add(monkey.actions.CallFunc(goto_room(*args)))


def pull_doormat(script, *args):
    def f():
        data.doormat = 'open'
        doormat = monkey.get_node(data.tag_to_id['doormat'])
        doormat.setAnimation('open')
        doormat.getMouseArea().setShape(monkey.shapes.AABB(0,64,0,8))

    if data.doormat == 'open':
        say(script, 22)
    else:
        script.add(monkey.actions.CallFunc(f))

def change_door_state(script, *args):
    # pass tag, state, variable
    setattr(data, args[2], args[1])
    #node = monkey.get_node(data.tag_to_id[args[0]])
    script.add(monkey.actions.Animate(data.tag_to_id[args[0]], args[1]))

def walkto_door(script, *args):
    # pass tag, variable
    if getattr(data, args[0]) == 'open':
        print('DOOR OPEN')
        change_room(script, *args[1:])
    else:
        print('DOOR CLOSED')

def rm(script, *args):
    script.add(monkey.actions.CallFunc(lambda: monkey.get_node(data.tag_to_id[args[0]]).remove()))


def push_doormat(script, *args):
    def f():
        data.doormat = 'closed'
        doormat = monkey.get_node(data.tag_to_id['doormat'])
        doormat.setAnimation('closed')
        doormat.getMouseArea().setShape(monkey.shapes.AABB(0,88,0,8))

    if data.doormat == 'open':
        script.add(monkey.actions.CallFunc(f))

def open_main_door(script, *args):
    if not data.maindoor_unlocked:
        say(script, 29)
    else:
        change_door_state(script, 'door_main', 'open', 'door_main')

def unlock_main_door(script, *args):
    data.maindoor_unlocked = True
    change_door_state(script, 'door_main', 'open', 'door_main')

def updateNodeState(id, state):
    if id in data.tag_to_id:
        node = monkey.get_node(data.tag_to_id[id])
        if node:
            node.state = state#monkey.NodeState.ACTIVE

def open_fridge(script, *args):
    change_door_state(script,'refrigerator', 'open', 'fridge')
    for a in ['cheese', 'batteries', 'lettuce', 'pepsi', 'ketchup']:
        updateNodeState(a, monkey.NodeState.ACTIVE)

def close_fridge(script, *args):
    change_door_state(script,'refrigerator', 'closed', 'fridge')
    for a in ['cheese', 'batteries', 'lettuce', 'pepsi', 'ketchup']:
        updateNodeState(a, monkey.NodeState.INACTIVE)

def open_panel(script, *args):
    change_door_state(script,'loose_panel', 'open', 'loose_panel')
    for a in ['cassette_tape']:
        updateNodeState(a, monkey.NodeState.ACTIVE)

def turn_on_tv(script, *args):
    script.add(monkey.actions.Animate(id=data.tag_to_id['tv'], anim='on'))
    script.add(monkey.actions.CallFunc(disable_ui))
    script.add(monkey.actions.Delay(2))
    script.add(monkey.actions.CallFunc(cut_scene('tv', 'pippo')))

def pippo():
    disable_ui()
    s = monkey.Script()
    mark_eteer = monkey.get_sprite('sprites/mark_eteer')
    mark_eteer.set_position(147, 56, 1)
    data.tag_to_id['mark_eteer'] = mark_eteer.id
    s.add(monkey.actions.Add(settings.id_game, mark_eteer))
    talk_char(s, 'mark_eteer', 'talk_s', 'idle_s', 85, 86, 87, 88, 89, 90)
    monkey.play(s)

def close_panel(script, *args):
    change_door_state(script,'loose_panel', 'closed', 'loose_panel')
    for a in ['cassette_tape']:
        updateNodeState(a, monkey.NodeState.INACTIVE)



def push_gargoyle(script, *args):
    change_door_state(script, 'door_entrance_reactor', 'open', 'door_reactor')
    def f():
        s = monkey.Script()
        change_door_state(s, 'door_entrance_reactor', 'closed', 'door_reactor')
        monkey.play(s)
    data.delayed_funcs[settings.characters[settings.player]] = f


def switch_light(script, room, value):
    def g():
        setattr(data, "light_" + room, value)
        nodes = monkey.get_node(settings.id_game).getNodes(True)
        for n in nodes:
            print('=== AA ===',n.id)
            n.setPalette('default' if value else 'dark')
    print('FIGAMERDA!!!!XX')
    script.add(monkey.actions.CallFunc(g))

def move_item(item, charFrom, charTo):
    def f():
        data.inventory[charFrom].remove(item)
        data.inventory[charTo].append(item)
    return f

def drop_item(item, charFrom):
    def f():
        data.inventory[charFrom].remove(item)
    return f


def hit_green_tentacle_stop(obj,player):
    settings.ui_enabled = False
    def ciao():
        settings.ui_enabled = True
    settings.ui_enabled = False
    script = monkey.Script(id="__player")
    print(player.id,player.x,player.y)
    if data.pass_green_tentacle==0:
        saycn(script, 'green_tentacle', 104 if data.food_given_to_gt else 98)
        data.pass_green_tentacle = 1
    else:
        say(script, 99)
    script.add(monkey.actions.Walk(player.id, (player.x + 50, player.y)), after=[0])
    script.add(monkey.actions.Turn(player.id, 'w'))
    script.add(monkey.actions.CallFunc(ciao))
    monkey.play(script)

def on_start_staircase():
    data.pass_green_tentacle = 0
    print ('ZXXXXX')

def give_green_tentacle_wax_fruit(script):
    script.add(monkey.actions.CallFunc(drop_item(settings.item1, settings.characters[settings.player])))
    script.add(monkey.actions.CallFunc(ui.refresh_inventory))
    data.food_given_to_gt = True
    data.pass_green_tentacle = 0
    saycn(script, 'green_tentacle', 101, 103)

def give_green_tentacle_fruit_drinks(script):
    if not data.food_given_to_gt:
        saycn(script, 'green_tentacle', 100)
    else:
        saycn(script, 'green_tentacle', 105)
        data.drink_given_to_gt = True
        monkey.get_node(data.tag_to_id['green_tentacle_stop']).remove()
        gt = monkey.get_node(data.tag_to_id['green_tentacle'])
        gt.getController().setCallback(lambda x: None)
        script.add(monkey.actions.Walk(gt.id, [138,29]))


def use_hunkomatic(script, *args):
    script.add(monkey.actions.CallFunc(disable_ui))
    for i in range(0,3):
        script.add(monkey.actions.Animate(data.tag_to_id['hunkomatic'], 'default'))
        script.add(monkey.actions.Delay(1))
        script.add(monkey.actions.Animate(data.tag_to_id['hunkomatic'], 'lift'))
        script.add(monkey.actions.Delay(1))
    script.add(monkey.actions.Animate(data.tag_to_id['hunkomatic'], 'default'))
    script.add(monkey.actions.CallFunc(enable_ui))
    say(script, 118)

def put_cassette_in_recorder(script, *args):
    data.tape_in_recorder = True
    script.add(monkey.actions.CallFunc(drop_item('cassette_tape', settings.characters[settings.player])))
    script.add(monkey.actions.CallFunc(ui.refresh_inventory))
    item = (data.items['items']['cassette_tape'])
    item.update({
        'rooms': 'music_room',
        'pos': [282, 34],
        'walk_to': [292, 25],
        'walk_dir': 'n',
        'anim': 'recorder'
    })
    script.add(monkey.actions.Add(settings.id_game, factory.createItem(item, 'cassette_tape')))

def turn_on_recorder(script, *args):
    if data.tape_in_recorder:
        data.cassette_recorder = 'recording'
        script.add(monkey.actions.Animate(data.tag_to_id['cassette_recorder'], data.cassette_recorder))
        say(script, 122)
    else:
        say(script, 121)

def turn_off_recorder(script, *args):
    if data.tape_in_recorder:
        data.cassette_recorder = 'off'
        script.add(monkey.actions.Animate(data.tag_to_id['cassette_recorder'], data.cassette_recorder))
        say(script, 123)

def check_tape(script):
    if settings.room == 'music_room':
        data.tape_in_recorder = False
