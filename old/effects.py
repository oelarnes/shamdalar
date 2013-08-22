import random
import classes
import copy
import output

COLOR_WORDS = ('White', 'Blue', 'Black', 'Red', 'Green')
LAND_WORDS = ('Plains', 'Island', 'Swamp', 'Mountain', 'Forest')
ORDINAL_WORDS = ('first', 'second', 'third', 'fourth', 'fifth')
COLOR_SYMB = ('{W}', '{U}', '{B}', '{R}', '{G}', '{1}')
NUMBER_WORDS = ('one', 'two', 'three', 'four', 'five')
STEP_LIST = ('untap','upkeep', 'draw','first_main',
                         'begCombat', 'declareAttackers','declareBlockers',
                         'combatDamage', 'endCombat','second_main', 'end',
                         'cleanup')
STEP_FANCY = ('Untap step', 'Upkeep step', 'Draw step',
                          'First main phase','Beginning of combat step',
                          'Declare attackers step', 'Declare blockers step',
                          'Combat damage step', 'End of combat step',
                          'Second main phase', 'End step', '')
STARTING_LIFE = 20
COUNTER_TYPES = ('+1/+1', '-1/-1', 'Loyalty', 'Charge', 'Slime', 'Study',
                 'Hatchling')
INF = 2**20
TYPES = ('Creature', 'Instant', 'Sorcery', 'Enchantment', 'Artifact', 'Land',
         'Planeswalker', 'Tribal')

                 
TRIGGER_PHRASES = ('etb', 'became_tapped', 'attacking', 'became_target',
                   'bf_to_gy', 'drew_card', 'dealt_damage', 'begin_step',
                   'cast', 'cast_from_gy', 'left_battlefield')

CREATURE_TYPES = ('Advisor', 'Ally', 'Angel', 'Anteater', 'Antelope', 'Ape',
                  'Archer', 'Archon', 'Artificer', 'Assassin',
                  'Assembly-Worker', 'Atog', 'Aurochs', 'Avatar', 'Badger',
                  'Barbarian', 'Basilisk', 'Bat', 'Bear', 'Beast', 'Beeble',
                  'Berserker', 'Bird', 'Blinkmoth', 'Boar', 'Bringer',
                  'Brushwagg', 'Camarid', 'Camel', 'Caribou',
                  'Carrier', 'Cat', 'Centaur', 'Cephalid', 'Chimera', 'Citizen',
                  'Cleric', 'Cockatrice', 'Construct', 'Coward', 'Crab',
                  'Crocodile', 'Cyclops', 'Dauthi', 'Demon', 'Deserter',
                  'Devil', 'Djinn', 'Dragon', 'Drake', 'Dreadnought', 'Drone',
                  'Druid', 'Dryad', 'Dwarf', 'Efreet', 'Elder', 'Eldrazi',
                  'Elemental', 'Elephant', 'Elf', 'Elk', 'Eye',
                  'Faerie', 'Ferret', 'Fish', 'Flagbearer', 'Fox', 'Frog',
                  'Fungus', 'Gargoyle', 'Germ', 'Giant', 'Gnome', 'Goat',
                  'Goblin', 'Golem', 'Gorgon', 'Graveborn', 'Gremlin',
                  'Griffin', 'Hag', 'Harpy', 'Hellion', 'Hippo', 'Hippogriff',
                  'Homarid', 'Homunculus', 'Horror', 'Horse', 'Hound', 'Human',
                  'Hydra', 'Hyena', 'Illusion', 'Imp', 'Incarnation', 'Insect',
                  'Jellyfish', 'Juggernaut', 'Kavu', 'Kirin', 'Kithkin',
                  'Knight', 'Kobold', 'Kor', 'Kraken', 'Lammasu', 'Leech',
                  'Leviathan', 'Lhurgoyf', 'Licid', 'Lizard',
                  'Manticore', 'Masticore', 'Mercenary', 'Merfolk', 'Metathran',
                  'Minion', 'Minotaur', 'Monger', 'Mongoose', 'Monk',
                  'Moonfolk', 'Mutant', 'Myr', 'Mystic', 'Nautilus', 'Nephilim',
                  'Nightmare', 'Nightstalker', 'Ninja', 'Noggle', 'Nomad',
                  'Octopus', 'Ogre', 'Ooze', 'Orb', 'Orc', 'Orgg', 'Ouphe',
                  'Ox', 'Oyster', 'Pegasus', 'Pentavite', 'Pest', 'Phelddagrif',
                  'Phoenix', 'Pincher', 'Pirate', 'Plant', 'Praetor', 'Prism',
                  'Rabbit', 'Rat', 'Rebel', 'Reflection', 'Rhino', 'Rigger',
                  'Rogue', 'Salamander', 'Samurai', 'Sand', 'Saproling',
                  'Satyr', 'Scarecrow', 'Scorpion', 'Scout', 'Serf', 'Serpent',
                  'Shade', 'Shaman', 'Shapeshifter', 'Sheep', 'Siren',
                  'Skeleton', 'Slith', 'Sliver', 'Slug', 'Snake',
                  'Soldier', 'Soltari', 'Spawn', 'Specter', 'Spellshaper',
                  'Sphinx', 'Spider', 'Spike', 'Spirit', 'Splinter', 'Sponge',
                  'Squid', 'Squirrel', 'Starfish', 'Surrakar', 'Survivor',
                  'Tetravite', 'Thalakos', 'Thopter', 'Thrull', 'Treefolk',
                  'Triskelavite', 'Troll', 'Turtle', 'Unicorn', 'Vampire',
                  'Vedalken', 'Viashino', 'Volver', 'Wall', 'Warrior', 'Weird',
                  'Whale', 'Wizard', 'Wolf', 'Wolverine', 'Wombat', 'Worm',
                  'Wraith', 'Wurm', 'Yeti', 'Zombie', 'Zubera')

##Layers:
##[0]:Copy, [1]:Control, [2]:Text, [3]: Type, [4]:Color, [5]:Abilities
##[6]:P/T CDA [7]: P/T Set [8]: P/T Adjust [9]: P/T Counters [10]: P/T Switch

##Functions used by Game methods:

def componentwise_add(list1, list2):
    new_list = list(list1)
    for i in range(len(new_list)):
        new_list[i] += list2[i]
    return new_list

def componentwise_subtract(list1, list2):
    new_list = list(list1)
    for i in range(len(new_list)):
        new_list[i] -= list2[i]
    return new_list

def mana_cost_subset(cost1, cost2):
    if all([cost1[i]<=cost2[i] for i in range(len(cost1))]):
        return True
    return False

def perm_from_base(game, perm):
    perm.cab = cab_copy(perm.base.cab, True)
    perm.name = perm.base.name
    perm.ref_name = perm.base.ref_name
    perm.sup_type = perm.base.sup_type
    perm.type_ = perm.base.type_
    perm.sub_type = perm.base.sub_type
    perm.power = perm.base.power
    perm.mana_cost = perm.base.mana_cost
    perm.color_indicator = list(perm.base.color_indicator)
    perm.toughness = perm.base.toughness
    perm.controller = perm.original_controller
    perm.color = list(perm.color_indicator)
    if perm.mana_cost != None:
        for i in range(5):
            if perm.mana_cost[i]>0:
                perm.color.append(COLOR_WORDS[i])
    perm.indestructible = False

    
def list_intersect(a,b):
    return [x for x in a if x in b]

def cab_copy(cab, ref=False):
    newcab = classes.CardAbilities()
    for zone in [[cab.act, newcab.act], [cab.act_mana, newcab.act_mana], \
                 [cab.act_grav, newcab.act_grav], \
                 [cab.act_hand, newcab.act_hand]]:
        for abts in zone[0]:
            newabts = classes.AbilToStack()
            newabts.ef_list = []
            if abts.mana_cost != None:
                newabts.mana_cost = list(abts.mana_cost)
            for cost in abts.other_cost:
                newabts.other_cost.append(cost)
            newabts.sporab_target = list(abts.sporab_target)
            for effect in abts.ef_list:
                newabts.ef_list.append(list(effect))
            for rule in abts.cost_inc:
                newabts.cost_inc.append(list(rule))
            for rule in abts.cost_red:
                newabts.cost_red.append(list(rule))
            newabts.cast_choice = list(abts.cast_choice)
            newabts.color_word = list(abts.color_word)
            newabts.ref_obj = []
            if ref:
                newabts.ref_obj = list(abts.ref_obj)
            newabts.type_word = list(abts.type_word)
            newabts.timing = list(abts.timing)
            newabts.rules_text = abts.rules_text
            zone[1].append(newabts)
    for i in range(len(cab.act_mana)):
        newcab.act_mana[i].would_produce = \
                        list(cab.act_mana[i].would_produce)
    for zone in [[cab.trig, newcab.trig], [cab.trig_grav, newcab.trig_grav],\
                [cab.other_static, newcab.other_static], \
                 [cab.grav_static, newcab.grav_static]]+\
                [[cab.layer_static[i], newcab.layer_static[i]]
                 for i in range(11)]:
        for stab in zone[0]:
            newstab = classes.StaticAbil()
            newstab.effect = list(stab.effect)
            newstab.ref_obj = []
            if ref:
                newstab.ref_obj = list(stab.ref_obj)
            newstab.rules_text = stab.rules_text
            newstab.color_word = list(stab.color_word)
            newstab.type_word = list(stab.type_word)
            newstab.name = stab.name
            zone[1].append(newstab)
    for rule in cab.as_enters:
        new_rule = classes.ReplacementEffect()
        new_rule.name = rule.name
        new_rule.ref_obj = []
        if ref:
            new_rule.ref_obj = list(rule.ref_obj)
        new_rule.test = rule.test
        new_rule.type_word = list(rule.type_word)
        new_rule.color_word = list(rule.color_word)
        new_rule.effect = list(rule.effect)
        newcab.as_enters.append(new_rule)
    newcab.keyword = list(cab.keyword)
    return newcab

