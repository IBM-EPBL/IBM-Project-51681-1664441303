from http import client
import cv2
import pyzbar
from pyzbar.pyzbar import decode
import time

from ibmcloudant.cloudant_v1 import CloudantV1 
from ibmcloudant import CouchDbSessionAuthenticator
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator

authenticator = BasicAuthenticator('apikey-v2-1oj043bu90m78ng4h2j27w5nob2nvcma6xanc6bk0a7m', 'daf3c00c2cc182af425a5691a07f7b93')
service = CloudantV1(authenticator=authenticator)

service.set_service_url('https://apikey-v2-1oj043bu90m78ng4h2j27w5nob2nvcma6xanc6bk0a7m:daf3c00c2cc182af425a5691a07f7b93@932393aa-9f82-4144-9251-2c519fb30962-bluemix.cloudantnosqldb.appdomain.cloud')

cap= cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

while True:
        _, frame = cap.read()
        decodedObjects = decode(frame)
        for obj in decodedObjects:
            #print ("Data", obj.data)
            a=obj.data.decode('UTF-8')
            cv2.putText(frame, "Ticket", (50, 50), font, 2, (255, 0, 0), 3)

            #print (a)
            try:
                response = service.get_document(
                db='booking',
                doc_id = a
                ).get_result()
                print (response)
                time.sleep(5)
            except Exception as e:
                print(a)
                print ("Not a Valid Ticket")
                time.sleep(5)

        cv2.imshow("Frame",frame)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
client.disconnect()
