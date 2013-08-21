

##Layers:
##[0]:Copy, [1]:Control, [2]:Test, [3]: Type, [4]:Color, [5]:Abilities
##[6]:P/T CDA [7]: P/T Set [8]: P/T Adjust [9]: P/T Counters [10]: P/T Switch

COLOR_WORDS = ('White', 'Blue', 'Black', 'Red', 'Green')
ORDINAL_WORDS = ('first', 'second', 'third', 'fourth', 'fifth')
NUMBER_WORDS = ('one', 'two', 'three', 'four', 'five')
STARTING_LIFE = 20
LAND_WORDS = ('Plains', 'Island', 'Swamp', 'Mountain', 'Forest')
CREAT_KEYWORD_LIST = ('Bloodthirst', 'Trample', 'First strike', 'Double strike',
                      'Lifelink', 'Hexproof', 'Vigilance', 'Haste', 'Flying',
                      'Reach', 'Deathtouch', 'Protection', 'Intimidate',
                      'Islandwalk', 'Swampwalk', 'Defender', 'Flash',
                        'Enchant ')

import effects
import copy
import inn_effects
import classes
    
def initCardList(card_set):
    f = open('card_list_inn.txt')
    finished = False
    data=[]
    j=0
    while not finished:
        data.append(classes.Data())
        line = f.readline()
        data[j].oracle=line
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        data[j].name=line.rstrip()
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        line=line.rstrip()
        if len(line)>0:
            data[j].mana_cost_str = line
            data[j].mana_cost = []
            data[j].mana_cost.append(line.count('W'))
            data[j].mana_cost.append(line.count('U'))
            data[j].mana_cost.append(line.count('B'))
            data[j].mana_cost.append(line.count('R'))
            data[j].mana_cost.append(line.count('G'))
            if line.lstrip('XY').rstrip('WUBRG') == '':
                data[j].mana_cost.append(0)
            else:
                data[j].mana_cost.append(int(line.lstrip('X').rstrip('WUBRG')))
        else: 
            data[j].mana_cost_str = ''
            data[j].mana_cost = None
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        line=line.rstrip()
        data[j].type_str = line
        if line.count(' ')==0:
            data[j].sup_type = ''
            data[j].type_= line
            data[j].sub_type = ''
        else:
            if line.count('Basic')==1 or line.count('Legendary')==1\
                    or line.count('World')==1:
                data[j].sup_type = line[:line.index(' ')]
                line = line[line.index(' ')+1:]
                if line.count('Snow')==1:
                    data[j].sup_type = data[j].sup_type + ' Snow'
                    line = line[line.index(' ')+1:]
            elif line.count('Snow')==1:
                data[j].sup_type = line[:line.index(' ')]
                line = line[line.index(' ')+1:]
            else: data[j].sup_type = ''
            if line.count('-')==0:
                type_ = line
                sub_type = ''
            if line.count('-')==1:
                type_ = line[:line.index(' -')]
                sub_type = line[line.index('-')+2:]
            data[j].type_ = type_
            data[j].sub_type = sub_type
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        if len(line)>1:
            if line.count('/')==1 and line.count('*')==0:
                data[j].power = int(line[1:line.index('/')])
                data[j].toughness = int(line[line.index('/')+ \
                                             1:line.index(')')])
                data[j].loyalty = None
            elif line.count('*')>0:
                data[j].power = 0
                data[j].toughness = 0
                data[j].loyalty = None
            else:
                data[j].power = None
                data[j].toughness = None
                data[j].loyalty = int(line[line.index('(')+1:line.index(')')])
        else:
            data[j].power= None
            data[j].toughness = None
            data[j].loyalty = None
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        line = f.readline()
        data[j].oracle = data[j].oracle+line
        rules_text = ''
        while line != 'Set/Rarity:\n':
            rules_text = rules_text + line
            line = f.readline()
            data[j].oracle = data[j].oracle+line
        data[j].rules_text = rules_text.rstrip()
        line = f.readline()
        data[j].oracle = data[j].oracle \
                        +line[line.index(card_set):line.find(',')]+'\n'
        data[j].set = card_set
        data[j].rarity = line[line.index(card_set)+len(card_set)+1:line.find(',')]
        line = f.readline()
        if line != '\n': finished=True
        data[j].real = True
        data[j].cab = classes.CardAbilities()
        j = j+1

            
    card_list = []
    for i in range(len(data)):
        card_list.append(classes.Card(data[i]))

    name = [x.name.replace('\xc3\x86', 'Ae') for x in card_list]

    card_dict = dict([(name[j],card_list[j]) for j in range(len(card_list))])
    
    for card_name in card_dict:
        card = card_dict[card_name]
        abil_part = []
        next_part = card.rules_text.partition('\n')
        while next_part[0]!='':
            for word in CREAT_KEYWORD_LIST:
                if word in next_part[0][:len(word)+2] and 'Flashb' \
                   not in next_part[0][:len(word)+2]:
                    if '(' in next_part[0]:
                        card.cab.keyword.append(
                                next_part[0][:next_part[0].index('(')].rstrip())
                    elif ',' in next_part[0]:
                        card.cab.keyword.append(
                                next_part[0][:next_part[0].index(',')].rstrip())
                    else:
                        card.cab.keyword.append(next_part[0].rstrip())
            if 'Flashback' in next_part[0][:9]:
                stab = classes.StaticAbil()
                stab.effect = [inn_effects.flashback]
                if '(' in next_part[0]:
                    stab.rules_text = next_part[0][:next_part[0].index('(')].rstrip()
                else:
                    stab.rules_text = next_part[0]
                card.cab.grav_static.append(stab)
            next_part = next_part[2].partition('\n')
        if 'Planeswalker' in card.type_:
            repef = classes.ReplacementEffect()
            repef.name = card.name + ' enters the battlefield with '+\
                         str(card.loyalty)+' loyalty counters on it'
            repef.test = effects.ase_test_true
            repef.effect = [effects.enters_with_counter, 'Loyalty', \
                            card.loyalty]
            card.cab.as_enters.append(repef)
            
            

    card = card_dict['Voiceless Spirit']
    card.cab.keyword.append('First strike')

    card = card_dict['Grave Bramble']
    card.cab.keyword.append('Protection from Zombies')

    card = card_dict['Elite Inquisitor']
    card.cab.keyword.insert(1, 'Vigilance')
    card.cab.keyword.append('Protection from Werewolves')
    card.cab.keyword.append('Protection from Zombies')

    card = card_dict['Abbey Griffin']
    card.cab.keyword.append('Vigilance')

    card = card_dict['Falkenrath Marauders']
    card.cab.keyword.append('Haste')
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.effect = [inn_effects.falkenrath_marauders]
    card.cab.trig.append(stab)

    card = card_dict['Slayer of the Wicked']
    stab = classes.StaticAbil()
    stab.type_word.extend(['Vampire', 'Zombie', 'Werewolf'])
    stab.rules_text = card.rules_text
    stab.effect = [inn_effects.slayer_of_the_wicked]
    card.cab.trig.append(stab)

    card = card_dict['Avacynian Priest']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,1]
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list.insert(0, [effects.tap_target])
    abts.rules_text = card.rules_text
    abts.type_word.append('Human')
    abts.sporab_target.append(inn_effects.ta_avacynian_priest)
    card.cab.act.append(abts)

    card = card_dict['Kessig Wolf']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,1,0,1]
    abts.ef_list.insert(0, [effects.abil_obj_keyword, 'First strike'])
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)

    card = card_dict['Tree of Redemption']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [inn_effects.tree_of_redemption])
    card.cab.act.append(abts)

    card = card_dict['Traveler\'s Amulet']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_sac_this]
    abts.other_cost.append(cost)
    abts.mana_cost = [0,0,0,0,0,1]
    abts.rules_text = card.rules_text
    abts.ef_list.insert(0, [inn_effects.travelers_amulet])
    card.cab.act.append(abts)

    card = card_dict['Brain Weevil']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_sac_this]
    abts.timing.append(effects.tim_sorcery)
    abts.other_cost.append(cost)
    abts.ef_list = [[effects.targeted_discard, 2]]
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.sporab_target.append(effects.ta_player)
    card.cab.act.append(abts)

    card = card_dict['Mindshrieker']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,2]
    abts.sporab_target.append(effects.ta_player)
    abts.ef_list.insert(0, [inn_effects.mindshrieker])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)

    card = card_dict['Lantern Spirit']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,1,0,0,0,0]
    abts.ef_list.insert(0, [effects.abil_obj_return_to_hand])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)

    card = card_dict['Mirror-Mad Phantasm']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,1,0,0,0,1]
    abts.ef_list.insert(0, [inn_effects.mirror_mad_phantasm])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)

    card = card_dict['Bloodline Keeper']
    card.other_face = card_dict['Lord of Lineage']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,1,0,0,0]
    abts.timing.append(inn_effects.tim_bloodline_keeper)
    abts.ef_list.insert(0, [inn_effects.transform])
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.type_word.append('Vampire')
    card.cab.act.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    abts.color_word.append('Black')
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.type_word.append('Vampire')
    abts.ef_list.insert(0, [effects.sporab_token, abts.color_word, \
                         abts.type_word[0], 2, 2, cab])
    card.cab.act.append(abts)

    card = card_dict['Lord of Lineage']
    card.color_indicator.append('Black')
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    abts.color_word.append('Black')
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.type_word.append('Vampire')
    abts.ef_list.insert(0, [effects.sporab_token, abts.color_word, \
                         abts.type_word[0], 2, 2, cab])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.effect = [effects.lord_layer_static, 2, 2]
    stab.type_word.append('Vampire')
    card.cab.layer_static[8].append(stab)
    card.other_face = card_dict['Bloodline Keeper']

    card = card_dict['Night Revelers']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text
    stab.type_word.append('Human')
    stab.effect = [inn_effects.night_revelers]
    card.cab.layer_static[5].append(stab)

    card = card_dict['Gallows Warden']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Spirit')
    stab.effect = [effects.lord_layer_static, 0, 1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Scourge of Geier Reach']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text
    stab.effect = [inn_effects.scourge_of_geier_reach]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Battleground Geist']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Spirit')
    stab.effect = [effects.lord_layer_static, 1, 0]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Avacyn\'s Pilgrim']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text
    abts.would_produce = [1,0,0,0,0,0]
    card.cab.act_mana.append(abts)

    card = card_dict['Clifftop Retreat']
    abts = classes.AbilToStack()
    cost =  classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {R} to your mana pool'
    abts.would_produce = [0,0,0,1,0,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {W} to your mana pool'
    abts.would_produce = [1,0,0,0,0,0]
    card.cab.act_mana.append(abts)
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()[0]
    repef.type_word = ['Plains', 'Mountain']
    repef.test = inn_effects.ase_test_duals
    repef.effect = [effects.ase_tapped]
    card.cab.as_enters.append(repef)

    card = card_dict['Woodland Cemetery']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {B} to your mana pool'
    abts.would_produce = [0,0,1,0,0,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {G} to your mana pool'
    abts.would_produce = [0,0,0,0,1,0]
    card.cab.act_mana.append(abts)
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()[0]
    repef.type_word = ['Forest', 'Swamp']
    repef.test = inn_effects.ase_test_duals
    repef.effect = [effects.ase_tapped]
    card.cab.as_enters.append(repef)

    card = card_dict['Sulfur Falls']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {U} to your mana pool'
    abts.would_produce = [0,1,0,0,0,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {R} to your mana pool'
    abts.would_produce = [0,0,0,1,0,0]
    card.cab.act_mana.append(abts)
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()[0]
    repef.type_word = ['Island', 'Mountain']
    repef.test = inn_effects.ase_test_duals
    repef.effect = [effects.ase_tapped]
    card.cab.as_enters.append(repef)

    card = card_dict['Isolated Chapel']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {W} to your mana pool'
    abts.would_produce = [1,0,0,0,0,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {B} to your mana pool'
    abts.would_produce = [0,0,1,0,0,0]
    card.cab.act_mana.append(abts)
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()[0]
    repef.type_word = ['Plains', 'Swamp']
    repef.test = inn_effects.ase_test_duals
    repef.effect = [effects.ase_tapped]
    card.cab.as_enters.append(repef)

    card = card_dict['Hinterland Harbor']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {G} to your mana pool'
    abts.would_produce = [0,0,0,0,1,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{T}: add {U} to your mana pool'
    abts.would_produce = [0,1,0,0,0,0]
    card.cab.act_mana.append(abts)
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()[0]
    repef.type_word = ['Forest', 'Island']
    repef.test = inn_effects.ase_test_duals
    repef.effect = [effects.ase_tapped]
    card.cab.as_enters.append(repef)

    card = card_dict['Nephalia Drownyard']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.sporab_target.append(effects.ta_player)
    abts.mana_cost = [0,1,1,0,0,1]
    abts.ef_list.insert(0, [effects.targeted_mill, 3])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)

    card = card_dict['Gavony Township']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.mana_cost = [1,0,0,0,1,2]
    abts.ef_list.insert(0, [inn_effects.gavony_township])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)

    card = card_dict['Stensia Bloodhall']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.mana_cost = [0,0,1,1,0,3]
    abts.sporab_target.append(effects.ta_player)
    abts.ef_list.insert(0, [effects.targeted_damage, 2])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)

    card = card_dict['Moorland Haunt']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    cost = classes.Cost()
    cost.test = [inn_effects.test_exile_creat_from_gy]
    cost.effect = [inn_effects.fun_exile_creat_from_gy]
    abts.other_cost.append(cost)
    abts.type_word.append('Spirit')
    abts.color_word.append('White')
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    abts.mana_cost = [1,1,0,0,0,0]
    abts.ef_list.insert(0, [effects.sporab_tokens, 1, 1, 1, cab])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)

    card = card_dict['Kessig Wolf Run']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.sporab_target.append(effects.ta_creature)
    abts.cast_choice.append(effects.choose_x)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.mana_cost = [0,0,0,1,1,0]
    abts.ef_list.insert(0, [inn_effects.kessig_wolf_run, 0])
    card.cab.act.append(abts)

    card = card_dict['Ghost Quarter']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_sac_this]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.sporab_target.append(effects.ta_land)
    abts.ef_list.insert(0, [inn_effects.ghost_quarter])
    card.cab.act.append(abts)
    
    card = card_dict['Shimmering Grotto']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.mana_cost = [0,0,0,0,0,1]
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{1}, {T}: Add {W} to your mana pool.'
    abts.would_produce = [1,0,0,0,0,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.mana_cost = [0,0,0,0,0,1]
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{1}, {T}: Add {U} to your mana pool.'
    abts.would_produce = [0,1,0,0,0,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.mana_cost = [0,0,0,0,0,1]
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{1}, {T}: Add {B} to your mana pool.'
    abts.would_produce = [0,0,1,0,0,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    abts.other_cost.append(cost)
    abts.mana_cost = [0,0,0,0,0,1]
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{1}, {T}: Add {R} to your mana pool.'
    abts.would_produce = [0,0,0,1,0,0]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.mana_cost = [0,0,0,0,0,1]
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = '{1}, {T}: Add {G} to your mana pool.'
    abts.would_produce = [0,0,0,0,1,0]
    card.cab.act_mana.append(abts)
    
    card = card_dict['Deranged Assistant']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    cost = classes.Cost()
    cost.test = [inn_effects.test_mill_one]
    cost.effect = [inn_effects.fun_mill_one]
    abts.other_cost.append(cost)
    abts.ef_list[0] = [effects.tap_for_mana]
    abts.rules_text = card.rules_text
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)

    card = card_dict['Darkthicket Wolf']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_once_per_turn]
    abts.other_cost.append(cost)
    abts.ef_list.insert(0, [effects.abil_obj_plus, 2, 2])
    abts.mana_cost = [0,0,0,0,1,2]
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)

    card = card_dict['Manor Gargoyle']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.effect = [inn_effects.manor_gargoyle1]
    card.cab.other_static.append(stab)
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,1]
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [inn_effects.manor_gargoyle2])
    card.cab.act.append(abts)

    card = card_dict['Liliana of the Veil']
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    cost =  classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_loyalty, 1]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.ef_list.insert(0, [inn_effects.liliana_of_the_veil0])
    card.cab.act.append(abts)
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    cost = classes.Cost()
    cost.test = [effects.test_loyalty, 2]
    cost.effect = [effects.fun_loyalty, -2]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [inn_effects.liliana_of_the_veil1])
    abts.sporab_target.append(effects.ta_player)
    card.cab.act.append(abts)
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    cost = classes.Cost()
    cost.test = [effects.test_loyalty, 6]
    cost.effect = [effects.fun_loyalty, -6]
    abts.other_cost.append(cost)
    abts.sporab_target.append(effects.ta_player)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [inn_effects.liliana_of_the_veil2])
    card.cab.act.append(abts)

    card = card_dict['Garruk Relentless']
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    cost =  classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_loyalty, 0]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [effects.sporab_token, ['Green'], 'Wolf', 2, 2])
    card.cab.act.append(abts)
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_loyalty, 0]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [inn_effects.garruk_relentless1])
    abts.sporab_target.append(effects.ta_creature)
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text.splitlines()[0]
    stab.effect = [inn_effects.garruk_relentless0]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Garruk, the Veil-Cursed']

    card = card_dict['Garruk, the Veil-Cursed']
    card.color_indicator = ['Black', 'Green']
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_loyalty, 1]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[0]
    cab = classes.CardAbilities()
    cab.keyword.append('Deathtouch')
    abts.ef_list.insert(0, [effects.sporab_token, ['Black'], 'Wolf', 1, 1, cab])
    card.cab.act.append(abts)
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    cost = classes.Cost()
    cost.test = [effects.test_loyalty, 1]
    cost.effect = [effects.fun_loyalty, -1]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [inn_effects.garruk_the_veil_cursed1])
    card.cab.act.append(abts)
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    cost = classes.Cost()
    cost.test = [effects.test_loyalty, 3]
    cost.effect = [effects.fun_loyalty, -3]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [inn_effects.garruk_the_veil_cursed2])
    card.cab.act.append(abts)

    card = card_dict['Disciple of Griselbrand']
    abts = classes.AbilToStack()
    cost =  classes.Cost()
    cost.test = [effects.test_sac_creat]
    cost.effect = [effects.fun_sac_creat]
    abts.other_cost.append(cost)
    abts.mana_cost = [0,0,0,0,0,1]
    abts.rules_text = card.rules_text
    abts.ef_list.insert(0, [inn_effects.disciple_of_griselbrand])
    card.cab.act.append(abts)

    card = card_dict['Skirsdag Cultist']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    cost = classes.Cost()
    cost.test = [effects.test_sac_creat]
    cost.effect = [effects.fun_sac_creat]
    abts.rules_text = card.rules_text
    abts.other_cost.append(cost)
    abts.mana_cost = [0,0,0,1,0,0]
    abts.sporab_target = [effects.ta_creature_or_player]
    abts.ef_list.insert(0 , [effects.targeted_damage, 2])
    card.cab.act.append(abts)

    card = card_dict['Civilized Scholar']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list.insert(0, [inn_effects.civilized_scholar])
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)
    card.other_face = card_dict['Homicidal Brute']

    card = card_dict['Manor Skeleton']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,1,0,0,1]
    abts.ef_list.insert(0, [effects.abil_obj_regenerate])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)

    card = card_dict['Ludevic\'s Test Subject']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,1,0,0,0,1]
    abts.ef_list.insert(0, [inn_effects.ludevics_test_subject])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)
    card.other_face = card_dict['Ludevic\'s Abomination']

    card = card_dict['Ludevic\'s Abomination']
    card.color_indicator.append('Blue')
    card.other_face = card_dict['Ludevic\'s Test Subject']

    card = card_dict['Cellar Door']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list.insert(0, [inn_effects.cellar_door])
    abts.mana_cost = [0,0,0,0,0,3]
    abts.type_word = ['Zombie']
    abts.color_word = ['Black']
    abts.rules_text = card.rules_text
    abts.sporab_target.append(effects.ta_player)
    card.cab.act.append(abts)

    card = card_dict['Ghoulcaller\'s Bell']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list.insert(0, [inn_effects.ghoulcallers_bell])
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)

    card = card_dict['Stitcher\'s Apprentice']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.mana_cost = [0,1,0,0,0,1]
    abts.rules_text = card.rules_text
    abts.ef_list.insert(0, [inn_effects.stitchers_apprentice])
    abts.type_word.append('Homunculus')
    abts.color_word.append('Blue')
    card.cab.act.append(abts)

    card = card_dict['Back from the Brink']
    abts = classes.AbilToStack()
    cost = classes.Cost()
    cost.test = [inn_effects.test_back_from_the_brink]
    cost.effect = [inn_effects.fun_back_from_the_brink]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text
    abts.ef_list.insert(0, [inn_effects.back_from_the_brink])
    abts.timing.append(effects.tim_sorcery)
    card.cab.act.append(abts)

    card = card_dict['Elder of Laurels']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,1,3]
    abts.rules_text = card.rules_text
    abts.ef_list.insert(0, [inn_effects.elder_of_laurels])
    abts.sporab_target.append(effects.ta_creature)
    card.cab.act.append(abts)

    card = card_dict['Feral Ridgewolf']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,1,0,1]
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [effects.abil_obj_plus, 2, 0])
    card.cab.act.append(abts)

    card = card_dict['Gatstaf Shepherd']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Gatstaf Howler']

    card = card_dict['Gatstaf Howler']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.color_indicator.append('Green')
    card.other_face = card_dict['Gatstaf Shepherd']

    card = card_dict['Snapcaster Mage']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.snapcaster_mage]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Screeching Bat']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.screeching_bat]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Stalking Vampire']

    card = card_dict['Stalking Vampire']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.screeching_bat]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.color_indicator.append('Black')
    card.other_face = card_dict['Screeching Bat']

    card = card_dict['Daybreak Ranger']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Nightfall Predator']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list.insert(0, [effects.targeted_damage, 2])
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.sporab_target.append(effects.ta_flying)
    card.cab.act.append(abts)

    card = card_dict['Nightfall Predator']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Daybreak Ranger']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.mana_cost = [0,0,0,1,0,0]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.ef_list.insert(0, [inn_effects.nightfall_predator])
    abts.sporab_target.append(effects.ta_creature)
    card.cab.act.append(abts)

    card = card_dict['Selfless Cathar']
    abts = classes.AbilToStack()
    abts.mana_cost = [1,0,0,0,0,1]
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_sac_this]
    abts.other_cost.append(cost)
    abts.ef_list.insert(0, [inn_effects.selfless_cathar])
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)

    card = card_dict['Mikaeus, the Lunarch']
    card.cast_choice.append(inn_effects.choose_mikaeus_the_lunarch)
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.ef_list.insert(0, [effects.abil_obj_counter, '+1/+1', 1])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    cost = classes.Cost()
    cost.test = [effects.test_counter, '+1/+1', 1]
    cost.effect = [effects.fun_counter, '+1/+1', 1]
    abts.other_cost.append(cost)
    abts.ef_list.insert(0, [inn_effects.mikaeus_the_lunarch])
    abts.rules_text = card.rules_text.splitlines()[2]
    card.cab.act.append(abts)

    card = card_dict['Unbreathing Horde']
    repef = classes.ReplacementEffect()
    repef.test = effects.ase_test_true
    repef.effect = [inn_effects.ase_unbreathing_horde]
    repef.type_word.append('Zombie')
    repef.name = card.rules_text.splitlines()[0]
    card.cab.as_enters.append(repef)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.unbreathing_horde]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)

    card = card_dict['Silverchase Fox']
    abts = classes.AbilToStack()
    abts.mana_cost = [1,0,0,0,0,1]
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_sac_this]
    abts.other_cost.append(cost)
    abts.ef_list.insert(0, [effects.targeted_exile])
    abts.sporab_target.append(effects.ta_enchantment)
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)

    card = card_dict['Graveyard Shovel']
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    abts.mana_cost = [0,0,0,0,0,2]
    abts.sporab_target.append(effects.ta_player)
    abts.ef_list.insert(0, [inn_effects.graveyard_shovel])
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)

    card = card_dict['Cobbled Wings']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,1]
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_keyword, 'Flying']
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[5].append(stab)

    card = card_dict['Mask of Avacyn']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,3]
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.mask_of_avacyn]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[5].append(stab)

    card = card_dict['Inquisitor\'s Flail']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,2]
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.inquisitors_flail0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.inquisitors_flail1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)

    card = card_dict['Laboratory Maniac']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.laboratory_maniac]
    stab.rules_text = card.rules_text
    card.cab.other_static.append(stab)

    card = card_dict['Gruesome Deformity']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_keyword, 'Intimidate']
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[5].append(stab)

    card = card_dict['Demonmail Hauberk']
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [effects.equip])
    cost = classes.Cost()
    cost.test = [effects.test_sac_creat]
    cost.effect = [effects.fun_sac_creat]
    abts.other_cost.append(cost)
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_plus, 4, 2]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Wooden Stake']
    abts = classes.AbilToStack()
    abts.timing.append(effects.tim_sorcery)
    abts.mana_cost = [0,0,0,0,0,1]
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [effects.equip])
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_plus, 1, 0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[8].append(stab)
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.wooden_stake]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Vampire')
    card.cab.trig.append(stab)

    card = card_dict['Runechanter\'s Pike']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,2]
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.runechanters_pike]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[5].append(stab)

    card = card_dict['Sharpened Pitchfork']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,1]
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_keyword, 'First strike']
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[5].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.sharpened_pitchfork, 1, 1]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Human')
    card.cab.layer_static[8].append(stab)

    card = card_dict['Silver-Inlaid Dagger']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,2]
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_plus, 2, 0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[8].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.sharpened_pitchfork, 1, 0]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Human')
    card.cab.layer_static[8].append(stab)

    card = card_dict['Trepanation Blade']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,2]
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.trepanation_blade]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.trig.append(stab)

    card = card_dict['Butcher\'s Cleaver']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,3]
    abts.timing.append(effects.tim_sorcery)
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_plus, 3, 0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[8].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.butchers_cleaver]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Human')
    card.cab.layer_static[5].append(stab)

    card = card_dict['Blazing Torch']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,1]
    abts.timing.append(effects.tim_sorcery)
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.ef_list.insert(0, [effects.equip])
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.type_word = ['Vampire', 'Zombie']
    stab.effect = [inn_effects.blazing_torch_0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.blazing_torch_1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[5].append(stab)

    card = card_dict['Witchbane Orb']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.witchbane_orb0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.trig.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.witchbane_orb1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)
    
    card = card_dict['Curse of Oblivion']
    card.sporab_target.append(effects.ta_player)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.curse_of_oblivion]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Curse of Stalked Prey']
    card.sporab_target.append(effects.ta_player)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.curse_of_stalked_prey]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Curse of Death\'s Hold']
    card.sporab_target.append(effects.ta_player)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.curse_of_deaths_hold]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Curse of the Nightly Hunt']
    card.sporab_target.append(effects.ta_player)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.curse_of_the_nightly_hunt]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)

    card = card_dict['Curse of the Bloody Tome']
    card.sporab_target.append(effects.ta_player)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.curse_of_the_bloody_tome]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Curse of the Pierced Heart']
    card.sporab_target.append(effects.ta_player)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.curse_of_the_pierced_heart]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Bonds of Faith']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.bonds_of_faith]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Wreath of Geists']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.wreath_of_geists]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Angelic Overseer']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.angelic_overseer]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Human')
    card.cab.layer_static[5].append(stab)

    card = card_dict['Full Moon\'s Rise']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.full_moons_rise0]
    stab.rules_text = card.rules_text.splitlines()[0]
    stab.type_word.append('Werewolf')
    card.cab.layer_static[5].append(stab)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_sac_this]
    abts.other_cost.append(cost)
    abts.ef_list.insert(0, [inn_effects.full_moons_rise1])
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.type_word.append('Werewolf')
    card.cab.act.append(abts)

    card = card_dict['Heretic\'s Punishment']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,1,0,3]
    abts.rules_text = card.rules_text
    abts.sporab_target.append(effects.ta_creature_or_player)
    abts.ef_list.insert(0, [inn_effects.heretics_punishment])
    card.cab.act.append(abts)

    card = card_dict['Essence of the Wild']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.essence_of_the_wild]
    stab.rules_text = card.rules_text
    card.cab.other_static.append(stab)

    card = card_dict['Dearly Departed']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.dearly_departed]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Human')
    card.cab.grav_static.append(stab)

    card = card_dict['Boneyard Wurm']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.boneyard_wurm]
    stab.rules_text = card.rules_text
    card.cab.layer_static[6].append(stab)

    card = card_dict['Vampire Interloper']
    stab = classes.StaticAbil()
    stab.effect = [effects.cant_block]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)

    card = card_dict['Sturmgeist']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.sturmgeist]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[6].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.sturmgeist2]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)

    card = card_dict['Stony Silence']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.stony_silence]
    stab.rules_text = card.rules_text
    card.cab.other_static.append(stab)

    card = card_dict['Undead Alchemist']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.undead_alchemist0]
    stab.type_word.append('Zombie')
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.type_word.append('Zombie')
    stab.color_word.append('Black')
    stab.effect = [inn_effects.undead_alchemist1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Splinterfright']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.boneyard_wurm]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[6].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.splinterfright]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)

    card = card_dict['Dead Weight']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_plus, -2, -2]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Sensory Deprivation']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_plus, -3, 0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Ghostly Possession']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_keyword, 'Flying']
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[5].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [effects.attached_prevent_combat_damage]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.other_static.append(stab)

    card = card_dict['Furor of the Bitten']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.furor_of_the_bitten]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Skeletal Grimace']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.skeletal_grimace]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[5].append(stab)

    card = card_dict['Spectral Flight']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.spectral_flight]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[5].append(stab)

    card = card_dict['Claustrophobia']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.claustrophobia_0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.claustrophobia_1]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)

    card = card_dict['Curiosity']
    card.sporab_target.append(effects.ta_creature)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.curiosity]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Cloistered Youth']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.cloistered_youth]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Unholy Fiend']

    card = card_dict['Delver of Secrets']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.delver_of_secrets]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Insectile Aberration']

    card = card_dict['Insectile Aberration']
    card.other_face = card_dict['Delver of Secrets']
    card.color_indicator = ['Blue']

    card = card_dict['Unholy Fiend']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.unholy_fiend]
    card.color_indicator = ['Black']
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Cloistered Youth']

    card = card_dict['Bloodcrazed Neonate']
    stab = classes.StaticAbil()
    stab.effect = [effects.attacks_each_turn]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.slith]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Stromkirk Noble']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.slith]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.stromkirk_noble]
    stab.type_word.append('Human')
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)

    card = card_dict['Stromkirk Patrol']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.slith]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Hamlet Captain']
    stab = classes.StaticAbil()
    stab.type_word.append('Human')
    stab.rules_text = card.rules_text
    stab.effect = [inn_effects.hamlet_captain]
    card.cab.trig.append(stab)

    card = card_dict['Rakish Heir']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text
    stab.type_word.append('Vampire')
    stab.effect = [inn_effects.rakish_heir]
    card.cab.trig.append(stab)

    card = card_dict['Rage Thrower']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text
    stab.effect = [inn_effects.rage_thrower]
    card.cab.trig.append(stab)

    card = card_dict['Galvanic Juggernaut']
    stab = classes.StaticAbil()
    stab.effect = [effects.attacks_each_turn]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [effects.doesnt_untap]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.galvanic_juggernaut]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)

    card = card_dict['Grimgrin, Corpse-Born']
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()[0]
    repef.test = effects.ase_test_true
    repef.effect = [effects.ase_tapped]
    card.cab.as_enters.append(repef)
    stab = classes.StaticAbil()
    stab.effect = [effects.doesnt_untap]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)
    abts = classes.AbilToStack()
    cost = classes.Cost()
    cost.test = [inn_effects.test_grimgrin_corpse_born]
    cost.effect = [inn_effects.fun_grimgrin_corpse_born]
    abts.other_cost.append(cost)
    abts.ef_list.insert(0, [inn_effects.grimgrin_corpse_born0])
    abts.rules_text = card.rules_text.splitlines()[1]
    card.cab.act.append(abts)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.grimgrin_corpse_born1]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)

    card = card_dict['Olivia Voldaren']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,1,0,1]
    abts.sporab_target.append(effects.another_ta_creature)
    abts.type_word.append('Vampire')
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list.insert(0, [inn_effects.olivia_voldaren1])
    card.cab.act.append(abts)
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,2,0,0,3]
    abts.rules_text = card.rules_text.splitlines()[2]
    abts.type_word.append('Vampire')
    abts.ef_list.insert(0, [inn_effects.olivia_voldaren2])
    abts.sporab_target.append(effects.ta_creature_type)
    card.cab.act.append(abts)

    card = card_dict['One-Eyed Scarecrow']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.one_eyed_scarecrow]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Grimoire of the Dead']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,1]
    abts.other_cost.append(classes.Cost())
    abts.ef_list.insert(0, [effects.abil_obj_counter, 'Study', 1])
    cost = classes.Cost()
    cost.test = [effects.test_discard, 1]
    cost.effect = [effects.fun_discard, 1]
    abts.other_cost.append(cost)
    abts.rules_text = card.rules_text.splitlines()[0]
    card.cab.act.append(abts)
    
    abts = classes.AbilToStack()
    abts.other_cost.append(classes.Cost())
    cost = classes.Cost()
    cost.test = [effects.test_counter, 'Study', 3]
    cost.effect = [effects.fun_counter, 'Study', 3]
    abts.other_cost.append(cost)
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_sac_this]
    abts.other_cost.append(cost)
    abts.ef_list.insert(0, [inn_effects.grimoire_of_the_dead])
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.color_word.append('Black')
    abts.type_word.append('Zombie')
    card.cab.act.append(abts)
    
    card = card_dict['Endless Ranks of the Dead']
    stab = classes.StaticAbil()
    stab.type_word.append('Zombie')
    stab.color_word.append('Black')
    stab.effect = [inn_effects.endless_ranks_of_the_dead]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Armored Skaab']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.armored_skaab]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Reaper from the Abyss']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.reaper_from_the_abyss]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Demon')
    card.cab.trig.append(stab)

    card = card_dict['Orchard Spirit']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.orchard_spirit]
    stab.rules_text = card.rules_text
    card.cab.other_static.append(stab)

    card = card_dict['Parallel Lives']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.parallel_lives]
    stab.rules_text = card.rules_text
    card.cab.other_static.append(stab)

    card = card_dict['Village Cannibals']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.village_cannibals]
    stab.type_word.append('Human')
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Murder of Crows']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.murder_of_crows]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Mentor of the Meek']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.mentor_of_the_meek]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Woodland Sleuth']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.woodland_sleuth]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Morkrut Banshee']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.morkrut_banshee]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Kessig Cagebreakers']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.kessig_cagebreakers]
    stab.type_word.append('Wolf')
    stab.color_word.append('Green')
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Hollowhenge Scavenger']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.hollowhenge_scavenger]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Gutter Grime']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.gutter_grime]
    stab.rules_text = card.rules_text
    stab.color_word.append('Green')
    stab.type_word.append('Ooze')
    card.cab.trig.append(stab)

    card = card_dict['Ghoulraiser']
    stab = classes.StaticAbil()
    stab.type_word.append('Zombie')
    stab.effect = [inn_effects.ghoulraiser]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Geist-Honored Monk']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.geist_honored_monk0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[6].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.geist_honored_monk1]
    stab.color_word.append('White')
    stab.type_word.append('Spirit')
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)

    card = card_dict['Geist of Saint Traft']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.geist_of_saint_traft]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.color_word = ['White']
    stab.type_word = ['Angel']
    card.cab.trig.append(stab)

    card = card_dict['Falkenrath Noble']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.falkenrath_noble]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Moldgraf Monstrosity']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.moldgraf_monstrosity]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Lumberknot']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.lumberknot]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Fiend Hunter']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.fiend_hunter0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.trig.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.fiend_hunter1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Champion of the Parish']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.champion_of_the_parish]
    stab.rules_text = card.rules_text
    stab.type_word.append('Human')
    card.cab.trig.append(stab)

    card = card_dict['Creepy Doll']
    stab = classes.StaticAbil()
    stab.effect = [effects.self_indestructible]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.creepy_doll]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.trig.append(stab)

    card = card_dict['Bitterheart Witch']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.bitterheart_witch]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Bloodgift Demon']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.bloodgift_demon]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Charmbreaker Devils']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.charmbreaker_devils_0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.trig.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.charmbreaker_devils_1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    
    card = card_dict['Angel of Flight Alabaster']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.angel_of_flight_alabaster]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Spirit')
    card.cab.trig.append(stab)

    card = card_dict['Selhoff Occultist']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.selhoff_occultist]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Homicidal Brute']
    card.color_indicator = ['Red']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text
    stab.effect = [inn_effects.homicidal_brute]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Civilized Scholar']

    card = card_dict['Pitchburn Devils']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.pitchburn_devils]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Mayor of Avabruck']
    stab = classes.StaticAbil()
    stab.effect = [effects.lord_layer_static, 1, 1]
    stab.type_word.append('Human')
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[8].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Howlpack Alpha']

    card = card_dict['Instigator Gang']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.instigator_gang, 1, 0]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[8].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Wildblood Pack']

    card = card_dict['Intangible Virtue']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.intangible_virtue]
    stab.rules_text = card.rules_text
    card.cab.layer_static[5].append(stab)

    card = card_dict['Wildblood Pack']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.instigator_gang, 3, 0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Instigator Gang']

    card = card_dict['Howlpack Alpha']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.howlpack_alpha0]
    stab.type_word.append('Werewolf')
    stab.type_word.append('Wolf')
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.layer_static[8].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.howlpack_alpha1]
    stab.type_word.append('Wolf')
    stab.color_word.append('Green')
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Mayor of Avabruck']

    card = card_dict['Howlpack of Estwald']
    card.color_indicator.append('Green')
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Villagers of Estwald']

    card = card_dict['Rampaging Werewolf']
    card.color_indicator.append('Red')
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Tormented Pariah']

    card = card_dict['Tormented Pariah']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Rampaging Werewolf']

    card = card_dict['Kruin Outlaw']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Terror of Kruin Pass']

    card = card_dict['Terror of Kruin Pass']
    card.color_indicator.append('Red')
    stab = classes.StaticAbil()
    stab.type_word.append('Werewolf')
    stab.effect = [inn_effects.terror_of_kruin_pass]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Kruin Outlaw']

    card = card_dict['Ironfang']
    stab = classes.StaticAbil()
    card.color_indicator.append('Red')
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Village Ironsmith']

    card = card_dict['Village Ironsmith']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Ironfang']

    card = card_dict['Villagers of Estwald']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Howlpack of Estwald']

    card = card_dict['Ulvenwald Mystics']
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text
    stab.effect = [inn_effects.werewolf_0]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Ulvenwald Primordials']

    card = card_dict['Ulvenwald Primordials']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,1,0]
    abts.ef_list.insert(0, [effects.abil_obj_regenerate])
    abts.rules_text = card.rules_text.splitlines()[0]
    card.cab.act.append(abts)

    card = card_dict['Hanweir Watchkeep']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Bane of Hanweir']

    card = card_dict['Grizzled Outcasts']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Krallenhorde Wantons']

    card = card_dict['Reckless Waif']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_0]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.other_face = card_dict['Merciless Predator']

    card = card_dict['Merciless Predator']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.color_indicator.append('Red')
    card.other_face = card_dict['Reckless Waif']
    
    card = card_dict['Krallenhorde Wantons']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.color_indicator.append('Green')
    card.other_face = card_dict['Grizzled Outcasts']

    card = card_dict['Bane of Hanweir']
    stab = classes.StaticAbil()
    stab.effect = [effects.attacks_each_turn]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.werewolf_1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.color_indicator.append('Red')
    card.other_face = card_dict['Hanweir Watchkeep']

    card = card_dict['Ashmouth Hound']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.ashmouth_hound]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Unruly Mob']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.unruly_mob]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Burning Vengeance']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.burning_vengeance]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Balefire Dragon']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.balefire_dragon]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    
    card = card_dict['Geistcatcher\'s Rig']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.geistcatchers_rig]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Crossway Vampire']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.crossway_vampire]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Heartless Summoning']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.heartless_summoning]
    stab.rules_text = card.rules_text.splitlines()[0]
    card.cab.other_static.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [effects.anthem, -1, -1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Thraben Sentry']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.thraben_sentry]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    card.other_face = card_dict['Thraben Militia']

    card = card_dict['Thraben Militia']
    card.other_face = card_dict['Thraben Sentry']
    card.color_indicator.append('White')

    card = card_dict['Village Bell-Ringer']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.village_bellringer]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Doomed Traveler']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.doomed_traveler]
    stab.color_word.append('White')
    stab.type_word.append('Spirit')
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Mausoleum Guard']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.mausoleum_guard]
    stab.color_word.append('White')
    stab.type_word.append('Spirit')
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)   

    card = card_dict['Elder Cathar']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.elder_cathar]
    stab.type_word.append('Human')
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Abattoir Ghoul']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.abattoir_ghoul]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Altar\'s Reap']
    card.ef_list.insert(0, [effects.draw_cont_cards, 2])
    cost = classes.Cost()
    cost.test = [effects.test_sac_creat]
    cost.effect = [effects.fun_sac_creat]
    card.other_cost.append(cost)

    card = card_dict['Infernal Plunge']
    cost = classes.Cost()
    cost.test = [effects.test_sac_creat]
    cost.effect = [effects.fun_sac_creat]
    card.other_cost.append(cost)
    card.ef_list.insert(0, [effects.spell_mana, [0,0,0,3,0,0]])

    card = card_dict['Dream Twist']
    card.sporab_target.append(effects.ta_player)
    card.ef_list.insert(0, [effects.targeted_mill, 3])

    card = card_dict['Feeling of Dread']
    card.sporab_target.append(effects.ta_up_to_creat)
    card.sporab_target.append(effects.ta_up_to_creat)
    card.ef_list.insert(0, [inn_effects.feeling_of_dread])

    card = card_dict['Naturalize']
    card.sporab_target.append(effects.ta_artifact_or_enchantment)
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Past in Flames']
    card.ef_list.insert(0, [inn_effects.past_in_flames])

    card = card_dict['Sever the Bloodline']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [inn_effects.sever_the_bloodline])

    card = card_dict['Purify the Grave']
    card.sporab_target.append(effects.ta_card_in_gy)
    card.ef_list.insert(0, [effects.targeted_exile_from_gy])

    card = card_dict['Bramblecrush']
    card.sporab_target.append(effects.ta_noncreature_permanent)
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Prey Upon']
    card.sporab_target.append(effects.ta_creature_you_control)
    card.sporab_target.append(effects.ta_creature_opponent_controls)
    card.ef_list.insert(0, [inn_effects.prey_upon])

    card = card_dict['Rolling Temblor']
    card.ef_list.insert(0, [inn_effects.rolling_temblor])

    card = card_dict['Rooftop Storm']
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.rooftop_storm]
    stab.rules_text = card.rules_text
    stab.type_word.append('Zombie')
    card.cab.other_static.append(stab)

    card = card_dict['Silent Departure']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [effects.return_target_to_hand])

    card = card_dict['Ancient Grudge']
    card.ef_list.insert(0, [effects.targeted_destroy])
    card.sporab_target.append(effects.ta_artifact)

    card = card_dict['Moan of the Unhallowed']
    card.type_word.append('Zombie')
    card.color_word.append('Black')
    card.ef_list.insert(0, [effects.sporab_tokens, 2, 2, 2])

    card = card_dict['Rebuke']
    card.ef_list.insert(0, [effects.targeted_destroy])
    card.sporab_target.append(effects.ta_attacking_creat)

    card = card_dict['Vampiric Fury']
    card.ef_list.insert(0, [inn_effects.vampiric_fury])
    card.type_word.append('Vampire')

    card = card_dict['Tribute to Hunger']
    card.ef_list.insert(0, [inn_effects.tribute_to_hunger])
    card.sporab_target.append(effects.ta_opponent)

    card = card_dict['Mulch']
    card.ef_list.insert(0, [inn_effects.mulch])

    card = card_dict['Rally the Peasants']
    card.ef_list.insert(0, [inn_effects.rally_the_peasants])

    card = card_dict['Moonmist']
    card.ef_list.insert(0, [inn_effects.moonmist])
    card.type_word.extend(['Human', 'Werewolf', 'Wolf'])

    card = card_dict['Cackling Counterpart']
    card.ef_list.insert(0, [effects.targeted_token_copy])
    card.sporab_target.append(effects.ta_creature_you_control)

    card = card_dict['Moment of Heroism']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [effects.targeted_creature_plus, 2,2])
    card.ef_list.insert(0, [effects.targeted_creature_keyword, 'Lifelink'])

    card = card_dict['Spidery Grasp']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [inn_effects.spidery_grasp])

    card = card_dict['Spider Spawning']
    card.type_word.append('Spider')
    card.color_word.append('Green')
    card.ef_list.insert(0, [inn_effects.spider_spawning])

    card = card_dict['Unburial Rites']
    card.sporab_target.append(effects.ta_creat_in_cont_gy)
    card.ef_list.insert(0, [effects.targeted_gy_to_bf])

    card = card_dict['Ranger\'s Guile']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [effects.targeted_creature_plus, 1,1])
    card.ef_list.insert(0, [effects.targeted_creature_keyword, 'Hexproof'])

    card = card_dict['Makeshift Mauler']
    cost = classes.Cost()
    cost.test = [inn_effects.test_exile_creat_from_gy]
    cost.effect = [inn_effects.fun_exile_creat_from_gy]
    card.other_cost.append(cost)

    card = card_dict['Stitched Drake']
    cost = classes.Cost()
    cost.test = [inn_effects.test_exile_creat_from_gy]
    cost.effect = [inn_effects.fun_exile_creat_from_gy]
    card.other_cost.append(cost)

    card = card_dict['Skaab Goliath']
    cost = classes.Cost()
    cost.test = [inn_effects.test_skaab_goliath]
    cost.effect = [inn_effects.fun_skaab_goliath]
    card.other_cost.append(cost)

    card = card_dict['Skaab Ruinator']
    cost = classes.Cost()
    cost.test = [inn_effects.test_skaab_ruinator]
    cost.effect = [inn_effects.fun_skaab_ruinator]
    card.other_cost.append(cost)
    stab = classes.StaticAbil()
    stab.effect = [inn_effects.skaab_ruinator]
    stab.rules_text = card.rules_text.splitlines()[2]
    card.cab.grav_static.append(stab)

    card = card_dict['Corpse Lunge']
    card.ef_list.insert(0, [inn_effects.corpse_lunge])
    card.sporab_target.append(effects.ta_creature)
    cost = classes.Cost()
    cost.test = [inn_effects.test_exile_creat_from_gy]
    cost.effect = [inn_effects.fun_exile_creat_from_gy]
    card.other_cost.append(cost)

    card = card_dict['Invisible Stalker']
    stab = classes.StaticAbil()
    stab.effect = [effects.unblockable]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.other_static.append(stab)

    card = card_dict['Brimstone Volley']
    card.ef_list.insert(0, [inn_effects.brimstone_volley])
    card.sporab_target.append(effects.ta_creature_or_player)

    card = card_dict['Traitorous Blood']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [inn_effects.traitorous_blood])

    card = card_dict['Into the Maw of Hell']
    card.ef_list.insert(0, [inn_effects.into_the_maw_of_hell])
    card.sporab_target.extend([effects.ta_land, effects.ta_creature])

    card = card_dict['Bump in the Night']
    card.ef_list.insert(0, [effects.targeted_life_change, -3])
    card.sporab_target.append(effects.ta_opponent)

    card = card_dict['Devil\'s Play']
    card.cast_choice.append(effects.choose_x)
    card.ef_list.insert(0, [effects.targeted_damage, 0])
    card.sporab_target.append(effects.ta_creature_or_player)

    card = card_dict['Nightbird\'s Clutches']
    card.sporab_target.append(effects.ta_up_to_creat)
    card.sporab_target.append(effects.ta_up_to_creat)
    card.ef_list.insert(0, [inn_effects.nightbirds_clutches])

    card = card_dict['Travel Preparations']
    card.sporab_target.append(effects.ta_up_to_creat)
    card.sporab_target.append(effects.ta_up_to_creat)
    card.ef_list.insert(0, [inn_effects.travel_preparations])
    

    card = card_dict['Harvest Pyre']
    card.cast_choice.append(inn_effects.choose_harvest_pyre)
    card.sporab_target.append(effects.ta_creature)
    cost = classes.Cost()
    cost.test = [inn_effects.test_exile_cards_from_gy, 0]
    cost.effect = [inn_effects.fun_exile_cards_from_gy, 0]
    card.other_cost.append(cost)
    card.ef_list.insert(0,[effects.targeted_damage, 0])

    card = card_dict['Dissipate']
    card.sporab_target.append(effects.ta_spell)
    card.ef_list.insert(0, [inn_effects.dissipate])

    card = card_dict['Midnight Haunting']
    card.type_word.append('Spirit')
    card.color_word.append('White')
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    card.ef_list.append([effects.sporab_tokens, 2, 1, 1, cab])

    card = card_dict['Grasp of Phantoms']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [effects.targeted_battlefield_to_top_of_library])

    card = card_dict['Victim of Night']
    card.sporab_target.append(inn_effects.ta_victim_of_night)
    card.type_word.extend(['Vampire', 'Werewolf', 'Zombie'])
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Maw of the Mire']
    card.sporab_target.append(effects.ta_land)
    card.ef_list.insert(0, [inn_effects.maw_of_the_mire])

    card = card_dict['Caravan Vigil']
    card.ef_list.insert(0, [inn_effects.caravan_vigil])

    card = card_dict['Divine Reckoning']
    card.ef_list.insert(0, [inn_effects.divine_reckoning])

    card = card_dict['Memory\'s Journey']
    card.sporab_target.append(effects.ta_player)
    for i in range(3):
        card.sporab_target.append(inn_effects.ta_memorys_journey)
    card.ef_list.insert(0, [inn_effects.memorys_journey])

    card = card_dict['Night Terrors']
    card.sporab_target.append(effects.ta_player)
    card.ef_list.insert(0, [inn_effects.night_terrors])

    card = card_dict['Desperate Ravings']
    card.ef_list.insert(0, [inn_effects.desperate_ravings])

    card = card_dict['Nevermore']
    repef = classes.ReplacementEffect()
    repef.test = effects.ase_test_true
    repef.effect = [inn_effects.ase_nevermore]
    repef.name = card.rules_text.splitlines()[0]
    card.cab.as_enters.append(repef)
    stab = classes.StaticAbil()
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.effect = [inn_effects.nevermore]
    card.cab.other_static.append(stab)

    card = card_dict['Gnaw to the Bone']
    card.ef_list.insert(0, [inn_effects.gnaw_to_the_bone])

    card = card_dict['Creeping Renaissance']
    card.ef_list.insert(0, [inn_effects.creeping_renaissance])

    card = card_dict['Forbidden Alchemy']
    card.ef_list.insert(0, [inn_effects.forbidden_alchemy])

    card = card_dict['Frightful Delusion']
    card.sporab_target.append(effects.ta_spell)
    card.ef_list.insert(0, [inn_effects.frightful_delusion])

    card = card_dict['Geistflame']
    card.sporab_target.append(effects.ta_creature_or_player)
    card.ef_list.insert(0, [effects.targeted_damage, 1])

    card = card_dict['Smite the Monstrous']
    card.sporab_target.append(inn_effects.ta_smite_the_monstrous)
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Think Twice']
    card.ef_list.insert(0, [effects.draw_cont_cards, 1])

    card = card_dict['Army of the Damned']
    card.ef_list.insert(0, [inn_effects.army_of_the_damned])
    card.type_word.append('Zombie')
    card.color_word.append('Black')

    card = card_dict['Blasphemous Act']
    card.cost_red.append([inn_effects.cost_red_blasphemous_act])
    card.ef_list.insert(0, [inn_effects.blasphemous_act])

    card = card_dict['Runic Repetition']
    card.sporab_target.append(inn_effects.ta_runic_repetition)
    card.ef_list.insert(0, [inn_effects.runic_repetition])

    card = card_dict['Lost in the Mist']
    card.sporab_target.append(effects.ta_spell)
    card.sporab_target.append(effects.ta_permanent)
    card.ef_list.insert(0, [effects.targeted_counterspell])
    card.ef_list.insert(1, [inn_effects.lost_in_the_mist])

    card = card_dict['Urgent Exorcism']
    card.sporab_target.append(inn_effects.ta_urgent_exorcism)
    card.type_word.append('Spirit')
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Spare from Evil']
    card.ef_list.insert(0, [inn_effects.spare_from_evil])

    card = card_dict['Make a Wish']
    card.ef_list.insert(0, [inn_effects.make_a_wish])

    card = card_dict['Hysterical Blindness']
    card.ef_list.insert(0, [inn_effects.hysterical_blindness])

    card = card_dict['Paraselene']
    card.ef_list.insert(0, [inn_effects.paraselene])

    card = card_dict['Ghoulcaller\'s Chant']
    card.cast_choice.append(inn_effects.choose_ghoulcallers_chant)
    card.type_word.append('Zombie')
    card.ef_list.insert(0, [effects.targeted_gy_to_hand])
    card.ef_list.insert(1, [inn_effects.ghoulcallers_chant])

    card = card_dict['Festerhide Boar']
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()[1]
    repef.test = inn_effects.ase_test_morbid
    repef.effect = [effects.enters_with_counter, '+1/+1', 2]
    card.cab.as_enters.append(repef)

    card = card_dict['Somberwald Spider']
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()[1]
    repef.test = inn_effects.ase_test_morbid
    repef.effect = [effects.enters_with_counter, '+1/+1', 2]
    card.cab.as_enters.append(repef)

    card = card_dict['Skirsdag High Priest']
    abts = classes.AbilToStack()
    abts.rules_text = card.rules_text
    abts.other_cost.append(classes.Cost())
    cost = classes.Cost()
    cost.test = [inn_effects.test_skirsdag_high_priest]
    cost.effect = [inn_effects.fun_skirsdag_high_priest]
    abts.other_cost.append(cost)
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    abts.type_word.append('Demon')
    abts.color_word.append('Black')
    abts.ef_list.insert(0, [effects.sporab_tokens, 1, 5, 5, cab])
    abts.timing.append(inn_effects.tim_morbid)
    card.cab.act.append(abts)

    card = card_dict['Evil Twin']
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text
    repef.test = effects.ase_test_true
    repef.effect = [inn_effects.ase_evil_twin]
    card.cab.as_enters.append(repef)

    card = card_dict['Diregraf Ghoul']
    repef = classes.ReplacementEffect()
    repef.name = card.rules_text.splitlines()
    repef.test = effects.ase_test_true
    repef.effect = [effects.ase_tapped]
    card.cab.as_enters.append(repef)

    return card_dict

def deckImport(deckFile):
    f = open(deckFile)
    line = f.readline()
    deck = []
    while line != '':
        line = line.rstrip().lstrip()
        if line[0].isdigit():
            for j in range(int(line[:line.index(' ')])):
                deck.append(line[line.index(' ')+1:])
        elif line!='' and line[0]!='/': deck.append(line)
        line = f.readline()
    return deck

