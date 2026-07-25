from pathlib import Path 
from time import sleep
from os import chdir, mkdir, remove, rmdir


#Get existing elements in a given uhhhhhh you know in a given directory.
def get_existing_elements_listing(current_directory):
    
    elements_to_choose_from = []

    for num, element in enumerate(current_directory.glob("*")):
        print(f"[{num + 1}. {element.name}]\n")
        elements_to_choose_from.append((num + 1, element))
    
    return elements_to_choose_from



#Go into a directory
def access_directory(current_directory, objective_element):

    directory_path = Path(current_directory, objective_element) 

    if directory_path.is_dir():
        chdir(directory_path)
        



#Get the element count for recipes and categories. This is for intial element validation so the user dont access to tools he wouldnt have the elements for
def get_elements_count(cur_directory):
    
    number_of_recipes = 0
    number_of_categories = 0

    for element in cur_directory.rglob("*"):
        if element.suffix == ".txt":
            number_of_recipes += 1

    for element in cur_directory.glob("*"):
        number_of_categories += 1

    return number_of_recipes, number_of_categories


    
#checks for "Recetas" in the same directory the script is in
def archives_validation(cur_directory, target_directory): 

    for element in cur_directory.glob("*"):

        if element.name == target_directory:
            return True



#String input checks
def string_input(string_type_flag):

    while True:

        if string_type_flag == "yes_or_no":

            new_y_or_n_input = input("\n\nColoque s para SI o n para NO. ")

            if new_y_or_n_input not in ["s", "n"]:
                print("Input invalido, coloca s para SI o n para NO.")
                continue
            
            return new_y_or_n_input
        
        if string_type_flag == "archive_name":

            new_name_input = input("\n\nColoque el nombre del archivo/directorio: ")

            if len(new_name_input) > 35:
                print("El nombre del archivo es demasiado largo, considera otro")
                continue

            return new_name_input
        
        if string_type_flag == "recipe_content":

            new_content_input = input("\n\nColoque el contenido de la receta: ")

            if len(new_content_input) > 90:
                print("La receta superó el limite de caracteres, considera hacerla mas pequeña.")
                continue

            return new_content_input
        


#Numerical input check
def numerical_input():

    while True:

        try:
            new_numerical_input = int(input("\n\nColoque un numero. "))
        except ValueError:
            print("ERROR: tu input no es un numero valido, intentalo de nuevo.")
            continue

        return new_numerical_input


#The menu, self explanatory
def options_menu(number_of_recipes, number_of_categories, main_options_message, base_directory):
    
    
    while True:
        print(main_options_message)
        new_numerical_input = numerical_input()
        
        if new_numerical_input < 1 or new_numerical_input > 6:
            print("NUMERO FUERA DE RANGO.")
            continue

        match new_numerical_input:

            case 1:
                
                if number_of_categories == 0:
                    print("ATENCIÓN: La acción solicitada es imposible de hacer. No hay categorias disponibles.")
                    continue
                
                if number_of_recipes == 0 and number_of_categories != 0:
                    print("ATENCIÓN: La acción solicitada es imposible de hacer. No hay recetas disponibles en ninguna categoria.")
                    continue
                
                return read_recipe(base_directory)
            
            case 2:
                
                if number_of_categories == 0:
                    print("ATENCIÓN: La acción solicitada es imposible de hacer. No hay categorias disponibles.")
                    continue
                
                return create_recipe(base_directory)

            case 3:
                return create_category(base_directory)

            case 4:
                
                if number_of_categories == 0:
                    print("ATENCIÓN: La acción solicitada es imposible de hacer. No hay categorias disponibles.")
                    continue
                
                if number_of_recipes == 0 and number_of_categories != 0:
                    print("ATENCIÓN: La acción solicitada es imposible de hacer. No hay recetas disponibles en ninguna categoria.")
                    continue
                
                return delete_recipe(base_directory)
            
            case 5:
                
                if number_of_categories == 0:
                    print("ATENCIÓN: La acción solicitada es imposible de hacer. No hay categorias disponibles.")
                    continue

                return delete_category(base_directory)
                
            case 6:

                print("\nSESIÓN FINALIZADA.")
                exit(0)

            case _:

                print("Error de logica. ???????????????")
                continue


#Program available actions
def read_recipe(current_directory): 

    ## categories
    print("Entra a una categoria: \n\n")
    choose_list = get_existing_elements_listing(current_directory)
    choose_number = 0
    
    while choose_number <= 0 or choose_number > len(choose_list):
        choose_number = numerical_input()

    for num, element in choose_list:

        if num == choose_number:
            chdir(Path(current_directory, element))
            print("Cambiando directorio...")
            
    
    ## archive read
    print("Elije la receta que quieres leer: \n\n")
    current_directory = Path.cwd()
    choose_list = get_existing_elements_listing(current_directory)
    choose_number = 0
    
    while choose_number <= 0 or choose_number > len(choose_list):
        choose_number = numerical_input()

    for num, element in choose_list:

        if num == choose_number:
            file_object = open(element)
            print("Tu receta: \n")
            print(f"{file_object.read()}\n")
            file_object.close()
                   


