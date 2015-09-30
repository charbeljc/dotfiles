#!/usr/bin/python3
"""
My QTile config file
"""
try:
    from libqtile.manager import Key, Group
except ImportError:
    from libqtile.config import Key, Group

from libqtile.manager import Screen, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os
import pyosd
OSD = None

def announce(*msgs):
    global OSD
    if not OSD:
        OSD = pyosd.osd()
    OSD.display('\n'.join(msgs))


def find_window(name, cli=None):
    """ find window by name """
    if cli is None:
        cli = lazy
    status, ids = cli.items('window')
    for wid in ids:
        win = cli.window[wid]
        info = win.info()
        if info['name'] == name:
            return win


def start_cli():
    import functools
    from libqtile.command import Client
    cli = Client()
    find = functools.partial(find_window, cli=cli)
    return {'cli': cli, 'find': find}

def setup_mouse():
    """ configure mouse """
    
    sup = "mod4"
    alt = "mod1"
    # This allows you to drag windows around with the mouse if you want.
    return [
        Drag([sup], "Button1", lazy.window.set_position_floating(),
             start=lazy.window.get_position()),
        Drag([sup], "Button3", lazy.window.set_size_floating(),
             start=lazy.window.get_size()),
        Click([sup], "Button2", lazy.window.bring_to_front())
    ]

mouse = setup_mouse()


def setup_key_bindings(groups):
    """ setup key bindings """
    announce('configure key bindings')
    sup = "mod4"
    alt = "mod1"
    
    base = [
        Key([sup], 'KP_Add', lazy.layout.grow()),
        Key([sup], 'KP_Subtract', lazy.layout.shrink()),
        Key([sup], 'equal', lazy.layout.grow()),
        Key([sup], 'minus', lazy.layout.shrink()),
        Key([alt], 'Tab', lazy.layout.down()),
        Key([alt, 'shift'], 'Tab', lazy.layout.up()),
        Key([sup, 'control'], 'k', lazy.layout.shuffle_down()),
        Key([sup, 'control'], 'j', lazy.layout.shuffle_up()),
        Key([sup], 'space', lazy.layout.next()),
        Key([sup, 'shift'], 'space', lazy.layout.rotate()),
        Key([sup, 'shift'], 'Return', lazy.layout.toggle_split()),
        Key([sup], 'Return', lazy.spawn('terminator')),
        Key([sup], 'i', lazy.spawn('icedove')),
        Key([sup], 'x', lazy.spawn('xchat')),
        Key([sup], 'f', lazy.spawn('iceweasel')),
        Key([sup], 'a', lazy.spawn('gajim')),
        Key([sup], 'p', lazy.spawn('pidgin')),
        # Key([sup], 'd', lazy.spawn('setxkbmap -layout es -variant dvorak')),
        # Key([sup], 'q', lazy.spawn('setxkbmap -layout latan')),
        Key([sup], 'w', lazy.window.kill()),
        Key([], 'XF86AudioRaiseVolume',
            lazy.spawn('amixer -c 0 -q set Master 2dB+')),
        Key([], 'XF86AudioLowerVolume',
            lazy.spawn('amixer -c 0 -q set Master 2dB-')),


        Key([sup, 'control'], 'r', lazy.restart()),
        # cycle to previous group
        Key([sup], 'Left', lazy.screen.prev_group()),
        # cycle to next group
        Key([sup], 'Right', lazy.screen.next_group()),

        # windows style alt-tab/alt-shift-tab
        Key([sup], 'Tab', lazy.next_layout()),
        Key([sup, 'shift'], 'Tab', lazy.prev_layout()),
        # PRINT SCREEN
        Key([sup], 'F10', lazy.spawn('import -window root ~/screenshot.png')),
        Key([alt], 't', lazy.window.toggle_floating()),
        Key([sup, 'control'], 'l', lazy.spawn('gnome-screensaver-command -l')),
        Key([sup, 'control'], 'q',
            lazy.spawn('gnome-session-quit --logout --no-prompt')),
        Key([sup, 'shift', 'control'], 'q',
            lazy.spawn('gnome-session-quit --power-off')),
    ]
    # More shortcuts


    def window_sorter(win):
        """ map window to topic """
        patterns = (
            ('Gajim', 'Messaging'),
            ('XChat', 'Messaging'),
            ('Icedove', 'Messaging'),
            ('pidgin', 'Messaging'),
            ('Vimperator', 'Util'),
            ('Krusader', 'Util'),
            ('playout', 'Work'),
            ('lifia', 'Work'),
        )
        for k, value in patterns:
            if k in win.name:
                return value
        return 'Other'

    base.append(Key([alt], 'r', lazy.layout.sort_windows(window_sorter)))

    
    def show_shortcuts(keys):
        key_map = {"mod1": "alt", "mod4": "super"}
        shortcuts_path = "{0}/{1}".format(os.environ["HOME"],
                                          "qtile_shortcuts")
        shortcuts = open("{0}".format(shortcuts_path), 'w')
        shortcuts.write("{0:30}| {1:50}\n".format("KEYS COMBINATION",
                                                  "COMMAND"))
        shortcuts.write("{0:80}\n".format("=" * 80))
        for key in keys:
            key_comb = ""
            for modifier in key.modifiers:
                key_comb += key_map.get(modifier, modifier) + "+"
            key_comb += key.key
            shortcuts.write("{0:30}| ".format(key_comb))
            cmd_str = ""
            for command in key.commands:
                cmd_str += command.name + " "
                for arg in command.args:
                    cmd_str += "{0} ".format(repr(arg))
            shortcuts.write("{0:50}\n".format(cmd_str))
            shortcuts.write("{0:80}\n".format("-" * 80))
        shortcuts.close()
        return lazy.spawn("xterm -wf -e less {0}".format(shortcuts_path))

    base.append(Key([sup], 'h', lambda: show_shortcuts(base)))
    base.append(Key([sup], 'l', lazy.spawn('xscreensaver-command -lock')))
    # base.append(Key([sup], 's', lazy.spawn('xscreensaver -no-splash')))

    for i in groups:
        base.append(
            Key([sup], i.name, lazy.group[i.name].toscreen())
        )
        base.append(
            Key([sup, 'shift'], i.name, lazy.window.togroup(i.name))
        )

        return base

