from webdriver_manager.chrome import ChromeDriverManager
from selenium .webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#FUNCTIONS
from functions import *


def main():
    print("------------------------------------")
    with open('Sources/logFlow.txt', mode='w') as file_object:
        file_object.close()
    with open('Sources/BillsToVerify.txt', mode='w') as file_object:
        file_object.close()
    logFlow(1)
    billings = get_Billing_info()
    for i in billings:
        making_bill(i)
    

if __name__ == "__main__":
    main()
        








#  try:
#         f = open("words.txt", "r")
#     except FileNotFoundError:
#         print("File not found...")
#     else:
#         content = f.read()
#         f.close()
#         listcontent = content.split("\n")
#         limit = len(listcontent)-1
#         naleatory = random.randrange(1,limit,1)
#         words = listcontent[naleatory].split("-")
#         if question(words[0],words[1]):
#             return True
#         else:
#             return False