def card_copy(card, player=None):
    newcard = classes.Card(card)
    newcard.timestamp = None
    newcard.base = card
    newcard.cast_choice = list(card.cast_choice)
    newcard.cost_inc = list(card.cost_inc)
    newcard.cost_red = list(card.cost_red)
    newcard.owner = None
    if player!=None:
        newcard.owner = player
    newcard.color_indicator = list(card.color_indicator)
    newcard.color = list(card.color)
    newcard.color_word = list(card.color_word)
    newcard.type_word = list(card.type_word)
    newcard.ef_list = []
    for item in card.ef_list:
        newcard.ef_list.append(list(item))
    newcard.other_cost = list(card.other_cost)
    newcard.sporab_target = list(card.sporab_target)
    newcard.power = card.power
    newcard.toughness = card.toughness
    newcard.loyalty = card.loyalty
    newcard.other_face = card.other_face
    newcard.cab = cab_copy(card.cab)
    return newcard

def card_from_base(card, player=None):
    card.cab = cab_copy(card.base.cab)

def choose_obj_from_list(game, player, set_, prompt=False, alt_input=None,
                         cont=True, just_looking=False):
    if prompt != False:
        output.output(game, player, prompt, prompt)
    number = 1
    first = False
    second = False
    players = False
    stack = False
    first_gy = False
    second_gy = False
    exile = False
    first_hand = False
    second_hand = False
    for item in set_:
        if cont:
            if item in game.battlefield:
                if item.controller == game.player[0]:
                    attached = False
                    if item.attached_to in game.battlefield:
                        if item.attached_to.controller == game.player[1]:
                            attached = True
                    if not first and not attached:
                        output.output(game, player, item.controller.name+':','')
                        first = True
                if item.controller == game.player[1]:
                    attached = False
                    if item.attached_to in game.battlefield:
                        if item.attached_to.controller == game.player[0]:
                            attached = True
                    if not second:
                        output.output(game, player, item.controller.name+':','')
                        second = True
            if item in game.player:
                if not players:
                    output.output(game, player, 'Players:')
                    players = True
            if item in game.player[0].hand:
                if not first_hand:
                    output.output(game, player, game.player[0].name+'\'s hand:','')
                    first_hand = True
            if item in game.player[1].hand:
                if not second_hand:
                    output.output(game, player, game.player[1].name+'\'s hand:','')
                    second_hand = True
            if item in game.player[0].graveyard:
                if not first_gy:
                    output.output(game, player, game.player[0].name+'\'s graveyard:','')
                    first_gy = True
            if item in game.player[1].graveyard:
                if not second_gy:
                    output.output(game, player, game.player[1].name +'\'s graveyard:','')
                    second_gy = True
            if item in game.exile:
                if not exile:
                    output.output(game, player, 'Exile', '')
                    exile = True
            if item in game.stack:
                if not stack:
                    output.output(game, player, 'On the stack', '')
                    stack = True
        if item in game.battlefield:
            if item.attached_to not in set_:
                out = ''
                if not just_looking: out +=str(number)+'. '
                out += game.print_perm(item)
                output.output(game, player, out,'')
                if item.attached_to != None:
                    output.output(game, player, '  on: '+item.attached_to.name,'')
            else:
                number-=1
            for item in item.attached:
                n=''
                if item in set_:
                    number+=1
                    if not just_looking:
                        n = str(number)+'. '
                output.output(game, player, '    '+n+item.name, '')
        else:
            out = ''
            if not just_looking: out+= str(number)+'. '
            if type(item) == type('No target'):
                output.output(game, player, out+item, '')
            else:
                output.output(game, player, out+item.name, '')
        number+=1
    if not just_looking:
        input_ = game.int_input(player, '', len(set_), alt_input = alt_input)
        if alt_input != None and type(input_)==type(''):
            if input_ in alt_input:
                return input_
        return set_[input_-1]
    return None

def get_target(game, player, sporab):
    for i in range(len(sporab.sporab_target)):
        zones = game.battlefield \
                + game.player[0].graveyard \
                + game.player[1].graveyard \
                + game.exile \
                + game.stack \
                + game.player \
                + ['No target']
        elig_target = [item for item in zones if \
                           sporab.sporab_target[i](game, sporab, item)]
        if len(elig_target) == 0:
            output.output(game, player, 'No legal targets')
            return False
        if i < len(ORDINAL_WORDS):
            prompt= 'Choose ' +ORDINAL_WORDS[i]+\
                  ' target'
        else:
            prompt = 'Choose next target'
        target_chosen = False
        if len(elig_target) == 1:
            if elig_target[0]!='No target':
                target=elig_target[0]
            else:
                break
        else:
            target = choose_obj_from_list(game, player, elig_target,
                                          prompt, cont = True)
            if target == 'No target':
                break
        sporab.target.append(target)
    if len(sporab.target)>0:
        game.update_battlefield()
        for item in sporab.target:
            game.add_to_tst([item, 'became_target'])

def determine_total_cost(game, sporab):
    for rule in game.rule_cost_inc:
        rule.effect[0](game, rule, sporab, *rule.effect[1:])
    for item in sporab.cost_inc:
        item[0](game, sporab, *item[1:])
    for rule in game.rule_cost_red:
        rule.effect[0](game, rule, sporab, *rule.effect[1:])
    for item in sporab.cost_red:
        item[0](game, sporab, *item[1:])
            
def pay_mana_cost(game, player, mana_cost, undo = True):
    left_to_pay = list(mana_cost)
    for i in range(5):
        to_pay = min([left_to_pay[i], player.mana_pool[i]])
        left_to_pay[i]-= to_pay
        player.mana_pool[i]-=to_pay
    avail = sum(player.mana_pool)
    if avail <= left_to_pay[5]:
        paid = 0
        for i in range(6):
            paid += player.mana_pool[i]
            player.mana_pool[i]=0
        left_to_pay[5]-=paid
    elif left_to_pay[5]>0 and left_to_pay[5]<avail:
        output.output(game, player,
                      "Specify amounts to spend for total "+str(left_to_pay[5]),
                      '')
        output.output(game, player, game.print_cost(player.mana_pool), '')
        valid_amount = False
        while not valid_amount:
            amount = []
            for i in range(5):
                if sum(amount)<left_to_pay[5] and player.mana_pool[i]>0:
                    amount.append(game.int_input(player,
                                COLOR_WORDS[i]+':', player.mana_pool[i], 0))
                else: amount.append(0)
            if sum(amount)<left_to_pay[5] and player.mana_pool[5]>0:
                    amount.append(game.int_input(player,
                                    'Colorless:', player.mana_pool[5], 0))
            else: amount.append(0)
            if sum(amount) == left_to_pay[5] \
                and not min([amount[i]>player.mana_pool[i] \
                    for i in range(5)]):
                valid_amount = True
            else:
                output.output(game, player, "Invalid amounts. Try again",'')
        for i in range(5):
            player.mana_pool[i]-=amount[i]
            left_to_pay[5] -= amount[i]
    if left_to_pay == [0,0,0,0,0,0]:
        return True
    
    output.output(game, player,
        'Activate mana abilities to pay cost '+ game.print_cost(left_to_pay)\
          +' or cancel', '')
    mana_abil_found = False
    if game.activate_ability(player, mana=True):
        if pay_mana_cost(game, player, left_to_pay):
            return True
        else:
            return False
    else:
        return False

def untap_step(game):
    dont_untap_list = []
    for rule in game.rule_untap:
        dont_untap_list.extend(rule.effect[0](game, rule, *rule.effect[1:]))
    for perm in game.battlefield:
        if perm not in dont_untap_list and \
                   perm.controller == game.active_player:
            perm.tapped = False

def declare_attackers(game):
    finished = False
    player = game.active_player
    attackables = [game.active_player.next_player]
    cant_attack_list = game.populate_cant_attack()
    for perm in game.battlefield:
        if 'Planeswalker' in perm.type_ and perm.controller == \
               game.active_player.next_player:
            attackables.insert(0, perm)
    elig_creat = [item for item in game.battlefield if \
                                not item.tapped and not \
                                (item.sum_sick and 'Haste' not in \
                                 item.cab.keyword) and \
                                  not item in cant_attack_list
                                and item.controller == game.active_player
                                and 'Creature' in item.type_ and \
                                  'Defender' not in item.cab.keyword]
    while not finished:
        attacks_declared = False
 
        attacks = []
        while not attacks_declared and len(elig_creat)>0:
            creature = choose_obj_from_list(game, game.active_player,
                                               elig_creat,
                                               'Choose a creature to attack'+\
                                               ' with or type done:',
                                               alt_input = ['done'])
            if creature == 'done':
                attacks_declared = True
            else:
                elig_creat.remove(creature)
                attacks.append([creature,attackables[0],None])
                if len(attackables)>1:
                    to_attack = choose_obj_from_list(game,
                                game.active_player, attackables,
                                'Choose a player or planeswalker to attack:')
                    attacks[-1][1] = to_attack
        elig_creat = [item for item in game.battlefield if \
                                not item.tapped and not \
                                (item.sum_sick and 'Haste' not in \
                                 item.cab.keyword) and \
                                  not item in cant_attack_list
                                and item.controller == game.active_player
                                and 'Creature' in item.type_ and \
                              'Defender' not in item.cab.keyword]
        switch = False
        if len(game.rule_attack)>0:
            set_to_check = []
            set_to_check.append([[creat, game.active_player.next_player] \
                                 for creat in elig_creat])
            gideon = [item.name == 'Gideon Jura' for item in attackables]
            if any(gideon):
                set_to_check.append([[creat, attackables[gideon.index(True)]] \
                                     for creat in elig_creat])
            max_ = -INF
            max_set = None
            for set_ in set_to_check:
                value = 0
                for rule in game.rule_attack:
                    value += rule.effect[0](game, rule, set_, *rule.effect[1:])
                if value > max_:
                    max_set = set_
                    max_ = value
            value = 0
            for rule in game.rule_attack:
                value += rule.effect[0](game, rule, attacks, *rule.effect[1:])
            if value < max_:
                switch = True
                output.output(game, game.active_player, 'Choice of attacks invalid', '')
        if not switch:
            for item in attacks:
                if 'Vigilance' not in item[0].cab.keyword:
                    become_tapped(game, item[0])
            if len(attacks)>0:
                output.output(game, game.active_player, 'Attacks declared')
            else:
                output.output(game, game.active_player, 'No attacking creatures')
            for item in attacks:
                output.output(game, player,
                              item[0].name+' attacking '+item[1].name)
            finished = True
            game.attacks = attacks
            game.attackers = [item[0] for item in game.attacks]
            for item in game.attacks:
                item[0].attacked_this_turn = True
            game.update_battlefield()
            for creat in game.attackers:
                game.add_to_tst([creat, 'attacking'])
            