groups = [
    Group("a"),
    Group("s"),
    Group("d"),
    Group("f"),
]

keys = setup_key_bindings(groups)



layouts = [
    layout.MonadTall(),
    layout.Max(),
    layout.TreeTab(sections=['Work', 'Messaging', 'Docs', 'Util', 'Other']),
    # a layout for pidgin
    layout.Slice('right', 256, name='pidgin', role='buddy_list',
         fallback=layout.Stack(stacks=2, border_width=1)),
    layout.Tile(ratio=0.35, borderwidth=1),
    layout.VerticalTile(),
    layout.Matrix(),
    layout.RatioTile(),
    layout.Zoomy(),
    layout.Floating(),
    ]

screens = [
    Screen(
        bottom = bar.Bar(
                    [
                        widget.GroupBox(fontsize=8),
                        widget.WindowName(fontsize=14),
                        widget.CurrentLayout(fontsize=14),
                        
                        widget.Sep(),
                        widget.Prompt(),
                        widget.Sep(),
                        
                        widget.CPUGraph(samples=40, line_width=1, width=40,
                                        graph_color='FF2020',
                                        fill_color='C01010'),
                        widget.MemoryGraph(samples=40, line_width=1, width=40,
                                           graph_color='0066FF',
                                           fill_color='001188'),
                        widget.NetGraph(samples=40, line_width=1,   width=40,
                                        interface="eth0",
                                        graph_color='22FF44',
                                        fill_color='11AA11'),
                        widget.Systray(),
                        widget.Clock(format='%a %d %b, %R (sem %V)',
                            fontsize=12),
                    ],
                    25,
                )
        #left = bar.Gap(60)
    ),
]

