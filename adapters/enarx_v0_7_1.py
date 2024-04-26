from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
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
        
        # Take the 1st byte which is the size (number of bytes) of the .wasm hash
        bytes_size_hash = all_bytes[0:1]
        num_bytes_hash = int.from_bytes(bytes_size_hash, "little")
        print("Size in bytes of the .wasm hash: " + str(num_bytes_hash))
        
        # Take the 2nd byte which is the size (number of bytes) of the .wasm signature
        bytes_size_signature = all_bytes[1:2]
        num_bytes_signature = int.from_bytes(bytes_size_signature, "little")
        print("Size in bytes of the signed .wasm: " + str(num_bytes_signature))
        
        # Take the hash of the .wasm
        bytes_hash = all_bytes[2:(num_bytes_hash+2)]
        print("Hash of the .wasm: " + bytes_hash.hex() + "\n")
        
        # Take the signature of the .wasm
        bytes_signature = all_bytes[(num_bytes_hash+2):(num_bytes_hash+2+num_bytes_signature)]
        print("Signature on the .wasm: " + bytes_signature.hex() + "\n")

        # Take the certificate of the Keep (bytes)
        bytes_cert = all_bytes[(num_bytes_hash+2+num_bytes_signature):(content_length+1)]

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
        hash_str = bytes_hash.hex()
        print("WASM hash: " + hash_str + "\n")
        try:
                if hash_str in allowed_wasm_hashes:
                    print("WASM hash is in the whitelist!")                

                    # SHA256 (Intel CPU)
                    if len(bytes_hash) == 32:
                        # Verify the signature over the .wasm's hash with the public key
                        if pubkey.verify(bytes_signature, bytes_hash, ec.ECDSA(utils.Prehashed(hashes.SHA256()))) == None:
                            att_result = bool(True) # Record successful attestation
                            print("Attestation: " + att_result.__str__())
                            self.send_response(200, "Certificate successfully received and signature over the .wasm verified!")
                            self.end_headers()
                            return

                    # SHA384 (AMD CPU)
                    if len(bytes_hash) == 48:
                        # Verify the signature over the .wasm's hash with the public key
                        if pubkey.verify(bytes_signature, bytes_hash, ec.ECDSA(utils.Prehashed(hashes.SHA384()))) == None:
                            att_result = bool(True) # Record successful attestation
                            print("Attestation: " + att_result.__str__())
                            self.send_response(200, "Certificate successfully received and signature over the .wasm verified!")
                            self.end_headers()
                            return
                else:
                    print("Error: WASM hash is not in the whitelist!")
                    self.send_response(400, "Bad Request!")
                    self.end_headers()
                    return
                
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
        
        def stop_server():
            print("Stopping server...")
            webServer.shutdown()
        
        if tech not in entity["att_tech"]:
            return {"error" : tech + " is not present into the entity's attestation technologies list"}
        
        
        if not whitelist["whitelist"]:
            return {"error" : " empty whitelist of WASM hashes"}
        
        global allowed_wasm_hashes
        allowed_wasm_hashes = whitelist["whitelist"]["wasm_hashes_list"]
        
        print(allowed_wasm_hashes)
    
        webServer = HTTPServer((hostname, port), AttestationServer)
        webServer.socket.settimeout(att_server_timeout) # Set the server timeout to 5 mins
        
        # Create a timer that will stop the server after a certain time
        shutdown_timer = threading.Timer(att_server_timeout, stop_server)
        
        # Start the timer
        shutdown_timer.start()
        
        print("TM Enarx Attestation Server started at http://%s:%s" %(hostname, port))
                
        webServer.serve_forever()
        
        if att_result == True:
            run_kafka_producer( {
                "entity_uuid": entity["entity_uuid"],
                "att_tech": tech,
                "trust": True
            }, topic )
        
        else:
            run_kafka_producer( {
                "entity_uuid": entity["entity_uuid"],
                "att_tech": tech,
                "trust": False
            }, topic )
            
        # If the server timeout expires, att_result is still None, otherwise is True or False and attestation has been performed
        if att_result == None:
            print("WASM Attestation Server Timeout Expired! - Server shutdown.")
        else:
            print("Attestation phase done! - Server Shutdown.")

    def delete(entity, verifier):
        """
        Enarx does not need an implementation for the delete method
        """
        pass