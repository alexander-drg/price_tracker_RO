from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore


class ProductInputDialog(QDialog):
    def __init__(self, parent=None):
        super(ProductInputDialog, self).__init__(parent)
        self.setWindowIcon(QIcon('protection.png'))
        self.setWindowTitle("Price Trakcing App")

        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)

        self.setStyleSheet("QDialog {background-color: #7d8780;}")

        self.product_input = QLineEdit(self)
        self.ok_button = QPushButton("Search", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.product_input)
        layout.addWidget(self.ok_button)

        self.ok_button.clicked.connect(self.accept)

    def get_product_name(self):
        return self.product_input.text()


class PriceDialog(QDialog):
    def __init__(self, emag_price, cel_price, parent=None):
        super(PriceDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~
                            QtCore.Qt.WindowContextHelpButtonHint)

        # Set the background color
        self.setStyleSheet("background-color: #d1eddb;")

        # Set the application icon
        self.setWindowIcon(QIcon('protection.png'))

        self.setWindowTitle("Price Trakcing App")

        self.emag_price_label = QLabel(f"eMAG Price: {emag_price}", self)
        self.cel_price_label = QLabel(f"CEL Price: {cel_price}", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.emag_price_label)
        layout.addWidget(self.cel_price_label)


# Create PyQt input dialog
app = QApplication([])
input_dialog = ProductInputDialog()
input_result = input_dialog.exec_()
product_name = input_dialog.get_product_name()

# Initialize variables to store product prices
emag_price = "Not found"
cel_price = "Not found"

# After entering the product name
if input_result == QDialog.Accepted and product_name:
    # Create a Chrome WebDriver instance
    browser = webdriver.Chrome()
    browser.get('https://www.emag.ro/')

    # Find the search input and enter the user-inputted product name
    search_input_emag = browser.find_element(
        By.XPATH, '//*[@id="searchboxTrigger"]')
    search_input_emag.send_keys(product_name)

    # Find the search button and click it
    search_button_emag = browser.find_element(
        By.XPATH, '//*[@id="masthead"]/div/div/div[2]/div/form/div[1]/div[2]')
    search_button_emag.click()

    # Wait for the first product to be present on the page
    wait_emag = WebDriverWait(browser, 10)
    try:
        first_product_emag = wait_emag.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="card_grid"]/div[1]/div/div/div[3]/a')))
        first_product_emag.click()

        # Wait for the price element to be present on the page
        price_element_emag = wait_emag.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-container"]/section[3]/div/div[1]/div[2]/div/div[2]/div[2]/form[1]/div[1]/div[1]/div[1]/div/div/div[1]/p[2]')))
        # Get the text of the price element
        emag_price = price_element_emag.text
    except NoSuchElementException as e:
        print(f"Error in eMAG: {e}")

    # Close the current tab (emag.ro)
    # browser.close()

    # Open the CEL tab in the same browser instance
    browser.get('https://www.cel.ro/')

    # Find the search input and enter the user-inputted product name
    search_input_cel = browser.find_element(
        By.XPATH, '//*[@id="keyword"]')
    search_input_cel.send_keys(product_name)

    # Find the search button and click it
    search_button_cel = browser.find_element(
        By.XPATH, '//*[@id="quick_find"]/div[2]/button')
    search_button_cel.click()

    # Wait for the first product to be present on the page
    wait_cel = WebDriverWait(browser, 10)
    try:
        first_product_cel = wait_cel.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="bodycode"]/div[2]/div[1]/div[2]/div[1]')))
        first_product_cel.click()

        # Wait for the price element to be present on the page
        price_element_cel = wait_cel.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="product-price"]')))
        # Get the text of the price element
        cel_price = price_element_cel.text
    except NoSuchElementException:
        pass

    # Close the current tab (cel.ro)
    browser.close()

# Display the product prices using PyQt dialog
price_dialog = PriceDialog(emag_price, cel_price)
price_dialog.exec_()
