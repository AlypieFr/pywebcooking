class RecipeConfigGlobal:
    directory_photos = "/Photos/"
    photo_in_recipe_width = "254px"


class RecipeConfigEn (RecipeConfigGlobal):
    ingredients_short = "Ingredients (for %d people):"
    ingredients_short_1p = "Ingredients (for %d person):"
    ingredients_long = "Ingredients (for %d people (%s)):"
    ingredients_long_1p = "Ingredients (for %d person (%s)):"
    ingredients_range_short = "Ingredients (from %d to %d people):"
    ingredients_range_long = "Ingredients (from %d to %d people (%s)):"
    equipment = "Required equipment:"
    instructions = "Instructions:"
    proposals = "Proposals:"
    timePreparation = "Prep:"
    timeCuis = "Cook:"
    timeRep = "Break:"


class RecipeConfigFr (RecipeConfigEn):
    ingredients_short = "Ingrédients (pour %d personnes)&#8239;:"
    ingredients_short_1p = "Ingrédients (pour %d personne)&#8239;:"
    ingredients_long = "Ingrédients (pour %d personnes (%s))&#8239;:"
    ingredients_long_1p = "Ingrédients (pour %d personne (%s))&#8239;:"
    ingredients_range_short = "Ingrédients (de %d à %d personnes)&#8239;:"
    ingredients_range_long = "Ingrédients (de %d à %d personnes (%s))&#8239;:"
    equipment = "Matériel nécessaire&#8239;:"
    instructions = "Préparation&#8239;:"
    proposals = "Conseils&#8239;:"
    timePreparation = "Temps de préparation&#8239;:"
    timeCuis = "Temps de cuisson&#8239;:"
    timeRep = "Temps de repos&#8239;:"