def declare_blockers(game):
    player = game.active_player.next_player
    finished = False
    elig_creat = [item for item in game.battlefield if \
                        not item.tapped \
                        and item.controller == game.active_player.next_player
                            and 'Creature' in item.type_
                      and any([can_block(game, item, creat) \
                               for creat in game.attackers])]
    while not finished:
        blockers_declared = False
        blocks = []
        while not blockers_declared and len(elig_creat)>0:
            creature = choose_obj_from_list(game, player,
                                               elig_creat,
                                               'Choose a creature to block'+\
                                               ' with or type done:',
                                               alt_input = ['done'])
            if creature == 'done':
                blockers_declared = True
            else:
                elig_creat.remove(creature)
                
                to_block_list = [item for item in game.attackers if can_block(
                                        game, creature, item)]
                blocks.append([creature,to_block_list[0]])
                if len(to_block_list)>1:
                    blocks[-1][1] = choose_obj_from_list(game,
                                player, to_block_list,
                                'Choose a creature to block')
        elig_creat = [item for item in game.battlefield if \
                        not item.tapped \
                        and item.controller == player
                            and 'Creature' in item.type_
                      and any([can_block(game, item, creat) \
                               for creat in game.attackers])]
        switch = False
        if len(game.rule_block)>0:
            set_to_check = []
            set_to_check.append([])
            for perm1 in game.attackers:
                set_ = []
                for perm2 in elig_creat:
                      if can_block(game, perm2, perm1):
                          set_.append([perm2, perm1])
                if len(set_)>0:
                    set_to_check.append(set_)
            max_ = -INF
            max_set = None
            for set_ in set_to_check:
                value = 0
                for rule in game.rule_block:
                    value += rule.effect[0](game, rule, set_, *rule.effect[1:])
                if value > max_:
                    max_set = set_
                    max_ = value
            value = 0
            for rule in game.rule_block:
                value += rule.effect[0](game, rule, blocks, *rule.effect[1:])
            if value < max_:
                output.output(game, player, 'Choice of blockers invalid','')
                switch = True
        if not switch:
            print 'Blockers declared'
            for item in blocks:
                game.add_to_tst([item, 'block'])
                print item[0].name, 'blocking', item[1].name
            finished = True
            game.blocks = blocks
            game.blockers = [item[0] for item in game.blocks]
    for attack in game.attacks:
        blocker_list = [item[0] for item in game.blocks if item[1]==attack[0]]
        if len(blocker_list)>=1:
            attack[2] = []
        while len(blocker_list)>1:
            attack[2].append(choose_obj_from_list(game, game.active_player,
                blocker_list,
                'Choose next blocker in damage assignment order for '+attack[0].name+':'))
            blocker_list.remove(attack[2][-1])
        if len(blocker_list)==1:
            attack[2].append(blocker_list[0])
        print 'Damage order for '+attack[0].name+' assigned'
        
def combat_damage(game):
    damage_list = []
    for creat in game.damage_creat:
        pow_damage = max([0, creat.power])
        if creat in game.attackers:
            attack = game.attacks[game.attackers.index(creat)]
            if attack[2]==None:
                if attack[1].name != 'Nothing':
                    creat_damage_list = [attack[1]]
                else:
                    creat_damage_list = []
            else:
                if 'Trample' in creat.cab.keyword:
                    if attack[1].name != 'Nothing':
                        creat_damage_list = list(attack[2])
                        creat_damage_list.append(attack[1])
                else:
                    creat_damage_list = list(attack[2])
            if len(creat_damage_list) == 0:
                print creat.name, 'deals no damage'
            elif len(creat_damage_list) == 1:
                print creat.name, 'assigns', pow_damage, 'damage to', \
                      creat_damage_list[0].name
                damage_list.append([creat, creat_damage_list[0], pow_damage])
            elif len(creat_damage_list) > 1:
                damage_left = pow_damage
                for blocker in creat_damage_list:
                    req_dam = lethal_damage(game, creat, blocker)
                    if blocker == creat_damage_list[-1] or req_dam >= damage_left:
                        if damage_left >0:
                            print creat.name, 'assigns', damage_left, 'damage to', \
                                  blocker.name
                            damage_list.append([creat, blocker, damage_left])
                            damage_left = 0
                    else:
                        print 'Assign at least', req_dam, 'damage to', blocker.name
                        damage_amt = game.int_input(creat.controller, u_range=damage_left,
                                                l_range = req_dam)
                        print creat.name, 'assigns', damage_amt, 'damage to', \
                              blocker.name
                        damage_list.append([creat, blocker, damage_amt])
                        damage_left -= damage_amt
    for creat in game.damage_creat:
        if creat in game.blockers:
            pow_damage = max([0, creat.power])
            block = game.blocks[game.blockers.index(creat)]
            creat_damage_list = block[1:]
            if len(creat_damage_list) == 0:
                print creat.name, 'deals no damage'
            elif len(creat_damage_list) == 1:
                print creat.name, 'assigns', pow_damage, 'damage to', \
                      creat_damage_list[0].name
                damage_list.append([creat, creat_damage_list[0], pow_damage])
            elif len(creat_damage_list) > 1:
                damage_left = pow_damage
                for attacker in creat_damage_list:
                    req_dam = lethal_damage(game, creat, attacker)
                    if attacker == creat_damage_list[-1] or req_dam >= damage_left:
                        if damage_left >0:
                            print creat.name, 'assigns', damage_left, 'damage to', \
                                  attacker.name
                            damage_list.append([creat, attacker, damage_left])
                    else:
                        print 'Assign at least', req_dam, 'damage to', attacker.name
                        damage_amt = game.int_input(creat.controller, u_range=damage_left,
                                                l_range = req_dam)
                        print creat.name, 'assigns', damage_amt, 'damage to', \
                              attacker.name
                        damage_list.append([creat, attacker, damage_amt])
                        damage_left -= damage_amt
    trig_list = []
    for item in damage_list:
        dealt = damage(game, item[0], item[1], item[2], True)
        if dealt!=None:
            trig_list.append([[item[0], item[1], dealt, True], 'dealt_damage'])
    game.update_battlefield()
    for item in trig_list:
        game.add_to_tst(item)

##Boolean functions called by other methods and functions:

def is_creature(game, obj):
    if obj in game.battlefield:
        if 'Creature' in obj.type_:
            return True
    return False

def card_timing(game, player, card):
    if any([word in card.type_ for word in ('Creature', 'Sorcery', 'Land',
                                            'Enchantment', 'Artifact',
                                            'Planeswalker')])\
                        and 'Flash' not in card.cab.keyword:
        if game.active_player == player and game.stack == [] and \
                           game.step in ('first_main', 'second_main'):
            return True
        return False
    return True

def can_block(game, blocker, attacker):
    if 'Intimidate' in attacker.cab.keyword:
        if 'Artifact' not in blocker.type_:
            if list_intersect(blocker.color,attacker.color) == []:
                return False
    if 'Flying' in attacker.cab.keyword:
        if not any([word in blocker.cab.keyword for word in ('Flying', 'Reach')]):
            return False
    for word in blocker.color:
        if 'Protection from '+word.lower() in attacker.cab.keyword:
            return False
    for word in blocker.sub_type.split():
        if 'Protection from '+word+'s' in attacker.cab.keyword or\
           word == 'Werewolf' and 'Protection from Werewolves' in attacker.cab.keyword:
            return False
    prot_list = [protection for protection in attacker.cab.keyword if \
                 'Protection from non-' in protection]
    if len(prot_list)>0:
        for item in prot_list:
            if all(['Protection from non-'+word+' creatures' != item for word\
                in blocker.sub_type.split()]):
                    return False
    if 'Protection from creatures' in attacker.cab.keyword:
        return False
    if 'Protection from artifacts' in attacker.cab.keyword and 'Artifact' in \
       blocker.type_:
        return False
    for word in LAND_WORDS:
        if word+'walk' in attacker.cab.keyword:
            if any([word in perm.sub_type for perm in game.battlefield if \
                        perm.controller == blocker.controller]):
                return False
    for rule in game.rule_cant_block:
        if not rule.effect[0](game, rule, blocker, attacker, *rule.effect[1:]):
            return False
    return True

