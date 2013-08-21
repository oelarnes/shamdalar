import effects
import copy
import random
import card_import_inn
import output

##Layers:
##[0]:Copy, [1]:Control, [2]:Text, [3]: Type, [4]:Color, [5]:Abilities
##[6]:P/T CDA [7]: P/T Set [8]: P/T Adjust [9]: P/T Counters [10]: P/T Switch

#sporab - spell or ability

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

class Data:
    def __init__(self):
        return None

class Nothing:
    def __init__(self):
        self.name = 'Nothing'

class SporabRule:
    def __init__(self, sporab, location):
        self.timestamp = sporab.timestamp
        self.obj = sporab.obj
        self.effect = []
        self.cleanup = effects.cl_until_eot
        self.location = location
        location.append(self)
        self.color_word = list(sporab.color_word)
        self.type_word = list(sporab.type_word)
        self.ref_obj = list(sporab.target)
        self.name = sporab.name

class ReplacementEffect:
    def __init__(self):
        self.name = ''
        self.test = None
        self.type_word = []
        self.color_word = []
        self.effect = []
        self.ref_obj = []

class PermRule:
    def __init__(self, perm, stab, location):
        self.timestamp = perm.timestamp
        self.effect = []
        self.obj = perm
        self.cleanup = effects.cl_bf_update
        self.location = location
        location.append(self)
        self.ref_obj = []
        self.target = None
        self.color_word = stab.color_word
        self.type_word = stab.type_word
        self.name = stab.rules_text

class CardAbilities:
    #name cab
    def __init__(self):
        self.act = []
        self.act_mana = []
        self.act_grav = []
        self.act_hand = []
        #the trigger abilities should be changed to functions that put abts
        #objects into game.trig_abil
        self.trig = []
        self.trig_grav = []
        #in the next two lists go funtions that put PermRule objects
        #into game.rule_ lists, depending on the arguments necessary
        self.layer_static = [[] for i in range(11)]
        self.other_static = []
        self.grav_static = []
        self.keyword = []
        self.as_enters = []

class Cost:
    def __init__(self):
        self.test = [effects.test_tap]
        self.effect = [effects.fun_tap]
        
class Card:
    #name card
    def __init__(self, data):
        #card only attributes
        self.timestamp = None
        self.base = None
        self.oracle = data.oracle
        self.name = data.name
        self.ref_name = self.name
        self.mana_cost_str = data.mana_cost_str
        self.type_str = data.type_str
        self.set = data.set
        self.rarity = data.rarity
        self.cast_choice = []
        self.real = data.real
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
        self.color = []
        self.color_word = []
        self.type_word = []
        #spell attributes
        self.mana_cost = None
        if data.mana_cost!=None:
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

class FakeCard:
    #name card
    def __init__(self):
        #card only attributes
        self.oracle = ''
        self.name = ''
        self.ref_name = ''
        self.mana_cost_str = ''
        self.base = None
        self.type_str = ''
        self.set = ''
        self.rarity = ''
        self.cast_choice = []
        self.real = False
        self.cost_inc = []
        self.cost_red = []
        self.other_face = None
        self.owner = None
        #attributes for all inheritance classes
        self.sup_type = ''
        self.type_ = ''
        self.sub_type = ''
        self.rules_text = ''
        self.color_indicator = []
        self.color = []
        self.color_word = []
        self.type_word = []
        #spell attributes
        self.mana_cost = None
        self.other_cost = []
        self.sporab_target = []
            #args (game, sporab, target)
        self.ef_list = []
        #perm attributes
        self.power = None
        self.toughness = None
        self.loyalty = None
        self.cab = CardAbilities()
        self.other_face = None

class PermBase:
    #copiable values
    def __init__(self, card_or_base):
        self.name = card_or_base.name
        self.ref_name = card_or_base.ref_name
        self.set = card_or_base.set
        self.sup_type = card_or_base.sup_type
        self.color_indicator = list(card_or_base.color_indicator)
        self.type_ = card_or_base.type_
        self.sub_type = card_or_base.sub_type
        self.rules_text = card_or_base.rules_text
        if card_or_base.mana_cost != None:
            self.mana_cost = list(card_or_base.mana_cost)
        else:
            self.mana_cost = None
        self.power = card_or_base.power
        self.toughness = card_or_base.toughness
        self.cab = effects.cab_copy(card_or_base.cab)

class AbilToStack:
    #lives in an attribute of perm.cab, analagous to a card for
    #the purpose of initializing an ability on the stack
    #name abts. effects and tests defined in card_import_inn, obj and name
    #defined in ability population, otherwise only changed by layer[2]
    #unique attributes
    def __init__(self):
        #shared with spell
        self.mana_cost = None
        self.other_cost = []
        self.timing = []
        self.ref_obj = []
        self.cast_choice = []
        self.sporab_target = []
        self.ef_list = [[effects.abil_resolve]]
        self.color_word = []
        self.cost_inc = []
        self.cost_red = []
        self.type_word = []
        self.rules_text = ''

class StabAbilToStack:
    def __init__(self, game, obj, stab):
        location = game.trig_abil
        self.trig_test = []
        self.mana_cost = None
        self.other_cost = []
        self.ref_obj = []
        self.cast_choice = []
        if obj in game.battlefield or obj in game.ghost_battlefield:
            self.controller = obj.controller
        else:
            self.controller = obj.owner
        self.add_cost = []
        self.ef_list = [[effects.abil_resolve]]
        self.sporab_target = []
        self.triggered = False
        self.cost_inc = []
        self.cost_red = []
        self.obj = obj
        self.rules_text = stab.rules_text
        self.name = obj.name + '\'s ability'
        self.cleanup = effects.cl_bf_update
        self.color_word = stab.color_word
        self.type_word = stab.type_word
        self.location = location
        location.append(self)

