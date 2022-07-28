import requests
from bs4 import BeautifulSoup

def get_recipe_url():
    url = input("What's the URL for the recipe you would like to view? ")
    return url

def is_recipe_ingredients_but_not_nutrition_info(tag):
    return tag.has_attr('class') and "recipe-ingredients" in tag["class"] and tag.name == "ul" and len(tag.find_all("div", class_="nutrition-container")) == 0

def parse_data_from_html(recipe):
    parsed_recipe = {}
    parsed_recipe["title"] = title = recipe.body.find("h1", class_="recipe-title")
    parsed_recipe["byline"] = recipe.body.find("div", class_="nytc---recipebyline---bylinePart").a
    yield_time_list = recipe.body.find("ul", class_="recipe-time-yield").find_all("li")
    parsed_recipe["yield_amount"] = yield_time_list[0].find("span", class_="recipe-yield-value")
    parsed_recipe["time"] = yield_time_list[1].find("span", class_="recipe-yield-value")
    
    topnote = recipe.body.find("div", class_="topnote")
    if topnote:
        parsed_recipe["topnote"] = topnote.p

    parsed_recipe["ingredients_title"] = recipe.body.find("section", class_="recipe-ingredients-wrap").find("h3", class_="recipe-instructions-heading")
    ingredients_parts = recipe.body.find("section", class_="recipe-ingredients-wrap").find_all(is_recipe_ingredients_but_not_nutrition_info)
    ingredients_parts_list = []
    for ingredients_part in ingredients_parts:
        part_name = ingredients_part.find_previous_sibling("h4")
        if part_name:
            part_name = part_name.text
        ingredients_list = []
        for ingredient in ingredients_part.find_all("li"):
            ingredients_list.append((ingredient.span.text.strip(), ingredient.span.next_sibling.next_sibling.text.strip()))
        ingredients_parts_list.append((part_name, ingredients_list))
    parsed_recipe["ingredients_parts_list"] = ingredients_parts_list
    
    parsed_recipe["instructions_title"] = recipe.body.find("section", class_="recipe-steps-wrap").find("h3", class_="recipe-instructions-heading")
    instructions = recipe.body.find("ol", class_="recipe-steps")
    instructions_list = []
    for instruction in instructions.find_all("li"):
        instructions_list.append(instruction.text.strip())
    parsed_recipe["instructions_list"] = instructions_list

    parsed_recipe["notes_title"] = recipe.body.find("h4", class_="recipe-notes-header")
    notes = recipe.body.find("ul", class_="recipe-notes")
    if notes:
        notes_list = []
        for note in notes.find_all("li"):
            notes_list.append(note.text.strip())
        parsed_recipe["notes_list"] = notes_list
    return parsed_recipe

def print_recipe(recipe):
    print(recipe['title'].text.strip())
    print("By:", recipe['byline'].text)
    print()
    print("Yield:", recipe['yield_amount'].text)
    print("Time:", recipe['time'].text)
    if "topnote" in recipe.keys():
        print()
        print(recipe['topnote'].text)
    print()
    print(f"{recipe['ingredients_title'].text.strip()}:")
    for part_name, part_list in recipe['ingredients_parts_list']:
        if part_name:
            print(part_name)
        for quantity, name in part_list:
            print("-", quantity, name)
    print()
    print(f"{recipe['instructions_title'].text.strip()}:")
    for number, instruction in enumerate(recipe['instructions_list']):
        print(f"{number}. {instruction}")
    if "notes_list" in recipe.keys():
        print()
        print(f"{recipe['notes_title'].text.strip()}:")
        for note in notes_list:
            print("-", note)
def main():
    # For testing, use a local html file
    # with open("html_examples/nyt2.html") as fp:
        # recipe = BeautifulSoup(fp, 'html.parser')

    url = get_recipe_url()
    r = requests.get(url)
    recipe = BeautifulSoup(r.text, 'html.parser')
    recipe = parse_data_from_html(recipe)
    print_recipe(recipe)

main()
