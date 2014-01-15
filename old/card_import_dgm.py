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
import dgm_effects
import classes

card = card_dict['Steeple Roc']
card.cab.keyword.append('First strie')

card = card_dict['Boros Mastiff']
stab = classes.StaticAbil()
stab.rules_text = card.rule_text
stab.effect = [dgm_effects.boros_mastiff]
card.cab.trig.append(stab)

card = card_dict['Haazda Snare Squad']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.haazda_snare_squad]
card.cab.trig.append(stab)

card = card_dcit['Scion of Vitu-Ghazi']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.scion_of_vitu_ghazi]
card.cab.trig.append(stab)

card = card_dict['Sunspire Gatekeepers']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.sunspire_gatekeepers]
card.cab.trig.append(stab)

card = card_dict['Opal Lake Gatekeepers']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.opal_lake_gatekeepers]
card.cab.trig.append(stab)

card = card_dict['Ubur Sar Gatekeepers']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.ubur_sar_gatekeepers]
card.cab.trig.append(stab)

card = card_dict['Smelt-Ward Gatekeepers']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.smelt_ward_gatekeepers]
card.cab.trig.append(stab)

card = card_dict['Battering Krasis']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[1]
stab.effect = [gtc_effects.evolve]
card.cab.trig.append(stab)

card = card_dict['Renegade Krasis']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[0]
stab.effect =[gtc_effects.evolve]
card.cab.trig.append(stab)
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[1]
stab.effect = [dgm_effects.renegade_krasis]
card.cab.trig.append(stab)

card = card_dict['Saruli Gatekeepers']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.saruli_gatekeepers]
card.cab.trig.append(stab)

card = card_dict['Ascended Lawmage']
card.cab.keyword.append('Hexproof')

card = card_dict['Blaze Commando']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.blaze_commando]
card.cab.trig.append(stab)

card = card_dict['Boros Battleshaper']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.boros_battleshaper]
card.cab.trig.append(stab)

card = card_dict['Bred for the Hunt']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.bred_for_the_hunt]
card.cab.trig.append(stab)

card = card_dict['Bronzebeak Moa']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.bronzebeak_moa]
card.cab.trig.append(stab)

card = card_dict['Deadbridge Chant']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[0]
stab.effect = [dgm_effects.deadbridge_chant_0]
card.cab.trig.append(stab)
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[1]
stab.effect = [dgm_effects.deadbridge_chant_1]
card.cab.trig.append(stab)

card = card_dict['Deputy of Acquittals']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[1]
stab.effect = [dgm_effects.deputy_of_acquittals]
card.cab.trig.append(stab)

card = card_dict['Fluxcharger']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[1]
stab.effect = [dgm_effects.fluxcharger]
card.cab.trig.append(stab)

card = card_dict['Gleam of Battle']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text
stab.effect = [dgm_effects.gleam_of_battle]
card.cab.trig.append(stab)

card = card_dict['Jelenn Sphinx']
card.cab.keyword.append('Vigilance']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[1]
stab.effect = [dgm_effects.jelenn_sphinx]
card.cab.trig.append(stab)

card = card_dict['Lavinia of the Tenth']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[1]
stab.effect = [dgm_effects.lavinia_of_the_tenth]
card.cab.trig.append(stab)

card = card_dict['Miro Vosk, Mind Drinker']
stab = classes.StaticAbil()
stab.rules_text = card.rules_text.splitlines()[1]
stab.effect = [dgm_effects.miro_vosk]
card.cab.trig.append(stab)