class StaticAbil:
    #this is activated after update_battlefield and puts either a permRule
    #into a game rule zone or a triggered ability into the game trig_abil zone
    def __init__(self):
        self.effect = []
        self.rules_text = ''
        self.color_word = []
        self.type_word = []
        self.ref_obj = []
        self.name = 'Ability'
        
class Player:
    #name player
    def __init__(self, data):
        self.prompt = data.prompt
        self.life = STARTING_LIFE
        lib = data.lib
        self.lib = [effects.card_copy(card, self) for card in lib]
        random.shuffle(self.lib)
        self.hand = []
        self.graveyard = []
        self.lost = False
        self.command = []
        self.attached = []
        self.damage_sources = []
        self.poison = 0
        self.max_hand_size = 7
        self.passed_for_turn = False
        self.mana_pool = [0,0,0,0,0,0]
        self.position = data.position
        self.name = 'Player ' + str(self.position)
        self.played_land = False
        self.next_player = None
        self.dealt_damage_this_turn = False
        self.storm_count = 0
        self.last_turn_storm_count = 0

class Permanent:
    #name perm or creature
    def __init__(self, game, player, card):
        #unique
        self.controller = player
        self.original_controller = player
        self.last_controller = player
        self.timestamp = game.timestamp
        self.tapped = False
        self.other_face_up = False
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
        self.base = PermBase(card)
        self.name = ''
        self.color_indicator = list(self.base.color_indicator)
        self.mana_cost = None
        self.ref_name = ''
        self.set = ''
        self.cab = None
        self.pointer = []
        self.color = []
        self.sup_type = ''
        self.type_ = ''
        self.sub_type = ''
        self.power = None
        self.toughness = None
                
class Spell:
        #name spell or sporab
    def __init__(self, game, player, card):
        self.spell = True
        self.obj = self
        self.card = card
        self.color = card.color
        self.timestamp = game.timestamp
        self.controller = player
        self.cast_choice = card.cast_choice
        self.name = card.name
        self.cost_inc = card.cost_inc
        self.cost_red = card.cost_red
        self.type_ = card.type_
        self.sup_type = card.sup_type
        self.sub_type = card.sub_type
        self.sporab_target = list(card.sporab_target)
        self.color_word = list(card.color_word)
        self.type_word = list(card.type_word)
        self.ref_obj = []
        self.target = []
        self.rules_text = card.rules_text
        self.ef_list = list(card.ef_list)
        self.cab = effects.cab_copy(card.cab)
        if card.mana_cost != None:
            self.mana_cost = list(card.mana_cost)
        else:
            self.mana_cost = None
        self.other_cost = list(card.other_cost)
        self.abts = None
        
class AbilOnStack:
        #name abil or sporab
    def __init__(self, game, player, abts):
        self.spell = False
        self.obj = abts.obj
        self.abts = abts
        self.timestamp = game.timestamp
        self.controller = player
        self.cast_choice = abts.cast_choice
        self.name = abts.obj.name +'\'s ability'
        self.sporab_target = abts.sporab_target
        self.color_word = abts.color_word
        self.type_word = abts.type_word
        self.cost_inc = abts.cost_inc
        self.cost_red = abts.cost_red
        self.ref_obj = list(abts.ref_obj)
        self.target = []
        self.ef_list = abts.ef_list
        self.mana_cost = abts.mana_cost
        self.other_cost = abts.other_cost
        self.rules_text = abts.rules_text

