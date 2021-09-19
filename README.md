# Cloudflare IP Updater  
This is a small script to automatically update the IP of a certain DNS record in Cloudflare.    
It's useful for people who, like me, have a dynamic IP that can't be turned off and want to keep their domains updated.    

## Installation   

 - Clone this repo.    
 - Run `pip install -r requirements.txt`    
 - Configure the .env file or run the script for the first time.
	 - CF_API_KEY: Your Cloudflare DNS API key or Token. Must have "Edit DNS Zones" permission.   
	 - DNS_ZONE: The name of your Cloudflare DNS zone.
	 - DOMAIN_NAME: The full name of your domain, including subdomains if needed.
 - Set up a Cronjob to run the script with whichever frequency you want to.

 
