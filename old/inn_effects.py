import copy
import effects
import random
import output
import classes

PERM_TYPES = ['Creature', 'Enchantment', 'Planeswalker', 'Artifact']

#Effects

def fight(game, creature1, creature2):
    damage1 = effects.damage(game, creature1, creature2, creature1.power)
    damage2 = effects.damage(game, creature2, creature1, creature2.power)
    return [[creature1, creature2, damage1, False],
            [creature2, creature1, damage2, False]]

#Spell effects:

def spider_spawning(game, spell):
    creats = [card for card in spell.controller.graveyard if 'Creature'\
              in card.type_]
    cab = classes.CardAbilities()
    cab.keyword.append('Reach')
    effects.sporab_tokens(game, spell, len(creats), 1, 2, cab)

def spidery_grasp(game, spell):
    effects.untap(game, spell.target[0])
    effects.targeted_creature_plus(game, spell, 2, 4)
    effects.targeted_creature_keyword(game, spell, 'Reach')

def undead_alchemist_ef(game, spell):
    card = spell.ref_obj[0]
    if card in card.owner.graveyard:
        card.owner.graveyard.remove(card)
        card = effects.card_copy(card.base, card.owner)
        game.exile.append(card)
        game.update_battlefield()
    effects.sporab_tokens(game, spell, 1, 2, 2)

def sever_the_bloodline(game, spell):
    destroy_list = []
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm.name == spell.target[0].name:
            destroy_list.append(perm)
    effects.destroy_list(game, destroy_list)

def runic_repetition(game, spell):
    game.exile.remove(spell.target[0])
    spell.controller.hand.append(spell.target[0])
    output.output(game, spell.controller, spell.target[0].name+\
                  ' went to '+spell.controller.name+'\'s hand')
    game.update_battlefield()

def prey_upon(game, spell):
    pair = fight(game, spell.target[0], spell.target[1])
    game.update_battlefield()
    for item in pair:
        if item[2]!=None:
            game.add_to_tst([item, 'dealt_damage'])

def past_in_flames(game, spell):
    card_list = [card for card in spell.controller.graveyard if 'Instant' \
                 in card.type_ or \
                 'Sorcery' in card.type_]
    rule = classes.SporabRule(spell, game.layer[5])
    rule.effect = [la_5_past_in_flames, card_list]
    game.update_battlefield()

def traitorous_blood(game, spell):
    rule = classes.SporabRule(spell, game.layer[1])
    rule.effect = [effects.la_1_change_control]
    game.update_battlefield()
    effects.untap(game, spell.target[0])
    game.update_battlefield()
    rule = classes.SporabRule(spell, game.layer[5])
    rule.effect = [effects.la_5_ta_gains_keyword, 'Haste']
    rule = classes.SporabRule(spell, game.layer[5])
    rule.effect = [effects.la_5_ta_gains_keyword, 'Trample']
    game.update_battlefield()

def snapcaster_mage_ef(game, spell):
    rule = classes.SporabRule(spell, game.layer[5])
    rule.effect = [la_5_snapcaster_mage]
    game.update_battlefield()
    
def army_of_the_damned(game, spell):
    rule = classes.ReplacementEffect()
    rule.cleanup = effects.bf_update
    rule.name = 'This creature enters the battlefield tapped'
    rule.test = effects.ase_test_creature
    rule.effect = [effects.ase_tapped]
    rule.location = game.rule_as_enters
    rule.location.append(rule)
    effects.make_tokens(game, spell.controller, 13, spell.color_word,\
                           spell.type_word[0], 2, 2)

def rakish_heir_ef(game, spell):
    effects.add_counter(game, spell.ref_obj[0][0], '+1/+1', 1)
    game.update_battlefield()

def into_the_maw_of_hell(game, spell):
    if spell.target[0] in game.battlefield:
        effects.targeted_destroy(game, spell)
    amount = None
    if spell.target[1] in game.battlefield:
        amount = effects.damage(game, spell, spell.target[1], 13)
    game.update_battlefield()
    if amount!=None:
        game.add_to_tst([[spell, spell.target[1], amount, False],
                         'dealt_damage'])

def vampiric_fury(game, spell):
    creat_list = [perm for perm in game.battlefield if spell.type_word[0] in\
                  perm.sub_type and 'Creature' in perm.type_]
    rule = classes.SporabRule(spell, game.layer[8])
    rule.effect= [effects.la_8_creat_list_plus, creat_list, 2, 0]
    rule = classes.SporabRule(spell, game.layer[5])
    rule.effect = [effects.la_5_creat_list_keyword, creat_list, 'First strike']
    game.update_battlefield()
    
def moonmist(game, spell):
    for perm in game.battlefield:
        if spell.type_word[0] in perm.sub_type and 'Creature' in perm.type_:
            transform_ef(game, perm)
    game.update_battlefield()
    rule = classes.SporabRule(spell, game.rule_damage)
    rule.effect = [r_damage_moonmist]

def tribute_to_hunger(game, spell):
   if  effects.fun_sac_creat(game, spell.target[0], spell):
       effects.change_cont_life(game, spell, spell.ref_obj[0].toughness)

def transform_ef(game, perm):
    if perm.card.other_face!=None:
        print perm.base.name,
        if not perm.other_face_up:
            perm.other_face_up = True
            perm.base = classes.PermBase(perm.card.other_face)
        else:
            perm.other_face_up = False
            perm.base = classes.PermBase(perm.card)
        print 'transformed into '+perm.base.name

def transform(game, sporab):
    perm = sporab.obj
    transform_ef(game, perm)
    game.update_battlefield()

def rolling_temblor(game, sporab):
    trig_list = []
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and 'Flying' not in perm.cab.keyword:
            amount = effects.damage(game, sporab, perm, 2)
            if amount!=None:
                trig_list.append([sporab, perm, amount, False])
    game.update_battlefield()
    for item in trig_list:
        game.add_to_tst([item, 'dealt_damage'])
            

def brimstone_volley(game, spell):
    if game.morbid:
        effects.targeted_damage(game, spell, 5)
    else:
        effects.targeted_damage(game, spell, 3)

def desperate_ravings(game, spell):
    effects.draw_cards(game, spell.controller, 2)
    effects.random_discard(game, spell.controller, 1)
    game.update_battlefield()

def make_a_wish(game, spell):
    cards = random.sample(spell.controller.graveyard,
                  min([2, len(spell.controller.graveyard)]))
    for card in cards:
        effects.gy_to_hand(game, card)
    game.update_battlefield()

def creeping_renaissance(game, spell):
    type_ = effects.choose_obj_from_list(game, spell.controller, PERM_TYPES,
                                    'Choose a card type')
    returned = []
    for item in spell.controller.graveyard:
        if type_ in item.type_:
            returned.append(item)
    for item in returned:
            item.owner.graveyard.remove(item)
            item = effects.card_copy(item.base, item.owner)
            output.output(game, spell.controller, item.name+' was returned'+\
                          ' to its owner\'s hand')
    game.update_battlefield()

def travelers_amulet(game, abil):
    land_list = [card for card in abil.controller.lib if 'Basic' in card.sup_type]
    card = effects.search_lib_for_subset(game, abil.controller, land_list)
    if card == None:
        print 'No card found'
        random.shuffle(abil.controller.lib)
        return None
    abil.controller.lib.remove(card)
    effects.go_to_hand(game, card)
    game.update_battlefield()
    random.shuffle(abil.controller.lib)

def tree_of_redemption(game, abil):
    rule = classes.SporabRule(abil, game.layer[7])
    rule.effect = [effects.la_7_set_pt, 0, abil.controller.life]
    rule.cleanup = effects.cl_rule_obj_gone
    rule.ref_obj.append(abil.obj)
    effects.set_life(game, abil.controller, abil.obj.toughness)
    game.update_battlefield()

def caravan_vigil(game, spell):
    land_list = [card for card in spell.controller.lib if 'Basic' in card.sup_type]
    if len(land_list)>0:
        card = effects.search_lib_for_subset(game, spell.controller, land_list)
        if card == None:
            print 'No card found'
            random.shuffle(spell.controller.lib)
            return None
        if game.morbid:
            print 'You may put the land on the battlefield instead of putting'\
                  +' it into your hand'
            if effects.may_choose(game, spell.controller):
                perm = classes.Permanent(game, spell.controller, card)
                effects.enter_battlefield(game, [perm])
                random.shuffle(spell.controller.lib)
                return None
        spell.controller.lib.remove(card)
        effects.go_to_hand(game, card)
        game.update_battlefield()
        random.shuffle(spell.controller.lib)

def corpse_lunge(game, spell):
    power = effects.get_card_power(game, spell.ref_obj[0])
    effects.targeted_damage(game, spell, power)

def maw_of_the_mire(game, spell):
    effects.targeted_destroy(game, spell)
    effects.change_cont_life(game, spell, 4)

def feeling_of_dread(game, spell):
    tapped_list = []
    for item in spell.target:
        if item in game.battlefield:
            if not item.tapped:
                tapped_list.append(item)
                effects.become_tapped(game, item)
    if len(tapped_list)>0:
        game.update_battlefield()
    for item in tapped_list:
        game.add_to_tst([item, 'became_tapped'])

def blasphemous_act(game, spell):
    creat_list = [perm for perm in game.battlefield if 'Creature' in perm.type_]
    for perm in creat_list:
        effects.damage(game, spell, perm, 13)
    game.update_battlefield()

def forbidden_alchemy(game, spell):
    player = spell.controller
    if len(player.lib)==0:
        print 'Your library is empty'
        return None
    n = min([len(player.lib), 4])
    card = effects.choose_obj_from_list(game, player, player.lib[-n:],
                                        prompt = 'Choose a card to put into'\
                                        +' your hand:')
    player.lib.remove(card)
    player.hand.append(card)
    print card.name + ' went to your hand'
    game.update_battlefield()
    effects.mill(game, spell.controller, n-1)

def memorys_journey(game, spell):
    player = spell.target[0]
    cards = spell.target[1:]
    for card in cards:
        player.graveyard.remove(card)
        card = effects.card_copy(card.base, card.owner)
        output.output(game, player, card.name+' was shuffled into '+\
                      player.name+ '\'s library')
    player.lib.extend(cards)
    random.shuffle(player.lib)
    game.update_battlefield()

def paraselene(game, spell):
    destroy_list = [perm for perm in game.battlefield if 'Enchantment' in perm.type_]
    life_list = effects.destroy_list(game, destroy_list)
    if len(life_list)>0:
        effects.change_cont_life(game, spell, len(life_list))

