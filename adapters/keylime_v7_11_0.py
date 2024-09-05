import json
from kafka_connector.kafka_connector import run_kafka_producer
from waiting import wait, TimeoutExpired
import os
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast
from database_connectors.instances import (edit_state_entity)
from database_connectors.whitelists import (retrieve_whitelist)

tech = "keylime_v7_11_0"

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


EXIT_SUCESS = 0

EnvType = Dict[str, str]

class KeyLimeAdapter():

    def __init__(self):
        pass

    def register(entity, whitelist, verifier):
        """
        Keylime does not need an implemetation for the register method
        """
        pass

    def attest(entity, verifier, whitelist, se, topic):

        # if tech not in entity["att_tech"]:
        #     return {"error" : tech + " is not present into the entity's attestation technologies list"}
        # json_data = '''
        # {
        #   "whitelist": {
        #     "a_list_data": [
        #       "9797edf8d0eed36b1cf92547816051c8af4e45ee boot_aggregate",
        #       "144d39136fe9b2a8ecb885c8e8c1643f76c6be99 /init",
        #       "851d29fc3a7a0321d50dfc77951a9fbf34c2e95b /bin/bash",
        #       "48c7bc5e73967f814fc311198eb3a641d55e5297 /bin/mount",
        #       "d868692abaf98f62c4f824382d5fbd7a84206296 /bin/busybox",
        #       "44d323d38dc68e41a3ffd33a9ab6e1b4262837df /sbin/swapon",
        #       "754718a94931af7ef00eb485b947b6bea5e5496d /etc/init.d/rcS",
        #       "2d4e5a83beec6890d34279a728d78e961a291bd0 /etc/init.d/S01syslogd",
        #       "4e7cea47d80cbe5a78bddf7867b93d29282637eb /etc/init.d/S02klogd",
        #       "391a039274c20057c2a175aee14ef05e0af53303 /etc/init.d/S02sysctl",
        #       "40e0f63f666c42b2886f9711082681058496e00f /etc/init.d/S20urandom",
        #       "e07ddca4980afb3f426d822274454cb30fd89bc5 /etc/init.d/S30cgroupfs",
        #       "b2909c1030fdf7d9e471ba8107b7d0b389e7c373 /usr/bin/cgroupfs-mount",
        #       "442285b4bc6a70490cda86aba140c0bcb4eef6cc /bin/mountpoint",
        #       "af35530c72e0ea4c8f247f6a455f065ab15e7b8e /etc/init.d/S35iptables",
        #       "82545ca4026a187785c16fdede04b8b2b5471e9a /usr/sbin/xtables-legacy-multi",
        #       "b7bafb3e99648f3cc39d559fcb9dff7e034eb246 /etc/init.d/S40network",
        #       "f76fddbd55c96ed622ca4f5528de1032e1268e69 /etc/network/if-pre-up.d/wait_iface",
        #       "4f2cc2a6d59a079929f2e5dbe7b2e44bda1ef108 /sbin/ip",
        #       "534de65d4dd60db45af94b8394d5a324cfaf70cf /etc/network/nfs_check",
        #       "cc587725a5dbe10cff2e73d1d68d67ea2f03ab2c /usr/share/udhcpc/default.script",
        #       "ff15e91731c40320832517a84895eb042e27ec41 /etc/init.d/S49ntp",
        #       "7e6d18fb8ee9608abcac863584b67b6045502b60 /usr/sbin/ntpd",
        #       "082461771b5d97660b3f7e8f0739aed6ff740cfa /etc/init.d/S50dropbear",
        #       "d67dc2d6a38884a7be14fd8d1c1beec7236fb5dd /usr/sbin/dropbear",
        #       "5e98f6df989b00cc1dfdc026178c2587de97ecb8 /etc/init.d/S51sysrepo-plugind",
        #       "a1f89a60937e85c0350e0ffbb315b1d6d1ca99de /usr/bin/sysrepo-plugind",
        #       "1f55337f63f090f59435a755770c262642ed1be6 /etc/init.d/S52netopeer2",
        #       "fd44199590ee0638fa09356e69bcf7a6b67f8f3a /usr/bin/sysrepoctl",
        #       "3ebe51a9005635cc1538d6bced3f0670c6014deb /usr/bin/sysrepocfg",
        #       "d647ceee24e741fa145523fb60312d83caed4f15 /usr/sbin/netopeer2-server",
        #       "bea0fa17dedc697bcef3c8f499ab114cdd6eede0 /etc/init.d/S60dockerd",
        #       "ba8744608e4a326b6c97ac3d6f74e40d3e5abb54 /usr/bin/dockerd",
        #       "80e65ade7bd7c899c792692399ca86b7271ea647 /usr/bin/containerd",
        #       "86e8c42a086633648993a75c79c62d93272aeb82 /usr/bin/kmod",
        #       "04b4ee7d6c3fc6641089a91dee3636897d0a9682 /root/agent"
        #     ]
        #   }
        # }
        # '''
        
        # return_data = {'retout': [b"Namespace(command='status', agent_ip=None, agent_port=None, registrar_ip=None, registrar_port=None, cv_agent_ip=None, verifier_ip=None, verifier_port=None, verifier_id=None, verifier_check=True, agent_uuid='5556d95f-7c71-46e3-9e04-dbfcbd7eb96d', file=None, ca_dir=None, keyfile=None, payload=None, incl_dir=None, allowlist=None, runtime_policy=None, ima_sign_verification_keys=[], ima_sign_verification_key_sigs=[], ima_sign_verification_key_sig_keys=[], ima_sign_verification_key_urls=[], ima_sign_verification_key_sig_urls=[], ima_sign_verification_key_sig_url_keys=[], mb_refstate=None, allowlist_url=None, ima_exclude=None, runtime_policy_checksum=None, runtime_policy_sig_key=None, runtime_policy_url=None, tpm_policy=None, verify=False, allowlist_name=None, runtime_policy_name=None, supported_version=None)\n", b"2024-07-15 14:21:19.758 - keylime.config - INFO - Reading configuration from ['/etc/keylime/tenant.conf']\n", b'2024-07-15 14:21:19.758 - keylime.tenant - INFO - Setting up client TLS...\n', b'2024-07-15 14:21:19.759 - keylime.tenant - INFO - Using default client_cert option for tenant\n', b'2024-07-15 14:21:19.759 - keylime.tenant - INFO - Using default client_key option for tenant\n', b'2024-07-15 14:21:19.759 - keylime.tenant - INFO - No value provided in client_key_password option for tenant, assuming the key is unencrypted\n', b'2024-07-15 14:21:19.764 - keylime.tenant - INFO - TLS is enabled.\n', b"2024-07-15 14:21:19.765 - keylime.config - INFO - Reading configuration from ['/etc/keylime/verifier.conf']\n", b'2024-07-15 14:21:19.891 - keylime.tenant - INFO - Status from Registrar (127.0.0.1:8891): Agent 5556d95f-7c71-46e3-9e04-dbfcbd7eb96d exists on registrar 127.0.0.1 port 8891.\n', b'2024-07-15 14:21:19.891 - keylime.tenant - INFO - {"code": 200, "status": "Agent 5556d95f-7c71-46e3-9e04-dbfcbd7eb96d exists on registrar 127.0.0.1 port 8891.", "results": {"5556d95f-7c71-46e3-9e04-dbfcbd7eb96d": {"aik_tpm": "ARgAAQALAAUAcgAAABAAFAALCAAAAAAAAQC7REVtHUHb/EAH2gRKfzwuo3YpIVVz4WNWmGRtzDMtlleOv9raA33RxvJD+G00Yh49LWdD6AJIlRy+AYdXQtVdF9rXXbD1dd+/QLFNyqF4SMazLAYoIgWFAhblm6O9Strjpa6qr4AK3jewpHVV4D7SIL2ZDifki5aFnzmj68yqYp9K80p1xL3qhzuqFUHeHPWeEHZXHX12pUP+TG1QnG+Rs/UsWUKx769EaXy2bgLpd66wjsQYaoXa7SMhyAwPAhmALKx8bq4V2xxFBGLcE/FeUxODVMEacX1hR8Cfs3tKfxf3kTZlFp6jZnoX6XNvf6X91fJwxuk1k1mHpq31oDBl", "regcount": 1, "ek_tpm": "ARoAAQALAAMAcgAAAAYAgABDABAIAAAAAAABANz6Cwu6zI/gWqzZDJD9Ub8KVIrcp5rMutPEY8KUQQ/n5sceeA8R22vYcGJ9sWc/QjhTJDXxsYniJoi6Pgxk6LWboqkNBEGwL/KrIUaav1DY05uabae2Fi+ebhJr2Y8+P9xRQFWmwYbFz4+JGB25glJAW45crWZep7Hhv6jC2PCvOSwkRLUfcITaKiUelKOUPU20oTMSNOhRuAEzm8uz/Fq9X3b2bSOXEKzevDXAKqdoi4NIeXBB8XweJC10foxKHyQBgBo+9YyxpVR1aH3W5cnJQdsQ4vP53+ziYRAfZnUa1ZTj3a5ZqcXAas2SMPi+csH9i4htTyvmh0h8ghcjVDU=", "ip": "127.0.0.1", "port": 8080, "mtls_cert": "-----BEGIN CERTIFICATE-----\\nMIIC4DCCAcgCAQEwDQYJKoZIhvcNAQELBQAwNjELMAkGA1UEBhMCSVQxEzARBgNV\\nBAoMCk15IENvbXBhbnkxEjAQBgNVBAMMCWxvY2FsaG9zdDAeFw0yNDA3MTUxMjA1\\nMTBaFw0yNTA3MTUxMjA1MTBaMDYxCzAJBgNVBAYTAklUMRMwEQYDVQQKDApNeSBD\\nb21wYW55MRIwEAYDVQQDDAlsb2NhbGhvc3QwggEiMA0GCSqGSIb3DQEBAQUAA4IB\\nDwAwggEKAoIBAQDBI3w4eDqW6DmlSYdGhrYzcCUbi6zCOabLPAAbpCmCulVKYU5w\\n/VVHUUkAPmkLGzn5vWjfDUM1F//SmFiFmZFxPpEgLVjLnl77BszFE42O8V/cLsRS\\nzsr59m2rZhWF/f8z/QSDzmKZVucKdINqr19m3zTsk6zDHnpG9irSRjk3rbY/pul4\\nkt581qq76wF3KshmzmyjNm6Vg03jVvzS94aigQ9qRKT3fPTlyeGLrEmpo254I3VG\\nW2Iwr4mJJqKLLPo+J/SWi420kfwN8nY8Of6UXFpETkDr7eMzkUFWQOlJEIrY1Osp\\nmHulGyaOQKAQLq2z6lErXqdUJMmYT57W6vobAgMBAAEwDQYJKoZIhvcNAQELBQAD\\nggEBAGHwROjyzfOB4nbZmO1uKEn25BYpEBM1/8GDOthS1e73qxzvIndR1jHT+zqA\\ncUkSRfqn2gEBt1K4rM1FFcrrgDwWc3fzDplKVuVVy8OQO2urV0Av5uZu+OFCG9RM\\niIfn9hLB6rN31R4vrEfJkWKWWJhdfzGnUkTvVw8Ezl7EgeNWuKGgcFewiYSiCN0w\\n/KKyVBjpRqZw6lrNaze53oYAdflx+QdlwJA1daO+fHM9x8MZzYRpBAA87cqWgwkn\\nOBG3m4D58TI4J98+W2FeWErOvF/XB3ioTU0g7QD+caNsF/IQsoi8+AoBBO2+E+h9\\nZcBAaXsZ0KpSr5eBMsXmILZju/k=\\n-----END CERTIFICATE-----\\n", "ekcert": "emulator", "operational_state": "Registered"}}}\n', b'2024-07-15 14:21:19.891 - keylime.tenant - INFO - Agent Info from Registrar (127.0.0.1:8891):\n', b'{"5556d95f-7c71-46e3-9e04-dbfcbd7eb96d": {"aik_tpm": "ARgAAQALAAUAcgAAABAAFAALCAAAAAAAAQC7REVtHUHb/EAH2gRKfzwuo3YpIVVz4WNWmGRtzDMtlleOv9raA33RxvJD+G00Yh49LWdD6AJIlRy+AYdXQtVdF9rXXbD1dd+/QLFNyqF4SMazLAYoIgWFAhblm6O9Strjpa6qr4AK3jewpHVV4D7SIL2ZDifki5aFnzmj68yqYp9K80p1xL3qhzuqFUHeHPWeEHZXHX12pUP+TG1QnG+Rs/UsWUKx769EaXy2bgLpd66wjsQYaoXa7SMhyAwPAhmALKx8bq4V2xxFBGLcE/FeUxODVMEacX1hR8Cfs3tKfxf3kTZlFp6jZnoX6XNvf6X91fJwxuk1k1mHpq31oDBl", "regcount": 1, "ek_tpm": "ARoAAQALAAMAcgAAAAYAgABDABAIAAAAAAABANz6Cwu6zI/gWqzZDJD9Ub8KVIrcp5rMutPEY8KUQQ/n5sceeA8R22vYcGJ9sWc/QjhTJDXxsYniJoi6Pgxk6LWboqkNBEGwL/KrIUaav1DY05uabae2Fi+ebhJr2Y8+P9xRQFWmwYbFz4+JGB25glJAW45crWZep7Hhv6jC2PCvOSwkRLUfcITaKiUelKOUPU20oTMSNOhRuAEzm8uz/Fq9X3b2bSOXEKzevDXAKqdoi4NIeXBB8XweJC10foxKHyQBgBo+9YyxpVR1aH3W5cnJQdsQ4vP53+ziYRAfZnUa1ZTj3a5ZqcXAas2SMPi+csH9i4htTyvmh0h8ghcjVDU=", "ip": "127.0.0.1", "port": 8080, "mtls_cert": "-----BEGIN CERTIFICATE-----\\nMIIC4DCCAcgCAQEwDQYJKoZIhvcNAQELBQAwNjELMAkGA1UEBhMCSVQxEzARBgNV\\nBAoMCk15IENvbXBhbnkxEjAQBgNVBAMMCWxvY2FsaG9zdDAeFw0yNDA3MTUxMjA1\\nMTBaFw0yNTA3MTUxMjA1MTBaMDYxCzAJBgNVBAYTAklUMRMwEQYDVQQKDApNeSBD\\nb21wYW55MRIwEAYDVQQDDAlsb2NhbGhvc3QwggEiMA0GCSqGSIb3DQEBAQUAA4IB\\nDwAwggEKAoIBAQDBI3w4eDqW6DmlSYdGhrYzcCUbi6zCOabLPAAbpCmCulVKYU5w\\n/VVHUUkAPmkLGzn5vWjfDUM1F//SmFiFmZFxPpEgLVjLnl77BszFE42O8V/cLsRS\\nzsr59m2rZhWF/f8z/QSDzmKZVucKdINqr19m3zTsk6zDHnpG9irSRjk3rbY/pul4\\nkt581qq76wF3KshmzmyjNm6Vg03jVvzS94aigQ9qRKT3fPTlyeGLrEmpo254I3VG\\nW2Iwr4mJJqKLLPo+J/SWi420kfwN8nY8Of6UXFpETkDr7eMzkUFWQOlJEIrY1Osp\\nmHulGyaOQKAQLq2z6lErXqdUJMmYT57W6vobAgMBAAEwDQYJKoZIhvcNAQELBQAD\\nggEBAGHwROjyzfOB4nbZmO1uKEn25BYpEBM1/8GDOthS1e73qxzvIndR1jHT+zqA\\ncUkSRfqn2gEBt1K4rM1FFcrrgDwWc3fzDplKVuVVy8OQO2urV0Av5uZu+OFCG9RM\\niIfn9hLB6rN31R4vrEfJkWKWWJhdfzGnUkTvVw8Ezl7EgeNWuKGgcFewiYSiCN0w\\n/KKyVBjpRqZw6lrNaze53oYAdflx+QdlwJA1daO+fHM9x8MZzYRpBAA87cqWgwkn\\nOBG3m4D58TI4J98+W2FeWErOvF/XB3ioTU0g7QD+caNsF/IQsoi8+AoBBO2+E+h9\\nZcBAaXsZ0KpSr5eBMsXmILZju/k=\\n-----END CERTIFICATE-----\\n", "ekcert": "emulator", "operational_state": "Registered"}}\n', b'2024-07-15 14:21:20.060 - keylime.tenant - INFO - Agent Info from Verifier (127.0.0.1:8881):\n', b'{"5556d95f-7c71-46e3-9e04-dbfcbd7eb96d": {"operational_state": "Provide V", "v": "CgaqJz2by9zovd7mpUsUALMOjjuvPsHMvcZMDD3OG+c=", "ip": "127.0.0.1", "port": 8080, "tpm_policy": "{\\"mask\\": \\"0x400\\"}", "meta_data": "ffffff000010000000000000e03d2abfaaaaaa00d83d2abfaaaaaa00e43d2180ffffff004c", "has_mb_refstate": 0, "has_runtime_policy": 1, "accept_tpm_hash_algs": ["sha512", "sha384", "sha256"], "accept_tpm_encryption_algs": ["ecc", "rsa"], "accept_tpm_signing_algs": ["ecschnorr", "rsassa"], "hash_alg": "sha256", "enc_alg": "rsa", "sign_alg": "rsassa", "verifier_id": "default", "verifier_ip": "127.0.0.1", "verifier_port": 8881, "severity_level": null, "last_event_id": null, "attestation_count": 197, "last_received_quote": 1721046078, "last_successful_attestation": 1721046078}}\n'], 'reterr': [b"INFO:keylime.config:Reading configuration from ['/etc/keylime/logging.conf']\n"], 'code': 0, 'fileouts': {}, 'timing': {'t1': 1721046080.256383, 't0': 1721046078.648763}}
        
        
        uuid = entity['external_id']
        filepath = f'/tmp/whitelist_entries_{uuid}.txt'

        with open(filepath, 'w') as file:
            for entry in whitelist['whitelist']['a_list_data']:
                file.write(entry + '\n')
                
        with open("/tmp/payload", 'w') as file:
            pass         
        retDic = run(cmd=["keylime_tenant", "-c", "add", "--uuid", uuid, "-f", "/tmp/payload", "--allowlist", filepath], raiseOnError=False)
        
        print(retDic)
        enc_body = {"_id": entity["whitelist_uuid"]} 
        whitelist_entity = retrieve_whitelist(enc_body)
        whitelist_enclaves = whitelist_entity["whitelist"]["enclaves"]
        
        print(whitelist_enclaves)

        while not se.is_set():
            retDic = run(cmd=["keylime_tenant", "-c", "status", "--uuid", uuid], raiseOnError=False)

            parsed_data = json.loads(retDic['retout'][-1])
            
            agent_data = parsed_data[uuid]
            
            report = {
                "entity_uuid": uuid,
                "trust": False,
                "enclaves": [],
                "containers": [],
                "att_tech": "keylime_v7_11_0"
    		}
            
            other_entities = json.loads(agent_data['meta_data'])
            
            print("other entities")
            print(other_entities)
            
            enclaves = []
            containers = []
            if 'enclaves' in other_entities: 
                if ',' in other_entities['enclaves'][0]:
                    enclaves = other_entities['enclaves'][0].split(",")
                elif other_entities['enclaves'][0] != "":
                    enclaves = other_entities['enclaves']
                    
                if ',' in other_entities['containers'][0]:
                    containers = other_entities['containers'][0].split(",")
                elif other_entities['containers'][0] != "":
                    containers = other_entities['containers']
               
            dict_enclaves = []

            for string in enclaves:
                parts = string.split(":")
                dict_item = {
                    "uuid": parts[0],
                    "hash": parts[1],
                    "signature": parts[2],
                    "trust": False
                }
                
                element_whitelist = next((d for d in whitelist_enclaves if d["uuid"] == dict_item["uuid"]), None)
                if element_whitelist is not None and element_whitelist["hash"] == dict_item["hash"] and element_whitelist["signature"] == dict_item["signature"]:
                    dict_item["trust"] = True
                dict_enclaves.append(dict_item)

            print(dict_enclaves)             
            entity['metadata']['enclaves'] = dict_enclaves
            entity['metadata']['containers'] = []
            
            
            
            if agent_data['operational_state'] == 'Provide V' or agent_data["operational_state"] == 'Get Quote':
                if len(containers) != 0:
                    containers_list = [{"uuid": uuid, "trust": True} for uuid in containers]
                    report['containers'] = containers_list
                    entity['metadata']['containers'] = containers_list
                report['enclaves'] = dict_enclaves
                report['trust'] = True
                entity['state'] = 'trusted'
                edit_state_entity( {"entity_uuid": entity["entity_uuid"], "state": "attesting"} )
            elif agent_data['operational_state'] == 'Registered':
                continue
            else:
                if len(containers) != 0:
                    containers_list = [{"uuid": uuid, "trust": False} for uuid in containers]
                    report['containers'] = containers_list
                    entity['metadata']['containers'] = containers_list
                report['enclaves'] = dict_enclaves
                report['trust'] = False
                entity['state'] = 'untrusted'
                
            run_kafka_producer(report, topic)
            try:
                if wait(lambda : se.is_set(), timeout_seconds=5, sleep_seconds=0.1) is True: # wait 5 s
                    break
            except TimeoutExpired:
                pass

    def delete(entity, verifier):
        """
        Keylime does not need an implemetation for the delete method
        """
        pass

    def status(verifier):
        pass

