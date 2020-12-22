
# kevin likes my stream of conscious comments, so lets keep going with that,
# although i think this is mostly self-explanatory.

with open('21input1.txt', 'r') as f:
    nutritional_info = [line.split(' (contains ') for line in f.read().split('\n')]
    allergens = {}
    for i, info in enumerate(nutritional_info):
        ingredient_list, allergen_list = info
        ingredient_list = ingredient_list.split(' ')
        allergen_list = allergen_list.split(', ')
        allergen_list[-1] = allergen_list[-1][0:-1]

        # this is really where the easy magic happens. all we know is that
        # lines marked "contains X" DEFINITELY contains X. but a line
        # not saying "contains X" doesn't mean that line doesn't contain X.
        # so to get the list of ingredients that could contain X, intersect
        # all the ingredients in the line that contain X.  (if a line has
        # y and z and contains X, and another line has y and a and contains X,
        # the ingredient that contains X must be y, the common ingredient
        # between the two food items)
        for allergen in allergen_list:
            if allergen not in allergens:
                allergens[allergen] = set(ingredient_list)
            else:
                allergens[allergen] &= set(ingredient_list)
        nutritional_info[i] = [ingredient_list, allergen_list]

    # great, now we can get a list of possibly allergenic ingredients.
    possibly_allergenic_ingredients = set()
    for allergen in allergens:
        possibly_allergenic_ingredients |= allergens[allergen]
    
    # and we only care about ingredients that are not allergenic, so pull
    # those out, but allow duplicates.
    inert_ingredients = []
    for ingredient_list, allergen_list in nutritional_info:
        for ingredient in ingredient_list:
            if ingredient not in possibly_allergenic_ingredients:
                inert_ingredients.append(ingredient)

    # and that's part 1
    print(len(inert_ingredients))

    # part 2
    # this is pretty easy. find the allergen with only one possible
    # ingredient. when it's found, add that to our map, and
    # remove that ingredients from the all lists of other allergen's
    # possible names. eventually, you'll get down to the full map.
    allergen_ingredient_map = {}
    while len(allergens) > 0:
        for allergen in allergens:
            if len(allergens[allergen]) == 1:
                allergen_to_remove = list(allergens[allergen])[0]
                allergen_ingredient_map[allergen] = allergen_to_remove
                for allergen_2 in allergens:
                    if allergen_to_remove in allergens[allergen_2]:
                        allergens[allergen_2].remove(allergen_to_remove)
                break
        # can't del on a dict in a loop on that dict, so we break
        # out and del out here
        del allergens[allergen]

    # and then do the output
    canonical_ingredient = ""
    for allergen in sorted(allergen_ingredient_map.keys()):
        canonical_ingredient += allergen_ingredient_map[allergen] + ','
    print(canonical_ingredient[0:-1])