#Reimplimentation of classes.py with fixed concepting of cards in game
#zones and full documentation.

#Phase 1: redefinition of classes 4/17/13 -

import random
import copy
import output

##Layers:
##[0]:Copy, [1]:Control, [2]:Text, [3]: Type, [4]:Color, [5]:Abilities
##[6]:P/T CDA [7]: P/T Set [8]: P/T Adjust [9]: P/T Counters [10]: P/T Switch

#
COLOR_WORDS = ('White', 'Blue', 'Black', 'Red', 'Green')
DECK_LISTS = ('WUdeck.txt', 'UBdeck.txt', 'BRdeck.txt', 'RGdeck.txt',
              'GWdeck.txt', 'WBdeck.txt', 'URdeck.txt', 'BGdeck.txt',
              'RWdeck.txt', 'GUdeck.txt')
COLOR_SYMB = ('{W}', '{U}', '{B}', '{R}', '{G}', '{1}')
ORDINAL_WORDS = ('first', 'second', 'third', 'fourth', 'fifth')
NUMBER_WORDS = ('one', 'two', 'three', 'four', 'five')
STEP_LIST = ('untap','upkeep', 'draw','first_main',
                         'begin_combat', 'declare_attackers','declare_blockers',
                         'combat_damage', 'end_combat','second_main', 'end',
                         'cleanup')
STEP_FANCY = ('Untap step', 'Upkeep step', 'Draw step',
                          'First main phase','Beginning of combat step',
                          'Declare attackers step', 'Declare blockers step',
                          'Combat damage step', 'End of combat step',
                          'Second main phase', 'End step', '')
STARTING_LIFE = 20
LAND_WORDS = ('Plains', 'Island', 'Swamp', 'Mountain', 'Forest')
COUNTER_TYPES = ('+1/+1', '-1/-1', 'Loyalty', 'Charge', 'Study',
                 'Slime', 'Hatchling')
INF = 2**20

HELP = '''List of Commands - hit {enter} after a command
__________

Always Valid:

-->help - View this help screen
-->b - View battlefield
-->l - Look at a permanent on the battlefield
-->s - View the stack
-->g - View graveyards
-->h - View hands
-->m - View mana pools
-->o - View the oracle entry for a card in your hand, a graveyard, exile, or a card on the stack
-->o {cardname} - View the oracle entry for the named card
-->li - View life and poison totals
-->t - View the step or phase and turn
-->e - View the exile zone
-->c {text} - display {text} to both players
__________

While you have priority:

-->p - Choose a card to play
-->ma - Choose a mana ability to activate
-->a - Choose an non-mana ability to activate
-->{enter} - Pass priority
-->pass - Pass priority for the remainder of the turn
-->concede - Concede the game
__________

Other situational commands:

-->1, 2, etc. - choose from a numbered list
-->x - Cancel a spell or activation
-->{enter} - Exit an optional list without making a choice
-->y or {enter} - accept an optional effect
-->n - decline an optional effect
-->d - finish declaring targets, attackers, or blockers
__________
'''

class Card:
    #name card
    def __init__(self, data):
        #card only attributes
        self.oracle = data.oracle
        self.name = data.name
        self.typeable_name = self.name
        self.mana_cost_str = data.mana_cost_str
        self.type_str = data.type_str
        self.set = data.set
        self.rarity = data.rarity
        self.cast_choice = []
        self.cost_inc = []
        self.cost_red = []
        self.other_face = None
        self.owner = None
        #attributes for all inheritance classes
        self.sup_type = data.sup_type
        self.type_ = data.type_
        self.sub_type = data.sub_type
        self.rules_text = data.rules_text
        self.color_indicator = []
        self.color_word = []
        self.type_word = []
        #spell attributes
        self.mana_cost = None
        if data.mana_cost != None:
            self.mana_cost = list(data.mana_cost)
        if self.mana_cost != None:
            for i in range(5):
                if self.mana_cost[i]>0:
                    self.color.append(COLOR_WORDS[i])
        self.other_cost = []
        self.sporab_target = []
            #args (game, sporab, target)
        self.ef_list = []
            #args (game, sporab, *)
        if 'Sorcery' in self.type_ or 'Instant' in self.type_:
            self.ef_list.append([effects.inst_sorc_resolve])
        if 'Enchantment' in self.type_ or 'Creature' in self.type_ \
            or 'Artifact' in self.type_ or 'Planeswalker' in self.type_:
                self.ef_list.append([effects.make_perm])
        #perm attributes
        self.power = data.power
        self.toughness = data.toughness
        self.loyalty = data.loyalty
        self.cab = data.cab