def mulch(game, spell):
    cards = []
    number = 0
    for i in range(min([4, len(spell.controller.lib)])):
        number+=1
        card = spell.controller.lib[-number]
        cards.append(card)
        effects.reveal(game, card)
    mill = list(cards)
    for card in cards:
        if 'Land' in card.type_:
            spell.controller.hand.append(card)
            spell.controller.lib.remove(card)
            mill.remove(card)
            output.output(game, spell.controller,
                          card.name+ ' was added to '+ spell.controller.name+\
                          '\'s hand')
        else:
            effects.mill(game, spell.controller, len(mill))
    game.update_battlefield()
        

def frightful_delusion(game, spell):
    player = spell.target[0].controller
    if effects.test_can_pay_mana(game, player, [0,0,0,0,0,1]):
        print 'Counter target spell unless its controller pays {1}'
        if effects.may_choose(game, player):
            if not effects.pay_mana_cost(game, player, [0,0,0,0,0,1]):
                effects.counterspell(game, spell, spell.target[0])
        else:
            effects.counterspell(game, spell, spell.target[0])
    else:
        effects.counterspell(game, spell, spell.target[0])
    game.update_battlefield()
    effects.choose_discard(game, spell.target[0].controller, 1)
    game.update_battlefield()

def lost_in_the_mist(game, spell):
    effects.return_to_hand(game, spell.target[1])
    game.update_battlefield()

def ghoulcallers_chant(game, spell):
    if spell.target[0] in spell.controller.graveyard:
        effects.gy_to_hand(game, spell.target[0])
    if spell.target[1] in spell.controller.graveyard:
        effects.gy_to_hand(game, spell.target[1])
    game.update_battlefield()

def dissipate(game, spell):
    rule = classes.SporabRule(spell, game.rule_leave_stack)
    rule.effect = [r_leave_stack_dissipate]
    rule.cleanup = effects.cl_never
    effects.counterspell(game, spell, spell.target[0])
    game.update_battlefield()

def divine_reckoning(game, spell):
    creat_list = [perm for perm in game.battlefield if game.active_player == \
             perm.controller and 'Creature' in perm.type_]
    if len(creat_list)>0:
        creat0 = effects.choose_obj_from_list(game, game.active_player,
                                              creat_list,
                                    'Choose a creature to not be destroyed')
    else:
        creat0 = None
    creat_list = [perm for perm in game.battlefield if \
                  game.active_player.next_player == \
                 perm.controller and 'Creature' in perm.type_]
    if len(creat_list)>0:
        creat1 = effects.choose_obj_from_list(game, game.active_player.next_player,
                                         creat_list,
                                    'Choose a creature to not be destroyed')
    else:
        creat1 = None
    destroy_list = []
    trig_list = []
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm!=creat1 and perm!=creat0:
            destroy_list.append(perm)
    for perm in destroy_list:
        if not perm.indestructible and not perm.regen_shield:
            effects.die(game, perm)
            trig_list.append(perm)
        elif perm.regen_shield:
            effects.regenerate(game, perm)
    game.update_battlefield()
    for perm in trig_list:
        game.add_to_tst([perm, 'bf_to_gy'])

def gnaw_to_the_bone(game, spell):
    grav_creat = [card for card in spell.controller.graveyard if 'Creature' in \
                  card.type_]
    effects.change_cont_life(game, spell, 2*len(grav_creat))

def night_terrors(game, spell):
    for card in spell.target[0].hand:
        effects.reveal(game, card)
    nonland = [card for card in spell.target[0].hand if 'Land' not in card.type_]
    if len(nonland)>0:
        output.output(game, spell.controller, 'Choose a card to exile', '')
        choice = effects.choose_obj_from_list(game, spell.controller, nonland)
        spell.target[0].hand.remove(choice)
        game.exile.append(choice)
        output.output(game, spell.controller, choice.name+' was exiled from '+\
                      spell.target[0].name+ '\'s hand')
        game.update_battlefield()

def nightbirds_clutches(game, spell):
    rule = classes.SporabRule(spell, game.rule_cant_block)
    rule.effect = [effects.r_cant_block_ref_obj]
    game.update_battlefield()

def travel_preparations(game, spell):
    for target in spell.target:
        effects.add_counter(game, target, '+1/+1', 1)
    game.update_battlefield()
    
#abts effects

def mikaeus_the_lunarch(game, abil):
    for perm in game.battlefield:
        if perm!=abil.obj and 'Creature' in perm.type_:
            effects.add_counter(game, perm, '+1/+1', 1)
    game.update_battlefield()

def manor_gargoyle2(game, abil):
    rule = classes.SporabRule(abil, game.layer[5])
    rule.effect = [la_5_manor_gargoyle]
    game.update_battlefield()

def liliana_of_the_veil0(game, abil):
    effects.choose_discard(game, game.active_player, 1)
    effects.choose_discard(game, game.active_player.next_player, 1)

def liliana_of_the_veil1(game, abil):
    effects.choose_sacrifice_creature(game, abil.target[0])

def liliana_of_the_veil2(game, abil):
    set1 = [perm for perm in game.battlefield if\
            abil.target[0] == perm.controller]
    set2 = []
    done = False
    if set1!=[]:
        while not done:
            number = 0
            output.output(game, abil.controller, 'Pile 1:', '')
            for item in set1:
                number+=1
                output.output(game, abil.controller, str(number)+'. '+item.name,'')
            output.output(game, abil.controller, 'Pile 2:', '')
            for item in set2:
                number+=1
                output.output(game, abil.controller, str(number)+'. '+item.name,'')
            output.output(game, abil.controller,
            'Choose an item to move to the other pile or enter "d" to finish','')
            choice = game.int_input(abil.controller, u_range=number, alt_input = 'd')
            if choice == 'd':
                done = True
            else:
                if choice <= len(set1):
                    item = set1[choice-1]
                    set1.remove(item)
                    set2.append(item)
                else:
                    item = set2[choice-1-len(set1)]
                    set2.remove(item)
                    set1.remove(item)
    output.output(game, abil.target[0], 'Choose a pile to sacrifice', '')
    output.output(game, abil.target[0], 'Pile 1:', '')
    effects.choose_obj_from_list(game, abil.target[0], set1,
                                 cont=False, just_looking=True)
    output.output(game, abil.target[0], 'Pile 2:', '')
    effects.choose_obj_from_list(game, abil.target[0], set2,
                                 cont = False, just_looking=True)
    choice = game.int_input(abil.target[0], u_range = 2)
    if choice == 1:
        set_ = set1
    else:
        set_ = set2
    for item in set_:
        effects.die(game, item)
    game.update_battlefield()
    for item in set_:
        game.add_to_tst([item, 'bf_to_gy'])                                              

def back_from_the_brink(game, abil):
    card = abil.ref_obj[0]
    perm = classes.Permanent(game, abil.controller, card)
    perm.card = classes.FakeCard()
    perm.card.owner = perm.controller
    effects.enter_battlefield(game, [perm])

def heretics_punishment(game, abil):
    cards = effects.mill(game, abil.controller, 3)
    highest_cmc = 0
    for card in cards:
        cmc = 0
        if card.mana_cost!=None:
            cmc = sum(card.mana_cost)
        highest_cmc = max([highest_cmc, cmc])
    effects.targeted_damage(game, abil, highest_cmc)
        

def grimgrin_corpse_born0(game, abil):
    effects.untap(game, abil.obj)
    effects.add_counter(game, abil.obj, '+1/+1', 1)
    game.update_battlefield()

def mirror_mad_phantasm(game, abil):
    effects.leave_battlefield(game, abil.obj)
    player = abil.obj.card.owner
    if abil.obj.card.real:
        player.lib.append(abil.obj.card)
    random.shuffle(player.lib)
    game.update_battlefield()
    game.add_to_tst([abil.obj, 'left_battlefield'])
    found = False
    if len(player.lib)==0:
        empty = True
    else:
        empty = False
    cards = []
    number = 1
    while not found and not empty:
        card = player.lib[-number]
        number+=1
        cards.append(card)
        effects.reveal(game, card)
        if card.name == 'Mirror-Mad Phantasm':
            found = True
        if len(player.lib)==number:
            empty = True
        game.update_battlefield()
    if found:
        perm = classes.Permanent(game, player, cards.pop())
        effects.enter_battlefield(game, [perm])
    effects.mill(game, abil.controller, len(cards))
    game.update_battlefield()

def trepanation_blade_ef(game, abil):
    player = game.active_player.next_player
    land = False
    cards = []
    number = 0
    while not land and len(player.lib)>number:
        number+=1
        card = player.lib[-number]
        cards.append(card)
        effects.reveal(game, card)
        if 'Land' in card.type_:
            land = True
    rule = classes.SporabRule(abil, game.layer[8])
    rule.effect = [effects.la_8_attached_plus, len(cards), 0]
    game.update_battlefield()
    effects.mill(game, player, len(cards))

def mindshrieker(game, abil):
    card = None
    for item in effects.mill(game, abil.target[0], 1):
        card = item
    cmc = 0
    if card != None:
        if card.mana_cost!=None:
            cmc = sum(card.mana_cost)
    rule = classes.SporabRule(abil, game.layer[8])
    rule.ref_obj[0] = abil.obj
    rule.effect = [effects.la_8_plus, cmc, cmc]
    game.update_battlefield()

def grimgrin_corpse_born1_ef(game, abil):
    effects.destroy(game, abil.target[0])
    effects.add_counter(game, abil.obj, '+1/+1', 1)
    game.update_battlefield()

def grimoire_of_the_dead(game, abil):
    creats = [card for card in game.player[0].graveyard+\
              game.player[1].graveyard if 'Creature' in card.type_]
    perm_list = []
    for card in creats:
        perm = classes.Permanent(game, abil.controller, card)
        perm.base.color_indicator.append(abil.color_word[0])
        if abil.type_word[0] not in perm.base.sub_type:
            perm.base.sub_type+=' '+abil.type_word[0]
        perm_list.append(perm)
    effects.enter_battlefield(game, perm_list)

def ghost_quarter(game, abil):
    effects.destroy(game, abil.target[0])
    player = abil.target[0].controller
    subset = [card for card in player.lib if 'Basic' in card.sup_type]
    choice = effects.search_lib_for_subset(game, player, subset)
    if choice!=None:
        perm = classes.Permanent(game, player, choice)
        effects.enter_battlefield(game, [perm])
    random.shuffle(player.lib)
    game.update_battlefield()

def olivia_voldaren1(game, abil):
    effects.targeted_damage(game, abil, 1)
    rule = classes.SporabRule(abil, game.layer[3])
    rule.cleanup = effects.cl_never
    rule.effect = [effects.la_3_add_type]
    game.update_battlefield()
    effects.abil_obj_counter(game, abil, '+1/+1', 1)
    game.update_battlefield()

