import monkey
import re
import random
from . import scripts
from . import settings
from . import data
from . import utils

def read(item, key: str, default=None):
	# some keys can contain code
	value = item.get(key, default)
	if not value and not default:
		print('Missing key:',key,'in item:',item)
		exit(1)
	if isinstance(value, str) and value[0] == '@':
		return eval(value[1:], {'item': item, 'items': settings.items})
	return value




def getCurrentRoom():
    return settings.items[settings.room]

def callScript(s):
    if isinstance(s, str):
        getattr(scripts, s)()
    else:
        getattr(scripts, s[0])(**s[1])

def callItemScript(s, item):
    if isinstance(s, str):
        getattr(scripts, s)(item=item)
    else:
        getattr(scripts, s[0])(**s[1], item=item)

# change item parent
def moveTo(id: str, parent: str, **kwargs):
    item = settings.getItem(id)
    if item['parent'] == settings.room:
        monkey.get_node(item['iid']).remove()
    item['parent'] = parent
    if 'pos' in kwargs:
        item['pos'] = kwargs['pos']
    if 'dir' in kwargs:
        item['dir'] = kwargs['dir']
    settings.tree.find(id).move_to(settings.tree.find(parent))
    settings.tree.print()


def makeWalkableCollider(outline):
    c = monkey.Node()
    c.add_component(monkey.components.Collider(2, 0, 0, monkey.shapes.Polygon(outline), batch='lines'))
    return c

def readShape(data):
    if 'path' in data:
        s = monkey.shapes.PolyLine(data['path'])
        m = data['path']
    elif 'poly' in data:
        s = monkey.shapes.Polygon(data['poly'])
        m = data['poly']
    elif 'trapezoid' in data:
        ymax= data['y_max']
        m = data['trapezoid'].copy()
        m.extend([m[-2], ymax, m[0], ymax])
        s = monkey.shapes.Polygon(m)
    return s, m

def makeCollider(data, shape=None):
    if not shape:
        shape = readShape(data)
    collideMask = data.get('mask', settings.CollisionFlags.player)
    collider = monkey.components.Collider(settings.CollisionFlags.hotspot,
        collideMask, 10, shape, batch='lines')
    for c in data['response']:
        f = getattr(scripts, c['on_enter'][0])(**c['on_enter'][1])
        collider.setResponse(c['tag'], on_enter=f)
    return collider

def makeScoreBar():
    menu_node = monkey.Node()
    menu_bar = monkey.Node()
    menu_bar.set_model(monkey.models.from_shape('tri2', monkey.shapes.AABB(0, 320, 0, 8),
        settings.Colors.White, monkey.FillType.Solid))
    menu_bar.set_position(0,192,0)
    menu_node.add(menu_bar)
    score_label = monkey.Text(batch='ui', font='sierra', text='Ciao', anchor=monkey.ANCHOR_BOTTOMLEFT, pal='black')
    score_label.set_position(8, 0, 0)
    sound_label = monkey.Text(batch='ui', font='sierra', text='Ciao', anchor=monkey.ANCHOR_BOTTOMLEFT, pal='black')
    sound_label.set_position(240, 0, 0)
    menu_bar.add(score_label)
    menu_bar.add(sound_label)
    return menu_node

def match_items(dobj: str):
    match = []
    for n in settings.tree.find('graham').parent:
        if utils.read(settings.items[n.name], 'active') != True:
            continue
        s = settings.parser['items'].get(n.name, {})
        if dobj in s:
            match.append(n)
    return match

def process_action(s: str):
    if not s:
        return
    settings.last_action = s
    ts = s.lower().strip()
    ts = " ".join(ts.split()).split(' ')
    # remove words
    a = [x for x in ts if x not in settings.parser['remove']]
    # extract verb
    istart_direct = 1
    istart_indirect = -1
    verb = settings.parser['verbs'].get(a[0])
    if not verb:
        verb = settings.parser['verbs'].get(' '.join(a[:2]))
        istart_direct = 2
    if not verb:
        print('Unknown verb: ', a[0])
        return
    else:
        print('verb:',verb)

    # find visible objects
    i = istart_direct
    iend_direct = -1
    while i < len(a):
        if a[i] in settings.parser['prepositions']:
            istart_indirect = i+1
            break
        i+=1
    iend_direct = i
    direct_object = ' '.join(a[istart_direct:iend_direct]) if iend_direct > istart_direct else None
    indirect_object = ' '.join(a[istart_indirect:]) if istart_indirect > 0 else None
    print('direct object:', direct_object)
    print('indirect object:', indirect_object)


    # if action is verb only ... skip this
    if direct_object:
        direct_object = settings.parser['remap'].get(direct_object, direct_object)
        # check all match
        dobj = match_items(direct_object)
        print('i can see',dobj)
        iobj = None
        if indirect_object:
            indirect_object = settings.parser['remap'].get(indirect_object, indirect_object)
            iobj = match_items(indirect_object)
        valid = dobj and (not indirect_object or not iobj)
        if not valid:
            # try with room actions
            actions = getCurrentRoom().get('actions')
            action_string = verb + '_' + direct_object + ('' if not indirect_object else indirect_object)
            if action_string in actions:
                print('found!')
                callScript(actions[action_string])
            else:
                scripts.msg(lines=[19])
        else:
            print('match object ', dobj,iobj)
            if len(dobj) == 1:
                print(dobj[0].name)
                item = getattr(settings.items, dobj[0].name)
                if 'link' in item:
                    item = getattr(settings.items, item['link'])
                actions = item.get('actions')
                if actions:
                    if verb in actions:
                        callItemScript(actions[verb], item)

            else:
                print('disambiguate ',dobj)







def id_to_string(string_id, **kwargs):
    message = settings.strings[string_id]
    aa = dict(kwargs, random=random, msg=id_to_string, game_state=data, settings=settings)
    expr = set(re.findall('(\#\#[^\#]*\#\#)', message))
    for ex in expr:
        message = message.replace(ex, str(eval(ex[2:-2], aa)))
    return message

def make_text(string_id, **kwargs):
    # allow for dynamic strings
    message = id_to_string(string_id, **kwargs)
    msg = monkey.Text(batch='sprites', font='sierra', anchor=monkey.ANCHOR_CENTER,
                      text=message,
                      width=29 * 8, pal='black')
    msg.set_position(160, 100, 10)
    border = monkey.Node()
    mw = msg.size[0]
    mh = msg.size[1]
    border.set_model(monkey.models.from_shape('tri',
                                              monkey.shapes.AABB(-10-mw*0.5, mw*0.5 + 10, -mh*0.5 - 5, mh*0.5+5),
                                              (1, 1, 1, 1),
                                              monkey.FillType.Solid))
    border.set_position(0, 0, -0.1)

    border2 = monkey.Node()
    border2.set_model(monkey.models.from_shape('lines',
                                               monkey.shapes.AABB(-mw*0.5-5, mw*0.5+ 5, -mh*0.5 - 3,mh*0.5+ 3),
                                               monkey.from_hex('AA0000'),
                                               monkey.FillType.Outline))
    border2.set_position(0, 0, -0.01)
    border3 = monkey.Node()
    border3.set_model(monkey.models.from_shape('lines',
                                               monkey.shapes.AABB(-mw*0.5-6, mw*0.5 + 6, -mh*0.5 - 3, mh*0.5+3),
                                               monkey.from_hex('AA0000'),
                                               monkey.FillType.Outline))
    border3.set_position(0, 0, -0.01)
    msg.add(border)
    msg.add(border2)
    msg.add(border3)
    return msg