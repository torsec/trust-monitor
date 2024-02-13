import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

import json
import requests
import time
from kafka_connector.kafka_connector import run_kafka_producer

#from core import read_entity, read_whitelist
import core
from waiting import wait, TimeoutExpired

# Disable insecure TLS requests warnings
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

tech = "enarx_v0_7_1"

hostname = "localhost"
port = 8080

# .wasm file to check (CHECK THE PATH!)
file = open('/home/jaco/Desktop/hello-world.wasm', "rb")
wasm_bytes =  file.read()

att_result = False

class AttestationServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, "Hello World!")
        self.end_headers()
    
    def do_POST(self):
        
        global att_result
        
        # Retrive the total lenght of the received bytes
        content_length = int(self.headers['Content-Length'])
        print("\nTotal Bytes Received: ", content_length, "\n")
        
        # Read all bytes received
        all_bytes = self.rfile.read(content_length)
        
        # Take the 1st byte which is the size (number of bytes) of the signature
        bytes_size_signature = all_bytes[0:1]
        num_bytes_signature = int.from_bytes(bytes_size_signature, "little")
        print("Size in bytes of the signed .wasm: " + str(num_bytes_signature))
        
        # Take the signature
        bytes_signature = all_bytes[1:(num_bytes_signature+1)]
        print("Signature on the .wasm: " + bytes_signature.hex() + "\n")

        # Take the certificate of the Keep (bytes)
        bytes_cert = all_bytes[(num_bytes_signature+1):(content_length+1)]

        # Parse the certificate bytes into Certificate object
        x509_cert = x509.load_der_x509_certificate(bytes_cert)
        
        # Take the current datetime UTC and compare it with the expiration date of the Keep's certificate
        current_utc_datetime = datetime.utcnow()
        if x509_cert.not_valid_after.__lt__(current_utc_datetime):
                raise ValueError("Certificate expired!\n")     
        
        # Print the certificate of the Keep
        print("CERTIFICATE OF THE KEEP:")
        print("Issuer: ", x509_cert.issuer)
        print("Subject: ", x509_cert.subject)
        print("Serial Number: ", x509_cert.serial_number)
        print("Expiration Date: ", x509_cert.not_valid_after_utc)
        print("Version: ", x509_cert.version)
        print("Signature: ", x509_cert.signature.hex())
        print("Signature Algorithm: ", x509_cert.signature_algorithm_oid.dotted_string)
        
        # Get the public key from the certificate
        pubkey = x509_cert.public_key()
        try:
                # Verify the signature over the .wasm with the public key
                pubkey.verify(bytes_signature, wasm_bytes, ec.ECDSA(hashes.SHA256()))
                att_result = True
                print("Attestation: " + att_result.__str__())
                self.send_response(200, "Certificate successfully received and signature over the .wasm verified!")
                self.end_headers()
        except:
                att_result = False
                print("Error: Invalid Signature exception!")
                self.send_response(400, "Bad Request!")
                self.end_headers()

class EnarxAdapter():

    def __init__(self) -> None:
        pass

    def register(entity, whitelist, verifier):
        pass

    def attest(entity, steward, whitelist, se, topic):
        
        if tech not in entity["att_tech"]:
            return {"error" : tech + " is not present into the entity's attestation technologies list"}
    
        webServer = HTTPServer((hostname, port), AttestationServer)
        print("TM Enarx Attestation Server started at http://%s:%s" %(hostname, port))
                
        try:
            webServer.handle_request()
            print("\nAttestation server shutdown.\n")
        except KeyboardInterrupt:
            print("\nAttestation server forced shutdown.\n")
        
        
        while not se.is_set():
            if att_result == True:
                run_kafka_producer( {
                    "entity_uuid": entity["entity_uuid"],
                    "att_tech": tech,
                    "trust": True
                }, topic )
            
                try:
                    if wait(lambda : se.is_set(), timeout_seconds=10, sleep_seconds=0.1) is True:
                        break
                except TimeoutExpired:
                    pass
            
            else:
                run_kafka_producer( {
                    "entity_uuid": entity["entity_uuid"],
                    "att_tech": tech,
                    "trust": False
                }, topic )
                
                try:
                    if wait(lambda : se.is_set(), timeout_seconds=10, sleep_seconds=0.1) is True:
                        break
                except TimeoutExpired:
                    pass