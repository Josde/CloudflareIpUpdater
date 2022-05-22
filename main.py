import os
import CloudFlare
import requests
from dotenv import load_dotenv
import ipaddress
import json

def main():
    #Initialization
    load_dotenv()
    dns_zone = getEnvironmentOrInput('DNS_ZONE')
    domain_name = getEnvironmentOrInput('DOMAIN_NAME')
    #CF_API_KEY must be defined in .env
    cf = CloudFlare.CloudFlare()
    #Getting our IP
    current_ip = requests.get('https://dynupdate.no-ip.com/ip.php').text
    try:
        ipaddress.ip_address(current_ip)
    except ValueError:
        print("Couldn't get our IP from the web. Exiting.")
        exit(-1)
    if (current_ip):
        IP_NEEDS_UPDATING = False
        if not os.path.exists(os.path.abspath('latest_ip')):
            ip_file = open('latest_ip', 'w+')
        else:
            ip_file = open('latest_ip', 'r+')
        try:
            last_ip = ip_file.readline()
            if (current_ip != last_ip):
                IP_NEEDS_UPDATING = True
                ip_file.truncate(0)
                ip_file.write(current_ip)
        except Exception: #Should be except OSError, but for some reason that doesn't work
            print("Error creating latest_ip file. Are you running with the correct permissions?")
            IP_NEEDS_UPDATING = True
        finally:
            ip_file.close()
        if (IP_NEEDS_UPDATING):
            #Get DNS zones
            zone_info = cf.zones.get(params={'name': dns_zone})
            zone_id = zone_info[0]['id']
            #Get DNS records
            dns_record = cf.zones.dns_records.get(zone_id, params={'name': domain_name})
            dns_record_id = dns_record[0]['id']
            #Update IP
            dns_record[0]['content'] = current_ip
            cf.zones.dns_records.put(zone_id, dns_record_id, data=dns_record[0])

def getEnvironmentOrInput(parameter):
    var = os.getenv(parameter)
    if (var is None):
        value = input("Environment variable {0} not found. Please input it: ".format(parameter))
        env_file = open('.env', 'a+')
        try:
            env_file.write("{0}={1}".format(parameter, value))
        except Exception:
            print("Couldn't create .env file. Are you running this with the correct permissions?\nYou may fix this by manually creating and configuring the .env file.\n")
        finally:
            env_file.close()
            return value
    return var

if __name__ == '__main__':
    main()
