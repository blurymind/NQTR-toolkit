init python:
    from pythonpackages.nqtr.navigation import isClosedRoom
    from pythonpackages.nqtr.routine import getBgRoomRoutine
    from pythonpackages.nqtr.action import getActions

screen room_navigation():
    modal True
    $ i = 0
    # More information by hovering the mouse
    $ (x,y) = renpy.get_mouse_pos()

    # Map
    if (map_open and cur_map_id):
        $ map_id_north = maps[cur_map_id].map_id_north
        $ map_id_south = maps[cur_map_id].map_id_south
        $ map_id_east = maps[cur_map_id].map_id_east
        $ map_id_west = maps[cur_map_id].map_id_west

        # North map
        if (not isNullOrEmpty(map_id_north) and not maps[map_id_north].isHidden(flags)):
            hbox:
                align (0.5, 0.1)
                imagebutton:
                    idle "gui triangular_button"
                    focus_mask True
                    sensitive not maps[map_id_north].isDisabled(flags)
                    action [
                        SetVariable('cur_map_id', map_id_north), 
                        Call("after_return_from_room_navigation", label_name_to_call = "set_image_map"),
                    ]
                    if renpy.variant("pc"):
                        tooltip maps[map_id_north].name
                    at middle_map(rotation = 270)
        # South map
        if (not isNullOrEmpty(map_id_south) and not maps[map_id_south].isHidden(flags)):
            hbox:
                align (0.5, 0.99)
                imagebutton:
                    idle "gui triangular_button"
                    focus_mask True
                    sensitive not maps[map_id_south].isDisabled(flags)
                    action [
                        SetVariable('cur_map_id', map_id_south), 
                        Call("after_return_from_room_navigation", label_name_to_call = "set_image_map"),
                    ]
                    if renpy.variant("pc"):
                        tooltip maps[map_id_south].name
                    at middle_map(rotation = 90)
        # West map
        if (not isNullOrEmpty(map_id_west) and not maps[map_id_west].isHidden(flags)):
            hbox:
                align (0.001, 0.5)
                imagebutton:
                    idle "gui triangular_button"
                    focus_mask True
                    sensitive not maps[map_id_west].isDisabled(flags)
                    action [
                        SetVariable('cur_map_id', map_id_west), 
                        Call("after_return_from_room_navigation", label_name_to_call = "set_image_map"),
                    ]
                    if renpy.variant("pc"):
                        tooltip maps[map_id_west].name
                    at middle_map(rotation = 180)
        # East map
        if (not isNullOrEmpty(map_id_east) and not maps[map_id_east].isHidden(flags)):
            hbox:
                align (0.999, 0.5)
                imagebutton:
                    idle "gui triangular_button"
                    focus_mask True
                    sensitive not maps[map_id_east].isDisabled(flags)
                    action [
                        SetVariable('cur_map_id', map_id_east), 
                        Call("after_return_from_room_navigation", label_name_to_call = "set_image_map"),
                    ]
                    if renpy.variant("pc"):
                        tooltip maps[map_id_east].name
                    at middle_map(rotation = 0)

        for location in locations:
            # If the Map where I am is the same as the Map where the room is located
            use location_button(location)

    else:
        # Rooms
        hbox:
            yalign 0.99
            xalign 0.01
            spacing 2

            for room in rooms:
                $ i += 1

                # If the Locations where I am is the same as the Locations where the room is located
                if (room.location_id == cur_location.id and room.isButton() != None and not room.isHidden(flags)):
                    button:
                        xysize (126, 190)
                        action [
                            SetVariable('prev_room', cur_room),
                            SetVariable('cur_room', room),
                            Call("after_return_from_room_navigation", label_name_to_call = "change_room"),
                        ]
                        has vbox xsize 126 spacing 0

                        frame:
                            xysize (126, 140)
                            background None

                            # Room icon
                            imagebutton:
                                align (0.5, 0.0)
                                idle room.getButtonOrDefault()
                                selected_idle room.getSelectedButtonOrDefault()
                                selected_hover room.getSelectedButtonOrDefault()
                                selected (True if cur_room and cur_room.id == room.id else False)
                                sensitive not room.isDisabled(flags)
                                focus_mask True
                                action [
                                    SetVariable('prev_room', cur_room),
                                    SetVariable('cur_room', room),
                                    Call("after_return_from_room_navigation", label_name_to_call = "change_room"),
                                ]
                                at middle_room

                            # Check the presence of ch in that room
                            $ there_are_ch = False
                            for comm in commitments_in_cur_location.values():
                                # If it is the selected room
                                if comm != None and room.id == comm.room_id:
                                    # I insert hbox only if they are sure that someone is there
                                    $ there_are_ch = True

                            if there_are_ch:
                                hbox:
                                    ypos 73
                                    xalign 0.5
                                    spacing - 30

                                    for comm in commitments_in_cur_location.values():
                                        # If it is the selected room
                                        if room.id == comm.room_id:
                                            for ch_icon in comm.getChIcons(ch_icons):
                                                imagebutton:
                                                    idle ch_icon
                                                    sensitive not room.isDisabled(flags)
                                                    focus_mask True
                                                    action [
                                                        SetVariable('prev_room', cur_room),
                                                        SetVariable('cur_room', room),
                                                        Call("after_return_from_room_navigation", label_name_to_call = "change_room"),
                                                    ]
                                                    at small_face

                        # Room name
                        text room.name:
                            size gui.little_text_size
                            drop_shadow [(2, 2)]
                            xalign 0.5
                            text_align 0.5
                            line_leading 0
                            line_spacing -2
                    key str(i) action [
                        SetVariable('prev_room', cur_room),
                        SetVariable('cur_room', room),
                        Call("after_return_from_room_navigation", label_name_to_call = "change_room"),
                    ]

        # Action wich Picture in background
        for room in rooms:
            # Adds the button list of possible actions in that room
            if (cur_room and room.id == cur_room.id and not room.id in closed_rooms):
                # actions: dict[str, Act], room: Room,  now_is_between: callable[[int, int], bool], cur_day: int
                for act in getActions(actions= actions | df_actions, room = room, now_hour = tm.get_hour_number() , cur_day = tm.get_day_number(), tm = tm):
                    use action_button(act)

        # Normal Actions (with side button)
        vbox:
            yalign 0.95
            xalign 0.99
            for room in rooms:
                # Adds the button list of possible actions in that room
                if (cur_room and room.id == cur_room.id):
                    for act in getActions(actions= actions | df_actions, room = room, now_hour = tm.get_hour_number() , cur_day = tm.get_day_number(), tm = tm):
                        use action_button(act, show_picture_in_background = True)

                # Talk
                # Adds a talk for each ch (NPC) and at the talk interval adds the icon for each secondary ch
                for comm in commitments_in_cur_location.values():
                    if (cur_room and comm and room.id == comm.room_id and room.id == cur_room.id):
                        # Insert in talk for every ch, main in that room
                        for ch_id, talk_obj in comm.ch_talkobj_dict.items():
                            use action_talk_button(ch_id, talk_obj, comm.getTalkBackground(ch_id))

            # Fixed button to wait
            use wait_button()

    # Time
    use time_text(tm, show_wait_button = map_open)

    # Tools
    hbox:
        align (0.01, 0.01)
        spacing 2

        imagebutton:
            idle '/interface/menu-options.webp'
            focus_mask True
            action ShowMenu('save')
            if renpy.variant("pc"):
                at small_menu
                tooltip _("Settings")
            else:
                at small_menu_mobile

        imagebutton:
            idle '/interface/menu-user.webp'
            focus_mask True
            action [
                Call("after_return_from_room_navigation", label_name_to_call = "development_characters_info"),
            ]
            if renpy.variant("pc"):
                at small_menu
                tooltip _("Characters info")
            else:
                at small_menu_mobile

        if len(current_quest_stages) > 0 :
            imagebutton:
                idle '/interface/menu-memo.webp'
                focus_mask True
                action [
                    Show('menu_memo'),
                ]
                if renpy.variant("pc"):
                    at small_menu
                    tooltip _("Memo")
                else:
                    at small_menu_mobile

        imagebutton:
            idle '/interface/menu-help.webp'
            focus_mask True
            action ShowMenu('help')
            if renpy.variant("pc"):
                at small_menu
                tooltip _("Help")
            else:
                at small_menu_mobile

    hbox:
        align (0.99, 0.01)
        spacing 2

        # Money
        text "$20":
            align(1.0, 0.5)
            size gui.interface_text_size
            drop_shadow [(2, 2)]

        imagebutton:
            idle '/interface/menu-inventory.webp'
            focus_mask True
            action [
                Call("after_return_from_room_navigation", label_name_to_call = "development_inventory"),
            ]
            if renpy.variant("pc"):
                at small_menu
                tooltip _("Backpack")
            else:
                at small_menu_mobile

        imagebutton:
            idle '/interface/menu-phone.webp'
            focus_mask True
            action [
                Call("after_return_from_room_navigation", label_name_to_call = "development"),
            ]
            if renpy.variant("pc"):
                at small_menu
                tooltip _("Smartphone")
            else:
                at small_menu_mobile

        imagebutton:
            idle '/interface/menu-map.webp'
            focus_mask True
            action [
                Call("after_return_from_room_navigation", label_name_to_call = "open_map"),
            ]
            if renpy.variant("pc"):
                at small_menu
                tooltip _("Map")
            else:
                at small_menu_mobile

    # More information by hovering the mouse
    if renpy.variant("pc"):
        $ text = GetTooltip()
        if text:
            text "[text]":
                xpos x-20
                ypos y-20
                size gui.little_text_size 
                drop_shadow [(2, 2)] 
                outlines [(2, "#000", 0, 1)]