def olivia_voldaren2(game, abil):
    rule = classes.SporabRule(abil, game.layer[1])
    rule.cleanup = cl_olivia
    rule.ref_obj.append(abil.controller)
    rule.effect = [la_1_olivia_voldaren]
    game.update_battlefield()
    
def selfless_cathar(game, abil):
    creat_list = []
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm.controller == abil.controller:
            creat_list.append(perm)
    rule = classes.SporabRule(abil, game.layer[8])
    rule.effect = [effects.la_8_creat_list_plus, creat_list, 1, 1]
    game.update_battlefield()

def rally_the_peasants(game, spell):
    creat_list = []
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm.controller == spell.controller:
            creat_list.append(perm)
    rule = classes.SporabRule(spell, game.layer[8])
    rule.effect = [effects.la_8_creat_list_plus, creat_list, 2, 0]
    game.update_battlefield()

def disciple_of_griselbrand(game, abil):
    effects.change_cont_life(game, abil, abil.ref_obj[0].toughness)

def spare_from_evil(game, abil):
    creat_list = []
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm.controller == abil.controller:
            creat_list.append(perm)
    rule = classes.SporabRule(abil, game.layer[5])
    rule.cleanup = effects.cl_until_eot
    rule.effect = [la_5_spare_from_evil, creat_list]
    game.update_battlefield()

def kessig_wolf_run(game, abil, x):
    rule = classes.SporabRule(abil, game.layer[8])
    rule.effect = [effects.la_8_plus, x, 0]
    rule.cleanup = effects.cl_until_eot
    game.update_battlefield()
    rule = classes.SporabRule(abil, game.layer[5])
    rule.effect = [effects.la_5_ta_gains_keyword, 'Trample']
    rule.cleanup = effects.cl_until_eot
    game.update_battlefield()

def garruk_relentless1(game, abil):
    amount = effects.damage(game, abil.obj, abil.target[0], 3)
    game.update_battlefield()
    if amount!=None:
        game.add_to_tst([[abil.obj, abil.target[0], amount, False], 'dealt_damage'])
    dam = effects.damage(game, abil.target[0], abil.obj, abil.target[0].power)
    game.update_battlefield()
    if dam!=None:
        game.add_to_tst([[abil.target[0], abil.obj, dam, False], 'dealt_damage'])

def garruk_the_veil_cursed1(game, abil):
    if effects.fun_sac_creat(game, abil.controller, abil):
        subset = [card for card in abil.controller.lib if 'Creature'\
                  in card.type_]
        card = effects.search_lib_for_subset(game, abil.controller, subset)
        if card == None:
            output.output(game, abil.controller, 'No card found')
        else:
            effects.reveal(game, card)
            abil.controller.lib.remove(card)
            effects.go_to_hand(game, card)
        random.shuffle(abil.controller.lib)
        game.update_battlefield()

def garruk_the_veil_cursed2(game, abil):
    grav_creat = [card for card in abil.controller.graveyard if 'Creature' in\
                  card.type_]
    creat_list = [perm for perm in game.battlefield if perm.controller == \
                  abil.controller and 'Creature' in perm.type_]
    x = len(grav_creat)
    rule = classes.SporabRule(abil, game.layer[8])
    rule.effect = [effects.la_8_creat_list_plus, creat_list, x, x]
    rule.cleanup = effects.cl_until_eot
    rule = classes.SporabRule(abil, game.layer[5])
    rule.effect = [effects.la_5_creat_list_keyword, creat_list, 'Trample']
    rule.cleanup = effects.cl_until_eot
    game.update_battlefield()

def gavony_township(game, abil):
    creat_list = [perm for perm in game.battlefield if perm.controller == \
                  abil.controller and 'Creature' in perm.type_]
    for item in creat_list:
        effects.add_counter(game, item, '+1/+1', 1)
    game.update_battlefield()

def elder_of_laurels(game, abil):
    creats = [perm for perm in game.battlefield if perm.controller == \
              abil.controller and 'Creature' in perm.type_]
    rule = classes.SporabRule(abil, game.layer[8])
    rule.cleanup = effects.cl_until_eot
    rule.effect = [effects.la_8_plus, len(creats), len(creats)]
    game.update_battlefield()

def hysterical_blindness(game, abil):
    creat_list = []
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm.controller != abil.controller:
            creat_list.append(perm)
    rule = classes.SporabRule(abil, game.layer[8])
    rule.cleanup = effects.cl_until_eot
    rule.effect = [effects.la_8_creat_list_plus, creat_list, -4, 0]
    game.update_battlefield()
    
def ashmouth_hound_ef(game, abil):
    for item in abil.ref_obj[0]:
        if item!=abil.obj:
            target = item
    dealt = effects.damage(game, abil.obj, target, 1)
    game.update_battlefield()
    if dealt!=None:
        game.add_to_tst([[abil.obj, target.controller, \
                          dealt, False], 'dealt_damage'])

def claustrophobia_0_ef(game, abil):
    if not abil.obj.attached_to.tapped:
        effects.become_tapped(game, abil.obj.attached_to)
        game.update_battlefield()
        game.add_to_tst([abil.obj.attached_to, 'became_tapped'])

def crossway_vampire_ef(game, abil):
    rule = classes.SporabRule(abil, game.rule_cant_block)
    rule.cleanup = effects.cl_until_eot
    rule.effect = [effects.r_cant_block_ref_obj]
    rule.ref_obj.append(abil.target[0])

def graveyard_shovel(game, abil):
    player = abil.target[0]
    if len(player.graveyard)>0:
        card = effects.choose_obj_from_list(game, player,
                                     player.graveyard,
                                     'Choose a card to exile')
        player.graveyard.remove(card)
        card = effects.card_copy(card.base, card.owner)
        game.exile.append(card)
        if 'Creature' in card.type_:
            effects.change_life(game, abil.controller, 2)
    game.update_battlefield()

def curse_of_oblivion_ef(game, abil):
    player = abil.obj.attached_to
    gy = list(player.graveyard)
    if len(gy)>0:
        card1 = effects.choose_obj_from_list(game, player, gy,
                        prompt = 'Choose a card to exile from your graveyard')
        gy.remove(card1)
        if len(gy)>0:
            card2 = effects.choose_obj_from_list(game, player, gy,
                       prompt = 'Choose a card to exile from your graveyard')
        player.graveyard.remove(card1)
        card1 = effects.card_copy(card1.base, card1.owner)
        print card1.name + ' exiled from '+player.name+'\'s graveyard'
        game.exile.append(card1)
        if len(gy)>0:
            player.graveyard.remove(card2)
            card2 = card_copy(card2.base, card2.owner)
            print card2.name + ' exiled from '+player.name+'\'s graveyard'
            game.exile.append(card2)
        game.update_battlefield()

def splinterfright_ef(game, abil):
    effects.mill(game, abil.controller, 2)
    
def curse_of_stalked_prey_ef(game, abil):
    effects.add_counter(game, abil.ref_obj[0][0], '+1/+1', 1)
    game.update_battlefield()

def curse_of_the_bloody_tome_ef(game, abil):
    player = abil.obj.attached_to
    effects.mill(game, player, 2)

def curse_of_the_pierced_heart_ef(game, abil):
    player = abil.obj.attached_to
    effects.damage(game, abil.obj, player, 1)
    game.update_battlefield()

def delver_of_secrets_ef(game, abil):
    effects.look_top_cards(game, abil.controller)
    if len(abil.controller.lib) >0:
        print 'You may reveal that card. If an instant or sorcery card'\
              +' is revealed this way, transform '+abil.obj.name+'.'
        if effects.may_choose(game, abil.controller):
            card = abil.controller.lib[-1]
            effects.reveal_card(game, abil.controller, card)
            if any([word in card.type_ for word in ('Instant', 'Sorcery')]):
                transform(game, abil)

def bloodgift_demon_ef(game, abil):
    effects.draw_cards(game, abil.target[0], 1)
    game.update_battlefield()
    game.add_to_tst([abil.target[0], 'drew_card'])
    effects.change_life(game, abil.target[0], -1)
    game.update_battlefield()

def elder_cathar_ef(game, abil):
    if abil.type_word[0] in abil.target[0].sub_type:
        effects.add_counter(game, abil.target[0], '+1/+1', 2)
    else:
        effects.add_counter(game, abil.target[0], '+1/+1', 1)
    game.update_battlefield()

def ludevics_test_subject(game, abil):
    effects.add_counter(game, abil.obj, 'Hatchling', 1)
    game.update_battlefield()
    if abil.obj.counter['Hatchling']>=3:
        abil.obj.counter['Hatchling']=0
        game.update_battlefield()
        transform(game, abil)
        game.update_battlefield()

def geist_of_saint_traft_ef(game, abil):
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    rule = classes.ReplacementEffect()
    rule.cleanup = effects.cl_bf_update
    rule.name = 'This creature enters the battlefield tapped and attacking'
    rule.test = effects.ase_test_creature
    rule.effect = [effects.ase_tapped_and_attacking]
    rule.location = game.rule_as_enters
    rule.location.append(rule)
    tokens = effects.make_tokens(game, abil.controller, 1, abil.color_word,
                               abil.type_word[0], 4, 4, cab)
    for token in tokens:
        abts = classes.AbilToStack()
        abts.location = game.trig_abil
        abts.location.append(abts)
        abts.name = abil.name
        abts.obj = abil.obj
        abts.controller = abil.controller
        abts.triggered = False
        abts.rules_text = abil.rules_text
        abts.trig_test = effects.tr_begin_end_combat
        abts.cleanup = effects.cl_triggered
        abts.ef_list.insert(0, [effects.ref_obj0_sacrifice])
        abts.ref_obj.append(token)
    game.update_battlefield()    

def village_bellringer_ef(game, abil):
    for perm in game.battlefield:
        if perm.controller == abil.controller and 'Creature' in perm.type_:
            effects.untap(game, perm)

def nightfall_predator(game, abil):
    pair = fight(game, abil.target[0], abil.obj)
    game.update_battlefield()
    for item in pair:
        if item[2]!=None:
            game.add_to_tst([item, 'dealt_damage'])
        

def stitchers_apprentice(game, abil):
    effects.make_tokens(game, abil.controller, 1, abil.color_word, abil.type_word[0],
                       2, 2)
    effects.fun_sac_creat(game, abil.controller, abil)

def bitterheart_witch_ef(game, abil):
    card_list = [card for card in abil.controller.lib if 'Curse' in card.sub_type]
    card = effects.search_lib_for_subset(game, abil.controller, card_list)
    if card != None:
        perm = classes.Permanent(game, abil.controller, card)
        perm.attached_to = abil.target[0]
        effects.enter_battlefield(game, [perm])
    
def ghoulcallers_bell(game, abil):
    effects.mill(game, game.active_player, 1)
    effects.mill(game, game.active_player.next_player, 1)