class RetDictType(TypedDict):
    retout: List[bytes]
    reterr: List[bytes]
    code: int
    fileouts: Dict[str, bytes]
    timing: Dict[str, float]


def _execute(cmd: Sequence[str], env: Optional[EnvType] = None, **kwargs: Any) -> Tuple[bytes, bytes, int]:
    with subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs) as proc:
        out, err = proc.communicate()
        # All callers assume to receive a list of bytes back; none of them uses 'text mode'
        assert isinstance(out, bytes)
        assert isinstance(err, bytes)
        return out, err, proc.returncode


def run(
    cmd: Sequence[str],
    expectedcode: int = EXIT_SUCESS,
    raiseOnError: bool = True,
    outputpaths: Optional[Union[List[str], str]] = None,
    env: Optional[EnvType] = None,
    **kwargs: Any,
) -> RetDictType:
    """Execute external command.

    :param cmd: a sequence of command arguments
    """
    if env is None:
        env = cast(EnvType, os.environ)  # cannot use os._Environ as type

    t0 = time.time()
    retout, reterr, code = _execute(cmd, env=env, **kwargs)

    t1 = time.time()
    timing = {"t1": t1, "t0": t0}

    # Gather subprocess response data; retout & reterr are assumed to be 'bytes'
    retout_list = retout.splitlines(keepends=True)
    reterr_list = reterr.splitlines(keepends=True)

    # Don't bother continuing if call failed and we're raising on error
    if code != expectedcode and raiseOnError:
        raise Exception(
            f"Command: {cmd} returned {code}, expected {expectedcode}, " f"output {reterr_list}, stderr {reterr_list}"
        )

    # Prepare to return their file contents (if requested)
    fileouts = {}
    if isinstance(outputpaths, str):
        outputpaths = [outputpaths]
    if isinstance(outputpaths, list):
        for thispath in outputpaths:
            with open(thispath, "rb") as f:
                fileouts[thispath] = f.read()

    returnDict: RetDictType = {
        "retout": retout_list,
        "reterr": reterr_list,
        "code": code,
        "fileouts": fileouts,
        "timing": timing,
    }
    return returnDict


# list_contains_substring checks whether a substring is contained in the given
# list. The list may be the reterr from 'run' and contains bytes-like objects.
def list_contains_substring(lst: List[bytes], substring: str) -> bool:
    for s in lst:
        if substring in str(s):
            return True
    return False
