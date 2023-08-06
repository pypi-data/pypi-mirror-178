from contextlib import contextmanager
import http.client
import ssl
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import json
import xmltodict
import random
import base64

### Core Classes


class PleskResponsePacket():
    """ PleskResponsePacket Class provides an easy way to read responses Packets from the PLESK XML API    

    Args:
        response_xml (string): Takes the response string from PleskClient.request()
        
    
    Use examples:

        request_packet = PleskRequestPacket("webspace", "add", webhosting = {"gen_setup":{'...':'...'}, "hosting": {'...':'...'}})  

        response = PleskApiClient.request(request_packet.to_string())


        response_packet = PleskResponsePacket(response)

        response_json = response_packet.to_JSON()

        response_dict = response_packet.to_dict()

        response_list = response_packet.to_list()
        
    """
    _is_error = True

    def __init__(self, response_xml):
       
        self.packet = ET.fromstring(response_xml)                      
        err = self.packet.find(".//errcode")        
        if err is None:                             
            self._is_error = False            


    def to_JSON(self) -> str:    ### easy to use with a JSON string        
        """ 
        Returns:
            str: Response as JSON string
        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:    ### easy to use as dictionary
        """ 
        Returns:
            dict: Response as dict
        """
        return xmltodict.parse(self.to_string())

    def to_list(self) -> list :    ### only usefull for few responses due to its structure
        """ 
        Returns:
            list: Response as string list
        """
        return ET.tostringlist(self.packet, encoding="UTF-8")

    def to_string(self) -> str:    ### get the plain XML String
        """ 
        Returns:
            str: Response as XML string
        """
        return ET.tostring(self.packet, encoding="UTF-8")

    def as_xml_etree_element(self) -> ET.Element:
        """
        Returns:
            xml.etree.ElementTree.Element: The response as xml.etree.ElementTree.Element object
        """
        return self.packet
        
    def is_error(self) -> bool:   ### see if it is an error before parsing any output
        """
        Returns:
            bool: True if response contains an error
        """
        return self._is_error





### get, set, del operations all have the same pattern:
#        packet/ module / operation / filter 
### other operations are less predictable

class PleskRequestPacket():        
    """ PleskRequestPacket Class provides an easy way to create PLESK XML API requests
        
        Use examples:

        packet = PleskRequestPacket("webspace", "get", filter={"owner-id":5}, dataset={})

        PleskApiClient.request(packet.to_string())

        packet2 = PleskRequestPacket("webspace", "add", webhosting = {"gen_setup":{'d':'d'}, "hosting": {'d':'d'}})    

        PleskApiClient.request(packet2.to_string())


        More practical example for use in a custom function :  

        def add_customer(self, cname, pname, login, passwd) -> PleskResponsePacket:

            request = PleskRequestPacket("customer","add", gen_info = { 
                'cname': cname, 
                'pname': pname,
                'login': login,
                'passwd': passwd,
                'status': 0,
                'phone': '',
                'fax': '',
                'email': '',
                'address': '',
                'city':'',
                'state':'',
                'pcode':'',
                'country':''
                })


        Or preparing a Statement in a variable: 
            customer_del = PleskRequestPacket("customer","del", filter = { 'login': 'login'})
    """

    def __init__(self, module:str ="webspace", operation:str = "get", **data) -> None:                                
        self.packet = ET.Element('packet') # The Packet (Root) Node          
        self.module = ET.SubElement(self.packet,module) # The Module Node
        self.operation = ET.SubElement(self.module,operation) # The Operation Node        
        self.filter = None # The Filter Node               
        self.set_packet_version()
        self._setup(**data)



    def _setup(self, **data):
        """ _setup function - Checks if there if the operation tag implies the use of a filter and adds it if needed 
        before adding the provided data to the operation node
            Should only be Called by __init__ 
            
        """
        if self.operation.tag in ["get", "set", "del"] and "filter" in data:   # possibly redundant condition 
            self.add_filter(**data["filter"]) 
            del data["filter"]                   
        self.add_data_to_node(self.operation, **data)         


    def set_packet_version(self, version:str="1.6.7.0") -> None:
        """Sets the packet version for the request

        Args:
            version (str, optional): Defaults to "1.6.7.0".
        """
        
        self.packet.set("version", version)


    def add_data_to_node(self,parent, **data) -> None:    
        """ add_data_to_node function - Adds all data sets to the given parent Element 
            
            TODO 
                -check if we can make private some manager classes access it directly 
                 this should no longer be necessary as the dataset will now be taken together with filter in the constructor of
                 PleskRequestPackage
        
        """
        if self.operation.tag in ["get","set","del"] and self.filter is None:
            print(f" Cant add Data {data} when craftin a {self.operation.tag} request when no filter is set. Use add_filter() to add a filter first.")
            return   
        for key, value in data.items(): 
            ## Python doesn't allow var names to have dashs 
            # if key contains substring "_id" replace it with "-id"  same for "_name"          
            key = key.replace("_id","-id")                                            
            key = key.replace("_name","-name")
            e = ET.SubElement(parent, key)            
            if type(value) == dict:
                self.add_data_to_node(e,**value) #recursion if we have another dict
            else:
                e.text = f"{value}"       


    def add_filter(self, **filter) -> None:
        
        """add_filter function - Adds a filter for a single get, set or del request
        
        Args:
            filter (dict): The filter to add                

        """

        if self.operation.tag not in ["get","set","del"]:
            print(f" Cant add Filter {filter} when craftin a {self.operation.tag} request. Use add_data_to_node() instead.")
            return
        elif self.filter is None: ### make sure filter is set when needed
            self.filter = ET.SubElement(self.operation,'filter')
        for key, value in filter.items():            
            ## Python doesn't allow the names to have dashs ???
            # if key contains substring "_id" replace it with "-id"            
            key = key.replace("_id","-id")    
            key = key.replace("_name","-name")                               
            e =ET.SubElement(self.filter, key)
            e.text = f"{value}"


    def to_string(self, encoding="UTF-8") -> str:
        """to_string function - returns the packet XML as a string
        Args:
            encoding (string): Set string encoding - defaults to: UTF-8
        Returns:
            str: The Plesk Response XML as string
        
        """
        return ET.tostring(self.packet,encoding=encoding)
    



class PyPleskiApiClient:
    """PyPleskApiClient Class - A simple http(s) client that uses http.client and ssl
    
    This classes request(request) method returns a PleskResponsePacket object instead of a String.
    The request argument can be a XML String or a PleskResponsePacket

    
      Args:
            server (_type_): The URL to your PLESK Server
            port (int, optional): The Port PLESK is listening. Defaults to 8443.
            use_ssl (str, optional): Use SSL (https). Defaults to True.
            unverified_ssl (bool, optional): Ignore ssl errors. Defaults to False.            
    """
    _access_token = None # will store the set access token as string
    _credentials = None # will store credentials as tuple("username","password")


    def __init__(self, server:str, port=8443, use_ssl = True, unverified_ssl = False):
        """Constructor

        Args:
            server (_type_): The URL to your PLESK Server
            port (int, optional): The Port PLESK is listening. Defaults to 8443.
            use_ssl (str, optional): Use SSL (https). Defaults to True.
            unverified_ssl (bool, optional): Ignore ssl errors. Defaults to False.
        """
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.unverified_ssl = unverified_ssl        
        
    def set_credentials(self, user:str, pswd:str ) -> None:        
        """Set the credentials for PLESK

        Args:
            user (str): Your PLESK username
            pswd (str): Your PLESK password
        """
        self._credentials = (user,pswd)

    def set_access_token(self, token:str) -> None:
        """Set an access token to use instead of your credentials

        Args:
            token (str): Your PLESK access token        
        """
        if not token:
            return
        self._access_token = token
        del self._credentials # No need to keep them in memory as we are using the token
    
    @contextmanager
    def _create_connection(self) -> http.client.HTTPSConnection or http.client.HTTPConnection:
        """ Create a Connection to the PLESK Server                  

        Returns:
            http.client.HTTPSConnection or http.client.HTTPConnection: Returns a Connection Object
        """
        try:
            if not self.use_ssl:
                connection = http.client.HTTPConnection(self.server, self.port) # implement log warning 

            if self.unverified_ssl:
                connection = http.client.HTTPSConnection(self.server, self.port, context=ssl._create_unverified_context())
            else:
                connection = http.client.HTTPSConnection(self.server, self.port)  
            yield connection
        finally: 
            connection.close()

    
    def _header(self) -> dict:
        """ Prepares the header for the Request        

        Returns:
            dict: A dictionary containing the headers for use with the http.client's request method
        """
        header = {"Content-Type": "TEXT/XML", "HTTP_PRETTY_PRINT": "TRUE"}        
        if self._access_token: # use access token     
            header["KEY"] = self._access_token
           
        else: # unpack the credentials from tuple into header dict
            header["HTTP_AUTH_LOGIN"], header["HTTP_AUTH_PASSWD"]  = self._credentials 
        
        return header

    def request(self, request:str or PleskRequestPacket) -> PleskResponsePacket:
        """ Send a Request to the set PLESK Server

        Args:
            request (str | PleskRequestPacket): The Request to the PLESK API as XML String or PleskRequestPacket Object

        Returns:
            PleskResponsePacket: The Response Packet as PleskResponsePacket Object
        """
        try:
            xml = request.to_string()
        except Exception:
            xml = request # set the XML with the request

        with(self._create_connection()) as connection:
            connection.request("POST", "/enterprise/control/agent.php", xml, self._header())
            response = connection.getresponse()
            data = response.read()
            print(data.decode("utf-8"))
            return PleskResponsePacket(data.decode("utf-8"))        
            
class PleskApiClient(PyPleskiApiClient):
    """ 
    PleskApiClient - compatibility class to support legacy apps 

    It is recommended to use PyPleskiApiClient instead. If you need the request method to return a string instead of an PleskResponsePacket use this legacy adapter.
    """

    def request(self, request:str or PleskRequestPacket) -> str:
        """ Send a Request to the set PLESK Server

        Args:
            request (str | PleskRequestPacket): The Request to the PLESK API as XML String or PleskRequestPacket Object

        Returns:
            str: The Response as XML string
        """
        try:
            xml = request.to_string()
        except Exception:
            xml = request # set the XML with the request

        with(self._create_connection()) as connection:
            connection.request("POST", "/enterprise/control/agent.php", xml, self._header())
            response = connection.getresponse()
            data = response.read()            
            return data.decode("utf-8")

class PleskApiClientDummy(PyPleskiApiClient):
    """ PleskApiClientDummy     

        This class acts as placeholder for testing

    """
    ### Just for testing purpose
    # no real connection 

    
    def request(self, request, error = False) -> str:
        """ simulates a request and returns a positive add user operation or an webspace error

        Args:
            request (_type_): the Request XML When using the dummy this does nothing.
            error (bool, optional): If you need an error set to True. Defaults to False.

        Returns:
            str: An XML Response String        
        
        """
        return """<packet>
                        <webspace>
                            <get>
                                <result>
                                    <status>error</status>
                                    <errcode>1013</errcode>
                                    <errtext>Object not found.</errtext>
                                    <id>1234</id>
                                </result>
                            </get>
                        </webspace>
                    </packet>""" if error else """
                        <packet version="1.6.7.0">
                            <customer>
                                <add>
                                    <result>
                                        <status>ok</status>
                                        <id>3</id>
                                        <guid>d7914f79-d089-4db1-b506-4fac617ebd60</guid>
                                    </result>
                                </add>
                            </customer>
                        </packet>"""


### Some more or less usefull functions
        
        
def get_plesk_session_token(plesk:str, user:str, password:str, ip:str) -> str:
    """Requests a Session token for the given credentials

    Args:
        plesk (str): The Plesk Server URL
        user (str): username
        password (str): password
        ip (str): Your IP address

    Returns:
        str: the response as string, should contain the session token or an error string.
    """
    
    request = PleskRequestPacket("server", "create_session", login=user,data={'user_ip':ip, 'source_server':''})
    print(request.to_string())
    api = PyPleskiApiClient(plesk)
    api.set_credentials(user,password)
    try:
        response = api.request(request)
        response = response.to_dict()[0]
    except Exception as e: 
        print(f"An error occured while trying to get a valid session token: {e}")       
        response = "An error occured. Check stdout for more details."          
    finally:
        return response
    

def generate_password(length:int=16) -> str:
    """ A simple random password generator

        The passwords are not spefically safe. You should not use this function unless your creativity lets you down. 

    Args:
        length (int, optional): The length of the generated string. Defaults to 16.

    Returns:
        _type_: _description_
    """
    pw = ''.join((chr(random.randint(0,255))) for _ in range(length))
    return (f"^{base64.encodestring(pw.encode('UTF-8')).strip().decode('UTF-8')}").replace('=',f"{(chr(random.randint(33,152)))}")