def abattoir_ghoul_ef(game, abil):
    effects.change_life(game, abil.controller, abil.ref_obj[0].toughness)

def balefire_dragon_ef(game, abil):
    for perm in game.battlefield:
        if perm.controller == abil.ref_obj[0][1] and 'Creature' in perm.type_:
            effects.damage(game, abil.obj, perm, abil.ref_obj[0][2])
    game.update_battlefield()

def charmbreaker_devils_0_ef(game, abil):
    card_list = [card for card in abil.controller.graveyard if \
                 'Sorcery' in card.type_ or\
                 'Instant' in card.type_]
    if len(card_list)>0:
        choice = random.choice(card_list)
        abil.controller.graveyard.remove(choice)
        choice = effects.card_copy(choice.base, choice.owner)
        effects.go_to_hand(game, choice)
        game.update_battlefield()

def falkenrath_noble_ef(game, abil):
    effects.change_life(game, abil.target[0], -1)
    game.update_battlefield()
    effects.change_life(game, abil.controller, 1)
    game.update_battlefield()

def cellar_door(game, abil):
    if len(abil.target[0].lib) > 0:
        card = abil.target[0].lib.pop(0)
        effects.go_to_gy(game, card)
        game.update_battlefield()
        game.add_to_tst([card, 'lib_to_gy'])
        if 'Creature' in card.type_:
            effects.make_tokens(game, abil.controller, 1, abil.color_word,\
                               abil.type_word[0], 2, 2)


def murder_of_crows_ef(game, abil):
    effects.draw_cards(game, abil.controller, 1)
    card = effects.choose_discard(game, abil.controller, 1)

def civilized_scholar(game, abil):
    effects.draw_cards(game, abil.controller, 1)
    card = effects.choose_discard(game, abil.controller, 1)
    if 'Creature' in card.type_:
        transform(game, abil)
        effects.untap(game, abil.obj)

def hollowhenge_scavenger_ef(game, abil):
    if game.morbid:
        effects.change_cont_life(game, abil, 5)

def woodland_sleuth_ef(game, abil):
    creats = [card for card in abil.controller.graveyard if 'Creature' in card.type_]
    if game.morbid and len(creats)>0:
        effects.gy_to_hand(game, random.choice(creats))
    game.update_battlefield()

def morkrut_banshee_ef(game, abil):
    rule = classes.SporabRule(abil, game.layer[8])
    rule.effect = [effects.la_8_plus, -4, -4]
    game.update_battlefield()

def homicidal_brute_ef(game, abil):
    transform(game, abil)
    effects.become_tapped(game, abil.obj)

def creepy_doll_ef(game, abil):
    won = effects.coin_flip(game, abil.controller)
    if won:
        effects.destroy(game, abil.ref_obj[0][1])

def endless_ranks_of_the_dead_ef(game, abil):
    zombies = [item for item in game.battlefield if abil.type_word[0] in \
           item.sub_type and 'Creature' in item.type_ and \
           item.controller == abil.controller]
    effects.sporab_tokens(game, abil, len(zombies)/2, 2, 2)

def mentor_of_the_meek_ef(game, abil):
    if effects.pay_mana_cost(game, abil.controller, [0,0,0,0,0,1]):
        effects.draw_cards(game, abil.controller, 1)
        game.update_battlefield()

def fiend_hunter0_ef(game, abil):
    card = abil.target[0].card
    effects.exile(game, abil.target[0])
    game.update_battlefield()
    game.add_to_tst([abil.target[0], 'left_battlefield'])
    rule = classes.SporabRule(abil, game.rule_obj_char)
    rule.ref_obj.append(card)
    rule.effect = [r_obj_char_fiend_hunter]
    rule.cleanup = effects.cl_never
    game.update_battlefield()

def screeching_bat_ef(game, abil):
    if effects.pay_mana_cost(game, abil.controller, [0,0,2,0,0,2]):
        transform(game, abil)
    else:
        game.undo()
        
        
def moldgraf_monstrosity_ef(game, abil):
    if abil.obj.card in abil.obj.card.owner.graveyard:
        abil.obj.card.owner.graveyard.remove(abil.obj.card)
        abil.obj.card = effects.card_copy(abil.obj.card.base, abil.obj.card.owner)
        game.exile.append(abil.obj.card)
    creat_list = [card for card in abil.controller.graveyard if 'Creature' in card.type_]
    choice = random.sample(creat_list,
                           min([2, len(creat_list)]))
    added = []
    for item in choice:
        perm = classes.Permanent(game, abil.controller, item)
        perm_list.append(perm)
    effects.enter_battlefield(game, perm_list)
        
def geist_honored_monk_ef(game, abil):
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    effects.make_tokens(game, abil.controller, 2, abil.color_word,
                                     abil.type_word[0], 1, 1, cab)

def witchbane_orb_ef(game, abil):
    destroy_list = [perm for perm in game.battlefield if 'Curse' in \
                    perm.sub_type\
                    and abil.controller == perm.attached_to]
    effects.destroy_list(game, destroy_list)

def fiend_hunter1_ef(game, abil):
    if len(abil.ref_obj)>1:
        if abil.ref_obj[0] in game.exile:
            card = abil.ref_obj[0]
            perm = classes.Permanent(game, card.owner, card)
            effects.enter_battlefield(game, [perm])
    game.update_battlefield()

def full_moons_rise1(game, abil):
    for perm in game.battlefield:
        if perm.controller == abil.controller and 'Creature' in perm.type_\
           and abil.type_word[0] in perm.sub_type:
            perm.regen_shield = True

def ghoulraiser_ef(game, abil):
    zombies = [card for card in abil.controller.graveyard if abil.type_word[0] in \
               card.sub_type]
    if len(zombies)>0:
        choice = random.choice(zombies)
        effects.gy_to_hand(game, choice)
        game.update_battlefield()

def gutter_grime_ef(game, abil):
    effects.add_counter(game, abil.obj, 'Slime', 1)
    game.update_battlefield()
    cab = classes.CardAbilities()
    stab1 = classes.StaticAbil()
    stab1.effect = [la_6_gutter_grime]
    stab1.ref_obj.append(abil.obj)
    stab1.rules_text = 'This creature\'s power and toughness are each equal '+\
        'to the number of slime counters of Gutter Grime'
    cab.layer_static[6].append(stab1)
    effects.make_tokens(game, abil.controller, 1, abil.color_word, \
                       abil.type_word[0], 0, 0, cab)

def kessig_cagebreakers_ef(game, abil):
    grav_creat = [card for card in abil.controller.graveyard if 'Creature' \
                  in card.type_]
    rule = classes.ReplacementEffect()
    rule.cleanup = effects.cl_bf_update
    rule.name = 'This creature enters the battlefield tapped and attacking'
    rule.test = effects.ase_test_creature
    rule.effect = [effects.ase_tapped_and_attacking]
    rule.location = game.rule_as_enters
    rule.location.append(rule)
    effects.make_tokens(game, abil.controller, len(grav_creat),
                                abil.color_word, abil.type_word[0], 2, 2)


def wooden_stake_ef(game, abil):
    if abil.ref_obj[0][0] == abil.obj.attached_to:
        perm = abil.ref_obj[0][1]
    else:
        perm = abil.ref_obj[0][0]
    if perm in game.battlefield:
        perm.regen_shielf = False
        effects.destroy(game, perm)
    
#Trig Abil generators

def trepanation_blade(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [trepanation_blade_ef])
    abts.trig_test = tr_trepanation_blade

def undead_alchemist1(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [undead_alchemist_ef])
    abts.trig_test = tr_undead_alchemist

def gutter_grime(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [gutter_grime_ef])
    abts.trig_test = effects.tr_nontoken_creature_you_control_dies

def garruk_relentless0(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [transform])
    abts.trig_test = tr_garruk_relentless

def grimgrin_corpse_born1(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [grimgrin_corpse_born1_ef])
    abts.sporab_target.append(effects.ta_creature_opponent_controls)
    abts.trig_test = effects.tr_self_attacking

def kessig_cagebreakers(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [kessig_cagebreakers_ef])
    abts.trig_test = effects.tr_self_attacking

def hamlet_captain(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.until_eot_lord, 1, 1])
    abts.trig_test = effects.tr_self_attacking_or_blocking

def werewolf_0(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [transform])
    abts.trig_test = tr_werewolf_0

def werewolf_1(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [transform])
    abts.trig_test = tr_werewolf_1

def charmbreaker_devils_0(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [charmbreaker_devils_0_ef])
    abts.trig_test = effects.tr_your_begin_upkeep

def ghoulraiser(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [ghoulraiser_ef])
    abts.trig_test = effects.tr_self_etb

def charmbreaker_devils_1(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.trig_test = effects.tr_you_cast_instant_or_sorcery
    abts.ef_list.insert(0, [effects.abil_obj_plus, 4, 0])

def doomed_traveler(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    abts.ef_list.insert(0, [effects.sporab_tokens, 1, 1, 1, cab])
    abts.trig_test = effects.tr_self_bf_to_gy

def slayer_of_the_wicked(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.sporab_target.append(ta_slayer_of_the_wicked)
    abts.ef_list.insert(0, [effects.may, [effects.targeted_destroy]])
    abts.trig_test = effects.tr_self_etb

def mausoleum_guard(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    cab = classes.CardAbilities()
    cab.keyword.append('Flying')
    abts.ef_list.insert(0, [effects.sporab_tokens, 2, 1, 1, cab])
    abts.trig_test = effects.tr_self_bf_to_gy

def angel_of_flight_alabaster(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.targeted_gy_to_hand])
    abts.sporab_target.append(ta_creat_type_in_cont_gy)
    abts.trig_test = effects.tr_your_begin_upkeep

def thraben_sentry(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.may, [transform]])
    abts.trig_test = tr_another_creat_you_control_dies

def burning_vengeance(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.targeted_damage, 2])
    abts.sporab_target.append(effects.ta_creature_or_player)
    abts.trig_test = tr_burning_vengeance

def balefire_dragon(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [balefire_dragon_ef])
    abts.trig_test = effects.tr_combat_damage_to_player

def abattoir_ghoul(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [abattoir_ghoul_ef])
    abts.trig_test = tr_abattoir_ghoul

def howlpack_alpha1(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.sporab_token, stab.color_word, stab.type_word[0],
                                              2, 2])
    abts.trig_test = effects.tr_your_begin_end

def reaper_from_the_abyss(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.targeted_destroy])
    abts.sporab_target.append(ta_avacynian_priest)
    abts.trig_test = tr_reaper_from_the_abyss

def hollowhenge_scavenger(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [hollowhenge_scavenger_ef])
    abts.trig_test = tr_etb_morbid

