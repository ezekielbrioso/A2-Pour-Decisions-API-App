# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 21:31:11 2024

@author: Ezekiel
"""
#These codes are for importing the modules, libraries, and packages that are needed for my API app
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from pygame import mixer  


#This is the link of the url which is needed for making API calls and get the necessary information
API_URL = "https://www.thecocktaildb.com/api/json/v1/1"

#This code is responsible for audio
mixer.init()
mixer.music.load("C:\\Users\\Ezekiel\\Downloads\\background music.mp3")  
mixer.music.play(-1)


#This includes the main content of my app
class CocktailApp: #This is used to define the classes that I used
    def __init__(self, root): #Initializing
        self.root = root
        self.root.title("Pour Decisions") #This sets the window title to "Pour Decisions"

        self.root.configure(bg="#F8EDE3")  #This sets the bg color to beige-peachy background
        self.setup_ui() #This calls the setup_ui method
        self.root.geometry('1520x780') #This sets the window's width and height  
        self.root.resizable(False, False)  #This makes the window size not resizable

    def setup_ui(self): #This section includes UI styling and designing
        #This includes the MAIN CONTAINER
        main_frame = tk.Frame(self.root, bg="#F8EDE3")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        

        #This code is for the SEARCH OPTIONS which can be seen in the left Panel 
        left_frame = tk.Frame(main_frame, bg="#F8EDE3")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        #This code is for the TITLE for SEARCH INPUTS
        tk.Label(left_frame, text="Search Cocktails", font=("Helvetica", 16, "bold"), bg="#F8EDE3", fg="#D68C7C").pack(pady=10)

        #This code is for styling the SEARCH BY NAME
        tk.Label(left_frame, text="Search by Name:", bg="#F8EDE3", fg="#8C5C53").pack(anchor=tk.W, pady=5)
        self.name_entry = tk.Entry(left_frame, width=25, bg="#FFF3E6", fg="#8C5C53")
        self.name_entry.pack(anchor=tk.W, pady=5)
        tk.Button(left_frame, text="Search", command=self.search_by_name, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=5)

        #This code is for styling the LIST BY FIRST LETTER
        tk.Label(left_frame, text="List by First Letter:", bg="#F8EDE3", fg="#8C5C53").pack(anchor=tk.W, pady=5)
        self.letter_combobox = ttk.Combobox(left_frame, values=[chr(i) for i in range(65, 91)], width=22)
        self.letter_combobox.pack(anchor=tk.W, pady=5)
        tk.Button(left_frame, text="List", command=self.list_by_letter, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=5)

        #This code is for styling the SEARCH BY INGREDIENT
        tk.Label(left_frame, text="Search by Ingredient:", bg="#F8EDE3", fg="#8C5C53").pack(anchor=tk.W, pady=5)
        self.ingredient_entry = tk.Entry(left_frame, width=25, bg="#FFF3E6", fg="#8C5C53")
        self.ingredient_entry.pack(anchor=tk.W, pady=5)
        tk.Button(left_frame, text="Search", command=self.search_by_ingredient, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=5)

        #This code is for styling the FILTER BY CATEGORY
        tk.Label(left_frame, text="Filter by Category:", bg="#F8EDE3", fg="#8C5C53").pack(anchor=tk.W, pady=5)
        self.category_combobox = ttk.Combobox(left_frame, width=22)
        self.category_combobox.pack(anchor=tk.W, pady=5)
        tk.Button(left_frame, text="Filter", command=self.filter_by_category, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=5)

        #This code is for styling the FILTER BY ALCOHOLIC TYPE
        tk.Label(left_frame, text="Filter by Alcoholic Type:", bg="#F8EDE3", fg="#8C5C53").pack(anchor=tk.W, pady=5)
        self.alcoholic_combobox = ttk.Combobox(left_frame, values=["Alcoholic", "Non Alcoholic"], width=22)
        self.alcoholic_combobox.pack(anchor=tk.W, pady=5)
        tk.Button(left_frame, text="Filter", command=self.filter_by_alcoholic, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=5)

        #These include styling for the other useful buttons such as OTHER OPTIONS, LIST CATEGORIES, LIST GLASSES, LIST INGREDIENTS, and RANDOM COCKTAIL
        tk.Label(left_frame, text="Other Options:", font=("Helvetica", 12, "bold"), bg="#F8EDE3", fg="#D68C7C").pack(anchor=tk.W, pady=10)
        tk.Button(left_frame, text="List Categories", command=self.list_categories, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=5)
        tk.Button(left_frame, text="List Glasses", command=self.list_glasses, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=5)
        tk.Button(left_frame, text="List Ingredients", command=self.list_ingredients, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=5)
        tk.Button(left_frame, text="Random Cocktail", command=self.get_random_cocktail, bg="#D68C7C", fg="white", relief=tk.FLAT).pack(anchor=tk.W, pady=10)

        #This code is for the RESULTS AND DETAILS which can be seen in the right panel
        right_frame = tk.Frame(main_frame, bg="#F8EDE3")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        #This code is for the RESULTS LISTBOX
        results_frame = tk.Frame(right_frame, relief=tk.FLAT, borderwidth=1, bg="#F8EDE3")  
        results_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=5)
        tk.Label(results_frame, text="Cocktail Results", font=("Georgia", 16, "bold"), bg="#F8EDE3", fg="#D68C7C").pack(pady=10)
        self.results_listbox = tk.Listbox(results_frame, width=50, height=10, bg="#FFF3E6", fg="#8C5C53")
        self.results_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=30)
        self.results_listbox.bind("<Double-1>", self.display_cocktail_details)

        #This code is for the SCROLLBAR in the listbox
        scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_listbox.yview)
        self.results_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        #This code is for the DETAILS PANEL 
        details_frame = tk.Frame(right_frame, relief=tk.RIDGE, borderwidth=2, bg="#F8EDE3")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=50, pady=10)
        tk.Label(details_frame, text="Cocktail Details", font=("Georgia", 14, "bold"), bg="#FFF3E6", fg="#8C5C53").pack(pady=10)

        #This code is for the COCKTAIL IMAGE
        self.image_label = tk.Label(details_frame, bg="#FFF3E6")
        self.image_label.pack(pady=10)
        
        #This code is for the COCKTAIL TITLE
        self.title_label = tk.Label(details_frame, text="", font=("Georgia", 16, "bold"), bg="#F8EDE3", fg="#64262E")
        self.title_label.pack(pady=10)

        #This code is for the COCKTAIL DETAILS TEXT
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, relief=tk.FLAT, state=tk.DISABLED, height=50, width=100, bg="#F8EDE3", fg="#8C5C53", font=("Calibri", 12))
        self.details_text.pack(padx=30, pady=30)

        #This code ensures that the a necessary information will be displayed
        self.populate_categories()

    #This is a function that is responsible for fetching the data from the API URL
    def fetch_data(self, endpoint):
        try:
            response = requests.get(API_URL + endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")
            return None
        
    #This is a function that is responsible for searching the cocktail by name
    def search_by_name(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Input Required", "Please enter a cocktail name.")
            return
        data = self.fetch_data(f"/search.php?s={name}")
        if data and data["drinks"]:
            self.populate_results(data["drinks"])
        else:
            messagebox.showinfo("No Results", "No cocktails found with that name.")
            
    #This is a function that is responsible for listing the cocktails by letter
    def list_by_letter(self):
        letter = self.letter_combobox.get()
        if not letter:
            messagebox.showwarning("Input Required", "Please select a letter.")
            return
        data = self.fetch_data(f"/search.php?f={letter.lower()}")
        if data and data["drinks"]:
            self.populate_results(data["drinks"])
        else:
            messagebox.showinfo("No Results", "No cocktails found starting with that letter.")
    
    #This is a function that is responsible for searching the cocktail by ingredient
    def search_by_ingredient(self):
        ingredient = self.ingredient_entry.get()
        if not ingredient:
            messagebox.showwarning("Input Required", "Please enter an ingredient.")
            return
    
        data = self.fetch_data(f"/filter.php?i={ingredient}")
    
        print("API response data:", data)
    
        if data and isinstance(data, dict) and "drinks" in data and isinstance(data["drinks"], list):
            self.populate_results(data["drinks"])  
        else:
            messagebox.showinfo("No Results", f"No cocktails found with the ingredient: {ingredient}")

    
    #This is a function that is responsible for filtering the cocktails by category
    def filter_by_category(self):
        category = self.category_combobox.get()
        if not category:
            messagebox.showwarning("Input Required", "Please select a category.")
            return
        data = self.fetch_data(f"/filter.php?c={category}")
        
        print("API response data:", data)
        
        if data and isinstance(data, dict) and "drinks" in data and isinstance(data["drinks"], list):
            self.populate_results(data["drinks"])
        else:
            messagebox.showinfo("No Results", "No cocktails found in that category.")
    
    #This is a function that is responsible for filtering the cocktails by alcoholic
    def filter_by_alcoholic(self):
        alcoholic = self.alcoholic_combobox.get()
        if not alcoholic:
            messagebox.showwarning("Input Required", "Please select an alcoholic type.")
            return
        data = self.fetch_data(f"/filter.php?a={alcoholic}")
        
        print("API response data:", data)
        
        if data and isinstance(data,dict) and "drinks" in data and isinstance (data["drinks"], list):
            self.populate_results(data["drinks"])
        else:
            messagebox.showinfo("No Results", "No cocktails found for that alcoholic type.")
    
    #This is a function that is responsible for showing the cocktails' category list
    def list_categories(self):
        data = self.fetch_data("/list.php?c=list")
        if data and data["drinks"]:
            categories = [category["strCategory"] for category in data["drinks"]]
            messagebox.showinfo("Categories", "\n".join(categories))
        else:
            messagebox.showinfo("No Results", "Failed to retrieve categories.")
    
    #This is a function that is responsible for showing the cocktails' glasses list
    def list_glasses(self):
        data = self.fetch_data("/list.php?g=list")
        if data and data["drinks"]:
            glasses = [glass["strGlass"] for glass in data["drinks"]]
            messagebox.showinfo("Glasses", "\n".join(glasses))
        else:
            messagebox.showinfo("No Results", "Failed to retrieve glasses.")
    
    #This is a function that is responsible for showing the cocktails' ingredients list
    def list_ingredients(self):
        data = self.fetch_data("/list.php?i=list")
        if data and data["drinks"]:
            ingredients = [ingredient["strIngredient1"] for ingredient in data["drinks"]]
            messagebox.showinfo("Ingredients", "\n".join(ingredients))
        else:
            messagebox.showinfo("No Results", "Failed to retrieve ingredients.")
    
    #This is a function that is responsible for showing the the user a random cocktail
    def get_random_cocktail(self):
        data = self.fetch_data("/random.php")
        if data and data["drinks"]:
            self.populate_results(data["drinks"])
        else:
            messagebox.showinfo("No Results", "Failed to retrieve a random cocktail.")

    #This is a function that is responsible for displaying the cocktail names in the result box
    def populate_results(self, drinks):
        self.results_listbox.delete(0, tk.END)
        for drink in drinks:
            self.results_listbox.insert(tk.END, drink["strDrink"])

    #This is a function that is responsible for displaying the cocktails' categories
    def populate_categories(self):
        data = self.fetch_data("/list.php?c=list")
        if data and data["drinks"]:
            categories = [category["strCategory"] for category in data["drinks"]]
            self.category_combobox['values'] = categories

    #This is a function that is responsible for displaying the information of the selected cocktail from the results box
    def display_cocktail_details(self, event):
        selected_cocktail = self.results_listbox.get(tk.ACTIVE)
        data = self.fetch_data(f"/search.php?s={selected_cocktail}")
        if data and data["drinks"]:
            cocktail = data["drinks"][0]
            self.display_details(cocktail)

    #This is a function that is responsible for displaying the detailed information of the selected cocktail
    def display_details(self, cocktail):
        #This updates and displays cocktail's name
        self.title_label.config(text=cocktail['strDrink']) 
        
        #This prepares the details_text for a new content
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        #These adds details about the cocktail
        self.details_text.insert(tk.END, f"Category: {cocktail['strCategory']}\n")
        self.details_text.insert(tk.END, f"Glass: {cocktail['strGlass']}\n")
        self.details_text.insert(tk.END, f"Instructions: {cocktail['strInstructions']}\n")
        self.details_text.insert(tk.END, "\nIngredients:\n")
        
        #This part of the code is necessary for looping through ingredients and shows them in the box
        for i in range(1, 16):
            ingredient = cocktail.get(f"strIngredient{i}")
            measure = cocktail.get(f"strMeasure{i}")
            if ingredient:
                self.details_text.insert(tk.END, f"- {ingredient} {measure or ''}\n")
        self.details_text.config(state=tk.DISABLED)
        
        #This part of the code is responsible for loading and displaying the cocktail's image 
        if cocktail.get("strDrinkThumb"):
            image_url = cocktail["strDrinkThumb"]
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk
            except Exception as e:
                messagebox.showerror("Image Error", f"Failed to load image: {e}")
        else:
            self.image_label.config(image=None)

#This part of code is responsible for intializing, setting up, and starting the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CocktailApp(root)
    root.mainloop()
