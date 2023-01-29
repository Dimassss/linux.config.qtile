import json
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import EzKey, Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
#from libqtile.command import lazy
from libqtile.log_utils import logger
from plasma import Plasma
from libqtile.bar import Gap

mod = "mod1"
terminal = 'urxvt'

keymap = {
    'A-h': lazy.layout.left(),
    'A-j': lazy.layout.down(),
    'A-k': lazy.layout.up(),
    'A-l': lazy.layout.right(),
    'A-S-h': lazy.layout.move_left(),
    'A-S-j': lazy.layout.move_down(),
    'A-S-k': lazy.layout.move_up(),
    'A-S-l': lazy.layout.move_right(),
    'A-C-h': lazy.layout.integrate_left(),
    'A-C-j': lazy.layout.integrate_down(),
    'A-C-k': lazy.layout.integrate_up(),
    'A-C-l': lazy.layout.integrate_right(),
    'A-d': lazy.layout.mode_horizontal(),
    'A-v': lazy.layout.mode_vertical(),
    'A-S-d': lazy.layout.mode_horizontal_split(),
    'A-S-v': lazy.layout.mode_vertical_split(),
    'A-a': lazy.layout.grow_width(30),
    'A-x': lazy.layout.grow_width(-30),
    'A-S-a': lazy.layout.grow_height(30),
    'A-S-x': lazy.layout.grow_height(-30),
    'A-C-5': lazy.layout.size(500),
    'A-C-8': lazy.layout.size(800),
    'A-n': lazy.layout.reset_size(),
}

keys = [EzKey(k, v) for k, v in keymap.items()]

keys += [
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    Plasma(
        border_normal='#333333',
        border_focus='#00e891',
        border_normal_fixed='#006863',
        border_focus_fixed='#00e8dc',
        border_width=1,
        border_width_single=1,
        margin=2
    ),
    layout.Max(),
]

widget_defaults = dict(
    font="mono",
    fontsize=12,
    padding=5,
)
extension_defaults = widget_defaults.copy()

def get_bar_options():

    bar_options = {"size": 24,
        "widgets": [
            widget.CurrentLayout(),
            widget.GroupBox(),
            widget.Prompt(),
            widget.WindowName(),
            widget.Chord(
                chords_colors={
                    "launch": ("#ff0000", "#ffffff"),
                },
                name_transform=lambda name: name.upper(),
            ),
            widget.TextBox("default config", name="default"),
            widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
            # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
            # widget.StatusNotifier(),
            widget.Systray(),
            widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
            widget.QuickExit(),
        ],
        "border_width": [2, 2, 2, 2],
        "border_color": "#444466",
        "margin": [10, 10, 10, 10],
        "background": "#f1112020",
        "opacity": 0.8
    }

    return bar_options

screens = [
    Screen(
        top=bar.Bar(**get_bar_options())
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


def toggle_top_bar(topbar=None, stick_bar = True):
    if topbar is None:
        topbar = qtile.current_screen.top

    if stick_bar:
        margin = [0,0,0,0]
        border_width = [0,0,2,0]
        size = 30
    else:
        margin = [10,10,10,10]
        border_width = [2,2,2,2]
        size = 24

    topbar._initial_margin = margin
    topbar.border_width = border_width
    topbar.initial_size = size
    
    # this line is needed to redraw the top bar
    topbar._configure(qtile, qtile.current_screen, reconfigure = True)
    #qtile.current_screen.top.draw()
    #this line is needed to redraw windows on the screen
    qtile.current_screen.group.layout_all()

    
def update_top_bar(screen=None, offset=0):
    if screen is None:
        screen = qtile.current_screen

    topbar = screen.top
    if not topbar:
        return

    nwindows = len(screen.group.windows) + offset
    if nwindows > 0:
        toggle_top_bar(topbar, stick_bar=True)
    else:
        toggle_top_bar(topbar, stick_bar=False)



@hook.subscribe.client_killed
def update_tabs_client_killed(window):
    update_top_bar(offset=-1)


@hook.subscribe.group_window_add
def update_tabs_group_window_add(group, window):
    update_top_bar(offset=1)


@hook.subscribe.layout_change
def update_tabs_layout_change(layout, group):
    update_top_bar()


@hook.subscribe.setgroup
def update_tabs_setgroup():
    for screen in qtile.screens:
        update_top_bar(screen)


@hook.subscribe.startup_complete
def update_tabs_startup_complete():
    for screen in qtile.screens:
        update_top_bar(screen)