def selhoff_occultist(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.targeted_mill, 1])
    abts.sporab_target.append(effects.ta_player)
    abts.trig_test = effects.tr_creature_dies

def village_bellringer(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [village_bellringer_ef])
    abts.trig_test = effects.tr_self_etb

def creepy_doll(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [creepy_doll_ef])
    abts.trig_test = effects.tr_combat_damage_to_creature

def unruly_mob(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.abil_obj_plus_one_counter, 1])
    abts.trig_test = tr_another_creat_you_control_dies

def elder_cathar(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [elder_cathar_ef])
    abts.sporab_target.append(effects.ta_creature_you_control)
    abts.trig_test = effects.tr_self_bf_to_gy

def geist_honored_monk1(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [geist_honored_monk_ef])
    abts.trig_test = effects.tr_self_etb

def champion_of_the_parish(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.abil_obj_counter, '+1/+1', 1])
    abts.trig_test = effects.tr_etb_another_type_your_control
                         
def cloistered_youth(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.may, [transform]])
    abts.trig_test = effects.tr_your_begin_upkeep

def pitchburn_devils(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.targeted_damage, 3])
    abts.sporab_target.append(effects.ta_creature_or_player)
    abts.trig_test = effects.tr_self_bf_to_gy

def delver_of_secrets(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [delver_of_secrets_ef])
    abts.trig_test = effects.tr_your_begin_upkeep

def bitterheart_witch(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.may, [bitterheart_witch_ef]])
    abts.sporab_target.append(effects.ta_player)
    abts.trig_test = effects.tr_self_bf_to_gy

def claustrophobia_0(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm,stab)
    abts.ef_list.insert(0, [claustrophobia_0_ef])
    abts.trig_test = effects.tr_self_etb

def snapcaster_mage(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [snapcaster_mage_ef])
    abts.sporab_target.append(ta_snapcaster_mage)
    abts.trig_test = effects.tr_self_etb

def curiosity(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.may, [effects.draw_cont_cards, 1]])
    abts.trig_test = tr_curiosity

def sturmgeist2(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.draw_cont_cards, 1])
    abts.trig_test = effects.tr_combat_damage_to_player

def unholy_fiend(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.change_cont_life, -1])
    abts.trig_test = effects.tr_your_begin_end
    
def ashmouth_hound(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [ashmouth_hound_ef])
    abts.trig_test = effects.tr_blocks_or_becomes_blocked

def wooden_stake(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [wooden_stake_ef])
    abts.trig_test = tr_wooden_stake

def witchbane_orb0(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [witchbane_orb_ef])
    abts.trig_test = effects.tr_self_etb
    
def geistcatchers_rig(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.targeted_damage, 4])
    abts.sporab_target.append(effects.ta_flying)
    abts.trig_test = effects.tr_self_etb

def crossway_vampire(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [crossway_vampire_ef])
    abts.sporab_target.append(effects.ta_creature)
    abts.trig_test = effects.tr_self_etb

def endless_ranks_of_the_dead(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [endless_ranks_of_the_dead_ef])
    abts.trig_test = effects.tr_your_begin_upkeep

def village_cannibals(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.abil_obj_counter, '+1/+1', 1])
    abts.trig_test = tr_village_cannibals

def armored_skaab(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.abil_obj_mill, 4])
    abts.trig_test = effects.tr_self_etb

def murder_of_crows(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.may, [murder_of_crows_ef]])
    abts.trig_test = effects.tr_another_creature_dies

def moldgraf_monstrosity(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [moldgraf_monstrosity_ef])
    abts.trig_test = effects.tr_self_bf_to_gy

def mentor_of_the_meek(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.may, [mentor_of_the_meek_ef]])
    abts.trig_test = tr_mentor_of_the_meek

def woodland_sleuth(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [woodland_sleuth_ef])
    abts.trig_test = tr_etb_morbid

def morkrut_banshee(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [morkrut_banshee_ef])
    abts.sporab_target.append(effects.ta_creature)
    abts.trig_test = tr_etb_morbid

def geist_of_saint_traft(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [geist_of_saint_traft_ef])
    abts.trig_test = effects.tr_self_attacking

def galvanic_juggernaut(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.abil_obj_untap])
    abts.trig_test = effects.tr_another_creature_dies

def rage_thrower(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.targeted_damage, 2])
    abts.sporab_target.append(effects.ta_player)
    abts.trig_test = effects.tr_another_creature_dies

def fiend_hunter0(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.may, [fiend_hunter0_ef]])
    abts.sporab_target.append(effects.another_ta_creature)
    abts.trig_test = effects.tr_self_etb

def fiend_hunter1(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [fiend_hunter1_ef])
    abts.trig_test = effects.tr_self_left_battlefield

def bloodgift_demon(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [bloodgift_demon_ef])
    abts.sporab_target.append(effects.ta_player)
    abts.trig_test = effects.tr_your_begin_upkeep

def falkenrath_noble(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [falkenrath_noble_ef])
    abts.sporab_target.append(effects.ta_player)
    abts.trig_test = effects.tr_creature_dies

def lumberknot(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.abil_obj_counter, '+1/+1', 1])
    abts.trig_test = effects.tr_creature_dies

def slith(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.abil_obj_plus_one_counter, 1])
    abts.trig_test = effects.tr_combat_damage_to_player

def rakish_heir(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [rakish_heir_ef])
    abts.trig_test = tr_rakish_heir

def falkenrath_marauders(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.abil_obj_plus_one_counter, 2])
    abts.trig_test = effects.tr_combat_damage_to_player

def curse_of_oblivion(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [curse_of_oblivion_ef])
    abts.trig_test = tr_cursed_player_begin_upkeep

def splinterfright(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [splinterfright_ef])
    abts.trig_test = effects.tr_your_begin_upkeep

def curse_of_the_pierced_heart(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [curse_of_the_pierced_heart_ef])
    abts.trig_test = tr_cursed_player_begin_upkeep

def curse_of_stalked_prey(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [curse_of_stalked_prey_ef])
    abts.trig_test = tr_curse_of_stalked_prey

def curse_of_the_bloody_tome(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [curse_of_the_bloody_tome_ef])
    abts.trig_test = tr_cursed_player_begin_upkeep

def homicidal_brute(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [homicidal_brute_ef])
    abts.trig_test = effects.tr_your_begin_end

def screeching_bat(game, perm, stab):
    abts = classes.StabAbilToStack(game, perm, stab)
    abts.ef_list.insert(0, [effects.may, [screeching_bat_ef]])
    abts.trig_test = effects.tr_your_begin_upkeep
    
#Other stab effects

def undead_alchemist0(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_damage)
    rule.effect = [r_damage_undead_alchemist]

def unbreathing_horde(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_damage)
    rule.effect = [r_damage_unbreathing_horde]

def stony_silence(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_activate)
    rule.effect = [r_activate_stony_silence]

def skaab_ruinator(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_can_cast)
    rule.effect = [r_can_cast_self]

