import tkinter as tk
from tkinter import font
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Search App")
        self.root.geometry("620x290")
        self.root.configure(bg="#2E2E2E")  # Set background color

        # Set fonts
        self.label_font = font.Font(family="Verdana", size=12, weight="bold")
        self.entry_font = font.Font(family="Verdana", size=12)
        self.button_font = font.Font(
            family="Verdana", size=12, )
        self.text_font = font.Font(family="Courier New", size=12)

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Search Prompt
        self.search_label = tk.Label(
            self.root, text="Product:", fg="white", bg="#2E2E2E", font=self.label_font
        )
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Entry for search input
        self.search_box = tk.Entry(
            self.root, width=30, bg="#95B2A7", font=self.entry_font)
        self.search_box.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Search Button
        self.search_button = tk.Button(
            self.root, text="Search", command=self.search, bg="#4CAF50", fg="white", width=15, font=self.button_font
        )
        self.search_button.grid(
            row=0, column=2, padx=10, pady=10, sticky=tk.W)

        # Results Text Widget
        self.search_info = tk.Text(
            self.root, height=10, width=60, wrap=tk.WORD, bg="#95B2A7", fg="white", font=self.text_font
        )
        self.search_info.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def search(self):
        product = self.search_box.get()
        self.search_info.delete('1.0', tk.END)  # Clear previous results
        self.search_info.insert(
            '1.0', f"Searching for {product} on Emag and Evomag...\n\n")

        emag_result = self.emag(product)
        self.search_info.insert(tk.END, f"\nEmag Result:\n{emag_result}\n\n")

        evomag_result = self.evomag(product)
        self.search_info.insert(tk.END, f"\nEvomag Result:\n{evomag_result}")

    def emag(self, product):
        options = Options()
        options.add_argument('--headless')
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        URL = "https://www.emag.ro/search/" + product + "?ref=effective_search"

        driver.get(URL)
        parent_window = driver.current_window_handle

        # Find and click on the first link
        first_link = driver.find_element(
            By.XPATH, "//body[1]/div[3]/div[2]/div[1]/section[1]/div[1]/div[3]/div[2]/div[6]/div[1]/div[1]/div[1]/div[3]/a[1]").click()

        try:
            pret_emag = driver.find_element(By.XPATH,
                                            "//p[@class='product-new-price']/span[@class='product-price'][last()]").text
        except NoSuchElementException:
            pret_emag = "Price not found"

        nume_emag = driver.find_element(
            By.XPATH, "//h1[@class='page-title']").text
        driver.quit()

        return (nume_emag[0:35] + ' PRET: ' + pret_emag)

    def evomag(self, product):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Now create your WebDriver instance using the options
        driver = webdriver.Chrome(options=options)

        URL = "https://www.evomag.ro/?sn.q=" + product

        driver.get(URL)

        parent_window = driver.current_window_handle

        first_link = driver.find_element(
            By.XPATH, "//div[@class='produse_liste_filter']//div[1]//div[1]//div[3]").click()

        pret = driver.find_element(
            By.XPATH, "//div[@class='price_ajax']/div[@class='pret_rons']/span[@class='product-price'][last()]").text
        nume = driver.find_element(
            By.XPATH, "//div[@class='product_right_inside slim']").text

        driver.quit()

        return (nume[0:35] + ' PRET: ' + pret)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GUI()
    app.run()