def create_recipe(current_directory):

    ## categories
    print("Entra a una categoria: \n\n")
    choose_list = get_existing_elements_listing(current_directory)
    choose_number = 0

    while choose_number <= 0 or choose_number > len(choose_list):
        choose_number = numerical_input()

    for num, element in choose_list:

        if num == choose_number:
            chdir(Path(current_directory, element))
            print("Cambiando directorio...")


    ##archive creation
    current_directory = Path.cwd()
    print("Da un nombre a la receta que quieres crear: \n\n")
    new_recipe_name = string_input("archive_name")
    new_recipe_content = string_input("recipe_content")

    new_archive_path = Path(current_directory, f"{new_recipe_name}.txt")

    with open(new_archive_path, "w") as recipe:
        recipe.write(new_recipe_content)

    print("La nueva receta creada") 

       

   

        

            


def create_category(current_directory):
    new_archive_name = string_input("archive_name")

    element_to_create = Path(current_directory, new_archive_name)
    mkdir(element_to_create)

    print(f"La categoria \"{new_archive_name}\" ha sido creada")
    

def delete_recipe(current_directory):
    ## categories
    print("Entra a una categoria: \n\n")
    choose_list = get_existing_elements_listing(current_directory)
    choose_number = 0

    while choose_number <= 0 or choose_number > len(choose_list):
        choose_number = numerical_input()

    for num, element in choose_list:

        if num == choose_number:
            chdir(Path(current_directory, element))
            print("Cambiando directorio...")
    
    print("Elije la receta que quieres borrar: \n\n")


    ##archive deletion
    current_directory = Path.cwd()
    choose_list = get_existing_elements_listing(current_directory)
    choose_number = 0

    while choose_number <= 0 or choose_number > len(choose_list):
        choose_number = numerical_input()

    for num, element in choose_list:

        if num == choose_number:
            remove(element)
            print("La receta ha sido borrada.")
    

def delete_category(current_directory):
    ## categories
    print("Entra a una categoria: \n\n")
    choose_list = get_existing_elements_listing(current_directory)
    choose_number = 0

    while choose_number <= 0 or choose_number > len(choose_list):
        choose_number = numerical_input()

    for num, element in choose_list:

        if num == choose_number:

            category_path = Path(current_directory, element)

            for recipe in category_path.glob("*.txt"):

                remove(recipe)

            rmdir(category_path)

            print("La categoria fue eliminada.")            

            
            
    
    print("Elije la receta que quieres borrar: \n\n")








##Self explanatory
def main():
    while True:
        OPTIONS_MESSAGE = """
        
        Coloca el numero de la acción que quieras realizar:

            1. Leer una receta.
            2. Crear una receta.
            3. Crear una categoria.
            4. Eliminar una receta.
            5. Eliminar una categoria.
            6. Terminar y salir.
        
        """
        CURRENT_DIRECTORY = Path(__file__).parent.resolve()
        RECIPES_TARGET_DIRECTORY_NAME = "Recetas"

        RECIPES_DIRECTORY = Path(CURRENT_DIRECTORY, RECIPES_TARGET_DIRECTORY_NAME)
        CURRENT_NUMBER_OF_RECIPES, CURRENT_NUMBER_OF_CATEGORIES = get_elements_count(RECIPES_DIRECTORY)
        chdir(CURRENT_DIRECTORY)

        #########################################################################################################################
        print("Bienvenidx al recetario, buscando el directorio...\n")
        sleep(2)
        
        validation_result = archives_validation(CURRENT_DIRECTORY, RECIPES_TARGET_DIRECTORY_NAME)
        if validation_result == False or validation_result == None:
            print(f"El directorio \"Recetas\" no se encuentra en {CURRENT_DIRECTORY}. Por favor, crea el directorio \"Recetas\" si aun no lo has hecho. \n")
            continue
        
        if CURRENT_NUMBER_OF_CATEGORIES == 0:
            print("ATENCIÓN: El numero actual de categorias es 0. Solo podrás usar funciones de edición de recetas una vez hayas creado categorias para guardarlas. \n" )
        else:
            print(f"ATENCIÓN: Actualmente tienes guardadas {CURRENT_NUMBER_OF_RECIPES} recetas y {CURRENT_NUMBER_OF_CATEGORIES} categorias en el recetario. \n")
        
        options_menu(CURRENT_NUMBER_OF_RECIPES, CURRENT_NUMBER_OF_CATEGORIES, OPTIONS_MESSAGE, RECIPES_DIRECTORY)

        print("¿Quiere continuar usando el programa?")
        yes_or_no_variable = string_input("yes_or_no")
        if yes_or_no_variable == "s":
            continue
        if yes_or_no_variable == "n":
            print("Gracias por usar el programa, hasta luego.")
            exit(0)        


## runtime

if __name__ == "__main__":
    main()