#Effects not used by cards

def become_tapped(game, perm):
    perm.tapped = True
    print perm.name+' is tapped'

def change_life(game, player, amount):
    player.life = player.life + amount
    print player.name, 'has', player.life, 'life.'

def mill(game, player, amount):
    cards = []
    for i in range(min([len(player.lib), amount])):
        card = player.lib.pop()
        cards.append(card)
        go_to_gy(game, card)
    game.update_battlefield()
    for card in cards:
        game.add_to_tst([card, 'lib_to_gy'])
    return cards

def counterspell(game, source, target):
    if can_counter(game, source, target):
        print target.name, 'is countered by', source.name
        
        inst_sorc_resolve(game, target)
    else:
        print source.name, 'has no effect'

def can_counter(game, source, target):
    if target in game.stack:
        check = True
        for rule in game.rule_counter:
            check = min([check, rule.effect[0](game, rule, source, target,
                                               *rule.effect[1:])])
    return check

def damage(game, source, target, amount, combat=False):
    if target in game.battlefield:
        if any(['Protection from '+word.lower() in target.cab.keyword \
                for word in source.color]) \
                or any(['Protection from '+word+'s' in \
                           target.cab.keyword for word in \
                        source.sub_type.split()]) or ('Protection from Werewolves'\
                        in target.cab.keyword and 'Werewolf' in source.sub_type):
            print amount, 'damage to', target.name, 'prevented'
            return None
        prot_list = [protection for protection in target.cab.keyword if \
                     'Protection from non-' in protection]
        if len(prot_list)>0:
            for item in prot_list:
                if all(['Protection from non-'+word+' creatures' != item for word\
                    in source.sub_type.split()]):
                        print amount, 'damage to', target.name, 'prevented'
                        return None
    rule_list = list(game.rule_damage)
    event = []
    newevent = [source, target, amount]
    while newevent!=event:
        event = newevent
        for rule in rule_list:
            result = rule.effect[0](game, rule, newevent[0],
                                    newevent[1], newevent[2],
                                      combat, *rule.effect[1:])
            if result != False:
                rule_list.remove(rule)
                newevent = result
    source = newevent[0]
    target = newevent[1]
    new_amount = newevent[2]
    if amount - new_amount >0:
        print amount-new_amount, 'damage to', target.name, 'prevented'
    if new_amount >0:
        print source.name, 'deals', new_amount, 'damage to',\
              target.name
        target.damage_sources.append(source)
        deal_damage(game, source, target, new_amount, combat)
        return amount

def deal_damage(game, source, target, amount, combat):
    #deal only positive amounts
    if 'Lifelink' in source.cab.keyword:
        change_life(game, source.controller, amount)
    if target in game.player:
        if 'Infect' in source.cab.keyword:
            target.poison += amount
            target.dealt_damage_this_turn = True
            return None
        target.dealt_damage_this_turn = True
        change_life(game, target, 0-amount)
    else:
        if 'Creature' in target.type_:
            if 'Wither' in source.cab.keyword or 'Infect' in source.cab.keyword:
                target.counter['-1/-1']+= amount
            else:
                target.damage += amount
            target.damage_to_check.append([source, amount])
        if 'Planeswalker' in target.type_:
            target.counter['Loyalty']-=min([target.counter['Loyalty'],amount])
        

def destroy(game, perm):
    #check that the object is on the battlefield before call
    #use only for a single instance of destroy in an action
    if not perm.indestructible and not perm.regen_shield:
        die(game, perm)
        game.update_battlefield()
        game.add_to_tst([perm, 'bf_to_gy'])
    if perm.regen_shield:
        regenerate(game, perm)
        game.update_battlefield()

def destroy_list(game, destroy_list):
    trig_list = []
    for perm in destroy_list:
        if not perm.indestructible and not perm.regen_shield:
            die(game, perm)
            trig_list.append(perm)
        elif perm.regen_shield:
            regenerate(game, perm)
    game.update_battlefield()
    for perm in trig_list:
        game.add_to_tst([perm, 'bf_to_gy'])
    return trig_list

def regenerate(game, perm):
    perm.tapped = True
    leave_combat(game, perm)
    perm.regen_shield = False
    perm.damage = 0

def look_top_card(game, player):
    if len(player.lib)==0:
        print 'Your library is empty'
    else:
        print 'Your top card is '+player.lib[-1].name

def reveal_card(game, player, card):
    print player.name + ' reveals ' + card.name
    

def choose_discard(game, player, number):
    card = None
    for i in range(min(len(player.hand), number)):
        card = choose_obj_from_list(game, player, player.hand,
                                    'Choose a card to discard:')
        discard(game, card)
    game.update_battlefield()
    return card

def choose_sacrifice_creature(game, player):
    creat_list = [perm for perm in game.battlefield if 'Creature' in \
                  perm.type_ and perm.controller == player]
    creat = choose_obj_from_list(game, player, creat_list,
                                 'Choose a creature to sacrifice')
    die(game, creat)
    game.update_battlefield()
    game.add_to_tst([creat, 'bf_to_gy'])
    return creat

def random_discard(game, player, number):
    choice = random.sample(player.hand, min([number, len(player.hand)]))
    for item in choice:
        discard(game, item)
                           
def discard(game, card):
    card.owner.hand.remove(card)
    go_to_gy(game, card)
    print card.owner.name, 'discarded', card.name

def return_to_hand(game, perm):
    leave_battlefield(game, perm)
    go_to_hand(game, perm.card)
        
def leave_combat(game, creature):
    if 'Planeswalker' in creature.type_:
        for item in game.attacks:
            if item[-1] == creature:
                item.remove(creature)
                item.append(classes.Nothing())
    if creature in game.attackers:
        game.attacks.remove(
            game.attacks[game.attackers.index(creature)])
        game.attackers.remove(creature)
        blocked = [item[1] for item in game.blocks]
        while creature in blocked:
            game.blocks.pop(blocked.index(creature))
            game.blockers.pop(blocked.index(creature))
            blocked.remove(creature)
    if creature in game.blockers:
        game.blocks.pop(game.blockers.index(creature))
        game.blockers.remove(creature)
        for item in game.attacks:
            if item[2]!=None:
                if creature in item[2]:
                    item[2].remove(creature)

def add_plus_one_counter(game, creat, amount):
    creat.counter['+1/+1']+=amount
    if amount==1:
        print 'A +1/+1 counter was added to '+creat.name
    else:
        print str(amount)+' +1/+1 counters were added to '+creat.name

def add_counter(game, perm, counter, amount):
    perm.counter[counter]+=amount
    if amount == 1:
        print 'A '+counter+' counter was added to '+perm.name
    else:
        print str(amount)+' '+counter+' was added to '+perm.name

def enters_with_counter(game, repef, creat, counter_type, amount):
    creat.counter[counter_type]+=amount
    if amount==1:
        print creat.name+' enters with a '+counter_type + ' counter'
    else:
        print creat.name+' enters with '+str(amount)+' ' + counter_type\
              + ' counters'
    
def leave_battlefield(game, perm):
    game.battlefield.remove(perm)
    game.ghost_battlefield.append(perm)
    if 'Creature' in perm.type_:
        leave_combat(game, perm)
    if perm.attached_to != None:
        perm.attached_to.attached.remove(perm)
        perm.attached_to = None
    for item in perm.attached:
        item.attached_to = None
    perm.attached = []
    
                
def die(game, perm):
    leave_battlefield(game, perm)
    if 'Creature' in perm.type_:
        print perm.name, 'died'
        game.morbid = True
    go_to_gy(game, perm.card)

def coin_flip(game, player):
    choice = choose_obj_from_list(game, player, ['Heads', 'Tails'], 'Choose heads or'\
                                  +' tails')
    output.output(game, player, player.name+' chose '+choice)
    flip = random.choice(['Heads', 'Tails'])
    output.output(game, player, 'The flip came up '+flip)
    if flip==choice:
        output.output(game, player, player.name+' won the flip')
        return True
    else:
        output.output(game, player, player.name+' lost the flip')
        return False
        
def get_card_power(game, card):
    perm = classes.Permanent(game, card.owner, card)
    perm_from_base(game, perm)
    for stab in perm.cab.layer_static[6]:
        stab.effect[0](game, perm, stab, *stab.effect[1:])
    return perm.power

def draw_cards(game, player, number):
        for i in range(number):
            if player.lib==[]:
                loser = player
                for rule in game.rule_laboratory_maniac:
                    if rule.effect[0](game, rule, player):
                        loser = player.next_player
                loser.lost = True
                return None
            else:
                card = player.lib.pop()
                output.output(game, player, 'You drew '+ card.name,
                              player.name+ ' drew a card')
                player.hand.append(card)

def gy_to_hand(game, card):
    card.owner.graveyard.remove(card)
    card1 = card_copy(card.base, card.owner)
    card.owner.hand.append(card1)
    output.output(game, card1.owner,
            card1.name+ ' was returned to '+card.owner.name+\
              '\'s hand')

def go_to_hand(game, card):
    if card.real:
        card.owner.hand.append(card)
        output.output(game, card.owner, card.name+' was added to '+card.owner.name\
                      +'\'s hand', 'A card went to '+card.owner.name+'\'s hand')

