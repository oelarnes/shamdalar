

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
                      'Reach', 'Deathtouch', 'Protection',
                      'Islandwalk', 'Swampwalk', 'Defender')

import effects
import copy
import m12_effects
import classes
    
def initCardList(card_set):
    f = open('cardList.txt')
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
    
    card = card_dict['Angel\'s Mercy']
    card.ef_list.insert(0, [effects.change_cont_life, 7])

    card = card_dict['Bountiful Harvest']
    card.ef_list.insert(0, [m12_effects.bountiful_harvest])

    card = card_dict['Cancel']
    card.sporab_target.append(effects.ta_spell)
    card.ef_list.insert(0, [effects.targeted_counterspell])

    card = card_dict['Negate']
    card.sporab_target.append(effects.ta_noncreature_spell)
    card.ef_list.insert(0, [effects.targeted_counterspell])

    card = card_dict['Celestial Purge']
    card.color_word.extend(['Black', 'Red'])
    card.sporab_target.append(m12_effects.ta_celestial_purge)
    card.ef_list.insert(0, [effects.targeted_exile])

    card = card_dict['Day of Judgment']
    card.ef_list.insert(0, [m12_effects.day_of_judgment])

    card = card_dict['Demystify']
    card.sporab_target.append(effects.ta_enchantment)
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Plummet']
    card.sporab_target.append(effects.ta_flying)
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Naturalize']
    card.sporab_target.append(m12_effects.ta_naturalize)
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Diabolic Tutor']
    card.ef_list.insert(0, [m12_effects.diabolic_tutor])

    card = card_dict['Disentomb']
    card.sporab_target.append(m12_effects.ta_disentomb)
    card.ef_list.insert(0, [effects.targeted_gy_to_hand])
    
    card = card_dict['Divination']
    card.ef_list.insert(0, [effects.draw_cont_cards, 2])

    card = card_dict['Doom Blade']
    card.color_word.append('Black')
    card.sporab_target.append(effects.ta_non_color_creature)
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Chandra\'s Outrage']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [m12_effects.chandras_outrage])

    card = card_dict['Flashfreeze']
    card.color_word.extend(['Red', 'Green'])
    card.sporab_target.append(m12_effects.ta_flashfreeze)
    card.ef_list.insert(0, [effects.targeted_counterspell])

    card = card_dict['Deathmark']
    card.color_word.extend(['White', 'Green'])
    card.sporab_target.append(m12_effects.ta_deathmark)
    card.ef_list.insert(0, [effects.targeted_destroy])

    card = card_dict['Archon of Justice']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.archon_of_justice]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    
    card = card_dict['Goblin Arsonist']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.goblin_arsonist]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    
    card = card_dict['Gravedigger']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.gravedigger]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Stingerfling Spider']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.stingerfling_spider]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Chasm Drake']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.chasm_drake]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Circle of Flame']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.circle_of_flame]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Auramancer']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.auramancer]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Chandra\'s Phoenix']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.chandras_phoenix]
    stab.rules_text = card.rules_text.splitlines()[2]
    stab.color_word = ['Red']
    card.cab.trig_grav.append(stab)

    card = card_dict['Belltower Sphinx']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.belltower_sphinx]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Aegis Angel']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.aegis_angel]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Blood Seeker']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.blood_seeker]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Grave Titan']
    stab = classes.StaticAbil()
    stab.color_word = ['Black']
    stab.type_word = ['Zombie']
    stab.effect = [m12_effects.grave_titan]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Benalish Veteran']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.benalish_veteran]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Manabarbs']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.manabarbs]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Angel\'s Feather']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.angels_feather]
    stab.rules_text = card.rules_text
    stab.color_word.append('White')
    card.cab.trig.append(stab)

    card = card_dict['Kraken\'s Eye']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.angels_feather]
    stab.rules_text = card.rules_text
    stab.color_word.append('Blue')
    card.cab.trig.append(stab)

    card = card_dict['Demon\'s Horn']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.angels_feather]
    stab.rules_text = card.rules_text
    stab.color_word.append('Black')
    card.cab.trig.append(stab)

    card = card_dict['Dragon\'s Claw']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.angels_feather]
    stab.rules_text = card.rules_text
    stab.color_word.append('Red')
    card.cab.trig.append(stab)

    card = card_dict['Wurm\'s Tooth']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.angels_feather]
    stab.rules_text = card.rules_text
    stab.color_word.append('Green')
    card.cab.trig.append(stab)

    card = card_dict['Aether Adept']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.aether_adept]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)
    card.ref_name = 'Aether Adept'

    card = card_dict['Call to the Grave']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.call_to_the_grave_0]
    stab.rules_text = card.rules_text.splitlines()[0]
    stab.type_word = ['Zombie']
    card.cab.trig.append(stab)
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.call_to_the_grave_1]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Acidic Slime']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.acidic_slime]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Manic Vandal']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.manic_vandal]
    card.cab.trig.append(stab)

    card = card_dict['Bloodlord of Vaasgoth']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.bloodlord_of_vaasgoth]
    stab.rules_text = card.rules_text.splitlines()[2]
    stab.type_word = ['Vampire']
    card.cab.trig.append(stab)

    card = card_dict['Act of Treason']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [m12_effects.act_of_treason])

    card = card_dict['Autumn\'s Veil']
    card.ef_list.insert(0, [m12_effects.autumns_veil])

    card = card_dict['Guardians\' Pledge']
    card.color_word.append('White')
    card.ef_list.insert(0, [m12_effects.guardians_pledge])

    card = card_dict['Honor of the Pure']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.honor_of_the_pure]
    stab.rules_text = card.rules_text
    stab.color_word.append('White')
    card.cab.layer_static[8].append(stab)

    card = card_dict['Levitation']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.levitation]
    stab.rules_text = card.rules_text
    card.cab.layer_static[5].append(stab)

    card = card_dict['Lava Axe']
    card.sporab_target.append(effects.ta_player)
    card.ef_list.insert(0, [effects.targeted_damage, 5])

    card = card_dict['Reclaim']
    card.sporab_target.append(effects.ta_card_in_cont_gy)
    card.ef_list.insert(0, [m12_effects.reclaim])

    card = card_dict['Timely Reinforcements']
    card.color_word.append('White')
    card.type_word.append('Soldier')
    card.ef_list.insert(0, [m12_effects.timely_reinforcements])

    card = card_dict['Titanic Growth']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [effects.targeted_creature_plus, 4,4])

    card = card_dict['Overrun']
    card.ef_list.insert(0, [m12_effects.overrun])
    
    card = card_dict['Wring Flesh']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [effects.targeted_creature_plus, -3,-1])

    card = card_dict['Stave Off']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [m12_effects.stave_off])

    card = card_dict['Fog']
    card.ef_list.insert(0, [m12_effects.fog])
                           
    card = card_dict['Sphinx of Uthuun']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.sphinx_of_uthuun]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Crumbling Colossus']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.crumbling_colossus]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)
    
    card = card_dict['Mighty Leap']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [effects.targeted_creature_plus, 2,2])
    card.ef_list.insert(0, [effects.targeted_creature_keyword, 'Flying'])

    card = card_dict['Distress']
    card.sporab_target.append(effects.ta_player)
    card.ef_list.insert(0, [m12_effects.distress])
    
    card = card_dict['Slaughter Cry']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [effects.targeted_creature_plus, 3, 0])
    card.ef_list.insert(0, [effects.targeted_creature_keyword,\
                           'First strike'])

    card = card_dict['Turn to Frog']
    card.sporab_target.append(effects.ta_creature)
    card.ef_list.insert(0, [m12_effects.turn_to_frog])
    card.type_word.append('Frog')
    card.color_word.append('Blue')

    card = card_dict['Frost Breath']
    for i in (1,2):
        card.sporab_target.append(m12_effects.ta_frost_breath)
    card.ef_list.insert(0, [m12_effects.frost_breath])

    card = card_dict['Fireball']
    for i in range(200):
        card.sporab_target.append(m12_effects.ta_fireball)
    card.cast_choice.append(effects.choose_x)
    card.other_cost.append([effects.test_true, m12_effects.fun_fireball])
    card.ef_list.insert(0, [m12_effects.fireball, 0])

    card = card_dict['Adaptive Automaton']
    card.as_enters.append([m12_effects.adaptive_automaton_as_enters])
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.adaptive_automaton]
    card.cab.layer_static[3].append(stab)
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.lord_layer_static]
    card.cab.layer_static[8].append(stab)

    card = card_dict['Llanowar Elves']
    abts = classes.AbilToStack()
    abts.other_cost = [[effects.test_tap, effects.fun_tap]]
    abts.ef_list = [effects.tap_for_mana]
    abts.rules_text = card.rules_text
    abts.would_produce = [0,0,0,0,1,0]
    card.cab.act_mana.append(abts)

    card = card_dict['Merfolk Looter']
    abts = classes.AbilToStack()
    abts.other_cost = [[effects.test_tap, effects.fun_tap]]
    abts.ef_list = [[m12_effects.merfolk_looter]]
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)

    card = card_dict['Azure Mage']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,1,0,0,0,3]
    abts.rules_text = card.rules_text
    abts.ef_list = [[effects.draw_cont_cards, 1]]
    card.cab.act.append(abts)

    card = card_dict['Brindle Boar']
    abts = classes.AbilToStack()
    abts.other_cost = [[effects.test_true, effects.fun_sac_this]]
    abts.ef_list = [[effects.change_cont_life, 4]]
    abts.rules_text = card.rules_text
    card.cab.act.append(abts)

    card = card_dict['Buried Ruin']
    abts = classes.AbilToStack()
    abts.other_cost = [[effects.test_tap, effects.fun_tap]]
    abts.ef_list = [[effects.tap_for_mana]]
    abts.rules_text = card.rules_text.splitlines()[0]
    abts.would_produce = [0,0,0,0,0,1]
    card.cab.act_mana.append(abts)
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,0,2]
    abts.other_cost = [[effects.test_tap, effects.fun_tap]]
    abts.rules_text = card.rules_text.splitlines()[1]
    abts.ef_list = [[effects.targeted_gy_to_hand]]
    abts.sporab_target = [m12_effects.ta_buried_ruin]
    card.cab.act.append(abts)

    card = card_dict['Onyx Mage']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,1,0,0,1]
    abts.rules_text = card.rules_text
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.ef_list = [[effects.targeted_creature_keyword, 'Deathtouch']]
    card.cab.act.append(abts)

    card = card_dict['Alabaster Mage']
    abts = classes.AbilToStack()
    abts.mana_cost = [1,0,0,0,0,1]
    abts.rules_text = card.rules_text
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.ef_list = [[effects.targeted_creature_keyword, 'Lifelink']]
    card.cab.act.append(abts)

    card = card_dict['Crimson Mage']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,1,0,0]
    abts.rules_text = card.rules_text
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.ef_list = [[effects.targeted_creature_keyword, 'Haste']]
    card.cab.act.append(abts)

    card = card_dict['Cudgel Troll']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,1,0]
    abts.rules_text = card.rules_text
    abts.ef_list = [[effects.self_regen_shield]]
    card.cab.act.append(abts)
    
    card = card_dict['Jade Mage']
    abts = classes.AbilToStack()
    abts.mana_cost = [0,0,0,0,1,2]
    abts.rules_text = card.rules_text
    abts.ef_list = [[effects.sporab_token, 'Green', 'Saproling', 1,1]]
    card.cab.act.append(abts)

    card = card_dict['Dungrove Elder']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.dungrove_elder]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.layer_static[6].append(stab)

    card = card_dict['Elvish Archdruid']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.lord_layer_static]
    stab.rules_text = card.rules_text.splitlines()[0]
    stab.type_word.append('Elf')
    card.cab.layer_static[8].append(stab)

    card = card_dict['Goblin Chieftain']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.goblin_chieftain]
    stab.rules_text = card.rules_text.splitlines()[1]
    stab.type_word.append('Goblin')
    card.cab.layer_static[5].append(stab)
    card.dependencies[5].extend(['Turn to Frog', 'Humility'])
    
    card = card_dict['Lord of the Unreal']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.lord_of_the_unreal]
    stab.rules_text = card.rules_text.splitlines()[0]
    stab.type_word.append('Illusion')
    card.cab.layer_static[5].append(stab)
    card.dependencies[5].extend(['Turn to Frog', 'Humility'])

    card = card_dict['Phantasmal Bear']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.illusion]
    stab.rules_text = card.rules_text
    card.cab.trig.append(stab)

    card = card_dict['Phantasmal Dragon']
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.illusion]
    stab.rules_text = card.rules_text.splitlines()[1]
    card.cab.trig.append(stab)

    card = card_dict['Phantasmal Image']
    card.as_enters.append([m12_effects.phantasmal_image_as_enters])
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.phantasmal_image]
    stab.type_word.append('Illusion')
    card.cab.layer_static[0].append(stab)
    
