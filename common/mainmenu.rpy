# This file contains code fo the main menu, and anything else that
# happens upon initial execution of a Ren'Py program.

init -498:

    python hide:

        library.old_names['Quit'] = 'Quit Game'
        
        # The contents of the main menu.
        library.main_menu = [
            ( u"Start Game", "start", 'True'),
            ( u"Continue Game", ui.jumps("_load_screen"), 'True' ),
            ( u"Preferences", ui.jumps("_prefs_screen"), 'True' ),
            ( u"Quit",  ui.jumps("_quit"), 'True' ),
            ]

        # If not None, this is used to fix the positions of the
        # things in the main menu.
        library.main_menu_positions = None

        # Music to play at the main menu.
        library.main_menu_music = None

# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:

    call _check_module from _call__check_module_1

    if renpy.has_label("splashscreen") and not _restart:
        call expression "splashscreen" from _call_splashscreen_1

    if library.main_menu_music:
        $ renpy.music.play(library.main_menu_music)

    # Clean out any residual scene from the splashscreen.
    scene black

    $ renpy.call_in_new_context("_enter_main_menu")

    # Should never happen... but might as well do something 
    jump start

# At this point, we've been switched into a new context. So we
# initialize it.
label _enter_main_menu:

    call _enter_menu from _call__enter_menu_1

    $ renpy.context().main_menu = True
    
# This is called to show the main menu to the user.
label _main_menu:    

    # Let the user completely override the main menu. (But please note
    # it still lives in the menu context, rather than the game context.)
    if renpy.has_label("main_menu"):
        jump expression "main_menu"

# This is the default main menu, which we get if the user hasn't
# defined his own, or if that function calls this explicitly.        
label _library_main_menu:

    python hide:

        ui.add(renpy.Keymap(toggle_fullscreen = renpy.toggle_fullscreen))

        ### mm_root default
        # (window) The style used for the root window of the main
        # menu. This is primarily used to set a background for the
        # main menu.

        ui.window(style='mm_root')
        ui.fixed()

        ### mm_menu_frame default
        # (window) A window that contains the choices in
        # the main menu. Change this to change the placement of
        # these choices on the main menu screen.

        ### mm_menu_frame_vbox thin_vbox
        # (box) The vbox containing the main menu choices.

        if library.main_menu_positions:
            ui.fixed()
        else:
            ui.window(style='mm_menu_frame')
            ui.vbox(style='mm_menu_frame_vbox')

        for text, clicked, enabled in library.main_menu:

            if isinstance(clicked, basestring):
                clicked = ui.jumpsoutofcontext(clicked)

            ### mm_button button
            # (window, hover) The style that is used on buttons that are
            # part of the main menu.

            ### mm_button_text button_text
            # (text, hover) The style that is used for the labels of
            # buttons that are part of the main menu.

            if library.main_menu_positions:
                kwargs = library.main_menu_positions.get(text, { })
            else:
                kwargs = { }

            if not eval(enabled):
                clicked = None
                disabled = True
            else:
                disabled = False

            _button_factory(text, "mm", clicked=clicked, disabled=disabled, properties=kwargs)

        ui.close()
        ui.close()

        store._result = ui.interact(suppress_overlay = True,
                                    suppress_underlay = True,
                                    mouse="mainmenu")

    # Computed jump to the appropriate label.
    jump _main_menu