def enter_battlefield(game, perm_list):
    for perm in perm_list:
        perm_from_base(game, perm)
        main_list = list(game.rule_as_enters)+list(perm.base.cab.as_enters)
        to_apply_list = []
        applied_list = []
        finished = False
        while not finished:
            for item in main_list:
                if item.test(game, item, perm):
                    to_apply_list.append(item)
            if len(to_apply_list)==0:
                finished = True
            else:
                if len(to_apply_list)==1:
                    to_apply_list[0].effect[0](game, to_apply_list[0], perm,
                                               *to_apply_list[0].effect[1:])
                    applied_list.append(to_apply_list[0])
                if len(to_apply_list)>1:
                    item = choose_obj_from_list(game, perm.controller,
                                                to_apply_list, prompt = \
                                    'Choose a replacement effect to apply')
                    item.effect[0](game, item, perm, *item.effect[1:])
                applied_list.append(item)
                perm_from_base(game, perm)
                main_list = list(game.rule_as_enters)+list(perm.base.cab.as_enters)
                for item in applied_list:
                    if item in main_list:
                        main_list.remove(item)
                to_apply_list = []
        perm.name = perm.base.name
    for perm in perm_list:
        if len(game.stack)!=0:
            if game.stack[-1].spell:
                if game.stack[-1].card == perm.card:
                    game.stack.pop()
        if perm.card in perm.card.owner.graveyard:
            perm.card.owner.graveyard.remove(perm.card)
            perm.card = card_copy(perm.card.base, perm.card.owner)
        elif perm.card in game.exile:
            game.exile.remove(perm.card)
            perm.card = card_copy(perm.card.base, perm.card.owner)
        elif perm.card in perm.card.owner.lib:
            perm.card.owner.lib.remove(perm.card)
            perm.card = card_copy(perm.card.base, perm.card.owner)
        elif perm.card in perm.card.owner.hand:
            perm.card.owner.hand.remove(perm.card)
            perm.card = card_copy(perm.card.base, perm.card.owner)
        game.insert_perm(perm)
        print perm.name, 'entered the battlefield under', \
              perm.controller.name+'\'s control'
    game.update_battlefield()
    for perm in perm_list:
        game.add_to_tst([perm, 'etb'])

def exile(game, perm):
    leave_battlefield(game, perm)
    if perm.card.real:
        game.exile.append(perm.card)
    print perm.name, 'was exiled'

def lethal_damage(game, creat1, creat2):
    #measures the amount of damage creat1 must deal to creat2 to
    #be considered lethal
    if creat2 not in game.player:
        if 'Deathtouch' in creat1.cab.keyword:
            return 1
        else:
            return creat2.toughness - creat2.damage
    else:
        return 0

def go_to_gy(game, card):
    if card.real:
        print card.name + ' is in '+card.owner.name+'\'s graveyard'
        card.timestamp = game.timestamp
        card.owner.graveyard.append(card)

def exile_card(game, spell):
    if spell.card.real:
        game.exile.append(spell.card)
    game.update_battlefield()

def return_card_to_hand(game, card):
    if card.real:
        card.owner.hand.append(card)
        game.update_battlefield()

def return_card_to_gy(game, card):
    if card.real:
        card.owner.graveyard.append(card)
        game.update_battlefield()

def make_tokens(game, player, number, color, sub_type, power, toughness, \
                cab = classes.CardAbilities()):
    for rule in game.rule_parallel_lives:
        number = rule.effect[0](game, rule, player, number)
    tokens = []
    for j in range(number):
        tokens.append(make_token(game, player, color, sub_type, power,
                                 toughness, cab))
    enter_battlefield(game, tokens)
    return tokens

def make_token(game, player, color, sub_type, power, toughness,
               cab = classes.CardAbilities()):
    card = classes.FakeCard()
    card.owner = player
    card.color_indicator = list(color)
    perm = classes.Permanent(game, player, card)
    perm.base.name = sub_type
    perm.base.type_ = 'Creature'
    perm.base.sub_type = sub_type
    perm.base.power = power
    perm.base.cab = cab_copy(cab, True)
    perm.base.power = power
    perm.base.toughness = toughness
    return perm

def mulligan(game, player):
    new_size = len(player.hand)-1
    player.lib = player.lib + list(player.hand)
    player.hand = []
    random.shuffle(player.lib)
    draw_cards(game, player, new_size)

def set_life(game, player, total):
    if player.life == total:
        return None
    change_life(game, player, total-player.life)

def choose_color(game, player):
    while True:
        print 'Choose a color:'
        input_ = game.get_input(player)
        if input_ in COLOR_WORDS:
            return input_

def reveal(game, card):
    output.output(game, card.owner, card.owner.name + ' reveals '+card.name)

def search_lib_for_subset(game, player, set_):
    while True:
        choice = choose_obj_from_list(game, player, set_, \
                                 alt_input = ['none', 'lib'],
                                 prompt = 'Choose a land, type none, or'+\
                                 ' type lib to see your library:')
        if choice == 'none':
            return None
        elif choice == 'lib':
            for item in player.lib:
                print item.name
        else:
            return choice
    
#Choices made while casting

def choose_x(game, sporab):
    output.output(game, sporab.controller, 'choose a value for X:', '')
    value = game.int_input(sporab.controller, l_range = 0)
    sporab.mana_cost[5]+=value
    sporab.ef_list[0][1] = value

def choose_mode_one_of_two(game, sporab):
    index1 = sporab.rules_text.index(' - ')+3
    index2 = sporab.rules_text.index('; ')
    output.output(game, sporab.controller, 'Choose a mode:', '')
    output.output(game, sporab.controller,
                  '1. '+sporab.rules_text[index1:index2], '')
    output.output(game, sporab.controller,
                  '2. '+sporab.rules_text.splitlines()[0][index2+2:], '')
    index = game.int_input(sporab.controller, u_range = 2)
    sporab.ef_list.pop(2-index)
    

#mana abilities

def tap_for_mana(game, player, abts):
    add_mana(game, player, abts)
    game.add_to_tst([abts.obj, 'tapped_for_mana'])
    
def add_mana(game, player, abts):
    player.mana_pool = componentwise_add(player.mana_pool, abts.would_produce)
    output.output(game, player, COLOR_SYMB[abts.would_produce.index(1)] + ' added to '+player.name+\
          '\'s mana pool')
    game.update_battlefield()

#undo effects

def untap(game, perm):
    update = False
    if perm.tapped:
        perm.tapped = False
        output.output(game, perm.controller, perm.name + ' is untapped')
        update = True
    if update:
        game.update_battlefield()
    
def undo_sacrifice(game, perm):
    game.insert_perm(perm)
    done = False
    number = 0
    while not done and number<len(perm.card.owner.graveyard):
        if perm.card.owner.graveyard[number].card == perm.card:
            perm.card.owner.graveyard.remove(perm.card)
            done = True
            number+=1

def undo_remove_rule(game, rule):
    rule.location.remove(rule)

#Sporab effects

def ref_obj0_sacrifice(game, abil):
    perm = abil.ref_obj[0]
    if perm in game.battlefield:
        exile(game, perm)
        game.update_battlefield()
        game.add_to_tst([perm, 'left_battlefield'])

def targeted_counterspell(game, sporab):
    counterspell(game, sporab.obj, sporab.target[0])
    game.update_battlefield()

def abil_obj_regenerate(game, abil):
    abil.obj.regen_shield = True
    game.update_battlefield()

def targeted_battlefield_to_top_of_library(game, sporab):
    leave_battlefield(game, sporab.target[0])
    card = sporab.target[0].card
    if card.real:
        card.owner.lib.append(card)
        output.output(game, sporab.controller,
                      card.name+' was put on top of '+card.owner.name+\
                      '\'s library')
    game.update_battlefield()

def abil_obj_plus_one_counter(game, sporab, amount):
    if sporab.obj in game.battlefield:
        add_plus_one_counter(game, sporab.obj, amount)
        game.update_battlefield()

def abil_obj_counter(game, sporab, counter, amount):
    if sporab.obj in game.battlefield:
        add_counter(game, sporab.obj, counter, amount)
        game.update_battlefield()

def abil_obj_untap(game, abil):
    untap(game, abil.obj)

def abil_obj_plus(game, sporab, power, toughness):
    rule = classes.SporabRule(sporab, game.layer[8])
    rule.effect = [la_8_plus, power, toughness]
    rule.ref_obj.append(sporab.obj)
    rule.cleanup = cl_until_eot
    game.update_battlefield()

def abil_obj_keyword(game, sporab, keyword):
    rule = classes.SporabRule(sporab, game.layer[5])
    rule.effect = [la_5_self_keyword, keyword]
    rule.cleanup = cl_until_eot
    game.update_battlefield()

def targeted_destroy(game, sporab):
    destroy(game, sporab.target[0])

def abil_obj_return_to_hand(game, sporab):
    return_to_hand(game, sporab.obj)
    game.update_battlefield()

def targeted_creature_plus(game, sporab, power_ch, tough_ch):
    new_rule = classes.SporabRule(sporab, game.layer[8])
    new_rule.effect = [la_8_plus, power_ch, tough_ch]
    new_rule.cleanup = cl_until_eot
    game.update_battlefield()
    
def targeted_discard(game, sporab, number):
    choose_discard(game,sporab.target[0],number)

def self_creature_plus(game, abil, power_ch, tough_ch):
    rule = classes.SporabRule(abil, game.layer[8])
    rule.ref_obj.append(abil.obj)
    rule.effect = [la_8_plus, power_ch, tough_ch]
    rule.cleanup = cl_until_eot
    game.update_battlefield()

def return_target_to_hand(game, sporab):
    return_to_hand(game, sporab.target[0])
    game.update_battlefield()
    game.add_to_tst([sporab.target[0], 'left_battlefield'])

def targeted_token_copy(game, sporab):
    card = classes.FakeCard()
    card.owner = sporab.controller
    perm = classes.Permanent(game, sporab.controller, sporab.target[0].base)
    perm.card = card
    enter_battlefield(game, [perm])
    
