def perm_from_cop_val(game, perm):
    perm.cab = cab_copy(perm.cop_val.cab, True)
    perm.name = perm.cop_val.name
    perm.sup_type = perm.cop_val.sup_type
    perm.type_ = perm.cop_val.type_
    perm.sub_type = perm.cop_val.sub_type
    perm.power = perm.cop_val.power
    perm.mana_cost = perm.cop_val.mana_cost
    perm.color_indicator = list(perm.base.color_indicator)
    perm.toughness = perm.base.toughness
    perm.controller = perm.original_controller
    perm.color = list(perm.color_indicator)
    if perm.mana_cost != None:
        for i in range(5):
            if perm.mana_cost[i]>0:
                perm.color.append(COLOR_WORDS[i])
    perm.indestructible = False
