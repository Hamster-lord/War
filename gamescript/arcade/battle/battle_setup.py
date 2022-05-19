import numpy as np

from gamescript import battleui
from gamescript.common import utility

from gamescript.common.ui import common_ui_selector

change_group = utility.change_group

setup_unit_icon = common_ui_selector.setup_unit_icon

def setup_battle_ui(self, change):
    """Change can be either 'add' or 'remove' for adding or removing ui"""
    if change == "add":
        self.time_ui.change_pos((self.screen_rect.width - self.time_ui.image.get_width(),
                                 0), self.time_number)
        self.inspect_ui.change_pos((self.inspect_ui.image.get_width() / 6, self.inspect_ui.image.get_height() / 2))

        self.troop_card_ui.change_pos((self.inspect_ui.rect.bottomleft[0] + self.troop_card_ui.image.get_width() / 2,
                                       (self.inspect_ui.rect.bottomleft[1] + self.troop_card_ui.image.get_height() / 2)))


        self.scale_ui.change_pos(self.time_ui.rect.bottomleft)
        self.test_button.change_pos((self.scale_ui.rect.bottomleft[0] + (self.test_button.image.get_width() / 2),
                                    self.scale_ui.rect.bottomleft[1] + (self.test_button.image.get_height() / 2)))
        self.warning_msg.change_pos(self.test_button.rect.bottomleft)

        # self.speed_number.change_pos(self.time_ui.rect.center)  # self speed number on the time ui

        # self.switch_button[0].change_pos((self.command_ui.pos[0] - 40, self.command_ui.pos[1] + 96))  # skill condition button
        # self.switch_button[1].change_pos((self.command_ui.pos[0] - 80, self.command_ui.pos[1] + 96))  # fire at will button
        # self.switch_button[2].change_pos((self.command_ui.pos[0], self.command_ui.pos[1] + 96))  # behaviour button
        # self.switch_button[3].change_pos((self.command_ui.pos[0] + 40, self.command_ui.pos[1] + 96))  # shoot range button
        # self.switch_button[4].change_pos((self.command_ui.pos[0] - 125, self.command_ui.pos[1] + 96))  # arc_shot button
        # self.switch_button[5].change_pos((self.command_ui.pos[0] + 80, self.command_ui.pos[1] + 96))  # toggle run button
        # self.switch_button[6].change_pos((self.command_ui.pos[0] + 120, self.command_ui.pos[1] + 96))  # toggle melee mode

        inspect_ui_pos = [self.inspect_ui.rect.topleft[0] + self.icon_sprite_width / 1.25,
                          self.inspect_ui.rect.topleft[1]]
        width, height = inspect_ui_pos[0], inspect_ui_pos[1]
        sub_unit_number = 0  # Number of subunit based on the position in row and column
        imgsize = (self.icon_sprite_width, self.icon_sprite_height)
        for _ in list(range(0, 25)):
            width += imgsize[0]
            self.inspect_subunit.append(battleui.InspectSubunit((width, height)))
            sub_unit_number += 1
            if sub_unit_number == 5:  # Reach the last subunit in the row, go to the next one
                width = inspect_ui_pos[0]
                height += imgsize[1]
                sub_unit_number = 0

        if self.mode == "unit_editor":
            change_group(self.unit_selector, self.battle_ui_updater, change)
            change_group(self.unit_selector_scroll, self.battle_ui_updater, change)

    else:
        change_group(self.unit_selector, self.battle_ui_updater, change)
        change_group(self.unit_selector_scroll, self.battle_ui_updater, change)

    change_group(self.scale_ui, self.battle_ui_updater, change)


def add_unit(subunit_list, position, game_id, colour, unit_leader, leader_stat, control, coa, command, start_angle, start_hp, start_stamina, team):
    """Create unit object into the battle and leader of the unit"""
    from gamescript import unit, leader
    old_subunit_list = subunit_list[~np.all(subunit_list == 0, axis=1)]  # remove whole empty column in subunit list
    subunit_list = old_subunit_list[:, ~np.all(old_subunit_list == 0, axis=0)]  # remove whole empty row in subunit list
    unit = unit.Unit(position, game_id, subunit_list, colour, control, coa, command, abs(360 - start_angle), start_hp, start_stamina, team)

    # add leader
    leader_pos = np.where(subunit_list == "h")[0]
    unit.leader = [leader.Leader(unit_leader, leader_pos, 0, unit, leader_stat)]
    return unit