def draw_cont_cards(game, sporab, number):
    draw_cards(game, sporab.controller, number)
    game.update_battlefield()
    for i in range(number):
        game.add_to_tst([sporab.controller, 'drew_card'])

def inst_sorc_resolve(game, spell):
    for rule in game.rule_leave_stack:
        rule.effect[0](game, rule, spell)
    if spell in game.stack:
        game.stack.remove(spell)
        go_to_gy(game, spell.card)
    game.update_battlefield()

def abil_resolve(game, abil):
    if abil in game.stack:
        game.stack.remove(abil)
    game.update_battlefield()

def targeted_damage(game, sporab, amount):
    source = sporab.obj
    dealt = damage(game, source, sporab.target[0], amount)
    if dealt != None:
        game.update_battlefield()
        game.add_to_tst([[source, sporab.target[0], dealt, False], 'dealt_damage'])

def ref_obj_targeted_damage(game, sporab, amount):
    source = sporab.ref_obj[0]
    dealt = damage(game, source, sporab.target[0], amount)
    if dealt != None:
        game.update_battlefield()
        game.add_to_tst([[source, sporab.target[0], dealt, False], 'dealt_damage'])

def targeted_gy_to_hand(game, sporab):
    gy_to_hand(game, sporab.target[0])
    game.update_battlefield()

def targeted_gy_to_bf(game, sporab):
    perm = classes.Permanent(game, sporab.controller, sporab.target[0])
    enter_battlefield(game, [perm])

def self_gy_to_hand(game, abil):
    if abil.obj in abil.obj.owner.graveyard:
        abil.target.append(abil.obj)
        targeted_gy_to_hand(game, abil)
        return None
    output.output(game,abil.controller, abil.name, 'has no effect')
    return None

def target_indestructible(game, sporab):
    sporab.target[0].indestructible = True

def sporab_token(game, sporab, color, sub_type, power, toughness,
               cab = classes.CardAbilities()):
    tokens = make_tokens(game, sporab.controller, 1, color, sub_type,
                       power, toughness, cab)

def sporab_tokens(game, sporab, number, power, toughness,
                  cab = classes.CardAbilities()):
    tokens = make_tokens(game, sporab.controller, number, sporab.color_word,
                         sporab.type_word[0], power, toughness, cab)

def spell_mana(game, spell, mana):
    for i in range(6):
        spell.controller.mana_pool[i]+=mana[i]
    game.update_battlefield()

def targeted_exile(game, sporab):
    exile(game, sporab.target[0])
    game.update_battlefield()
    game.add_to_tst([sporab.target[0], 'left_battlefield'])

def targeted_exile_from_gy(game, sporab):
    sporab.target[0].owner.graveyard.remove(sporab.target[0])
    card = card_copy(sporab.target[0].base, sporab.target[0].player)
    game.exile.append(card)
    output.output(game, sporab.controller, card.name+\
                  ' was exiled from '+\
                  card.owner.name+'\'s graveyard')
    game.update_battlefield()

def may(game, abil, effect):
    output.output(game, abil.controller, abil.rules_text, '')
    if may_choose(game, abil.controller):
        effect[0](game, abil, *effect[1:])
    return None

def may_choose(game, player):
    output.output(game, player, 'Do you want to do this?', '')
    input_ = game.get_input(player)
    if 'n' in input_ or 'N' in input_:
        return False
    return True
        
def change_cont_life(game, sporab, amount):
    change_life(game, sporab.controller, amount)
    game.update_battlefield()

def targeted_creature_keyword(game, sporab, keyword):
    rule = classes.SporabRule(sporab, game.layer[5])
    rule.effect = [la_5_ta_gains_keyword, keyword]
    rule.cleanup = cl_until_eot
    game.update_battlefield()

def equip(game, sporab):
    if sporab.obj.attached_to!=sporab.target[0]:
        if sporab.obj.attached_to!=None:
            sporab.obj.attached_to.attached.remove(sporab.obj)
        sporab.obj.attached_to = sporab.target[0]
        sporab.target[0].attached.append(sporab.obj)
        output.output(game, sporab.controller,
                      sporab.obj.name + ' is attached to '+sporab.target[0].name)
        game.battlefield.remove(sporab.obj)
        game.insert_perm(sporab.obj)
        game.update_battlefield()

def tap_target(game, sporab):
    become_tapped(game, sporab.target[0])
    game.update_battlefield()

def make_perm(game, spell):
    perm = classes.Permanent(game, spell.controller, spell.card)
    perm.base.cab = cab_copy(spell.cab)
    if 'Aura' in spell.sub_type:
        perm.attached_to = spell.target[0]
        spell.target[0].attached.append(perm)
    enter_battlefield(game, [perm])

def self_regen_shield(game, abil):
    abil.obj.regen_shield = True

def sacrifice_abil_obj(game, abil):
    perm = abil.obj
    if perm in game.battlefield:
        die(game, perm)
        game.update_battlefield()
        game.add_to_tst([perm, 'bf_to_gy'])

def targeted_mill(game, abil, amount):
    mill(game, abil.target[0], amount)

def abil_obj_mill(game, abil, amount):
    mill(game, abil.obj.controller, amount)

def targeted_life_change(game, abil, amount):
    change_life(game, abil.target[0], amount)
    game.update_battlefield()

def until_eot_lord(game, abil, power, toughness):
    rule = classes.SporabRule(abil, game.layer[8])
    rule.effect = [la_8_lord, 1, 1]
    rule.cleanup = cl_until_eot
    game.update_battlefield()
        
#4. Target tests
#always (game, sporab, target)

def ta_basic(game, sporab, target):
    if target in game.battlefield:
        if target.controller != sporab.controller and 'Hexproof' in \
           target.cab.keyword:
            return False
        if 'Shroud' in target.cab.keyword:
            return False
        if any(['Protection from '+word.lower() in target.cab.keyword for word \
                in sporab.obj.color]):
            return False
        if any(['Protection from '+word.lower()+'s' in target.cab.keyword for \
                word in sporab.obj.type_.split()]):
            return False
        if any(['Protection from '+word+'s' in target.cab.keyword for word in \
                sporab.obj.sub_type.split()]) or ('Protection from Werewolves' in \
                target.cab.keyword and 'Werewolf' in sporab.obj.sub_type):
            return False
        prot_list = [protection for protection in target.cab.keyword if\
                     'Protection from non-' in protection]
        if len(prot_list)>0:
            for item in prot_list:
                if all(['Protection from non-'+word+' creatures' != item for word\
                    in sporab.obj.sub_type.split()]):
                        return False
    if any([not rule.effect[0](game, rule, sporab, target,
                            *rule.effect[1:]) for rule in game.rule_target]):
        return False
    return True

def ta_permanent(game, sporab, target):
    if target in game.battlefield and ta_basic(game, sporab, target):
        return True
    return False
    
def ta_player(game, sporab, target):
    if target in game.player and ta_basic(game, sporab, target):
        return True
    return False

def ta_spell(game, sporab, target):
    if target in game.stack and target != sporab \
               and ta_basic(game, sporab, target):
        if target.spell:
            return True
    return False

def ta_flying(game, sporab, target):
    if ta_creature(game, sporab, target):
        if 'Flying' in target.cab.keyword:
            return True
    else:
        return False

def ta_noncreature_spell(game, sporab, target):
    if ta_spell(game,sporab,target) and 'Creature' not in target.type_:
        if target.spell:
            return True
    return False

def ta_noncreature_permanent(game, sporab, target):
    if ta_permanent(game, sporab, target):
        if 'Creature' not in target.type_:
            return True
    return False

def ta_enchantment(game, sporab, target):
    if target in game.battlefield and ta_basic(game, sporab, target):
        if 'Enchantment' in target.type_:
            return True
    return False

def ta_creature(game, spell, target):
    if is_creature(game, target) and ta_basic(game, spell, target):
        return True
    return False

def ta_land(game, spell, target):
    if ta_permanent(game, spell, target) and 'Land' in target.type_:
        return True
    return False

def ta_creature_type(game, spell, target):
    if ta_creature(game, spell, target):
        if spell.type_word[0] in target.sub_type:
            return True
    return False

def ta_attacking_creat(game, spell, target):
    if ta_creature(game, spell, target) and target in game.attackers:
        return True
    return False

def ta_creature_you_control(game, spell, target):
    if ta_creature(game, spell, target) and spell.controller == target.controller:
        return True
    return False

def ta_creature_opponent_controls(game, spell, target):
    if ta_creature(game, spell, target) and spell.controller != target.controller:
        return True
    return False

def another_ta_creature(game, sporab, target):
    if ta_creature(game, sporab, target) and target != sporab.obj:
        return True
    return False

def ta_creature_or_player(game, sporab, target):
    if ta_creature(game, sporab, target) or ta_player(game, sporab, target):
        return True
    return False
                
def ta_card_in_cont_gy(game, sporab, target):
    if target in sporab.controller.graveyard and ta_basic(game, sporab, target):
        return True
    return False

def ta_card_in_gy(game, sporab, target):
    if (target in sporab.controller.graveyard or \
       target in sporab.controller.next_player.graveyard) and \
       ta_basic(game, sporab, target):
        return True
    return False

def ta_creat_in_cont_gy(game, sporab, target):
    if ta_card_in_cont_gy(game, sporab, target):
        if 'Creature' in target.type_:
            return True
    return False

def ta_non_color_creature(game, sporab, target):
    if ta_creature(game, sporab, target):
        if sporab.color_word[0] not in target.color:
            return True
    return False

