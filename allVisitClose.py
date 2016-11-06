import requests
import xml.etree.ElementTree as ET

def getOrderList():
    return b'<RK7Query><RK7CMD CMD="GetOrderList"/></RK7Query>'

def closeVisit(visitID):
    return b'<RK7Query><RK7CMD CMD="CLOSEVISIT" VisitID="' + visitID.encode("UTF-8") + b'"/></RK7Query>'

def payOrder(orderGuid, orderToPaySum, idStation, codeCashier):
    xml = '<RK7Query><RK7CMD CMD="PayOrder" calcBySeats="0" seat="0"><Station id="' + idStation + '"/><Cashier code="' + codeCashier + '"/><Order guid="' + orderGuid + '"/><Payment code="1" amount="' + orderToPaySum + '"/><ReceiptMaket code="17"/></RK7CMD></RK7Query>'
    return xml.encode("UTF-8")

ip = "172.22.3.89"
port = "8855"
idStation = "15007"
codeCashier = "7"
host = 'https://' + ip + ':' + port + '/rk7api/v0/xmlinterface.xml'
login = "9"
password = "9"

requests.packages.urllib3.disable_warnings()
resGetOrderList = requests.post(host, auth=(login, password), verify=False, data=getOrderList())
tree = ET.fromstring(resGetOrderList.content)

print("Pay оrders\n==================")
for child in tree:
    for child1 in child:
        if child1.tag == "Orders":
            for child2 in child1:
                if child2.attrib["Finished"] == "0":
                    orderGuid = child2.attrib["guid"]
                    orderToPaySum = child2.attrib["ToPaySum"]
                    print (child2.tag, "OrderName =", child2.attrib["OrderName"], "guid =", orderGuid, "ToPaySum = ",
                           orderToPaySum)
                    resPayOrder = requests.post(host, auth=(login, password), verify=False,
                                                data=payOrder(orderGuid, orderToPaySum, idStation, codeCashier))
                    parseResPayOrder = ET.fromstring(resPayOrder.content)
                    if parseResPayOrder.attrib["Status"] == "Ok":
                        print("Status: Ok")
                    else:
                        print(parseResPayOrder.attrib["ErrorText"])

print ("\nClose visits\n==================")
for child in tree:
    if child.attrib["Finished"] == "0":
        orderVisit = child.attrib["VisitID"]
        resCloseVisit = requests.post(host, auth=(login, password), verify=False, data=closeVisit(orderVisit))
        print("VisitID", orderVisit)
        resCloseVisit = ET.fromstring(resCloseVisit.content)
        if resCloseVisit.attrib["Status"] == "Ok":
            print("Status: Ok")
        else:
            print(resCloseVisit.attrib["ErrorText"])

