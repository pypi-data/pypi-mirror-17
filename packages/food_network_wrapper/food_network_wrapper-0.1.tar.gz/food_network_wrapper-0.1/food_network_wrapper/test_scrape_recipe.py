from food_network_wrapper import scrape_recipe

def test_apple_crisp():
    recipe = scrape_recipe("http://www.foodnetwork.com/recipes/apple-crisp.html")
    assert recipe.title == "Apple Crisp"
    assert recipe.author == "Kelsey Nixon"
    assert recipe.total_time == "1 hr 10 min"
    assert recipe.prep_time == "25 min"
    assert recipe.cook_time == "45 min"
    assert recipe.servings == "6 to 8 servings"
    assert recipe.level == "Easy"
    assert recipe.picture_url == "http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2010/10/21/1/CCKEL109L_Apple-Crisp_s4x3.jpg.rend.sni12col.landscape.jpeg"
    assert recipe.ingredients == [
            "6 baking apples, peeled, cored, and cut into wedges",
            "1 tablespoon lemon juice",
            "1/2 cup sugar",
            "2 tablespoons flour",
            "1 1/4 cups flour",
            "1/2 cup rolled oats",
            "1/2 cup light brown sugar",
            "1/2 teaspoon ground cinnamon",
            "1/4 teaspoon salt",
            "12 tablespoons butter (1 1/2 sticks), chilled and cut into small pieces",
            "1/2 cup nuts, coarsely chopped and toasted",
    ]
    assert recipe.directions == [
            "Preheat the oven to 350 degrees F.",
            "For the fruit filling:",
            "In a large mixing bowl, toss together the apples, lemon juice, sugar, and flour. Pour the apple mixture into a buttered 2-quart baking dish and set aside.",
            "For the topping:",
            "In a large mixing bowl, mix the flour, rolled oats, brown sugar, cinnamon, and salt. With a food processor, a pastry blender, or your fingers work the butter into the flour mixture just until it comes together and large clumps form. Fold nuts into mixture.",
            "Sprinkle the topping evenly over the fruit. Bake the apple crisp until the fruit is bubbling and the topping is golden brown and crisp, about 45 minutes.",
            "Serve the crisps warm with vanilla bean ice cream or fresh whipped cream, if desired.",
    ]
    assert recipe.categories == ["Apple", "Dessert", "Pastry"]
