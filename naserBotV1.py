from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint
from random import seed
from tkinter import *
import time
#Version 1.0: Buys first card in stock


# Constant declaration
PATH = "./chromedriver.exe"
URL = 'https://www.newegg.ca/p/pl?LeftPriceRange=0+700&N=100007708%20601394871%20601388251%20601361654%20601359415%20601357250'
password = ""
email = ""
cvv = ""
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#--------------------------- Functions definition -----------------------#
def searchGraphCard() -> bool :
    graphicCardsList = driver.find_elements(By.NAME, "item-container")
    for g in graphicCardsList:
        # info = str(g.text).splitlines()
        # title = info[1]
        time.sleep(0.2)
        if "OUT OF STOCK" not in g.text:
            print("Buy this card: " + g.text)
            g.click()
            # findBestPrice(info, title)
            return True
        else:
            print("This card is out of stock !")

    return False

def addToCart():
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ProductBuy"]/div/div[2]/button')))
            btn1 = driver.find_element(By.XPATH, '//*[@id="ProductBuy"]/div/div[2]/button')
            btn1.click()
            print(str(btn1.text) + " button found")
        finally:
            print(str(btn1.text) + " clicked")

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="modal-intermediary"]/div/div/div/div[3]/button[1]')))

            btn2 = driver.find_element_by_xpath('//*[@id="modal-intermediary"]/div/div/div/div[3]/button[1]')
            print(str(btn2.text) + " FOUND")

            if 'NO, THANKS' in str(btn2.text):
                print("skip Warrenty")
                btn2.click()
        except:
            print("No warrenty offered")
        finally:
            print("Possible warrenty passed")

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="modal-intermediary"]/div/div/div[2]/div[2]/button[2]')))

            driver.find_element_by_xpath('//*[@id="modal-intermediary"]/div/div/div[2]/div[2]/button[2]').click()
            print('Button proceed checkout clicked')
        finally:
            print('Going to login page')
   
        return


def finalizeOrder():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="paymentItemCell"]/div/div[2]/div[1]/div[2]/div[3]/input')))
        print("Writin CC security code")
        driver.find_element(By.XPATH, '//*[@id="paymentItemCell"]/div/div[2]/div[1]/div[2]/div[3]/input').click()
        driver.find_element(By.XPATH, '//*[@id="paymentItemCell"]/div/div[2]/div[1]/div[2]/div[3]/input').send_keys(cvv)         
        driver.execute_script("document.getElementsByName('cvvNumber')[0].value = '"+ cvv +"';")
        print("CVV entered")
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="btnCreditCard"]').click()
    finally:
        print("Item purchased")


def loginToAccount(): 
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div/div/div/form[1]/div/div[1]/div/label')))
        print("Writing email")        
        driver.find_element(By.XPATH, '//*[@id="labeled-input-signEmail"]').send_keys(email)
        driver.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()
    finally:
        print("Email entered")


    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div/div/div/form[1]/div/div[2]/div/label')))
        print("Writing password")        
        driver.find_element(By.XPATH, '//*[@id="labeled-input-password"]').send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()
    finally:
        print("Password entered")


# IGNORE FOR v1.0
# def findBestPrice(info, title):
#     price = int(re.findall("[0-9]+", info[3])[0])
#     # Conditon for RX 6600 (First choice)
#     if "RX 6600" in title and "RX 6600 XT" not in title and price < 600:
#         print(" we buying")
#     # Condition for RTX 3060 and RX 6600 XT
#     elif price < 650:
#         print("Buy Card")
#     # Condition for 3060 Ti
#     elif "3060 Ti" in title and price < 700:
#         print("Buy Card")               


def startBot():
    global driver
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(URL)
    print("Bot launched")
    found = False
    seed(1)
    time.sleep(1)
    while not found:
        found = searchGraphCard()
        if(found):
            break
        else:
            refTime = randint(5, 10)
            time.sleep(refTime)
            driver.refresh()

    print("Card has been found !")
    time.sleep(1)
    addToCart()
    loginToAccount()
    print("login In ...")
    finalizeOrder()
    print("Order completed")
    time.sleep(5)
    print("bye !")
    time.sleep(10)
 
# ------------------------------------ UI -------------------------------#
root = Tk()
root.title("Naser App")
root.geometry("500x500")
root.resizable(width=False, height=False)

def connectClick():
    email = entryEmail.get()
    print("Email: " + email)
    password = entryPassword.get()
    print("password: " + password)
    userNameLabel.destroy()
    passwordLabel.destroy()
    entryPassword.destroy()
    entryEmail.destroy()
    header.destroy()
    connectButton.destroy()
    startingPage()

def startingPage():
    header2.pack()
    cvvLabel.pack()
    entryCvv.pack()
    space2.pack()
    launchBtn.pack()

def launchBot():
    cvv = entryCvv.get()
    print("cvv: " + cvv)
    header2.destroy()
    cvvLabel.destroy()
    entryCvv.destroy()
    launchBtn.destroy()
    root.destroy()
    startBot()
    



header = Label(root, text="Connect to Newegg account", padx=100, pady=50, font=("Arial", 30))
header.pack()
userNameLabel = Label(root, text="Email: ", padx=10, pady=10, font=("Arial", 18))
userNameLabel.pack()
entryEmail = Entry(root, width=25, borderwidth= 3, font=("Arial", 14))
entryEmail.pack()
passwordLabel = Label(root, text="Password: ", padx=10, pady=10, font=("Arial", 18))
passwordLabel.pack()
entryPassword = Entry(root, width=25, borderwidth= 3,font=("Arial", 14))
entryPassword.pack()
space = Label(root, padx=10, pady=10)
space.pack()
connectButton = Button(root, text="Connect", bg="green", fg="white", font=("Arial", 20), command=connectClick)
connectButton.pack()
space = Label(root, padx=10, pady=10)
space.pack()

header2 = Label(root, text="", padx=100, pady=50)
cvvLabel = Label(root, text="Enter credit card CVV: ", padx=10, font=("Arial", 18))
entryCvv = Entry(root, width=10, borderwidth= 3,font=("Arial", 14), )
space2 = Label(root, padx=10, pady=10)
launchBtn = Button(root, text="Launch Bot !", bg="green", fg="white", font=("Arial", 20), command=launchBot)

root.iconbitmap('./robot.ico')

#------------------ Execute code -------------------#
root.mainloop()
    