class CardObject:
    #name card_obj
    def __init__(self, card):
        self.mana_cost = card.mana_cost
        self.color_indicator = list(card.color_indicator)
        self.name = card.name
        self.sup_type = ''
        self.type_ = ''
        self.sub_type = ''
        self.cab = None
        self.color = []
        self.power = None
        self.toughness = None
        self.attached = []

class Permanent:
    #name perm or creature
    def __init__(self, game, player, card):
        #unique
        self.controller = player
        self.owner = card.owner
        self.original_controller = player
        self.last_controller = player
        self.timestamp = game.timestamp
        self.tapped = False
        self.other_face_up = False
        self.face_down = False
        self.counter = dict()
        for count in COUNTER_TYPES:
            self.counter[count] = 0
        self.attached = []
        self.attached_to = None
        self.regen_shield = False
        self.damage = 0
        self.damage_to_check = []
        self.indestructible = False
        self.damage_sources = []
        self.attacked_this_turn = False
        self.sum_sick = True
        #inherited from card
        self.card = card
        self.cop_val = None
        self.name = ''
        self.color_indicator = []
        self.mana_cost = None
        self.set = ''
        self.cab = None
        self.pointer = []
        self.color = []
        self.sup_type = ''
        self.type_ = ''
        self.sub_type = ''
        self.power = None
        self.toughness = None
                
class CopiableValues:
    def __init__(self, values):
        self.name = values.name
        self.set = values.set
        self.sup_type = values.sup_type
        self.color_indicator = list(values.color_indicator)
        self.type_ = values.type_
        self.sub_type = values.sub_type
        self.rules_text = values.rules_text
        if values.mana_cost != None:
            self.mana_cost = list(values.mana_cost)
        else:
            self.mana_cost = None
        self.power = values.power
        self.toughness = values.toughness
        self.cab = new_effects.cab_copy(values.cab)
        self.ase_color_word = []
        self.ase_creat_type_word = []

class StaticAbil:
    #puts either a permRule into a game rule zone or a triggered ability into the game trig_abil zone
    def __init__(self):
        self.zone_test = None 
        self.effect = []
        self.rules_text = ''
        self.color_word = []
        self.type_word = []
        self.ref_obj = []
        self.name = 'Ability'