def change_state(self):
    self.previous_game_state = self.game_state
    if self.game_state == "battle":  # change to battle state
        self.camera_mode = self.start_zoom_mode
        self.mini_map.draw_image(self.show_map.true_image, self.camera)

        if self.current_selected is not None:  # any unit is selected
            self.current_selected = None  # reset last_selected
            self.before_selected = None  # reset before selected unit after remove last selected

        # self.command_ui.rect = self.command_ui.image.get_rect(
        #     center=(self.command_ui.image.get_width() / 2, self.command_ui.image.get_height() / 2))  # change leader ui position back
        self.troop_card_ui.rect = self.troop_card_ui.image.get_rect(
            center=self.troop_card_ui.pos)  # change subunit card position back

        self.troop_card_button[0].rect = self.troop_card_button[0].image.get_rect(
            center=(self.troop_card_ui.rect.topleft[0] + (self.troop_card_button[0].image.get_width() / 2),
                    self.troop_card_ui.rect.topleft[1] + (self.troop_card_button[2].image.get_width() * 3)))  # description button
        self.troop_card_button[1].rect = self.troop_card_button[1].image.get_rect(
            center=(self.troop_card_ui.rect.topleft[0] + (self.troop_card_button[1].image.get_width() / 2),
                    self.troop_card_ui.rect.topleft[1] + (self.troop_card_button[2].image.get_width())))  # stat button
        self.troop_card_button[2].rect = self.troop_card_button[2].image.get_rect(
            center=(self.troop_card_ui.rect.topleft[0] + (self.troop_card_button[2].image.get_width() / 2),
                    self.troop_card_ui.rect.topleft[1] + (self.troop_card_button[2].image.get_width()) * 2))  # skill button
        self.troop_card_button[3].rect = self.troop_card_button[3].image.get_rect(
            center=(self.troop_card_ui.rect.topleft[0] + (self.troop_card_button[3].image.get_width() / 2),
                    self.troop_card_ui.rect.topleft[1] + (self.troop_card_button[2].image.get_width() * 4)))  # equipment button

        self.battle_ui_updater.remove(self.filter_stuff, self.unit_setup_stuff, self.leader_now, self.button_ui, self.warning_msg)
        self.battle_ui_updater.add(self.event_log, self.log_scroll)

        self.game_speed = 1

        # Run starting method
        for this_unit in self.unit_updater:
            this_unit.start_set(self.subunit_updater)
        for this_subunit in self.subunit_updater:
            this_subunit.start_set(self.camera_zoom, self.subunit_animation_pool)
        for this_leader in self.leader_updater:
            this_leader.start_set()

    elif self.game_state == "editor":  # change to editor state
        self.camera_mode = "Free"
        self.inspect = False  # reset inspect ui
        self.mini_map.draw_image(self.show_map.true_image, self.camera)  # reset mini_map
        for arrow in self.range_attacks:  # remove all range melee_attack
            arrow.kill()
            del arrow

        for this_unit in self.battle.all_team_unit["alive"]:  # reset all unit state
            this_unit.player_input(self.battle_mouse_pos, False, False, False, self.last_mouseover, None, other_command=2)

        self.troop_card_ui.rect = self.troop_card_ui.image.get_rect(bottomright=(self.screen_rect.width,
                                                                                 self.screen_rect.height))  # troop info card ui
        self.troop_card_button[0].rect = self.troop_card_button[0].image.get_rect(
            center=(self.troop_card_ui.rect.topleft[0] + (self.troop_card_button[0].image.get_width() / 2),
                    self.troop_card_ui.rect.topleft[1] + (self.troop_card_button[2].image.get_width() * 3)))  # description button
        self.troop_card_button[1].rect = self.troop_card_button[1].image.get_rect(
            center=(self.troop_card_ui.rect.topleft[0] + (self.troop_card_button[1].image.get_width() / 2),
                    self.troop_card_ui.rect.topleft[1] + (self.troop_card_button[2].image.get_width())))  # stat button
        self.troop_card_button[2].rect = self.troop_card_button[2].image.get_rect(
            center=(self.troop_card_ui.rect.topleft[0] + (self.troop_card_button[2].image.get_width() / 2),
                    self.troop_card_ui.rect.topleft[1] + (self.troop_card_button[2].image.get_width()) * 2))  # skill button
        self.troop_card_button[3].rect = self.troop_card_button[3].image.get_rect(
            center=(self.troop_card_ui.rect.topleft[0] + (self.troop_card_button[3].image.get_width() / 2),
                    self.troop_card_ui.rect.topleft[1] + (self.troop_card_button[2].image.get_width() * 4)))  # equipment button

        self.battle_ui_updater.remove(self.event_log, self.log_scroll, self.troop_card_button, self.col_split_button, self.row_split_button,
                                      self.event_log_button, self.time_button, self.unitstat_ui, self.inspect_ui, self.leader_now, self.inspect_subunit,
                                      self.inspect_selected_border, self.inspect_button, self.behaviour_switch_button)

        self.leader_now = [this_leader for this_leader in self.preview_leader]  # reset leader in command ui
        self.battle_ui_updater.add(self.filter_stuff, self.unit_setup_stuff, self.test_button, self.command_ui, self.troop_card_ui, self.leader_now,
                                   self.time_button)
        self.slot_display_button.event = 0  # reset display editor ui button to show
        self.game_speed = 0  # pause battle

        # for slot in self.subunit_build:
        #     if slot.troop_id != 0:
        #         self.command_ui.value_input(who=slot)
        #         break

        setup_unit_icon(self.unit_selector, self.unit_icon,
                        self.all_team_unit[self.team_selected], self.unit_selector_scroll)
        self.unit_selector_scroll.change_image(new_row=self.unit_selector.current_row)

    self.speed_number.speed_update(self.game_speed)