def ta_artifact(game, spell, target):
    if target in game.battlefield and ta_basic(game, spell, target):
        if 'Artifact' in target.type_:
            return True
    return False

def ta_artifact_or_enchantment(game, spell, target):
    if ta_artifact(game, spell, target) or ta_enchantment(game, spell, target):
            return True
    return False

def ta_opponent(game, spell, target):
    if target == spell.controller.next_player:
        return True
    return False

def ta_up_to_creat(game, spell, target):
    if target == 'No target' or ta_creature(game, spell, target)\
       and target not in spell.target:
        return True
    return False
        
#StaticAbil effects

def lord_layer_static(game, perm, stab, power, toughness):
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [la_8_lord, power, toughness]

def unblockable(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_cant_block)
    rule.effect = [r_cant_block_unblockable]

def cant_block(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_cant_block)
    rule.effect = [r_cant_block_abil_obj]

def anthem(game, perm, stab, power, toughness):
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [la_8_anthem, power, toughness]

def attacks_each_turn(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_attack)
    rule.effect = [r_attack_obj_attacks_each_turn]

def doesnt_untap(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_untap)
    rule.effect = [r_untap_self]

def attached_plus(game, perm, stab, power, toughness):
    if perm.attached_to!= None:
        rule = classes.PermRule(perm, stab, game.layer[8])
        rule.effect = [la_8_attached_plus, power, toughness]

def attached_keyword(game, perm, stab, keyword):
    if perm.attached_to!=None:
        rule = classes.PermRule(perm, stab, game.layer[5])
        rule.effect = [la_5_attached_gains_keyword, keyword]

def attached_prevent_combat_damage(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_damage)
    rule.effect = [r_damage_attached_prevent_combat_damage]

def self_indestructible(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_obj_char)
    rule.effect = [r_obj_char_rule_obj_indestructible]
    
#5. Layer effects

def la_8_plus(game, rule, power, toughness):
    if is_creature(game, rule.ref_obj[0]):
        rule.ref_obj[0].power += power
        rule.ref_obj[0].toughness += toughness

def la_8_anthem(game, rule, power, toughness):
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm.controller == rule.obj.controller:
            perm.power+=power
            perm.toughness+=toughness

def la_8_creat_list_plus(game, rule, creat_list, power, toughness):
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm in creat_list:
            perm.power+=power
            perm.toughness+=toughness

def la_5_creat_list_keyword(game, rule, creat_list, keyword):
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm in creat_list:
            perm.cab.keyword.append(keyword)

def la_8_attached_plus(game, rule, power, toughness):
    rule.obj.attached_to.power += power
    rule.obj.attached_to.toughness += toughness

def la_5_ta_gains_keyword(game, rule, keyword):
    if is_creature(game, rule.ref_obj[0]):
        rule.ref_obj[0].cab.keyword.append(keyword)

def la_5_self_keyword(game, rule, keyword):
    rule.obj.cab.keyword.append(keyword)

def la_5_attached_gains_keyword(game, rule, keyword):
    rule.obj.attached_to.cab.keyword.append(keyword)

def la_7_set_pt(game, rule, power, toughness):
    if is_creature(game, rule.ref_obj[0]):
        rule.ref_obj[0].power = power
        rule.ref_obj[0].toughness = toughness

def la_5_loses_abil(game, rule):
    if is_creature(game, rule.ref_obj[0]):
        rule.ref_obj[0].cab = classes.CardAbilities()

def la_3_set_creature_type(game, rule, sub_type):
    if is_creature(game, rule.ref_obj[0]):
        rule.ref_obj[0].sub_type = sub_type

def la_3_add_type(game, rule):
    for item in rule.ref_obj:
        if 'Creature' in item.type_ and item in game.battlefield and \
           rule.type_word[0] not in item.sub_type:
            if len(item.sub_type)>0:
                item.sub_type += ' '+rule.type_word[0]
            else:
                item.sub_type += rule.type_word[0]

def la_4_set_color(game, rule, color):
    rule.ref_obj[0].color = [color]
    
def la_8_lord(game, rule, power, toughness):
    for perm in game.battlefield:
        if is_creature(game, perm) and rule.type_word[0] \
            in perm.sub_type and perm!=rule.obj and perm.controller == \
                rule.obj.controller:
            perm.power += power
            perm.toughness +=toughness

def la_8_type_plus(game, rule, power, toughness):
    for perm in game.battlefield:
        if is_creature(game, perm) and rule.type_word[0] \
            in perm.sub_type and perm.controller == \
                rule.obj.controller:
            perm.power += power
            perm.toughness +=toughness

def la_1_change_control(game, rule):
    rule.ref_obj[0].controller = rule.obj.controller

def r_obj_char_rule_obj_indestructible(game, rule):
    rule.obj.indestructible = True

#other game.rule effects

def skip_draw_phase(game, rule, event):
    if game.step == 'upkeep':
        if event == [game.active_player, 'draw']:
            return [game.active_player, 'first_main']
    return event

def skip_blockers_damage(game, rule, event):
    if game.step == 'declare_attackers':
        if event == [game.active_player, 'declare_blockers'] and \
                game.attackers == []:
            return [game.active_player, 'end_combat']
    return event

def first_strike_step(game, rule, event):
    if game.step == 'combat_damage':
        if event == [game.active_player, 'end_combat']:
            return [game.active_player, 'combat_damage']
    return event


def r_damage_planeswalker_redirect(game, rule, source, target, amount, combat):
    if target in game.player and not combat:
        if source.controller != target:
            planeswalker_list = [perm for perm in game.battlefield if \
                                 'Planeswalker' in perm.type_ and \
                                 perm.controller == target]
            if planeswalker_list!= []:
                new_target = choose_obj_from_list(game, source.controller,\
                                     planeswalker_list+[target],
                                    prompt = 'Redirect the damage to '+\
                                                  target.name+':'
                                                  )
                return [source, new_target, amount]
    return False

def r_damage_attached_prevent_combat_damage(game, rule, source, target, amount,
                                            combat):
    if target == rule.obj.attached_to or source == rule.obj.attached_to and \
       combat:
        return [source, target, 0]
    else:
        return False

def r_untap_attached(game, rule):
    return [rule.obj.attached_to]

def r_untap_self(game, rule):
    return [rule.obj]

def r_attack_obj_attacks_each_turn(game, rule, attacks):
    if any([item[0] == rule.obj for item in attacks]):
        return 1
    return 0

def r_attack_attached_attacks_each_turn(game, rule, attacks):
    if any([item[0] == rule.obj.attached_to for item in attacks]):
        return 1
    return 0

def r_activate_cant_activate(game, rule, player, abts):
    if abts == rule.ref_obj[0]:
        return False
    return True

def r_activate_loyalty(game, rule, player, abts):
    if rule.obj == abts.obj and abts.other_cost[0].effect[0]==fun_loyalty:
        return False
    return True

def r_cant_block_ref_obj(game, rule, blocker, attacker):
    if blocker in rule.ref_obj:
        return False
    return True

def r_cant_block_abil_obj(game, rule, blocker, attacker):
    if blocker == rule.obj:
        return False
    return True

def r_cant_block_unblockable(game, rule, blocker, attacker):
    if rule.obj == attacker:
        return False
    return True

def r_cant_block_attached(game, rule, blocker, attacker):
    if blocker == rule.obj.attached_to:
        return False
    return True

def r_cant_attack_attached(game, rule):
    return [rule.obj.attached_to]

def r_can_play_normal(game, rule):
    player = game.prior_player
    spell_list = []
    sorc = False
    if game.stack == [] and game.step in ('first_main', 'second_main') and\
       game.prior_player == game.active_player:
        sorc = True
    for card in game.prior_player.hand:
        if 'Land' in card.type_ and sorc:
            spell_list.append(classes.Spell(game, player, card))
        elif ('Instant' in card.type_ or 'Flash' in card.cab.keyword or sorc)\
                and card.mana_cost!=None:
            spell_list.append(classes.Spell(game, player, card))
    return spell_list

def r_cant_play_lands(game, rule):
    player = game.prior_player
    land_list = []
    if player.played_land or game.prior_player != game.active_player:
        for card in game.prior_player.hand:
            if 'Land' in card.type_:
                land_list.append(classes.Spell(game, player, card))
    return land_list

#Trigger tests
    
def tr_self_etb(game, abts, trig_obj, event_str):
    if event_str == 'etb' and abts.obj == trig_obj:
        return True
    return False

def tr_self_bf_to_gy(game, abts, trig_obj, event_str):
    if event_str == 'bf_to_gy' and abts.obj == trig_obj:
        return True
    return False

def tr_self_left_battlefield(game, abts, trig_obj, event_str):
    if (event_str == 'left_battlefield' or event_str == 'bf_to_gy')\
            and abts.obj == trig_obj:
        return True
    return False

def tr_self_attacking_or_blocking(game, abts, trig_obj, event_str):
    if tr_self_attacking(game, abts, trig_obj, event_str) or \
       tr_blocks(game, abts, trig_obj, event_str):
        return True
    return False

def tr_self_attacking(Game, abts, trig_obj, event_str):
    if event_str == 'attacking' and abts.obj == trig_obj:
        return True
    return False

def tr_begin_upkeep(game, abts, trig_obj, event_str):
    if event_str == 'begin_upkeep':
        return True
    return False

def tr_begin_end(game, abts, trig_obj, event_str):
    if event_str == 'begin_end':
        return True
    return False

def tr_your_begin_upkeep(game, abts, trig_obj, event_str):
    if event_str == 'begin_upkeep' and abts.controller == game.active_player:
        return True
    return False

def tr_your_begin_end(game, abts, trig_obj, event_str):
    if event_str == 'begin_end' and abts.controller == game.active_player:
        return True
    return False

