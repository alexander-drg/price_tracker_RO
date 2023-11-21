import tkinter as tk
from tkinter import font
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Price tracker")
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
        print(product)
        self.search_info.insert(
            '1.0', "Se cauta pe Emag.....\nSe cauta pe Evomag.....\nSe cauta pe Cel.....")
        # Schedule the execution of the emag and evomag methods after a delay
        self.root.after(100, lambda: self.update_search_info(product))

    def update_search_info(self, product):
        emag_pret = self.emag(product, self.driver)
        #evomag_pret = self.evomag(product, self.driver)
        cel_pret = self.cel(product, self.driver)
        #elefant_pret = self.elefant(product, self.driver)
        self.search_info.delete('1.0', tk.END)
        self.search_info.insert('1.0', emag_pret)
        #self.search_info.insert(tk.END, "\n" + evomag_pret)
        self.search_info.insert(tk.END, "\n" + cel_pret)
        #self.search_info.insert(tk.END, "\n" + elefant_pret)

    def emag(self, product):
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        URL = "https://www.emag.ro/search/" + product + "?ref=effective_search"

        driver.get(URL)
        parent_window = driver.current_window_handle
        try:
            check = (driver.find_element(
                By.XPATH, "//span[@class='title-phrasing title-phrasing-sm text-danger']").text)
        except NoSuchElementException:
            check = "All good"
        if check == "0 rezultate pentru:":
            nume_emag = "Product dosen't exist"
            pret_emag = "Price not found"
        else:
            # Find and click on the first link

            first_link = driver.find_element(By.XPATH,
                                             "//body[1]/div[3]/div[2]/div[1]/section[1]/div[1]/div[3]/div[2]/div[6]/div[1]/div[1]/div[1]/div[3]/a[1]").click()
            try:
                pret_emag = driver.find_element(
                    By.XPATH, "//p[@class='product-new-price']/span[@class='product-price'][last()]").text
                nume_emag = (driver.find_element(
                    By.XPATH, "/html[@class='doc-desktop ']/body/div[@class='main-container-outer']/div[@class='main-container-inner']/div[@id='main-container']/section[@class='page-section page-section-light'][1]/div[@class='container']/div[@class='page-header d-flex justify-space-between hidden-xs']/h1[@class='page-title']").text)
            except NoSuchElementException:
                try:
                    pret_emag = driver.find_element(
                        By.XPATH, "//div[@class='product-page-pricing product-highlight']//div//p[@class='product-new-price']").text
                    nume_emag = (driver.find_element(
                        By.XPATH, "/html[@class='doc-desktop ']/body/div[@class='main-container-outer']/div[@class='main-container-inner']/div[@id='main-container']/section[@class='page-section page-section-light'][1]/div[@class='container']/div[@class='page-header d-flex justify-space-between hidden-xs']/h1[@class='page-title']").text)
                except NoSuchElementException:
                    pret_emag = "Price not found"
            finally:
            # Close the current tab
            driver.close()
            # Switch back to the main window
            driver.switch_to.window(self.parent_window)

        return (nume_emag[0:35] + ' PRET: ' + pret_emag)

    def evomag(self, product):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        URL = "https://www.evomag.ro/?sn.q=" + product
        driver.get(URL)

        try:
            check = (driver.find_element(
                By.XPATH, "/html/body[@class='homepage']/div[@class='main_wrap']/div[@class='wrap_inside_container main_body_container']/div[@class='meniu_produse_list searchnode']/div[@class='produse_body']/div[@class='produse_liste_filter']/h3/div[@class='sub_taburi_produse sub_taburi_produse-search']/div[@class='noResults']").text)
        except NoSuchElementException:
            check = "All good"

        if check == "CRITERIILE DE FILTRARE SELECTATE DE DUMNEAVOASTRA NU AU RETURNAT NICI UN REZULTAT!":
            nume = "Product dosen't exist"
            pret = "Price not found"
        else:
            first_link = driver.find_element(
                By.XPATH, "//div[@class='produse_liste_filter']//div[1]//div[1]//div[3]").click()
            pret = (driver.find_element(
                By.XPATH, "//div[@class='price_ajax']//div[@class='pret_rons']").text)
            nume = (driver.find_element(
                By.XPATH, "//div[@class='product_right_inside slim']").text)

        driver.quit()
        return (nume[0:35] + ' PRET: ' + pret)

    def cel(self, product):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        URL = "https://www.cel.ro/cauta/" + product
        driver.get(URL)

        try:
            check = (driver.find_element(
                By.XPATH, "/html/body[@id='advancedsearchresult']/div[@id='mainWrapper']/div[@class='content-wrapper']/div[@id='bodycode3']/div[@id='bodycode']/div[@class='listingPageWrapper']/div[@class='listingWrapper no-filters']/div[@class='productlisting']/div").text)
        except NoSuchElementException:
            check = "All good"

        if check == "Nu sunt produse disponibile":
            nume = "Product dosen't exist"
            pret = "Price not found"
        else:
            first_link = driver.find_element(
                By.XPATH, "//body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/h2[1]/a[1]").click()
            pret = (driver.find_element(
                By.XPATH, "//span[@id='product-price']").text)
            nume = (driver.find_element(
                By.XPATH, "//h1[@id='product-name']").text)

        finally:
            # Close the current tab
            driver.close()
            # Switch back to the main window
            driver.switch_to.window(self.parent_window)
            driver.quit()
        
        return (nume[0:35] + ' PRET: ' + pret + ' LEI')

    def elefant(self, product):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        URL = "https://www.elefant.ro/search?SearchTerm=" + product + "&StockAvailability=true"
        driver.get(URL)

        try:
            check = (driver.find_element(
                By.XPATH, "//div[@class='errorpage-cta']").text)
            nume = "Product dosen't exist"
            pret = "Price not found"
        except NoSuchElementException:
            check = "All good"

        if check == "NE PARE RĂU, NU EXISTĂ PRODUSE ÎN ACEASTĂ CATEGORIE.":
            nume = "Product dosen't exist"
            pret = "Price not found"
        else:
            first_link = driver.find_element(
                By.XPATH, "//div[@class='product-tile js-product-tile js-product-tile-1722011e-b8f5-4f8c-a720-4834d7382cc4']//a[@class='product-title']").click()
            pret = (driver.find_element(
                By.XPATH, "//div[@id='product-main-details-price']//div[@class='product-price vendor-offer-data js-vendor-price']").text)
            nume = (driver.find_element(
                By.XPATH, "//div[@class='product-title']").text)

        finally:
            # Close the current tab
        driver.close()
            # Switch back to the main window
        driver.switch_to.window(self.parent_window)
        driver.quit()

        return (nume[0:35] + ' PRET: ' + pret)


app = GUI()
# Run the application
app.run()