class Game:
        #name game
    def __init__(self):
        self.player_choice = None
        self.card_dict = card_import_inn.initCardList('Innistrad')
        self.trig_to_stack = [[],[]]
        self.stack = []
        self.battlefield = []
        self.exile = []
        self.more_cleanup_req = False
        self.ghost_battlefield = []
        self.player = []
        for i in (0,1):
            data = Data()
            prompt = ['-p1->','-p2->']
            data.lib = []
            data.position = i+1
            data.prompt = prompt[i]
            self.player.append(Player(data))
        self.player[0].next_player = self.player[1]
        self.player[1].next_player = self.player[0]
        for player in self.player:
            decklist = effects.choose_obj_from_list(self, player, DECK_LISTS, \
                            'Choose a deck')
            lib_names = card_import_inn.deckImport(decklist)
            lib = [effects.card_copy(self.card_dict[name], player) for name\
                   in lib_names]
            random.shuffle(lib)
            player.lib = lib
        for i in (0,1):
            print self.player[i].name
            effects.draw_cards(self, self.player[i], 7)
        print '__________'
        print
        print 'Type "help" for a list of commands'
        print '__________'
        print
        

        self.active_player = self.player[0]
        self.prior_player = self.player[0]
        self.passed_prior = False

        self.attacks = []
        self.attackers = []
        self.blocks = []
        self.blockers = []
        self.timestamp = 0

        self.morbid = False
        
        self.extra_turn = []
        self.turn_is_extra = False
        self.next_player_reg_turn = None
        
        #Rules are rule objects with cleanup and effect attributes
        #that apply to effects in certain categories.
        #Rules are maintained by card effects
        #Rules can add triggers to activeTrigger, act as replacement effects,
        #or modify a test value. until eot effects add a cleanupRule
        self.layer = [[] for i in range(11)]
            ##Layers:
            ##[0]:Copy [1]:Control [2]:Test [3]: Type
            ##[4]:Color [5]:Abilities [6]:P/T CDA [7]: P/T Set
            ##[8]: P/T Adjust [9]: P/T Counters [10]: P/T Switch
        self.rule_untap = []
        #effect arg: (game, *) return perm List
        self.rule_can_cast = []
        #effect arg (game, rule) return list
        self.rule_alt_cost = []
        #effect arg (game, rule, spell_list) adds to the list
        self.rule_cant_cast = []
        self.rule_target = []
        #effect arg: (game, rule, sporab, target, *) return Bool
        self.rule_counter = []
        #effect arg: (game, rule, source, target, *) return Bool
        self.rule_cant_attack = []
        #effect arg: (game, *), returns creat list
        self.rule_attack = []
        #effect arg: (game, rule, attacks, *) returns Int (#req satis.)
        self.rule_damage = []
        #effect arg: (game, rule, source, target, amount, *) return Int

        self.rule_leave_stack = []
        #effect arg: (game, rule, spell)
        self.rule_block = []
        #effect arg: (game, rule, block, *) return Int (#req satis)
        #block consists of pairs [A,B], assign a value to the blocks
        #where A blocks B
        self.rule_cant_block = []
        #effect arg: (game, rule, blocker, attacker) can A block B?
        self.rule_obj_char = []
        #effect arg: (game, rule, *)
        self.rule_activate = []
        self.rule_as_enters = []
        self.rule_parallel_lives = []
        self.rule_laboratory_maniac = []
        self.trig_abil = []
        self.rule_step = []
        self.rule_cost_inc = []
        #effect arg (game, rule, player, sporab)
        self.rule_cost_red = []

        self.undo_list = []
        
        self.step = 'untap'
        self.damage_creat = []
        self.first_strike_phase = False
        print 'Player 1\'s turn, untap step'
        self.increment_step()

        rule = Data()
        rule.cleanup = effects.cl_first_turn
        rule.effect = [effects.skip_draw_phase]
        rule.location = self.rule_step
        rule.location.append(rule)

        rule = Data()
        rule.cleanup = effects.cl_never
        rule.effect = [effects.skip_blockers_damage]
        rule.location = self.rule_step
        rule.location.append(rule)

        rule = Data()
        rule.cleanup = effects.cl_never
        rule.effect = [effects.r_damage_planeswalker_redirect]
        rule.location = self.rule_damage
        rule.location.append(rule)

        rule = Data()
        rule.cleanup = effects.cl_never
        rule.effect = [effects.r_can_play_normal]
        rule.location = self.rule_can_cast
        rule.location.append(rule)
            
    def print_hand(self, player):
        print player.name+'\'s hand:'
        for card in player.hand:
            print card.name

    def ask_oracle(self, card_name):
        if self.card_dict[card_name].other_face==None:
            print self.card_dict[card_name].oracle
        else:
            print self.card_dict[card_name].oracle
            print self.card_dict[card_name].other_face.oracle

    def print_stack(self):
        for i in range(len(self.stack)):
            self.print_sporab(self.stack[-1-i])

    def print_life(self, player):
        print player.name + '\'s life:'
        print player.life

    def perm_order(self, perm1, perm2):
        exc = [None, self.player[0], self.player[1]]
        if perm1.attached_to not in exc and perm2.attached_to in exc:
            return self.perm_order(perm1.attached_to,perm2)
        if perm2.attached_to not in exc and perm1.attached_to in exc:
            if perm2.attached_to == perm1:
                return perm1
            if self.battlefield.index(perm2.attached_to)< \
               self.battlefield.index(perm1):
                return perm2
            return perm1
        if perm1.attached_to not in exc and perm2.attached_to not in exc:
            if perm1.attached_to != perm2.attached_to:
                if self.battlefield.index(perm2.attached_to) <\
                    self.battlefield.index(perm1.attached_to):
                    return perm2
                else:
                    return perm1
            else:
                return self.perm_order(perm1.attached_to, perm2)
        if perm1.controller == self.player[1] and \
                perm2.controller == self.player[0]:
            return perm2
        if perm1.controller == self.player[0] and \
                perm2.controller == self.player[1]:
            return perm1
        if 'Land' in perm1.type_ and 'Land' not in perm2.type_:
            return perm2
        if 'Land' in perm1.type_ and 'Land' not in perm2.type_:
            return perm2
        if 'Creature' in perm1.type_ and 'Creature' not in perm2.type_:
            return perm1
        if 'Creature' in perm2.type_ and 'Creature' not in perm1.type_:
            return perm2
        return perm1

    def insert_perm(self, perm):
        #want the index to insert the new guy. Insert is 'before this one'
        for perm1 in self.battlefield:
            if self.perm_order(perm1, perm)==perm:
                self.battlefield.insert(self.battlefield.index(perm1), perm)
                return None
        self.battlefield.insert(len(self.battlefield), perm)
        return None
    
    def sort_battlefield(self, battlefield):
        if len(battlefield) == 1 or len(battlefield)==0:
            return battlefield
        if len(battlefield) == 2:
            greater = self.perm_order(battlefield[0], battlefield[1])
            battlefield.remove(greater)
            return [greater, battlefield[0]]
        else:
            list1 = self.sort_battlefield(battlefield[:len(battlefield)/2])
            list2 = self.sort_battlefield(battlefield[len(battlefield)/2:])
            new_battlefield = []
            item1 = list1.pop(0)
            item2 = list2.pop(0)
            done = False
            while not done:
                if self.perm_order(item1,item2)==item1:
                    new_battlefield.append(item1)
                    if list1 == []:
                        new_battlefield.append(item2)
                        new_battlefield.extend(list2)
                        done = True
                    else:
                        item1 = list1.pop(0)
                else:
                    new_battlefield.append(item2)
                    if list2 == []:
                        new_battlefield.append(item1)
                        new_battlefield.extend(list1)
                        done = True
                    else:
                        item2 = list2.pop(0)
            return new_battlefield

    def sort_layer(self, layer, i):
        if len(layer) == 1 or 0:
            return layer
        if len(layer) == 2:
            greater = self.layer_order(layer[0], layer[1], i)
            layer.remove(greater)
            return [greater, layer[0]]
        else:
            list1 = self.sort_layer(layer[:len(layer)/2], i)
            list2 = self.sort_layer(layer[len(layer)/2:], i)
            new_layer = []
            item1 = list1.pop(0)
            item2 = list2.pop(0)
            done = False
            while not done:
                if self.layer_order(item1,item2,i)==item1:
                    new_layer.append(item1)
                    if list1 == []:
                        new_layer.append(item2)
                        new_layer.extend(list2)
                        done = True
                    else:
                        item1 = list1.pop(0)
                else:
                    new_layer.append(item2)
                    if list2 == []:
                        new_layer.append(item1)
                        new_layer.extend(list1)
                        done = True
                    else:
                        item2 = list2.pop(0)
            return new_layer
        
    def print_perm(self, perm, number = False):
        out = perm.name
        if 'Creature' in perm.type_:
            out+= ' '+ str(perm.power)+'/' \
                      + str(perm.toughness)
        if perm.damage > 0:
            out+= ' d:'+str(perm.damage)
        if perm.tapped:
            out+= ' (t)'
        attackers = [item[0] for item in self.attacks]
        if perm in attackers:
            out+= ' (a)'
        if number!= False:
            out+= ' ('+str(number)+')'
        return out

    def print_sporab(self, sporab):
        print sporab.name, '('+sporab.controller.name+')'
        if sporab.target != []:
            print '    targeting:',
            for item in sporab.target:
                if item == sporab.target[-1]:
                    plus = ''
                else:
                    plus = ','
                print item.name+plus,
            print


    def print_act_list(self, abts_list, land_dict=[]):
        perms = []
        for item in abts_list:
            if item.obj not in perms:
                perms.append(item.obj)
        counter = 0
        for perm in perms:
            if 'Basic' in perm.sup_type and perm.attached==[]:
                output.output(self, perm.controller,
                              self.print_perm(perm,
                                    number=len(land_dict[perm.sub_type])),'')
            else:
                output.output(self, perm.controller,
                                self.print_perm(perm), '')
            if perm != perms[-1]:
                while abts_list[counter].obj == perm:
                    print str(counter+1)+'. '+abts_list[counter].rules_text
                    counter+=1
            else:
                while counter < len(abts_list):
                    print str(counter+1)+'. ' + abts_list[counter].rules_text
                    counter+=1
        
    def look_battlefield(self, player, battlefield):
        if len(battlefield)>0:
            perm = effects.choose_obj_from_list(self, player, battlefield,
                        prompt='Choose a permanent to look at or hit enter',
                                                 alt_input =[''])
            if perm == '':
                return None
            self.look_perm(player, perm)

    def print_battlefield(self, player, battlefield):
        if len(battlefield)>0:
            effects.choose_obj_from_list(self, player,
                                         battlefield, just_looking=True)

    def print_graveyard(self, player):
        if len(self.player[0].graveyard+self.player[1].graveyard)>0:
            effects.choose_obj_from_list(self, player,
                                         self.player[0].graveyard+self.player[1].graveyard
                                         , just_looking=True)

    def print_exile(self,player):
        if len(self.exile)>0:
            effects.choose_obj_from_list(self, player,
                                         self.exile, just_looking=True)

    def print_library(self, player):
        for card in player.lib:
            print card.name

    def look_perm(self, player, perm):
        print perm.name
        if not perm.card.real:
            print 'Token'
        if perm.attached_to!=None:
            print '  on: '+perm.attached_to.name
        for item in perm.attached:
            print '    '+item.name
        print 'Controller:', perm.controller.name
        for color in perm.color:
            print color,
        if perm.color == []:
            print 'Colorless',
        print
        bit = ' '
        if perm.sup_type == '': bit = ''
        print perm.sup_type + bit + perm.type_,
        if perm.sub_type != '':
            print '-', perm.sub_type,
        print
        for word in perm.cab.keyword:
            print word
        zones = perm.cab.act+ perm.cab.act_mana+perm.cab.trig + \
                perm.cab.other_static + perm.cab.grav_static
        for layer in perm.cab.layer_static:
            zones += layer
        for item in zones:
            print item.rules_text
        if perm.indestructible:
            print 'Indestructible'
        for item in perm.pointer:
            output.output(self, player,
                          item[0]+item[1].name, '')
        for counter in COUNTER_TYPES:
            if counter not in ('+1/+1', '-1/-1', 'Loyalty'):
                if perm.counter[counter]==1:
                    output.output(self, player, str(perm.counter[counter])+\
                                  ' '+counter+' counter','')
                if perm.counter[counter]>1:
                    output.output(self, player, str(perm.counter[counter])+\
                                  ' '+counter+' counters','')
        if 'Planeswalker' in perm.type_:
            print 'Loyalty:', perm.counter['Loyalty']
        if effects.is_creature(self, perm):
            print str(perm.power)+'/'+str(perm.toughness)
            print 'Damage: ', perm.damage
        if perm.tapped or perm in self.attackers:
            if perm.tapped:
                print 'Tapped',
            if perm.tapped and perm in self.attackers:
                print 'and',
            if perm in self.attackers:
                print 'Attacking',
                print self.attacks[self.attackers.index(perm)][1].name,
            print

    def get_input(self, player, extra_prompt=''):
        player_input = raw_input(player.prompt+extra_prompt)
        input_found = False
        while True:
            if 'help' == player_input:
                print HELP
            if 'o' == player_input:
                item_list = player.hand+self.player[0].graveyard+\
                            self.player[1].graveyard+\
                            self.exile+self.stack
                card = effects.choose_obj_from_list(self, player, item_list,\
                            'Choose a card to see its oracle text or hit enter',
                                                    [''])
                if card != '':
                    if card.other_face==None:
                        output.output(self, player, card.oracle\
                                      , '')
                    else:
                        output.output(self, player, card.oracle\
                                      +'\n'+card.other_face.\
                                      oracle, '')
            elif 'o ' == player_input[:2]:
                card_name = player_input[2:]
                if card_name in self.card_dict:
                    self.ask_oracle(player_input[2:])
                else: print 'Invalid card name'
            elif 'c ' == player_input[:2]:
                output.output(self, player, player_input[2:])
            elif player_input=='l':
                self.look_battlefield(player, self.battlefield)
            elif player_input=='b':
                self.print_battlefield(player, self.battlefield)
            elif player_input=='s':
                self.print_stack()
            elif player_input=='li':
                self.print_life(player)
                self.print_life(player.next_player)
            elif player_input=='g':
                self.print_graveyard(player)
            elif player_input=='h':
                self.print_hand(player)
                print player.next_player.name + ':'
                print len(player.next_player.hand), 'cards in hand'
            elif player_input=='m':
                print player.name + '\'s mana pool:'
                print(self.print_cost(player.mana_pool))
                print player.next_player.name + '\'s mana pool:'
                print(self.print_cost(player.next_player.mana_pool))
            elif player_input=='t':
                print self.active_player.name+'\'s turn,',
                print STEP_FANCY[STEP_LIST.index(self.step)].lower()
            elif player_input=='e':
                self.print_exile(player)
            else:
                return player_input
            player_input = raw_input(player.prompt)

    def int_input(self, player, extra_prompt='', u_range=INF, l_range = 1,
                  alt_input = None):
        while True:
            input_ = self.get_input(player, extra_prompt)
            if input_.isdigit():
                if int(input_)>u_range or l_range > int(input_):
                    print 'Out of range'
                else: return int(input_)
            elif alt_input!= None:
                if input_ in alt_input:
                    return input_
            print 'Enter an integer'

    def can_cast(self, spell):
        if any([not rule.effect[0](self, rule, spell) for rule \
                in self.rule_cant_cast]):
            return False
        spell1 = Spell(self, spell.controller, spell.card)
        effects.determine_total_cost(self, spell1)
        player = spell1.controller
        if spell1.mana_cost!=None:
            if not effects.test_can_pay_mana(self, player,
                                              spell1.mana_cost):
                return False
            #choices made while casting may affect the final cost, so
            #this should return the minimal possible cost among possible
            #choices
        else:
            return False
        for cost in spell1.other_cost:
            if not cost.test[0](self, spell1.controller, spell1, *cost.test[1:]):
                return False
        return True

    def can_act(self, abil):
        effects.determine_total_cost(self, abil)
        player = abil.controller
        if abil.mana_cost!=None:
            if len(abil.other_cost)>0:
                if abil.other_cost[0].test[0]!=effects.test_tap:
                    if not effects.test_can_pay_mana(self, player, abil.mana_cost):
                        return False
                else:
                    if not effects.test_can_pay_mana(self, player, abil.mana_cost,
                                                     used_producers = [abil.obj]):
                        return False
            else:
                if not effects.test_can_pay_mana(self, player, abil.mana_cost):
                    return False
        for cost in abil.other_cost:
            if not cost.test[0](self, abil.controller, abil, *cost.test[1:]):
                return False
        return True
    
    def cast_list_insert(self, player, cast_list, card):
        for item in cast_list:
            if card in player.hand and item in player.graveyard:
                cast_list.insert(cast_list.index(item), card)
                return None
        cast_list.append(card)
        return None

    def play(self, player):
        first_list = []
        elig_cards = []
        for rule in self.rule_can_cast:
            first_list.extend(rule.effect[0](self, rule, *rule.effect[1:]))
        for rule in self.rule_alt_cost:
            rule.effect[0](self, rule, first_list)
        d = dict()
        for item in first_list:
            if 'Land' in item.type_: #this may be wrong
                elig_cards.append(item)
            elif self.can_cast(item):
                elig_cards.append(item)
        for item in elig_cards:
            if item.card not in d:
                d[item.card]=[item]
            else:
                d[item.card]+=[item]
        cards = []
        for card in d:
            self.cast_list_insert(player, cards, card)
        if len(cards)==0:
            print 'You do not have any cards which can be played at this time'
            return None
        card = effects.choose_obj_from_list(self, player, cards,
                        'Choose a card to play or hit enter', alt_input = '')
        if card == '':
            return None
        elif len(d[card])==1:
            self.play_card(player, d[card][0])
        else:
            mana_costs = [self.print_cost(item.mana_cost) for item in d[card]]
            choice = effects.choose_obj_from_list(self, player, mana_costs,
                                        'Choose a mana cost to pay for this spell')
            self.play_card(player, d[card][mana_costs.index(choice)])
    
    def activate_ability(self, player, mana=False):
        elig_abts = []
        land_dict = dict()
        for word in LAND_WORDS:
            land_dict[word] = []
        for perm in self.battlefield:
            if perm.controller == player:
                if mana:
                    act = perm.cab.act_mana
                else:
                    act = perm.cab.act
                for abts in act:                        
                    check = True
                    for rule in abts.timing:
                        check = min([check, rule(self, player, abts)])
                    for rule in self.rule_activate:
                        check = min([check, rule.effect[0](self, rule, player,
                                        abts, *rule.effect[1:])])
                    if check:
                        abil = AbilOnStack(self, player, abts)
                        if self.can_act(abil):
                            if 'Basic' in perm.sup_type and mana:
                                land_dict[perm.sub_type].append(abts)
                            else:
                                elig_abts.append(abts)
        for word in LAND_WORDS:
            if land_dict[word]!=[]:
                elig_abts.append(land_dict[word][0])
        if len(elig_abts)==0:
            print 'You do not have any abilities which can be activated at this time'
            return False
        self.print_act_list(elig_abts, land_dict)
        print 'Choose an ability to activate or hit enter'
        index = self.int_input(player, u_range = len(elig_abts),
                               alt_input = [''])
        if index == '':
            return False
        else:
            abts = elig_abts[index-1]
            if 'Basic' in abts.obj.sup_type and abts.obj.attached==[]:
                key  = abts.obj.sub_type
                if len(land_dict[key])>1:
                    print 'How many?'
                    number = self.int_input(player,
                                u_range = len(land_dict[key]))
                    for i in range(number):
                        abts = land_dict[key][i]
                        abts.other_cost[0].effect[0](self, player, abts)
                        abts.ef_list[0][0](self, player, abts)
                else:
                    abts.other_cost[0].effect[0](self, player, abts)
                    abts.ef_list[0][0](self, player, abts)                                          
            else:
                if mana:
                    if abts.other_cost[0].test[0]==effects.test_tap:
                        abts.other_cost[0].effect[0](self, player, abts)
                    if abts.mana_cost!=None:
                        effects.pay_mana_cost(self, player, abts.mana_cost)
                    for cost in abts.other_cost:
                        if cost.test[0]!=effects.test_tap:
                            cost.effect[0](self, player, abts)
                    abts.ef_list[0][0](self, player, abts,
                                                 *abts.ef_list[0][1:])
                else:
                    sporab = AbilOnStack(self, player, abts)
                    if not self.stack_sporab(sporab):
                        print 'Activation canceled'
                        for item in self.undo_list:
                            item[0](self, *item[1:])
                        for i in (0,1):
                            for item in self.trig_to_stack[i]:
                                print 'Trigger canceled'
                                self.trig_to_stack[i].remove(item)
                        self.undo_list = []
                    else:
                        self.update_battlefield()
        return True
    def undo(self):
        for item in self.undo_list:
            item[0](self, *item[1:])
        for i in (0,1):
            for item in self.trig_to_stack[i]:
                print 'Trigger canceled'
                self.trig_to_stack[i].remove(item)
        self.undo_list = []
        
                 
    def stack_sporab(self, sporab, cheat=False):
        for item in sporab.cast_choice:
            item(self, sporab)
        if effects.get_target(self, sporab.controller, sporab) == False:
            return False
        effects.determine_total_cost(self, sporab)
        if len(sporab.other_cost)>0:
            if sporab.other_cost[0].test[0] == effects.test_tap:
                sporab.other_cost[0].effect[0](self, sporab.controller, sporab)
        if sporab.mana_cost != None and not cheat:
            if not effects.pay_mana_cost(self, sporab.controller,
                                      sporab.mana_cost):
                return False
        for item in sporab.other_cost:
            if item.test[0]!=effects.test_tap:
                if item.effect[0](self, sporab.controller, sporab,
                                  *item.effect[1:])==False:
                    print sporab.other_cost.index(item)
                    return False
        print 'Added to the stack:'
        self.stack.append(sporab)
        self.print_sporab(sporab)
        if sporab.spell:
            sporab.controller.storm_count+=1
        self.passed_prior = False
        return True
        
    def update_battlefield(self):
        self.timestamp += 1
        self.rule_cleanup('bf_update')
        for perm in self.battlefield:
            effects.perm_from_base(self, perm)
        for card in self.player[0].graveyard + self.player[1].graveyard+self.exile:
            effects.card_from_base(card)
        for i in range(9):
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
        
    def layer_order(self, obj1, obj2, layer):
        if obj1.timestamp < obj2.timestamp:
            return obj1
        return obj2
    
    def populate_cant_attack(self):
        cant_attack_list = []
        for rule in self.rule_cant_attack:
            cant_attack_list.extend(rule.effect[0](self, rule,
                                                   *rule.effect[1:]))
        return cant_attack_list

    def rule_cleanup(self, key):
        zones = self.rule_untap + self.rule_can_cast + self.rule_target +\
                self.rule_damage + self.rule_counter + \
                self.rule_cant_attack + self.rule_activate +\
                self.rule_block + self.rule_attack + self.trig_abil + \
                self.rule_cant_block + self.rule_obj_char + self.rule_step\
                +self.rule_as_enters + self.rule_cost_inc + self.rule_cost_red\
                +self.rule_parallel_lives + self.rule_laboratory_maniac \
                +self.rule_cant_cast + self.rule_leave_stack + self.rule_alt_cost
        for i in range(11):
            zones += self.layer[i]
        for rule in zones:
            rule.cleanup(self, rule, key)
                
    def check_state(self):
        self.update_battlefield()
        actions_taken = False
        trig_list = []
        for player in self.player:
            if player.life <= 0:
                player.lost = True
                return False
            if player.poison >= 10:
                player.lost = True
                return False
        if self.player[0].lost or self.player[1].lost:
            actions_taken = True
        battlefield = list(self.battlefield)
        for perm in battlefield:
            if perm.attached_to==None and 'Aura' in perm.sub_type:
                effects.die(self, perm)
            if perm.attached_to!=None and perm.attached_to not in self.player:
                check = True
                if 'Enchant Creature' in perm.cab.keyword:
                    if 'Creature' not in perm.attached_to:
                        perm.attached_to.attached.remove(perm)
                        perm.attached_to = None
                        check = False
                elif 'Creature' in perm.type_:
                    perm.attached_to.attached.remove(perm)
                    perm.attached_to = None
                    check = False
                elif 'Aura' not in perm.sub_type and \
                     'Equipment' not in perm.sub_type:
                    perm.attached_to.attached.remove(perm)
                    perm.attached_to = None
                    check = False
                elif any(['Protection from '+word.lower()+'s' in \
                          perm.attached_to.cab.keyword for word in \
                          perm.type_.split()]):
                    perm.attached_to.attached.remove(perm)
                    perm.attached_to = None
                    check = False
                elif any(['Protection from '+word.lower() in \
                             perm.attached_to.cab.keyword for word in perm.color]):
                    perm.attached_to.attached.remove(perm)
                    perm.attached_to = None
                    check = False
                if perm.attached_to == perm:
                    perm.attached_to.attached.remove(perm)
                    perm.sttached_to = None
                    check = False
                if not check:
                    if 'Aura' in perm.sub_type:
                        effects.die(self, perm)
                    else:
                        self.battlefield.remove(perm)
                        self.insert_perm(perm)
                    actions_taken = True
            if 'Creature' in perm.type_:
                if perm.toughness <= 0:
                    effects.die(self, perm)
                    trig_list.append([perm, 'bf_to_gy'])
                    actions_taken = True
                elif perm.damage > 0 and (perm.damage >= perm.toughness or \
                        any(['Deathtouch' in item[0].cab.keyword for item in \
                            perm.damage_to_check])):
                    if not perm.indestructible:
                        if not perm.regen_shield:
                            actions_taken = True
                            effects.die(self, perm)
                            trig_list.append([perm, 'bf_to_gy'])
                        else:
                            effects.regenerate(self, perm)
                            actions_taken = True
                perm.damage_to_check = []
            if 'Planeswalker' in perm.type_:
                if perm.counter['Loyalty']<=0:
                    effects.die(self,perm)
                    trig_list.append([perm, 'bf_to_gy'])
                    actions_taken = True
                for perm1 in battlefield:
                    if perm1 != perm and perm1.sub_type == perm.sub_type \
                       and perm not in self.ghost_battlefield:
                        effects.die(self, perm)
                        trig_list.append([perm, 'bf_to_gy'])
                        actions_taken = True
            if 'Legendary' in perm.sup_type:
                for perm1 in battlefield:
                    if perm1 != perm and perm1.name == perm.name and \
                       perm not in self.ghost_battlefield:
                            effects.die(self, perm)
                            trig_list.append([perm, 'bf_to_gy'])
                            actions_taken = True

            m = min([perm.counter['+1/+1'], perm.counter['-1/-1']])
            if m > 0:
                perm.counter['+1/+1'] -= m
                perm.counter['-1/-1'] -= m
                actions_taken = True
        if actions_taken:
            self.update_battlefield()
            for item in trig_list:
                self.add_to_tst(item)
            return False
        player = self.active_player
        for i in range(2):
            tst = self.trig_to_stack[player.position-1]
            while len(tst)>1:
                print 'Choose an ability to stack next:'
                number = 1
                for item in tst:
                    print str(number)+'.',
                    print item.rules_text
                    number+=1
                number = self.int_input(player, l_range = 1,
                                        u_range = len(tst))
                item = tst[number-1]
                self.stack_sporab(item)
                self.update_battlefield()
                tst.remove(item)
            if len(tst)==1:
                self.stack_sporab(tst[0])
                self.update_battlefield()
                actions_taken = True
                tst.remove(tst[0])
            player = player.next_player
        if actions_taken:
            self.undo_list = []
            return False
        return True

    def add_to_tst(self, item):
        for abts in self.trig_abil:
            if abts.trig_test(self, abts, *item):
                print abts.name, 'triggered'
                abts.triggered = True
                sporab = AbilOnStack(self, abts.controller, abts)
                sporab.rules_text = abts.rules_text
                sporab.ref_obj.append(item[0])
                self.trig_to_stack[ \
                    abts.controller.position-1].append(sporab)
        self.ghost_battlefield = []
        
    def play_card(self, player, spell, cheat=False):
        if 'Land' in spell.type_:
            self.undo_list = []
            player.hand.remove(spell.card)
            perm = Permanent(self, player, spell.card)
            effects.enter_battlefield(self, [perm])
            player.played_land = True
        else:
            self.undo_list = []
            self.cast_spell(player, spell, cheat)

    def print_cost(self, cost):
        cost_str = ''
        if cost[5]>0:
            cost_str+='{'+str(cost[5])+'}'
        for i in range(5):
            for j in range(cost[i]):
                cost_str+=COLOR_SYMB[i]
        if cost_str == '':
            cost_str = '{0}'
        return cost_str

    def convert_cost_str(self, cost_str):
        cost = [0,0,0,0,0,0]
        while cost_str!='':
            if cost_str[1].isdigit():
                cost[5]+=int(cost_str[1])
            else:
                if cost_str[1] != 'X':
                    cost[COLOR_SYMB.index(cost_str[0:3])]+=1
            cost_str=cost_str[3:]
        return cost

    def cast_spell(self, player, spell, cheat = False):        
        from_gy = False
        if spell.card in player.graveyard:
            from_gy = True
            player.graveyard.remove(spell.card)
            self.undo_list.append([effects.return_card_to_gy, spell.card])
        else:
            player.hand.remove(spell.card)
            self.undo_list.append([effects.return_card_to_hand, spell.card])
        spell.card = effects.card_copy(spell.card.base, spell.card.owner)
        if self.stack_sporab(spell, cheat)==False:
            print 'Casting of spell canceled'
            for item in self.undo_list:
                item[0](self, *item[1:])
            self.trig_to_stack = [[],[]]
            self.undo_list = []
        else:
            self.update_battlefield()
            self.add_to_tst([spell, 'cast'])
            if from_gy:
                self.add_to_tst([spell, 'cast_from_gy'])
                
    def increment_step(self):
        event = [self.active_player, STEP_LIST[STEP_LIST.index(self.step)+1]]
        for rule in self.rule_step:
            event = rule.effect[0](self, rule, event)
        self.rule_cleanup('next_step')
        self.active_player = event[0]
        self.step = event[1]
        if self.step!='cleanup':
            print STEP_FANCY[STEP_LIST.index(self.step)]
        self.add_to_tst([None, 'begin_'+self.step])
        self.rule_cleanup('begin_'+self.step)
        self.prior_player=self.active_player

    def end_the_turn(self):
        self.step = 'cleanup'
        diff = len(self.active_player.hand)\
               -self.active_player.max_hand_size
        if diff>0:
            effects.choose_discard(self, self.active_player, diff)
        self.rule_cleanup('cleanup')
        for perm in self.battlefield:
            perm.damage = 0
            perm.damage_sources = []
            perm.attacked_this_turn = False
            perm.regen_shield = False
        self.prior_player = self.active_player
        self.update_battlefield()
        state = self.check_state()
        if state:
            self.active_player.player_land = False
            self.active_player.passed_for_turn = False
            self.active_player.last_turn_storm_count = \
                            self.active_player.storm_count
            self.active_player.storm_count = 0
            self.morbid = False
            self.active_player = self.active_player.next_player
            self.active_player.played_land = False
            self.active_player.passed_for_turn = False
            self.active_player.last_turn_storm_count = \
                            self.active_player.storm_count
            self.active_player.storm_count = 0
            for perm in self.battlefield:
                if perm.controller == self.active_player:
                    perm.sum_sick = False
            print 'Player', str(self.active_player.position) \
                              + '\'s turn'
            self.step = 'untap'
            print 'Untap step'
            effects.untap_step(self)
            self.add_to_tst([None, 'begin_untap'])
            self.rule_cleanup('begin_untap')
            self.increment_step()

    def priority(self):
        while True:
            player_input = self.get_input(self.prior_player)
            #wait for the next actionable input
            if 'concede' in player_input:
                self.prior_player.lost = True
                return None
            elif player_input=='':
                self.resolve_next()
                return None
            elif player_input=='pass':
                self.prior_player.passed_for_turn = True
                self.resolve_next()
                return None
            elif 'p' == player_input:
                self.play(self.prior_player)
                return None
            elif 'cheat' == player_input[:5]:
                card_name = player_input[6:]
                if card_name in self.card_dict:
                    card = effects.card_copy(self.card_dict[card_name],
                                             self.prior_player)
                    self.prior_player.hand.append(card)
                else:
                    print 'Invalid card name'
                    return None
                spell = Spell(self, self.prior_player, card)
                self.play_card(self.prior_player, spell,\
                    cheat=True)
                return None
            elif 'a' == player_input:
                self.activate_ability(self.prior_player)
                return None
            elif 'ma' == player_input:
                self.activate_ability(self.prior_player, mana=True)
                return None
            else:
                print 'Invalid command'
            
    def resolve_next(self):
        self.undo_list = []
        if not self.passed_prior:
            self.prior_player = self.prior_player.next_player
            self.passed_prior = True
        else:
            self.passed_prior = False
            if self.stack == []:
                self.player[0].mana_pool = [0,0,0,0,0,0]
                self.player[1].mana_pool = [0,0,0,0,0,0]
                if self.step == 'end_combat':
                    self.damage_creat = []
                    self.attacks = []
                    self.attackers = []
                    self.blocks = []
                    self.blockers = []

                if self.step == 'end' or self.step == 'cleanup':
                    self.end_the_turn()
                else:
                    self.increment_step()
                if self.step == 'draw':
                    effects.draw_cards(self, self.active_player, 1)
                elif self.step == 'declare_attackers':
                    effects.declare_attackers(self)
                elif self.step == 'declare_blockers':
                    effects.declare_blockers(self)
                elif self.step == 'combat_damage':
                    if not self.first_strike_phase:
                        combat_creatures = self.attackers+self.blockers
                        first_strike = False
                        for creat in combat_creatures:
                            if any([word in creat.cab.keyword for word in \
                                    ('First strike', 'Double strike')]):
                                first_strike = True
                        if first_strike:
                            for creat in combat_creatures:
                                if any([word in creat.cab.keyword for word in \
                                        ('First strike', 'Double strike')]):
                                    self.damage_creat.append(creat)
                            self.first_strike_phase = True
                            rule = Data()
                            rule.cleanup = effects.cl_first_strike
                            rule.effect = [effects.first_strike_step]
                            rule.location = self.rule_step
                            rule.location.append(rule)
                        else:
                            self.damage_creat = combat_creatures
                        effects.combat_damage(self)
                    else:
                        self.first_strike_phase = False
                        damage_creat = []
                        combat_creatures = self.attackers + self.blockers
                        for creat in combat_creatures:
                            if creat not in self.damage_creat or \
                                    'Double strike' in creat.cab.keyword:
                                damage_creat.append(creat)
                        self.damage_creat = damage_creat
                        effects.combat_damage(self)
            else:
                sporab = self.stack[-1]
                legal_target=False
                if sporab.target == []:
                    legal_target = True
                i=-1
                targets = sporab.target
                sporab.target = []
                for i in range(len(targets)):
                    if sporab.sporab_target[i](self, sporab, targets[i]):
                        legal_target = True
                        sporab.target.append(targets[i])
                if legal_target:
                    for effect in sporab.ef_list:
                        effect[0](self, sporab, *effect[1:])
                if legal_target:
                    print sporab.name, 'resolves.'
                else:
                    print sporab.name, 'is countered because it has'\
                     ' no legal targets'
                    if sporab.spell:
                        effects.inst_sorc_resolve(self, sporab)
                    else:
                        effects.abil_resolve(self, sporab)
                self.prior_player = self.active_player
