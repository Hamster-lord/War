import numpy as np
import pygame

battle_side_cal = (1, 0.5, 0.1, 0.5)  # battle_side_cal is for melee combat side modifier


def destroyed(self, battle, morale_hit=True):
    """remove unit when it dies"""
    if self.team == 1:
        group = battle.team1_unit
        enemy_group = battle.team2_unit
        battle.team1_pos_list.pop(self.game_id)
    else:
        group = battle.team2_unit
        enemy_group = battle.team1_unit
        battle.team2_pos_list.pop(self.game_id)

    if morale_hit:
        if self.commander:  # more morale penalty if the unit is a command unit
            for army in group:
                for this_subunit in army.subunit_sprite:
                    this_subunit.base_morale -= 30

        for this_army in enemy_group:  # get bonus authority to the another army
            this_army.authority += 5

        for this_army in group:  # morale dmg to every subunit in army when allied unit destroyed
            for this_subunit in this_army.subunit_sprite:
                this_subunit.base_morale -= 20

    battle.all_unit_list.remove(self)
    battle.all_unit_index.remove(self.game_id)
    group.remove(self)
    self.got_killed = True


def move_leader_subunit(this_leader, old_army_subunit, new_army_subunit, already_pick=()):
    """old_army_subunit is subunit_list list that the subunit currently in and need to be move out to the new one (new_army_subunit),
    already_pick is list of position need to be skipped"""
    replace = [np.where(old_army_subunit == this_leader.subunit.game_id)[0][0],
               np.where(old_army_subunit == this_leader.subunit.game_id)[1][0]]  # grab old array position of subunit
    new_row = int((len(new_army_subunit) - 1) / 2)  # set up new row subunit will be place in at the middle at the start
    new_place = int((len(new_army_subunit[new_row]) - 1) / 2)  # setup new column position
    place_done = False  # finish finding slot to place yet

    while place_done is False:
        if this_leader.subunit.unit.subunit_list.flat[new_row * new_place] != 0:
            for this_subunit in this_leader.subunit.unit.subunit_sprite:
                if this_subunit.game_id == this_leader.subunit.unit.subunit_list.flat[new_row * new_place]:
                    if this_subunit.leader is not None or (new_row, new_place) in already_pick:
                        new_place += 1
                        if new_place > len(new_army_subunit[new_row]) - 1:  # find new column
                            new_place = 0
                        elif new_place == int(
                                len(new_army_subunit[new_row]) / 2):  # find in new row when loop back to the first one
                            new_row += 1
                        place_done = False
                    else:  # found slot to replace
                        place_done = True
                        break
        else:  # fill in the subunit if the slot is empty
            place_done = True

    old_army_subunit[replace[0]][replace[1]] = new_army_subunit[new_row][new_place]
    new_army_subunit[new_row][new_place] = this_leader.subunit.game_id
    new_position = (new_place, new_row)
    return old_army_subunit, new_army_subunit, new_position


def check_split(self, who):
    """Check if unit can be splitted, if not remove splitting button"""
    # v split by middle column
    if np.array_split(who.subunit_list, 2, axis=1)[0].size >= 10 and np.array_split(who.subunit_list, 2, axis=1)[1].size >= 10 and \
            who.leader[1].name != "None":  # can only split if both unit size will be larger than 10 and second leader exist
        self.battle_ui.add(self.col_split_button)
    elif self.col_split_button in self.battle_ui:
        self.battle_ui.remove(self.col_split_button)
    # ^ End col

    # v split by middle row
    if np.array_split(who.subunit_list, 2)[0].size >= 10 and np.array_split(who.subunit_list, 2)[1].size >= 10 and \
            who.leader[1].name != "None":
        self.battle_ui.add(self.row_split_button)
    elif self.row_split_button in self.battle_ui:
        self.battle_ui.remove(self.row_split_button)