#import subprocess
#import os
@hook.subscribe.client_new
def qtile_config(window):
    #info = window.inspect()
    announce('subscribe {}'.format(repr((dir(window)))))
    #if info['name'] == u'pcmanfm-qt':
    #    window.static(0)

@hook.subscribe.startup
def coucou():
    announce('QTile startup hook')
    
@hook.subscribe.startup_once
def startup_once_hook(*args, **kwargs):
    announce('QTile startup Once\nargs=%r, kw=%r\n' % (args, kwargs))

@hook.subscribe.addgroup
def addgroup_hook(*args, **kwargs):
    announce('addgroup:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.setgroup
def setgroup_hook(*args, **kwargs):
    announce('setgroup:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.delgroup
def startup_once_hook(*args, **kwargs):
    announce('delgroup:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.changegroup
def startup_once_hook(*args, **kwargs):
    announce('changegroup:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.focus_change
def startup_once_hook(*args, **kwargs):
    announce('focus_change:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.float_change
def startup_once_hook(*args, **kwargs):
    announce('float_change:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.group_window_add
def startup_once_hook(*args, **kwargs):
    announce('group_window_add:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.window_name_change
def startup_once_hook(*args, **kwargs):
    # announce('window_name_change:\nargs=%r, kw=%r\n' % (args, kwargs))
    pass
@hook.subscribe.client_new
def startup_once_hook(*args, **kwargs):
    announce('client_new:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.client_managed
def startup_once_hook(*args, **kwargs):
    announce('client_managed:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.client_killed
def startup_once_hook(*args, **kwargs):
    announce('client_killed:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.client_state_changed
def startup_once_hook(*args, **kwargs):
    announce('client_state_changed:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.client_type_changed
def startup_once_hook(*args, **kwargs):
    announce('client_type_changed:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.client_focus
def startup_once_hook(*args, **kwargs):
    announce('client_focus:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.client_mouse_enter
def startup_once_hook(*args, **kwargs):
    announce('client_mouse_enter:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.client_name_updated
def startup_once_hook(*args, **kwargs):
    announce('client_name_updated:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.client_urgent_hint_changed
def startup_once_hook(*args, **kwargs):
    announce('client_urgent_hint_changed:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.layout_change
def startup_once_hook(*args, **kwargs):
    announce('layout_change:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.net_wm_icon_change
def startup_once_hook(*args, **kwargs):
    announce('net_wm_icon_change:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.selection_notify
def startup_once_hook(*args, **kwargs):
    announce('selection_notify:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.selection_change
def startup_once_hook(*args, **kwargs):
    announce('selection_change:\nargs=%r, kw=%r\n' % (args, kwargs))
@hook.subscribe.screen_change
def startup_once_hook(*args, **kwargs):
    announce('screen_change:\nargs=%r, kw=%r\n' % (args, kwargs))
#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@hook.subscribe.startup
#def dbus_register():
#        x = os.environ['DESKTOP_AUTOSTART_ID']
#        subprocess.Popen(['dbus-send',
#            '--session',
#            '--print-reply=string',
#            '--dest=org.gnome.SessionManager',
#            '/org/gnome/SessionManager',
#            'org.gnome.SessionManager.RegisterClient',
#            'string:qtile',
#            'string:' + x])
#@hook.subscribe.startup
#def dvorak():
#    os.system("setxkbmap -layout es -variant dvorak")
@hook.subscribe.startup
def french():
    os.system("setxkbmap -layout fr")
    os.system("xmodmap ~/.Xmodmap")

@hook.subscribe.client_new
def dialogs(window):
    announce('client_type: %s' % window.window.get_wm_type())
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

main = None
follow_mouse_focus = True
cursor_warp = False
floating_layout = layout.Floating()
mouse = ()