##    
##    card = card_dict['Cemetery Reaper']
##    card.cab.layer_static[8].append([m12_effects.la_8_zombie_lord])
##    
##    card = card_dict['Adaptive Automaton']
##    card.cab.layer_static[8].append([m12_effects.la_8_robot_lord])

    card = card_dict['Shock']
    card.sporab_target.append(effects.ta_creature_or_player)
    card.ef_list.insert(0, [effects.targeted_damage, 2])

    card = card_dict['Combust']
    card.color_word.extend(['White', 'Blue'])
    card.sporab_target.append(m12_effects.ta_combust)
    card.ef_list.insert(0, [effects.targeted_damage, 5])

    data = classes.Data()
    data.name = 'Humility'
    data.mana_cost_str = '2WW'
    data.mana_cost = [2,0,0,0,0,2]
    data.set = 'Tempest'
    data.oracle = ''
    data.rarity = 'Rare'
    data.color = ['White']
    data.type_str = 'Enchantment'
    data.type_ = 'Enchantment'
    data.sup_type = ''
    data.sub_type = ''
    data.real = True
    data.rules_text = ''
    data.power = None
    data.toughness = None
    data.loyalty = None
    cab = classes.CardAbilities()
    data.cab = cab
    card = classes.Card(data)
    stab = classes.StaticAbil()
    stab.effect = [m12_effects.humility_layer_static]
    stab.rules_text = card.rules_text
    card.cab.layer_static[5].append(stab)
    card.dependencies[5].append('Turn to Frog')
    card_dict['Humility'] = card

    for card_name in card_dict:
        card = card_dict[card_name]
        abil_part = []
        if 'Creature' in card.type_:
            next_part = card.rules_text.partition('\n')
            while next_part[0]!='':
                for word in CREAT_KEYWORD_LIST:
                    if word in next_part[0][:len(word)+2]:
                        if '(' in next_part[0]:
                            card.cab.keyword.append(
                                    next_part[0][:next_part[0].index('(')].rstrip())
                        else:
                            card.cab.keyword.append(next_part[0].rstrip())
                next_part = next_part[2].partition('\n')
        bloodthirst = ['Bloodthirst' in word for word in card.cab.keyword]
        if any(bloodthirst):
           card.as_enters.append([m12_effects.bloodthirst,\
               int(card.cab.keyword[bloodthirst.index(True)][12])])
    
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