def split_unit(battle, who, how):
    """split unit either by row or column into two seperate unit"""  # TODO check split when moving
    from gamescript import unit, leader
    from gamescript.tactical.subunit import fight
    from gamescript.tactical.battle import setup

    move_leader_subunit = fight.move_leader_subunit
    add_new_unit = setup.add_new_unit

    if how == 0:  # split by row
        new_army_subunit = np.array_split(who.subunit_list, 2)[1]
        who.subunit_list = np.array_split(who.subunit_list, 2)[0]
        new_pos = pygame.Vector2(who.base_pos[0], who.base_pos[1] + (who.base_height_box / 2))
        new_pos = who.rotation_xy(who.base_pos, new_pos, who.radians_angle)  # new unit pos (back)
        base_pos = pygame.Vector2(who.base_pos[0], who.base_pos[1] - (who.base_height_box / 2))
        who.base_pos = who.rotation_xy(who.base_pos, base_pos, who.radians_angle)  # new position for original unit (front)
        who.base_height_box /= 2

    else:  # split by column
        new_army_subunit = np.array_split(who.subunit_list, 2, axis=1)[1]
        who.subunit_list = np.array_split(who.subunit_list, 2, axis=1)[0]
        new_pos = pygame.Vector2(who.base_pos[0] + (who.base_width_box / 3.3), who.base_pos[1])  # 3.3 because 2 make new unit position overlap
        new_pos = who.rotation_xy(who.base_pos, new_pos, who.radians_angle)  # new unit pos (right)
        base_pos = pygame.Vector2(who.base_pos[0] - (who.base_width_box / 2), who.base_pos[1])
        who.base_pos = who.rotation_xy(who.base_pos, base_pos, who.radians_angle)  # new position for original unit (left)
        who.base_width_box /= 2
        frontpos = (who.base_pos[0], (who.base_pos[1] - who.base_height_box))  # find new front position of unit
        who.front_pos = who.rotation_xy(who.base_pos, frontpos, who.radians_angle)
        who.set_target(who.front_pos)

    if who.leader[
        1].subunit.game_id not in new_army_subunit.flat:  # move the left sub-general leader subunit if it not in new one
        who.subunit_list, new_army_subunit, new_position = move_leader_subunit(who.leader[1], who.subunit_list, new_army_subunit)
        who.leader[1].subunit_pos = new_position[0] * new_position[1]
    who.leader[1].subunit.unit_leader = True  # make the sub-unit of this leader a gamestart leader sub-unit

    already_pick = []
    for this_leader in (who.leader[0], who.leader[2], who.leader[3]):  # move other leader subunit to original one if they are in new one
        if this_leader.subunit.game_id not in who.subunit_list:
            new_army_subunit, who.subunit_list, new_position = move_leader_subunit(this_leader, new_army_subunit,
                                                                                who.subunit_list, already_pick)
            this_leader.subunit_pos = new_position[0] * new_position[1]
            already_pick.append(new_position)

    new_leader = [who.leader[1], leader.Leader(1, 0, 1, who, battle.leader_stat), leader.Leader(1, 0, 2, who, battle.leader_stat),
                 leader.Leader(1, 0, 3, who, battle.leader_stat)]  # create new leader list for new unit

    who.subunit_position_list = []

    width, height = 0, 0
    subunit_number = 0  # Number of subunit based on the position in row and column
    for this_subunit in who.subunit_list.flat:
        width += who.image_size[0]
        who.subunit_position_list.append((width, height))
        subunit_number += 1
        if subunit_number >= len(who.subunit_list[0]):  # Reach the last subunit in the row, go to the next one
            width = 0
            height += who.image_size[1]
            subunit_number = 0

    # v Sort so the new leader subunit position match what set before
    subunit_sprite = [this_subunit for this_subunit in who.subunit_sprite if
                     this_subunit.game_id in new_army_subunit.flat]  # new list of sprite not sorted yet
    new_subunit_sprite = []
    for this_id in new_army_subunit.flat:
        for this_subunit in subunit_sprite:
            if this_id == this_subunit.game_id:
                new_subunit_sprite.append(this_subunit)

    subunit_sprite = [this_subunit for this_subunit in who.subunit_sprite if
                     this_subunit.game_id in who.subunit_list.flat]
    who.subunit_sprite = []
    for this_id in who.subunit_list.flat:
        for this_subunit in subunit_sprite:
            if this_id == this_subunit.game_id:
                who.subunit_sprite.append(this_subunit)
    # ^ End sort

    # v Reset position of subunit in inspect_ui for both old and new unit
    for sprite in (who.subunit_sprite, new_subunit_sprite):
        width, height = 0, 0
        subunit_number = 0
        for this_subunit in sprite:
            width += battle.icon_sprite_width

            if subunit_number >= len(who.subunit_list[0]):
                width = 0
                width += battle.icon_sprite_width
                height += battle.icon_sprite_height
                subunit_number = 0

            this_subunit.inspect_pos = (width + battle.inspect_ui_pos[0], height + battle.inspect_ui_pos[1])
            this_subunit.rect = this_subunit.image.get_rect(topleft=this_subunit.inspect_pos)
            this_subunit.pos = pygame.Vector2(this_subunit.rect.centerx, this_subunit.rect.centery)
            subunit_number += 1
    # ^ End reset position

    # v Change the original unit stat and sprite
    original_leader = [who.leader[0], who.leader[2], who.leader[3], leader.Leader(1, 0, 3, who, battle.leader_stat)]
    for index, this_leader in enumerate(original_leader):  # Also change army position of all leader in that unit
        this_leader.army_position = index  # Change army position to new one
        this_leader.img_position = this_leader.base_img_position[this_leader.army_position]
        this_leader.rect = this_leader.image.get_rect(center=this_leader.img_position)
    team_commander = who.team_commander
    who.team_commander = team_commander
    who.leader = original_leader

    add_new_unit(battle, who, False)
    # ^ End change original unit

    # v start making new unit
    if who.team == 1:
        whose_army = battle.team1_unit
    else:
        whose_army = battle.team2_unit
    new_game_id = battle.all_unit_list[-1].game_id + 1

    new_unit = unit.Unit(start_pos=new_pos, gameid=new_game_id, squadlist=new_army_subunit, colour=who.colour,
                         control=who.control, coa=who.coa_list, commander=False, startangle=who.angle, team=who.team)

    whose_army.add(new_unit)
    new_unit.team_commander = team_commander
    new_unit.leader = new_leader
    new_unit.subunit_sprite = new_subunit_sprite

    for this_subunit in new_unit.subunit_sprite:
        this_subunit.unit = new_unit

    for index, this_leader in enumerate(new_unit.leader):  # Change army position of all leader in new unit
        this_leader.unit = new_unit  # Set leader unit to new one
        this_leader.army_position = index  # Change army position to new one
        this_leader.img_position = this_leader.base_img_position[this_leader.army_position]  # Change image pos
        this_leader.rect = this_leader.image.get_rect(center=this_leader.img_position)
        this_leader.poschangestat(this_leader)  # Change stat based on new army position

    add_new_unit(battle, new_unit)

    # ^ End making new unit