label set_background_nqtr:
    if (not map_open):
        if(isClosedRoom(room_id= cur_room.id, closed_rooms= closed_rooms, now_hour= tm.get_hour_number(), tm = tm)):
            # Change the background image to the current room image.
            call closed_room_event
        else:
            $ sp_bg_change_room = getBgRoomRoutine(commitments_in_cur_location, cur_room.id)
            call set_room_background(sp_bg_change_room)
    return

label set_room_background(sp_bg_change_room = ""):
    if (not isNullOrEmpty(sp_bg_change_room)):
        call set_background(sp_bg_change_room)
    else:
        call set_background(cur_room.bg)
    return

# making calls safely:
# Why? Because if I use Call("label") in sleep mode from the room_navigation
# and in the "label" I use "return" an almost all cases the game will end.
label after_return_from_room_navigation(label_name_to_call = ""):
    if isNullOrEmpty(label_name_to_call):
        $ log_error("label_name_to_call is empty", renpy.get_filename_line())
    else:
        $ renpy.call(label_name_to_call)
    call set_background_nqtr
    # Custom Code:
    # ...
    call screen room_navigation
    $ log_error("thera is a anomaly in room_navigation. value: " + label_name_to_call, renpy.get_filename_line())
    jump after_return_from_room_navigation