class Game:
    def update_game_state(self):
        all_zones = self.battlefield + self.player[0].graveyard +
            self.player[1].graveyard + self.player[0].hand +
            self.player[1].hand + self.exile + self.command_zone +
            self.player[0].library + self.player[1].library + self.stack
        self.timestamp += 1
        self.rule_cleanup('update_game_state')
        for card_obj in self.player[0].graveyard + self.player[1].graveyard +
            self.exile + self.player[0].library + self.player[1].library:
            new_effects.card_obj_from_card(card_obj)
        for perm in self.battlefield:
            perm.cop_val = CopiableValues(perm.card)
            new_effects.perm_from_cop_val(perm)
        added_list = []
        elig_list = list(self.layer[0])
        for obj in self.all_zones:
            if obj.cab.layer_static[0]!=[]:
                if 
                elig_list.append(perm)
        while elig_list !=[]:
            elig_list = self.sort_layer(elig_list, i)
            item = elig_list[0]
            added_list.append(item)
            if item in self.battlefield:
                for stab in item.cab.layer_static[i]:
                    stab.effect[0](self, item, stab, *stab.effect[1:])
            else:
                item.effect[0](self, item, *item.effect[1:])
            elig_list = [item for item in self.layer[i] \
                         if item not in added_list]
            for perm in self.battlefield:
                if perm.cab.layer_static[i]!=[] and perm not in \
                            added_list:
                    elig_list.append(perm)       
        for i in range(1,9):
            added_list = []
            elig_list = list(self.layer[i])
            for perm in self.battlefield:
                if perm.cab.layer_static[i]!=[]:
                    elig_list.append(perm)
            while elig_list !=[]:
                elig_list = self.sort_layer(elig_list, i)
                item = elig_list[0]
                added_list.append(item)
                if item in self.battlefield:
                    for stab in item.cab.layer_static[i]:
                        stab.effect[0](self, item, stab, *stab.effect[1:])
                else:
                    item.effect[0](self, item, *item.effect[1:])
                elig_list = [item for item in self.layer[i] \
                             if item not in added_list]
                for perm in self.battlefield:
                    if perm.cab.layer_static[i]!=[] and perm not in \
                                added_list:
                        elig_list.append(perm)
        for perm in self.battlefield:
            if 'Creature' in perm.type_:
                perm.power += perm.counter['+1/+1']
                perm.toughness += perm.counter['+1/+1']
                perm.power -= perm.counter['-1/-1']
                perm.toughness -= perm.counter['-1/-1']
        added_list = []
        elig_list = list(self.layer[10])
        for perm in self.battlefield:
            if perm.cab.layer_static[10]!=[]:
                elig_list.append(perm)
        while elig_list !=[]:
            elig_list = self.sort_layer(elig_list, i)
            item = elig_list[0]
            added_list.append(item)
            if item in self.battlefield:
                for stab in item.cab.layer_static[10]:
                    stab.effect[0](self, item, stab, *stab.effect[1:])
            else:
                item.effect[0](self, item, *item.effect[1:])
            elig_list = [item for item in self.layer[10] \
                         if item not in added_list]
            for perm in self.battlefield:
                if perm.cab.layer_static[10]!=[] and perm not in \
                            added_list:
                    elig_list.append(perm)
        for perm in self.battlefield:
            if 'Land' in perm.type_:
                land_words = [word for word in perm.sub_type.split() if \
                              word in LAND_WORDS]
                for item in land_words:
                    abts = AbilToStack()
                    abts.other_cost.append(Cost())
                    abts.would_produce = [0,0,0,0,0,0]
                    abts.would_produce[LAND_WORDS.index(item)]+=1
                    abts.ef_list = [[effects.tap_for_mana]]
                    symb = COLOR_SYMB[LAND_WORDS.index(item)]
                    abts.rules_text = '{T}: Add '+symb+' to your mana pool.'
                    perm.cab.act_mana.append(abts)
            for abts in perm.cab.act+perm.cab.act_mana:
                abts.obj = perm
        for perm in self.battlefield:
            for stab in perm.cab.other_static:
                stab.effect[0](self, perm, stab, *stab.effect[1:])
        for card in self.player[0].graveyard+self.player[1].graveyard:
            for stab in card.cab.grav_static:
                stab.effect[0](self, card, stab, *stab.effect[1:])
        for perm in self.battlefield:
            if perm.controller != perm.last_controller:
                self.rule_cleanup('changed_controller')
                self.battlefield.remove(perm)
                self.insert_perm(perm)
                if perm.controller == perm.original_controller:
                    output.output(self, perm.controller, perm.controller.name+\
                                  ' regained control of '+ perm.name)
                else:
                    output.output(self, perm.controller, perm.controller.name + \
                  ' gained control of '+perm.name)
                for item in perm.attached:
                    self.battlefield.remove(item)
                    self.insert_perm(item)
                perm.sum_sick = True
            perm.last_controller = perm.controller
            for stab in perm.cab.trig:
                stab.effect[0](self, perm, stab, *stab.effect[1:])
        for perm in self.ghost_battlefield:
            for stab in perm.cab.trig:
                stab.effect[0](self, perm, stab, *stab.effect[1:])
        for player in self.player:
            for card in player.graveyard:
                for stab in card.cab.trig_grav:
                    stab.effect[0](self, card, stab, *stab.effect[1:])
        for rule in self.rule_obj_char:
            rule.effect[0](self, rule, *rule.effect[1:])
