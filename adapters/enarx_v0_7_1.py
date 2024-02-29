from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import (ec, utils)
from cryptography.hazmat.primitives import hashes
import pytz
import configparser

import requests
from kafka_connector.kafka_connector import run_kafka_producer

#from core import read_entity, read_whitelist
from waiting import wait, TimeoutExpired

# Disable insecure TLS requests warnings
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

config = configparser.ConfigParser()
config.read('config/config.ini')

tech = "enarx_v0_7_1"

hostname = config["enarx_wasm_att_service"]["hostname"]
port = int(config["enarx_wasm_att_service"]["port"])
att_server_timeout = int(config["enarx_wasm_att_service"]["timeout"])

att_result = None # Used to check if the attestation has been done (att_result = bool(True) or bool(False))
allowed_wasm_hashes = []
run_wasm_hash = ""
attempted_wasm_hash = ""

class AttestationServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, "Hello World!")
        self.end_headers()
    
    def do_POST(self):
        
        global att_result
        global allowed_wasm_hashes
        
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
        current_utc_datetime = current_utc_datetime = datetime.now(pytz.utc)
        if x509_cert.not_valid_after_utc.__lt__(current_utc_datetime):
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
                for hash in allowed_wasm_hashes:
                    
                    wasm_hash_bytes = bytes.fromhex(hash)
                    
                    global run_wasm_hash
                    run_wasm_hash = hash
                    
                    # SHA256 (Intel CPU)
                    if len(wasm_hash_bytes) == 32:
                        # Verify the signature over the .wasm's hash with the public key
                        
                        if  pubkey.verify(bytes_signature, wasm_hash_bytes, ec.ECDSA(utils.Prehashed(hashes.SHA256()))) == None:
                            break
                    
                    # SHA384 (AMD CPU)
                    if len(wasm_hash_bytes) == 48:
                        # Verify the signature over the .wasm's hash with the public key
                        
                        if  pubkey.verify(bytes_signature, wasm_hash_bytes, ec.ECDSA(utils.Prehashed(hashes.SHA384()))) == None:
                            break
                
                att_result = bool(True) # Record successful attestation
                print("Attestation: " + att_result.__str__())
                self.send_response(200, "Certificate successfully received and signature over the .wasm verified!")
                self.end_headers()
        except:
                att_result = bool(False) # Record unsuccessful attestation with invalid signature
                print("Error: Invalid Signature exception!")
                self.send_response(400, "Bad Request!")
                self.end_headers()

class EnarxAdapter():

    def __init__(self) -> None:
        pass

    def register(entity, whitelist, verifier):
        """
        Enarx does not need an implementation for the delete method
        """
        pass

    def attest(entity, _steward, whitelist, _se, topic):
        
        if tech not in entity["att_tech"]:
            return {"error" : tech + " is not present into the entity's attestation technologies list"}
        
        
        if not whitelist["whitelist"]:
            return {"error" : " empty whitelist of WASM hashes"}
        
        global allowed_wasm_hashes
        allowed_wasm_hashes = whitelist["whitelist"]["wasm_hashes_list"]
        
        print(allowed_wasm_hashes)
    
        webServer = HTTPServer((hostname, port), AttestationServer)
        webServer.socket.settimeout(att_server_timeout) # Set the server timeout to 5 mins
        
        print("TM Enarx Attestation Server started at http://%s:%s" %(hostname, port))
                
        webServer.handle_request()
        
        if att_result == True:
            run_kafka_producer( {
                "entity_uuid": entity["entity_uuid"],
                "att_tech": tech,
                # "run_wasm_hash": run_wasm_hash,
                "trust": True
            }, topic )
        
        else:
            run_kafka_producer( {
                "entity_uuid": entity["entity_uuid"],
                "att_tech": tech,
                # "attempted_wasm_hash": run_wasm_hash,
                "trust": False
            }, topic )
            
        # If the server timeout expires, att_result is still None, otherwise is True or False and attestation has been performed
        if att_result == None:
            print("WASM Attestation Server Timeout Expired! - Server shutdown.")
        else:
            print("Attestation done! - Server Shutdown.")

    def delete(entity, verifier):
        """
        Enarx does not need an implementation for the delete method
        """
        pass