from webdriver_manager.chrome import ChromeDriverManager
from selenium .webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[1]/a #FORMATO DE LAS CASILLAS DE DATEBOX SELECTOR
#//*[@id="form:growl_container"]/div/div/div[2]/span    #CONTENEDOR EMERGENTE
#//*[@id="form:growl_container"]/div/div/div[2]/span    #CONTENEDOR EMERGENTE ID VENTA
#//*[@id="form:growl_container"]/div/div/div[2]/span    #
#//*[@id="form:growl_container"]/div/div/div[2]/span    #EL TICKET INGRESADO ES VALIDO
#//*[@id="form:tblTickets:0:j_idt137"]   Boton para retirar ticket de lista

def logFlow(LogFlowCode, info="NO INFO"):
    with open('Sources/logFlow.txt', mode='a') as file_object:
        if LogFlowCode == 1:
            print('INICIANDO...', file=file_object)
        elif LogFlowCode == 2:
            print('\nAbriendo chrome para generar factura: ' + " ".join(info), file=file_object)
        elif LogFlowCode == 3:
            print('Datos de la factura agregados a la pagina', file=file_object)
        elif LogFlowCode == 4:
            print('Validando ticket....', file=file_object)
        elif LogFlowCode == 5:
            print('ERROR!!! ESTE TICKET NO ES VALIDO HAY QUE VERIFICAR LA INFORMACION INGRESADA', file=file_object)
        elif LogFlowCode == 6:
            print('El ticket es valido, ingresando informacion fiscal... ', file=file_object)
        elif LogFlowCode == 7:
            print('Existe un problema al intentar extraer la informacion fiscal de "taxInfo.txt" ', file=file_object)
        elif LogFlowCode == 8:
            print('Ocurrio un error al intentar enviar la informacion de facturacion a la pagina', file=file_object)
    file_object.close()

def get_Billing_info():
    try:
        f = open("Sources/BillingInfo.txt", "r")
    except FileNotFoundError:
        print("File not found...")
    else:
        content = f.read()
        f.close()
        list_content = content.split("\n")
    return list_content

def check_day(date):
    date_list = date.split("/")# we create a new list from de bill date to compare it with a day in DaysSource.txt
    try:
        f = open("Sources/DaysSource.txt", "r")
    except FileNotFoundError:
        print("File not found...")
    else:
        content = f.read()
        f.close()
        list_days = content.split("\n")
        for i in list_days: #here i iterate on all the "day-x-y" elements from list_days variable 
            if date_list[0] == i[0:2]:
                return i[3:6].split("-") 

def save_invoice_to_reverify(bill):
    #THIS FUNCTION ADDS A BILL WITH AN ISSUE TO A TXT TO CHECK AGAIN AFTER FINISH THE PRIMARY BILLING CYCLE
    with open ('Sources/BillsToVerify.txt', "a") as file_object:
        print(str("-".join(bill)), file=file_object)

def get_tax_information():
    #HERE WE GET TAX INFO FROM THE SOURCE
    try:
        file_object = open("Sources/taxInfo.txt", "r")
    except:
        logFlow(7)
    else:
        info = file_object.read()
        tax_info_list = info.split("\n")
    finally:
        file_object.close()
    #GENERATE A DICCIONARY WITH THE INFORMATION
    tax_info_diccionary = {}
    for i in tax_info_list:
        x = i.split(":")
        tax_info_diccionary[x[0]] = x[1]
    return tax_info_diccionary
    
       
def making_bill(billing_info):
    billing_info = billing_info.split("-")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    logFlow(2, billing_info)
    driver.get("https://www4.oxxo.com:9443/facturacionElectronica-web/views/layout/inicio.do")
    time.sleep(5)
    radio_bt = driver.find_element(By.XPATH, "//*[@id='form:dlgInfoTicket']/div[1]/a")
    radio_bt.click()#CLOSE INFO TICKET 
    #time.sleep(1)
    radio_bt = driver.find_element(By.XPATH, "//*[@id='form:fecha_input']")
    radio_bt.click()#OPEN DATE INPUT BOX
    #time.sleep(1)
    radio_bt = driver.find_element(By.XPATH, "//*[@id='ui-datepicker-div']/div/a[1]/span")
    radio_bt.click()#CHANGE FROM SEPTEMBER TO AUGUST
    #In the next lineS select the day
    day_position = check_day(billing_info[0])#BILLING INFO 0 IS THE DATE
    radio_bt = driver.find_element(By.XPATH, "//*[@id='ui-datepicker-div']/table/tbody/tr[" + day_position[0] + "]/td[" + day_position[1] +"]")
    radio_bt.click()
    #Send information 
    radio_bt = driver.find_element(By.XPATH, "//*[@id='form:folio']").send_keys(billing_info[1])
    radio_bt = driver.find_element(By.XPATH, "//*[@id='form:venta']").send_keys(billing_info[2])
    radio_bt = driver.find_element(By.XPATH, "//*[@id='form:total']").send_keys(billing_info[3])
    logFlow(3)
    radio_bt = driver.find_element(By.XPATH, "//*[@id='form:j_idt149']/span")
    radio_bt.click()#VALIDATE TICKET
    time.sleep(2)
    #THE NEXT LINES ARE TO VERIFY IF THE DELETE TICKET BUTTON IS IN THE PAGE THAT MEANS THE TICKET WAS SUCCESFULLY VALIDATED 
    try:
        logFlow(4)
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:tblTickets:0:j_idt137']")
    except:
        print("NO SE HA PODIDO AGREGAR LA FACTURA")
        logFlow(5, billing_info)
        save_invoice_to_reverify(billing_info)    
    else:
        logFlow(6)
    #CLICK ON CONTINUE BUTTON
    radio_bt = driver.find_element(By.XPATH, "//*[@id='form:continuar']/span")
    radio_bt.click()
    time.sleep(2)
    #ONCE THE TICKET WAS SUCCESSFULLY VALIDATED THE PROGRAM SEND THE TAX INFO TO THE PAGE
    tax_info = get_tax_information()
    print(tax_info)
    try:
        driver.find_element(By.XPATH, "//*[@id='form:rfc']").send_keys(tax_info.get("RFC"))
        time.sleep(1)
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:calle']")
        radio_bt.click()
        time.sleep(1)
        radio_bt.send_keys(tax_info.get("calle"))
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id='form:ext']").send_keys(tax_info.get("ext"))
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id='form:int']").send_keys(tax_info.get("int"))
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id='form:colonia']").send_keys(tax_info.get("colonia"))
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id='form:dele']").send_keys(tax_info.get("municipio"))
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id='form:codigo']").send_keys(tax_info.get("codigoPostal"))
        time.sleep(1)
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:razon']")
        radio_bt.click()
        time.sleep(1)
        radio_bt.send_keys(tax_info.get("razonSocial"))
        time.sleep(1)
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:estado_label']")
        radio_bt.click()
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:estado_panel']/div/ul/li[23]")
        radio_bt.click()
        time.sleep(1)
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:selectOneMenuRegFis_label']")
        radio_bt.click()
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:selectOneMenuRegFis_panel']/div/ul/li[2]")
        radio_bt.click()
        time.sleep(1)
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:selectOneMenuCFDI_label']")
        radio_bt.click()
        radio_bt = driver.find_element(By.XPATH, "//*[@id='form:selectOneMenuCFDI_panel']/div/ul/li[9]")
        radio_bt.click()
        time.sleep(1)
    except:
        logFlow(8)
    else:
        print("TODO CHIDO")
    time.sleep(2)
    driver.close()



if __name__ == "__main__":
    get_Billing_info()