def tr_begin_end_combat(game, abts, trig_obj, event_str):
    if event_str == 'begin_end_combat':
        return True
    return False

def tr_blocks_or_becomes_blocked(game, abts, trig_obj, event_str):
    if tr_blocks(game, abts, trig_obj, event_str) or \
       tr_becomes_blocked(game, abts, trig_obj, event_str):
        return True
    return False

def tr_blocks(game, abts, trig_obj, event_str):
    if event_str == 'block' and abts.obj == trig_obj[0]:
        return True
    return False

def tr_becomes_blocked(game, abts, trig_obj, event_str):
    if event_str == 'block' and abts.obj == trig_obj[1]:
        return True
    return False

def tr_combat_damage_to_player(game, abts, trig_obj, event_str):
    if event_str == 'dealt_damage':
        if trig_obj[0] == abts.obj and trig_obj[1] in game.player and \
           trig_obj[3]==True:
            return True
    return False


def tr_combat_damage_to_creature(game, abts, trig_obj, event_str):
    if event_str == 'dealt_damage':
        if trig_obj[0] == abts.obj and trig_obj[1] in game.battlefield \
               and trig_obj[3]==True:
            if 'Creature' in trig_obj[1].type_:
                return True
    return False

def tr_creature_dies(game, abts, trig_obj, event_str):
    if event_str == 'bf_to_gy':
        if 'Creature' in trig_obj.type_:
            return True
    return False

def tr_another_creature_dies(game, abts, trig_obj, event_str):
    if tr_creature_dies(game, abts, trig_obj, event_str):
        if trig_obj != abts.obj:
            return True
    return False

def tr_nontoken_creature_you_control_dies(game, abts, trig_obj, event_str):
    if tr_creature_dies(game, abts, trig_obj, event_str):
        if trig_obj.card.real and trig_obj.controller == abts.obj.controller:
            return True
    return False

def tr_etb_another_type_your_control(game, abts, trig_obj, event_str):
    if event_str == 'etb':
        if 'Creature' in trig_obj.type_ and \
           abts.type_word[0] in trig_obj.sub_type\
           and abts.obj != trig_obj\
           and abts.obj.controller == trig_obj.controller:
            return True
    return False

def tr_you_cast_instant_or_sorcery(game, abts, trig_obj, event_str):
    if event_str == 'cast':
        if trig_obj.controller == abts.obj.controller and \
           ('Instant' or 'Sorcery' in trig_obj.type_):
            return True
    return False

#Cleanup

def cl_until_eot(game, rule, key):
    if key == 'cleanup':
        rule.location.remove(rule)

def cl_bf_update(game, rule, key):
    if key == 'bf_update':
        rule.location.remove(rule)

def cl_never(game, rule, key):
    return None    

def cl_first_turn(game, rule, key):
    if key == 'next_step' and game.step == 'first_main':
        rule.location.remove(rule)

def cl_first_strike(game, rule, key):
    if key == 'next_step':
        rule.location.remove(rule)

def cl_triggered(game, rule, key):
    if rule in game.trig_abil:
        if rule.triggered:
            rule.location.remove(rule)

def cl_rule_obj_gone(game, rule, key):
    if rule.obj not in game.battlefield:
        rule.location.remove(rule)

#additional (non-mana) costs: [test, fun]
    
def test_tap(game, player, abts):
    if not abts.obj.tapped and (not abts.obj.sum_sick or 'Creature' \
                                not in abts.obj.type_ or 'Haste' in \
                                abts.obj.cab.keyword):
        return True

def fun_tap(game, player, abil_or_abts):
    if abil_or_abts.obj.tapped or abil_or_abts.obj not in game.battlefield or \
       abil_or_abts.obj.controller!=player:
        return False
    become_tapped(game, abil_or_abts.obj)
    game.undo_list.append([untap, abil_or_abts.obj])
    game.update_battlefield()
    game.add_to_tst([abil_or_abts.obj, 'became_tapped'])

def test_loyalty(game, player, abts, amount):
    if abts.obj.counter['Loyalty']>=amount:
        return True
    return False

def fun_loyalty(game, player, abil, amount):
    rule = classes.SporabRule(abil, game.rule_activate)
    rule.effect = [r_activate_loyalty]
    rule.cleanup = cl_until_eot
    if abil.obj.counter['Loyalty']<0-amount:
        return False
    abil.obj.counter['Loyalty']+=amount
    game.update_battlefield()


def test_counter(game, player, abts, counter, amount):
    if abts.obj.counter[counter]>=amount:
        return True
    else:
        return False

def fun_counter(game, player, abts, counter, amount):
    if abts.obj.counter[counter]>=amount:
        abts.obj.counter[counter]-=amount
        return True
    return False

def test_true(game, player, abts):
    return True

def test_discard(game, player, abts, number):
    if len(player.hand)>=number:
        return True
    return False

def fun_discard(game, player, abts, number):
    if len(player.hand)>=number:
        choose_discard(game, player, number)
        return True
    else:
        return False

def test_sac_creat(game, player, abts):
    if any(['Creature' in perm1.type_ for perm1 in game.battlefield if \
            player == perm1.controller]):
        return True
    return False

def fun_sac_creat(game, player, sporab_or_abts):
    if test_sac_creat(game, player, sporab_or_abts):
        creat = choose_sacrifice_creature(game, player)
        sporab_or_abts.ref_obj.append(creat)
        game.undo_list.append([undo_sacrifice, creat])
        return True
    return False

def fun_sac_this(game, player, abil_or_abts):
    if abil_or_abts.obj not in game.battlefield or abil_or_abts.obj.controller!=player:
        return False
    die(game, abil_or_abts.obj)
    game.update_battlefield()
    game.add_to_tst([abil_or_abts.obj, 'bf_to_gy'])
    game.undo_list.append([undo_sacrifice, abil_or_abts.obj])
    return True

def fun_sac_ref_obj(game, player, abil_or_abts):
    if abil_or_abts.obj not in game.battlefield or abil_or_abts.ref_obj[0] not in game.battlefield:
        return False
    die(game, abil_or_abts.ref_obj[0])
    game.update_battlefield()
    game.add_to_tst([abil_or_abts.ref_obj[0], 'bf_to_gy'])
    game.undo_list.append([undo_sacrifice, abil_or_abts.ref_obj[0]])

def fun_once_per_turn(game, player, abil):
    rule = classes.SporabRule(abil, game.rule_activate)
    rule.effect = [r_activate_cant_activate]
    rule.cleanup = cl_until_eot
    rule.ref_obj.append(abil.abts)
    game.undo_list.append([undo_remove_rule, rule])

def test_can_pay_mana(game, player, cost, mana_pool = None,
                      used_producers = None):
    cost = list(cost)
    if used_producers == None:
        used_producers = []
    if mana_pool == None:
        mana_pool = list(player.mana_pool)
    for i in range(5):
        m = min([mana_pool[i], cost[i]])
        mana_pool[i]-=m
        cost[i]-=m
    m = sum(mana_pool)
    if m>=cost[5] and all([cost[i]==0 for i in range(5)]):
        return True
    mana_pool = [0,0,0,0,0,m]  
    #prevents the activation of mana abilities that require colored mana.
    for perm in game.battlefield:
        can_produce = []
        if perm.controller == player and perm not in used_producers:
            act = perm.cab.act_mana
            for abts in act:
                check = True
                if abts.mana_cost!=None:
                    if not mana_cost_subset(abts.mana_cost, mana_pool):
                        check = False
                for other_cost in abts.other_cost:
                    check = min([check, other_cost.test[0](game, player, abts,
                                                           *other_cost.test[1:])])
                if check:
                    can_produce.append(abts)
        used_producers1 = list(used_producers)
        for abts in can_produce:
            mana_pool1 = componentwise_add(mana_pool, abts.would_produce)
            if test_tap == abts.other_cost[0].test[0]:
                    used_producers1 += [abts.obj]
            if abts.mana_cost!=None:
                    mana_pool1 = componentwise_subtract(mana_pool1, abts.mana_cost)
            if test_can_pay_mana(game, player, cost,
                                 mana_pool1, used_producers1):
                    return True
        if len(can_produce)>0:
            if all([abts.mana_cost==None for abts in can_produce[0].obj.cab.act_mana]):
                break
        if perm not in used_producers and not any([abts.mana_cost!=None for abts in \
                                                   perm.cab.act_mana]):
            used_producers.append(perm)
    return False

def ase_test_true(game, repef, perm):
    return True

def ase_test_creature(game, repef, perm):
    if 'Creature'in perm.type_:
        return True
    return False

def ase_test_creature_you_control(game, repef, perm):
    if 'Creature' in perm.type_ and perm.controller == repef.obj.controller:
        return True
    return False

def ase_tapped(game, repef, perm):
    perm.tapped = True

def ase_tapped_and_attacking(game, repef, perm):
    perm.tapped = True
    creature = perm
    attackables = [game.active_player.next_player]
    for perm in game.battlefield:
        if 'Planeswalker' in perm.type_ and perm.controller == \
               game.active_player.next_player:
            attackables.insert(0, perm)
    game.attacks.append([creature,attackables[0],None])
    if len(attackables)>1:
        to_attack = choose_obj_from_list(game,
                    game.active_player, attackables,
                    'Choose a player or planeswalker to attack:')
        game.attacks[-1][1] = to_attack
    game.attackers.append(creature)

#abts Timing tests

def tim_sorcery(game,player,abts):
    if game.active_player != player:
        return False
    if game.stack!= []:
        return False
    if game.step not in ('first_main', 'second_main'):
        return False
    return True

    