def scourge_of_geier_reach(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.ref_obj.append(perm)
    creats = [item for item in game.battlefield if item.controller != perm.controller\
              and 'Creature' in item.type_]
    rule.effect = [effects.la_8_plus, len(creats), len(creats)]

def rooftop_storm(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_alt_cost)
    rule.effect = [r_alt_cost_rooftop_storm]

def flashback(game, card, stab):
    rule = classes.PermRule(card, stab, game.rule_can_cast)
    rule.effect = [r_can_cast_flashback]
    
def one_eyed_scarecrow(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [la_8_one_eyed_scarecrow]

def parallel_lives(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_parallel_lives)
    rule.effect = [r_parallel_lives]

def orchard_spirit(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_cant_block)
    rule.effect = [r_cant_block_orchard_spirit]

def manor_gargoyle1(game, perm, stab):
    if 'Defender' in perm.cab.keyword:
        perm.indestructible = True

def full_moons_rise0(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.layer[5])
    rule.effect = [la_5_type_gains_keyword, 'Trample']
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [effects.la_8_type_plus, 1, 0]

def night_revelers(game, perm, stab):
    humans = [item for item in game.battlefield if \
              item.controller!=perm.controller and\
              'Creature' in item.type_ and stab.type_word[0] in item.sub_type]
    if len(humans)>0:
        rule = classes.PermRule(perm, stab, game.layer[5])
        rule.effect = [effects.la_5_self_keyword, 'Haste']

def intangible_virtue(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.layer[5])
    rule.effect = [la_5_intangible_virtue]
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [la_8_intangible_virtue]

def blazing_torch_0(game, perm, stab):
    if perm.attached_to!=None:
        rule = classes.PermRule(perm, stab, game.rule_cant_block)
        rule.effect = [r_cant_block_blazing_torch]

def stromkirk_noble(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_cant_block)
    rule.effect = [r_cant_block_stromkirk_noble]

def laboratory_maniac(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_laboratory_maniac)
    rule.effect = [r_laboratory_maniac]

def wreath_of_geists(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [la_8_wreath_of_geists]

def runechanters_pike(game, perm, stab):
    if perm.attached_to!=None:
        rule = classes.PermRule(perm, stab, game.layer[5])
        rule.effect = [effects.la_5_attached_gains_keyword, 'First Strike']
        num = len([card for card in perm.controller.graveyard if\
                   'Instant' in card.type_ or 'Sorcery' in card.type_])
        rule = classes.PermRule(perm, stab, game.layer[8])
        rule.effect = [effects.la_8_attached_plus, num, 0]

def blazing_torch_1(game, perm, stab):
    if perm.attached_to!=None:
        rule = classes.PermRule(perm, stab, game.layer[5])
        rule.effect = [la_5_blazing_torch]

def angelic_overseer(game, perm, stab):
    human = False
    for item in game.battlefield:
        if item.controller == perm.controller and stab.type_word[0] in \
           item.sub_type and 'Creature' in item.type_:
            rule = classes.PermRule(perm, stab, game.layer[5])
            rule.effect = [effects.la_5_self_keyword, 'Hexproof']
            perm.indestructible = True

def mask_of_avacyn(game, perm, stab):
    if perm.attached_to!=None:
        rule = classes.PermRule(perm, stab, game.layer[5])
        rule.effect = [effects.la_5_attached_gains_keyword, 'Hexproof']
        rule = classes.PermRule(perm, stab, game.layer[8])
        rule.effect = [effects.la_8_attached_plus, 1, 2]

def claustrophobia_1(game, perm, stab):
    if perm.attached_to in game.battlefield:
        rule = classes.PermRule(perm, stab, game.rule_untap)
        rule.effect = [effects.r_untap_attached]

def terror_of_kruin_pass(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_block)
    rule.effect = [r_block_terror_of_kruin_pass]

def bonds_of_faith(game, perm, stab):
    if perm.attached_to in game.battlefield:
        if 'Human' in perm.attached_to.sub_type:
            rule = classes.PermRule(perm, stab, game.layer[8])
            rule.effect = [effects.la_8_attached_plus, 2, 2]
        else:
            rule = classes.PermRule(perm, stab, game.rule_cant_attack)
            rule.effect = [effects.r_cant_attack_attached]
            rule = classes.PermRule(perm, stab, game.rule_cant_block)
            rule.effect = [effects.r_cant_block_attached]

def curse_of_deaths_hold(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [la_8_curse_of_deaths_hold]

def heartless_summoning(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_cost_red)
    rule.effect = [r_cost_dec_heartless_summoning]

def curse_of_the_nightly_hunt(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_attack)
    rule.effect = [r_attack_curse_of_the_nightly_hunt]

def butchers_cleaver(game, perm, stab):
    if perm.attached_to != None:
        if stab.type_word[0] in perm.attached_to.sub_type:
            rule = classes.PermRule(perm, stab, game.layer[5])
            rule.effect = [effects.la_5_attached_gains_keyword, 'Lifelink']

def sharpened_pitchfork(game, perm, stab, power, toughness):
    if perm.attached_to != None:
        if stab.type_word[0] in perm.attached_to.sub_type:
            rule = classes.PermRule(perm, stab, game.layer[8])
            rule.effect = [effects.la_8_attached_plus, power, toughness]

def furor_of_the_bitten(game, perm, stab):
    if perm.attached_to in game.battlefield:
        rule = classes.PermRule(perm, stab, game.rule_attack)
        rule.effect = [effects.r_attack_attached_attacks_each_turn]
        rule = classes.PermRule(perm, stab, game.layer[8])
        rule.effect = [effects.la_8_attached_plus, 2, 2]

def skeletal_grimace(game, perm, stab):
    if perm.attached_to in game.battlefield:
        rule = classes.PermRule(perm, stab, game.layer[5])
        rule.effect = [la_5_skeletal_grimace]
        rule = classes.PermRule(perm, stab, game.layer[8])
        rule.effect = [effects.la_8_attached_plus, 1, 1]
        
def spectral_flight(game, perm, stab):
    if perm.attached_to in game.battlefield:
        rule = classes.PermRule(perm, stab, game.layer[5])
        rule.effect = [effects.la_5_attached_gains_keyword, 'Flying']
        rule = classes.PermRule(perm, stab, game.layer[8])
        rule.effect = [effects.la_8_attached_plus, 2, 2]

def boneyard_wurm(game, perm, stab):
    pt = 0
    for card in perm.controller.graveyard:
        if 'Creature' in card.type_:
            pt+=1
    perm.power = pt
    perm.toughness = pt

def sturmgeist(game, perm, stab):
    perm.power = len(perm.controller.hand)
    perm.toughness = len(perm.controller.hand)

def la_6_gutter_grime(game, perm, stab):
    if stab.ref_obj[0] in game.battlefield:
        pt = stab.ref_obj[0].counter['Slime']
        perm.power = pt
        perm.toughness = pt

def geist_honored_monk0(game, perm, stab):
    pt = 0
    for item in game.battlefield:
        if 'Creature' in item.type_ and item.controller == perm.controller:
            pt+=1
    perm.power = pt
    perm.toughness = pt

def dearly_departed(game, card, stab):
    rule = classes.PermRule(card, stab, game.rule_as_enters)
    rule.test = ase_test_dearly_departed
    rule.effect = [ase_dearly_departed]

def essence_of_the_wild(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_as_enters)
    rule.test = effects.ase_test_creature_you_control
    rule.effect = [ase_essence_of_the_wild]

def witchbane_orb1(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_target)
    rule.effect = [r_target_witchbane_orb]

def howlpack_alpha0(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [la_8_howlpack_alpha]

def instigator_gang(game, perm, stab, power, toughness):
    rule = classes.PermRule(perm, stab, game.layer[8])
    rule.effect = [la_8_instigator_gang, power, toughness]

def inquisitors_flail0(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_damage)
    rule.effect = [r_damage_inquisitors_flail0]

def inquisitors_flail1(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_damage)
    rule.effect = [r_damage_inquisitors_flail1]

def nevermore(game, perm, stab):
    rule = classes.PermRule(perm, stab, game.rule_cant_cast)
    rule.effect = [r_cant_cast_nevermore]
        
#timing

def tim_bloodline_keeper(game, player, abts):
    vamps = [perm for perm in game.battlefield if perm.controller == player and \
             abts.type_word[0] in perm.sub_type]
    if len(vamps)>=5:
        return True
    return False

def tim_morbid(game, player, abts):
    if game.morbid:
        return True
    return False

#undo

def undo_mill_one(game, card):
    card.owner.lib.append(card)
    random.shuffle(card.owner.lib)
    print card.name + ' was returned to its owners library, and the library '+\
                              'was reshuffled'
    card.owner.graveyard.remove(card)

def undo_exile_card_from_gy(game, card):
    game.exile.remove(card)
    card.owner.graveyard.append(card)
    print card.name + 'was returned to '+card.owner.name+'\'s graveyard'

#trig_tests

def tr_trepanation_blade(game, abts, trig_obj, event_str):
    if event_str == 'attacking' and abts.obj.attached_to == trig_obj:
        return True
    return False

def tr_undead_alchemist(game, abts, trig_obj, event_str):
    if event_str == 'lib_to_gy' and \
       trig_obj.owner == abts.obj.controller.next_player and \
       'Creature' in trig_obj.type_:
        return True
    return False
                                                     

def tr_werewolf_0(game, abts, trig_obj, event_str):
    if effects.tr_begin_upkeep(game, abts, trig_obj, event_str) and game.player[0].last_turn_storm_count == 0 and\
       game.player[1].last_turn_storm_count == 0:
        return True
    return False

def tr_werewolf_1(game, abts, trig_obj, event_str):
    if effects.tr_begin_upkeep(game, abts, trig_obj, event_str) and (game.player[0].last_turn_storm_count >= 2 or\
                                    game.player[1].last_turn_storm_count >= 2):
        return True
    return False

def tr_homicidal_brute(game, abts, trig_obj, event_str):
    if effects.tr_your_begin_end and not abts.obj.attacked_this_turn:
        return True
    return False

def tr_cursed_player_begin_upkeep(game, abts, trig_obj, event_str):
    if event_str == 'begin_upkeep' and game.active_player == abts.obj.attached_to:
        return True
    return False

def tr_reaper_from_the_abyss(game, abts, trig_obj, event_str):
    if event_str == 'begin_end' and game.morbid:
        return True
    return False

def tr_etb_morbid(game, abts, trig_obj, event_str):
    if effects.tr_self_etb(game, abts, trig_obj, event_str) and game.morbid:
        return True
    return False

def tr_mentor_of_the_meek(game, abts, trig_obj, event_str):
    if event_str == 'etb':
        if 'Creature' in trig_obj.type_ and trig_obj != abts.obj:
            if trig_obj.power <= 2 and trig_obj.controller == abts.obj.controller:
                return True
    return False

def tr_village_cannibals(game, abts, trig_obj, event_str):
    if event_str == 'bf_to_gy':
        if abts.type_word[0] in trig_obj.sub_type and 'Creature' in trig_obj.type_\
           and trig_obj != abts.obj:
            return True
    return False

def tr_another_creat_you_control_dies(game, abts, trig_obj, event_str):
    if event_str == 'bf_to_gy':
        if trig_obj.controller == abts.obj.controller and trig_obj!=abts.obj:
            return True
    return False

def tr_wooden_stake(game, abts, trig_obj, event_str):
    if event_str == 'block':
        if (abts.obj.attached_to == trig_obj[0] and abts.type_word[0] \
           in trig_obj[1].sub_type) or (abts.obj.attached_to == trig_obj[1] and abts.type_word[0] \
           in trig_obj[0].sub_type):
            return True
    return False

def tr_abattoir_ghoul(game, abts, trig_obj, event_str):
    if event_str == 'bf_to_gy':
        if abts.obj in trig_obj.damage_sources:
            return True
    return False

def tr_curse_of_stalked_prey(game, abts, trig_obj, event_str):
    if event_str == 'dealt_damage':
        if abts.obj.attached_to == trig_obj[1] and trig_obj[3]:
            return True
    return False

def tr_rakish_heir(game, abts, trig_obj, event_str):
    if event_str == 'dealt_damage':
        if abts.type_word[0] in trig_obj[0].sub_type and trig_obj[0].controller\
           == abts.obj.controller and trig_obj[1] in game.player and trig_obj[3]:
            return True
    return False

def tr_burning_vengeance(game, abts, trig_obj, event_str):
    if event_str == 'cast_from_gy':
        if trig_obj.controller == abts.obj.controller:
            return True
    return False

def tr_curiosity(game, abts, trig_obj, event_str):
    if event_str == 'dealt_damage':
        if trig_obj[0] == abts.obj.attached_to and trig_obj[1] ==\
        abts.controller.next_player and trig_obj[3]== True:
            return True
    return False

def tr_garruk_relentless(game, abts, trig_obj, event_str):
    abils = [sporab for sporab in game.stack if not sporab.spell]
    if abts.obj.counter['Loyalty']<=2 and not any([abil.abts==abts for abil in\
                                               game.stack]):
        return True
    return False

#target_tests

def ta_memorys_journey(game, sporab, target):
    if target == 'No target' or (target in sporab.target[0].graveyard \
                                 and target not in sporab.target):
        return True
    return False

def ta_runic_repetition(game, sporab, target):
    if effects.ta_basic(game, sporab, target) and (target in\
       game.exile):
        if target.owner == sporab.controller and any(['Flashback' in stab.rules_text\
                                                  for stab in target.cab.grav_static]):
            return True
    return False

def ta_victim_of_night(game, sporab, target):
    if effects.ta_creature(game, sporab, target):
        if sporab.type_word[0] not in target.sub_type \
       and sporab.type_word[1] not in target.sub_type and sporab.type_word[2]\
       not in target.sub_type:
            return True
    return False

def ta_slayer_of_the_wicked(game, sporab, target):
    if effects.ta_creature(game, sporab, target):
        if any([word in target.sub_type for word in sporab.type_word]):
            return True
    return False

def ta_avacynian_priest(game, sporab, target):
    if effects.ta_creature(game, sporab, target):
        if sporab.type_word[0] not in target.sub_type:
            return True
    return False

def ta_smite_the_monstrous(game, sporab, target):
    if effects.ta_creature(game, sporab, target):
        if target.power >= 4:
            return True
    return False

def ta_urgent_exorcism(game, sporab, target):
    if effects.ta_enchantment(game, sporab, target)\
        or effects.ta_creature_type(game, sporab, target):
        return True
    return False

def ta_creat_type_in_cont_gy(game, sporab, target):
    if effects.ta_creat_in_cont_gy(game, sporab, target):
        if sporab.type_word[0] in target.sub_type and target not in sporab.target:
            return True
    return False

def ta_snapcaster_mage(game, sporab, target):
    if effects.ta_card_in_cont_gy(game, sporab, target):
        if 'Sorcery' in target.type_ or 'Instant' in target.type_:
            return True
    return False

def ta_evil_twin(game, sporab, target):
    if effects.ta_creature(game, sporab, target):
        if target.name == sporab.obj.name:
            return True
    return False

#rule effects

def cl_olivia(game, rule, key):
    if rule.obj.controller!=rule.ref_obj[1]:
        rule.location.remove(rule)

def r_activate_stony_silence(game, rule, player, abts):
    if 'Artifact' in abts.obj.type_:
        return False
    return True

def r_cant_block_blazing_torch(game, rule, blocker, attacker):
    if attacker == rule.obj.attached_to:
        if rule.type_word[0] in blocker.sub_type or \
           rule.type_word[1] in blocker.sub_type:
            return False
    return True

def r_cant_block_stromkirk_noble(game, rule, blocker, attacker):
    if attacker == rule.obj:
        if rule.type_word[0] in blocker.sub_type:
            return False
    return True

def r_can_cast_flashback(game, rule):
    card = rule.obj
    flashback_cost = game.convert_cost_str(rule.name[10:])
    sorc = False
    if game.stack == [] and game.step in ('first_main', 'second_main'):
        sorc = True
    if card.owner == game.prior_player and ('Instant' in card.type_ or sorc):
        spell = classes.Spell(game, card.owner, rule.obj)
        spell.mana_cost = flashback_cost
        cost = classes.Cost()
        cost.test = [effects.test_true]
        cost.effect = [fun_flashback]
        spell.other_cost.append(cost)
        return [spell]
    return []

def r_can_cast_self(game, rule):
    if effects.card_timing(game, rule.obj.owner, rule.obj) and \
       game.prior_player == rule.obj.owner:
        return [classes.Spell(game, rule.obj.owner, rule.obj)]
    return []

def r_alt_cost_rooftop_storm(game, rule, cast_list):
    alt_list = []
    for spell in cast_list:
        if 'Creature' in spell.type_ and rule.type_word[0] in spell.sub_type:
            spell2 = classes.Spell(game, rule.obj.controller, spell.card)
            spell2.mana_cost = [0,0,0,0,0,0]
            alt_list.append(spell2)
    cast_list.extend(alt_list)

def r_cant_block_orchard_spirit(game, rule, blocker, attacker):
    if attacker == rule.obj:
        if 'Flying' not in blocker.cab.keyword and 'Reach' not in blocker.cab.keyword:
            return False
    return True

def r_parallel_lives(game, rule, player, number):
    if player == rule.obj.controller:
        return 2*number
    return number

def la_1_olivia_voldaren(game, rule):
    rule.ref_obj[0].controller = rule.ref_obj[1]

def la_5_blazing_torch(game, rule):
    abts = classes.AbilToStack()
    abts.sporab_target.append(effects.ta_creature_or_player)
    abts.ef_list.insert(0, [effects.ref_obj_targeted_damage, 2])
    abts.other_cost.append(classes.Cost())
    cost = classes.Cost()
    cost.test = [effects.test_true]
    cost.effect = [effects.fun_sac_ref_obj]
    abts.other_cost.append(cost)
    abts.ref_obj.append(rule.obj)
    abts.rules_text = '{T}, Sacrifice Blazing Torch: Blazing Torch deals '\
                      +'2 damage to target creature or player.'
    rule.obj.attached_to.cab.act.append(abts)

def la_5_skeletal_grimace(game, rule):
    abts = classes.AbilToStack()
    abts.ef_list.insert(0, [effects.abil_obj_regenerate])
    abts.mana_cost = [0,0,1,0,0,1]
    abts.rules_text = '{1}{B}: Regenerate '+rule.obj.attached_to.name+'.'
    rule.obj.attached_to.cab.act.append(abts)

def la_5_intangible_virtue(game, rule):
    for perm in game.battlefield:
        if not perm.card.real and 'Creature' in perm.type_ and perm.controller\
           == rule.obj.controller:
            perm.cab.keyword.append('Vigilance')

def la_8_intangible_virtue(game, rule):
    for perm in game.battlefield:
        if not perm.card.real and 'Creature' in perm.type_ and perm.controller\
           == rule.obj.controller:
            perm.power+=1
            perm.toughness+=1

def la_8_one_eyed_scarecrow(game, rule):
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and perm.controller !=rule.obj.controller:
            if 'Flying' in perm.cab.keyword:
                perm.power-=1

def la_5_spare_from_evil(game, rule, creat_list):
    for perm in creat_list:
        if effects.is_creature(game, perm):
            perm.cab.keyword.append('Protection from non-Human creatures')

def la_5_type_gains_keyword(game, rule, keyword):
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and rule.type_word[0] in perm.sub_type\
           and perm.controller == rule.obj.controller:
            perm.cab.keyword.append(keyword)

def la_5_manor_gargoyle(game, rule):
    if 'Defender' in rule.obj.cab.keyword:
        rule.obj.cab.keyword.remove('Defender')
    rule.obj.cab.keyword.append('Flying')

def la_8_type_plus(game, rule, power, toughness):
    for perm in game.battlefield:
        if 'Creature' in perm.type_ and rule.type_word[0] in perm.sub_type\
           and perm.controller == rule.obj.controller:
            perm.power+=power
            perm.toughness+=toughness

def la_8_curse_of_deaths_hold(game, rule):
    for perm in game.battlefield:
        if perm.controller == rule.obj.attached_to and 'Creature' in perm.type_:
            perm.power -= 1
            perm.toughness -= 1

def la_8_instigator_gang(game, rule, power, toughness):
    for perm in game.battlefield:
        if perm.controller == rule.obj.controller and perm in game.attackers:
            perm.power += power
            perm.toughness += toughness

def la_8_howlpack_alpha(game, rule):
    for perm in game.battlefield:
        if perm.controller == rule.obj.controller and perm != rule.obj and \
           (rule.type_word[0] in perm.sub_type or rule.type_word[1] in \
            perm.sub_type) and 'Creature' in perm.type_:
            perm.power +=1
            perm.toughness += 1

def la_8_wreath_of_geists(game, rule):
    number = len([card for card in rule.obj.controller.graveyard if 'Creature'\
                  in card.type_])
    rule.obj.attached_to.power+=number
    rule.obj.attached_to.toughness+=number

def r_attack_curse_of_the_nightly_hunt(game, rule, attacks):
    if game.active_player == rule.obj.attached_to:
        return len(attacks)
    return 0

def r_block_terror_of_kruin_pass(game, rule, blocks):
    werewolves = []
    for item in blocks:
        if rule.type_word[0] in item[1].sub_type and rule.obj.controller == \
           item[1].controller:
            location = [item[1] in pair for pair in werewolves]
            if any(location):
                werewolves[location.index(True)][1]+=1
            else:
                werewolves.append([item[1], 1])
    for item in werewolves:
        if item[1] == 1:
            return -effects.INF
    return 0

def la_5_past_in_flames(game, rule, card_list):
    for card in card_list:
        if 'Instant' in card.type_ or 'Sorcery' in card.type_ and card in \
           rule.obj.controller.graveyard:
            stab = classes.StaticAbil()
            stab.effect = [flashback]
            stab.rules_text = 'Flashback '+game.print_cost(card.mana_cost)
            card.cab.grav_static.append(stab)

def la_5_snapcaster_mage(game, rule):
    card = rule.ref_obj[0]
    stab = classes.StaticAbil()
    stab.effect = [flashback]
    stab.rules_text = 'Flashback '+game.print_cost(rule.ref_obj[0].mana_cost)
    card.cab.grav_static.append(stab)
        
def r_obj_char_fiend_hunter(game, rule):
    for item in game.trig_abil:
        if item.obj == rule.obj and 'return the exiled card to the battlefield'\
           in item.rules_text:
            if rule.ref_obj[1] in game.exile:
                item.ref_obj=rule.ref_obj[1:]
                pointer = ['Exiled card: ', rule.ref_obj[1]]
                if pointer not in rule.obj.pointer:
                    rule.obj.pointer.append(pointer)
            elif rule.ref_obj[1] in item.ref_obj:
                item.ref_obj.remove(rule.ref_obj[1])
                rule.obj.pointer = []

def r_obj_char_nevermore(game, rule):
    for item in game.rule_cant_cast:
        if item.obj == rule.obj and 'named card' in item.name:
            item.ref_obj.append(rule.ref_obj[0])
            pointer = ['Named card: ', rule.ref_obj[0]]
            rule.obj.pointer[:1] = [pointer]

def r_cost_dec_heartless_summoning(game, rule, sporab):
    if sporab.spell:
        if'Creature' in sporab.type_ and sporab.controller == rule.obj.controller:
            sporab.mana_cost[5] -= min([sporab.mana_cost[5], 2])

def r_damage_inquisitors_flail0(game, rule, source, target, amount,
                                combat):
    if combat and source == rule.obj.attached_to:
        return [source, target, 2*amount]
    return False

def r_damage_undead_alchemist(game, rule, source, target, amount, combat):
    if combat and rule.type_word[0] in source.sub_type and source.controller\
       == rule.obj.controller and target in game.player:
        effects.mill(game, target, amount)
        return [source, target, 0]
    return False

def r_damage_unbreathing_horde(game, rule, source, target, amount, combat):
    if target == rule.obj:
        rule.obj.counter['+1/+1']-=min([rule.obj.counter['+1/+1'], 1])
        game.update_battlefield()
        return [source, target, 0]
    return False

def r_damage_inquisitors_flail1(game, rule, source, target, amount, combat):
    if combat and target == rule.obj.attached_to:
        return [source, target, 2*amount]
    return False

def r_damage_moonmist(game, rule, source, target, amount, combat):
    if 'Creature' in source.type_:
        if rule.type_word[1] not in source.sub_type and rule.type_word[2] not\
           in source.sub_type:
            return [source, target, 0]
    return False

def r_cant_cast_nevermore(game, rule, spell):
    if spell.name == rule.ref_obj[0].name:
        return False
    return True

def r_laboratory_maniac(game, rule, player):
    if player == rule.obj.controller:
        return True
    else:
        return False

def r_target_witchbane_orb(game, rule, sporab, target):
    if target == rule.obj.controller and sporab.controller == \
       rule.obj.controller.next_player:
        return False
    return True

def r_leave_stack_flashback(game, rule, spell):
    if spell == rule.obj:
        game.stack.remove(spell)
        if spell.card.real:
            game.exile.append(spell.card)
            output.output(game, spell.controller, spell.card.name + \
                          ' went to exile')
        rule.location.remove(rule)

def r_leave_stack_dissipate(game, rule, spell):
    if spell in rule.ref_obj:
        game.stack.remove(spell)
        if spell.card.real:
            output.output(game, spell.controller, spell.card.name +
                          ' went to exile')
            game.exile.append(spell.card)
        rule.location.remove(rule)
        
#choices made while costing

def choose_harvest_pyre(game, sporab):
    output.output(game, sporab.controller, 'Choose a value for X:', '')
    value = game.int_input(sporab.controller, l_range = 0)
    sporab.other_cost[0].effect[1] = value
    sporab.ef_list[0][1] = value

def choose_mikaeus_the_lunarch(game, sporab):
    output.output(game, sporab.controller, 'Choose a value for X:', '')
    value = game.int_input(sporab.controller, l_range = 0)
    sporab.mana_cost[5]+=value
    repef = classes.ReplacementEffect()
    repef.test = effects.ase_test_true
    repef.effect = [effects.enters_with_counter, '+1/+1', value]
    repef.name = 'Mikaeus, the Lunarch enters the battlefield '+\
                 'with '+str(value)+' +1/+1 counters on it'
    sporab.cab.as_enters.append(repef)
    
#alternate costs

def test_skirsdag_high_priest(game, player, abts):
    elig_list = [perm for perm in game.battlefield if not perm.tapped and \
                 'Creature' in perm.type_ and perm.controller == \
                 abts.obj.controller and perm!=abts.obj]
    if len(elig_list)>=2:
        return True
    return False

def fun_skirsdag_high_priest(game, player, abil):
    elig_list = [perm for perm in game.battlefield if not perm.tapped and \
             'Creature' in perm.type_ and perm.controller == \
             abil.obj.controller and perm!=abil.obj]
    if len(elig_list)>=2:
        item1 = effects.choose_obj_from_list(game, player, elig_list, \
                            'Choose a creature to tap')
        elig_list.remove(item1)
        item2 = effects.choose_obj_from_list(game, player, elig_list, \
                            'Choose a creature to tap')
        effects.become_tapped(game, item1)
        effects.become_tapped(game, item2)
        game.update_battlefield()
        return True
    return False

def test_exile_creat_from_gy(game, player, abts):
    elig_list = [card for card in player.graveyard if 'Creature' in card.type_]
    if len(elig_list)>0:
        return True
    return False

def fun_exile_creat_from_gy(game, player, sporab):
    elig_list = [card for card in player.graveyard if 'Creature' in card.type_]
    if len(elig_list)==0:
        return False
    choice = effects.choose_obj_from_list(game, player, elig_list, prompt = \
                                      'Choose a creature card to exile')
    sporab.ref_obj.append(choice)
    player.graveyard.remove(choice)
    choice1 = effects.card_copy(choice.base, choice.owner)
    print choice1.name + ' exiled from '+player.name+'\'s graveyard'
    game.exile.append(choice1)
    game.undo_list.append([undo_exile_card_from_gy, choice1])
    game.update_battlefield()
    return True

def fun_flashback(game, player, sporab):
    rule = classes.SporabRule(sporab, game.rule_leave_stack)
    rule.cleanup = effects.cl_never
    rule.effect = [r_leave_stack_flashback]

def test_exile_cards_from_gy(game, player, abts, cards):
    if len(player.graveyard)>=cards:
        return True
    else:
        return False

def fun_exile_cards_from_gy(game, player, spell, cards):
    if len(player.graveyard)>=cards:
        for i in range(cards):
            choice = effects.choose_obj_from_list(game, player, player.graveyard,
                                            'Choose a card to exile')
            player.graveyard.remove(choice)
            choice1 = effects.card_copy(choice.base, choice.owner)
            game.exile.append(choice1)
            output.output(game, player, choice1.name+' was exiled from '+\
                          player.name+'\'s graveyard')
            game.update_battlefield()
        return True
    return False

def test_skaab_goliath(game, player, card):
    elig_list = [card for card in player.graveyard if 'Creature' in card.type_]
    if len(elig_list)>1:
        return True
    return False

def test_skaab_ruinator(game, player, card):
    elig_list = [card for card in player.graveyard if 'Creature' in card.type_]
    if len(elig_list)>=3:
        return True
    return False

def fun_skaab_goliath(game, player, spell):
    if fun_exile_creat_from_gy(game, player, spell) and \
       fun_exile_creat_from_gy(game, player, spell):
        return True
    else:
        return False

def fun_skaab_ruinator(game, player, spell):
    if fun_exile_creat_from_gy(game, player, spell) and \
       fun_exile_creat_from_gy(game, player, spell) and \
       fun_exile_creat_from_gy(game, player, spell):
        return True
    else:
        return False

def test_mill_one(game, player, abts):
    if len(player.lib)>0:
        return True
    return False

def fun_mill_one(game, player, sporab_or_abts):
    if len(player.lib)==0:
        return False
    card = player.lib[-1]
    effects.mill(game, player, 1)
    game.undo_list.append([undo_mill_one, card])

def test_back_from_the_brink(game, player, abts):
    elig_list = [card for card in player.graveyard if 'Creature' in card.type_\
                 and effects.test_can_pay_mana(game, player, card.mana_cost)]
    if len(elig_list)>0:
        return True

def fun_back_from_the_brink(game, player, abil):
    elig_list = [card for card in player.graveyard if 'Creature' in card.type_\
                 and effects.test_can_pay_mana(game, player, card.mana_cost)]
    if len(elig_list)==0:
        return False
    if len(elig_list)==1:
        choice = elig_list[0]
    else:
        choice = effects.choose_obj_from_list(game, player, elig_list, prompt = \
                                      'Choose a creature card to exile')
    player.graveyard.remove(choice)
    choice = effects.card_copy(choice.base, choice.owner)
    print choice.name + ' exiled from '+player.name+'\'s graveyard'
    game.exile.append(choice)
    abil.ref_obj.append(choice)
    game.undo_list.append([undo_exile_card_from_gy, choice])
    if effects.pay_mana_cost(game, player, choice.mana_cost):
        return True
    else:
        game.undo()
        return False

def test_grimgrin_corpse_born(game, player, abts):
    if any(['Creature' in perm1.type_ for perm1 in game.battlefield if \
            player == perm1.controller and perm1!=abts.obj]):
        return True
    return False

def fun_grimgrin_corpse_born(game, player, sporab_or_abts):
    creat_list = [perm1 for perm1 in game.battlefield if 'Creature' in perm1.type_ and \
                  perm1.controller == player and perm1!=sporab_or_abts.obj]
    if creat_list == []:
        return False
    creat = effects.choose_obj_from_list(game, player, creat_list,
                                 'Choose a creature to sacrifice')
    effects.die(game, creat)
    game.update_battlefield()
    game.add_to_tst([creat, 'bf_to_gy'])
    sporab_or_abts.ref_obj.append(creat)
    game.undo_list.append([effects.undo_sacrifice, creat])
    return True

def ase_test_morbid(game, repef, perm):
    if game.morbid:
        return True
    return False

def ase_test_duals(game, repef, perm):
    if any([(repef.type_word[0] in item.sub_type or
            repef.type_word[1] in item.sub_type) and
            item.controller == perm.controller\
            for item in game.battlefield]):
        return False
    return True

def ase_test_dearly_departed(game, repef, perm):
    if repef.type_word[0] in perm.sub_type and repef.obj.owner == perm.controller:
        return True
    return False

def ase_dearly_departed(game, repef, perm):
    effects.enters_with_counter(game, perm, '+1/+1', 1)

def ase_nevermore(game, repef, perm):
    found = False
    while not found:
        output.output(game, perm.controller, 'Name a nonland card', '')
        card_name = game.get_input(perm.controller)
        if card_name in game.card_dict:
            card = game.card_dict[card_name]
            if 'Land' not in card.type_:
                found = True
    rule = classes.Data()
    rule.timestamp = perm.timestamp
    rule.obj = perm
    rule.effect = [r_obj_char_nevermore]
    rule.location = game.rule_obj_char
    rule.color_word = []
    rule.type_word = []
    rule.ref_obj = [card]
    rule.cleanup = effects.cl_rule_obj_gone
    rule.name = perm.name+'\'s ability'
    rule.location.append(rule)

def ase_unbreathing_horde(game, repef, perm):
    zombies = [card for card in perm.controller.graveyard if repef.type_word[0]\
               in card.sub_type and 'Creature' in card.type_]+[item for \
                item in game.battlefield if repef.type_word[0] in item.sub_type\
                and 'Creature' in item.type_ and perm.controller == \
                        item.controller]
    effects.enters_with_counter(game, repef, perm, '+1/+1', len(zombies))

def ase_essence_of_the_wild(game, repef, perm):
    perm.base = classes.PermBase(repef.obj.base)

def ase_evil_twin(game, repef, perm):
    creats = [item for item in game.battlefield if 'Creature' in item.type_]
    if len(creats)>0:
        print repef.name
        if effects.may_choose(game, perm.controller):
            choice = effects.choose_obj_from_list(game, perm.controller, creats,
                            'Choose a creature on the battlefield to copy')
            perm.base = classes.PermBase(choice.base)
            abts = classes.AbilToStack()
            abts.mana_cost = [0,1,1,0,0,0]
            abts.rules_text = '{U}{B}, {T}: Destroy target creature with the same name as this creature.'
            abts.other_cost.append(classes.Cost())
            abts.ef_list.insert(0, [effects.targeted_destroy])
            abts.sporab_target.append(ta_evil_twin)
            perm.base.cab.act.append(abts)

def choose_ghoulcallers_chant(game, spell):
    index1 = spell.rules_text.index(' - ')+3
    index2 = spell.rules_text.index('; ')
    print 'Choose a mode:'
    print '1. '+spell.rules_text[index1:index2]
    print '2. '+spell.rules_text.splitlines()[0][index2+2:]
    index = game.int_input(spell.controller, u_range = 2)
    spell.ef_list.pop(2-index)
    if index == 1:
        spell.sporab_target.append(effects.ta_creat_in_cont_gy)
    if index == 2:
        spell.sporab_target.append(ta_creat_type_in_cont_gy)
        spell.sporab_target.append(ta_creat_type_in_cont_gy)
    
def cost_red_blasphemous_act(game, spell):
    creat_list = [perm for perm in game.battlefield if 'Creature' in perm.type_]
    spell.mana_cost[5]-=min([len(creat_list), spell.mana_cost[5]])
                                          
        
