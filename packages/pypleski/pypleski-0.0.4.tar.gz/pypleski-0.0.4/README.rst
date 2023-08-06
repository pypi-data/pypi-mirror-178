# What is pypleski?

pypleski (Pythonic Plesk Interface) is a collection of functions and classes that aim to ease the use of the Plesk XML API. The most important classes being PleskRequestPacket and PleskResponsePacket which are designed to represent the Request and Response Packets defined by Plesk.

For more information on Request and Response Packets, refer to the definition as described in the Plesk XML API Documentation.
https://docs.plesk.com/en-US/obsidian/api-rpc/about-xml-api/xml-api-packets.50168/

The PleskRequestPacket class takes the work of writing complete XML requests thus reducing the amount of written code for each request significantly.


To create a new customer the XML in your request should look somewhat like this:
<?xml version="1.0" encoding="UTF-8" ?>	
<packet>
<customer> 
<add>   
 <gen_info>       
<cname>LogicSoft Ltd.</cname>        
<pname>Stephen Lowell</pname> 
<login>stevelow</login>
<passwd>Jhtr66fBB</passwd>
<status>0</status>        
<phone>416 907 9944</phone>        
<fax>928 752 3905</fax>        
<email>host@logicsoft.net</email>        
<address>105 Brisbane Road, Unit 2</address>        <city>Toronto</city> 
<state/>        
<pcode/>       
 <country>CA</country>    
 </gen_info> 
</add> 
</customer>
</packet>

….
Example cited from the official Plesk docs: https://docs.plesk.com/en-US/obsidian/api-rpc/about-xml-api/xml-api-packets/a-sample-packet.50169/
….

This can be reduced to the following lines:

request = PleskRequestPacket("customer","add", gen_info = { 
                'cname': ‘LogicSoft Ltd.’, 
                'pname': ‘Stephen Lowell’,
                'login': ‘stevelow’,
                'passwd': ‘Jhtr66fBB’,
                'status': 0,
                'phone': '416 907 9944',
                'fax': '928 752 3905',
                'email': 'host@logicsoft.net',
                'address': '105 Brisbane Road, Unit 2',
                'city':'Toronto',
                'state':'',
                'pcode':'',
                'country':'CA'
                })

This approach provides a more pythonic way of interfacing the Plesk API.

The first argument selects the module we want to talk to. The second argument sets the operation we want to process on that module. The third argument takes all further information in the form of a dictionary. In the example above that would be everything within the “gen_info” tag. 

# What pypleski is not
Pypleski is not a security tool. Sanitation of input and error handling should be implemented by app developers. 

Pypleski is not a full fledged API wrapper yet. However, we keep working towards implementing more and more manager classes, to cover as many modules as possible.

# Getting started 

You can install pypleski using pip by running the following command:

pip install pypleski

Write a little request and print out the response:

from pypleski.core import *

TOKEN = "token_here"  # change this to a valid access token

HOST = "localhost" # change this to your servers URL 

client = PyPleskiApiClient(HOST) 

request = PleskRequestPackage(a,b,c) # need to compose a fitting request 

response = client.request(request)

print(f" The response XML is: \n {response.to_string()}")









