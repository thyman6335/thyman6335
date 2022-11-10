import pexpect

#===================================================================================
#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        self.name = name
        self.ip_address = ip
        self.username = user
        self.password = pw
        self.os_type = None

    def connect(self):
        self.session = None

    def get_interfaces(self):
        self.interfaces = '--- Base Device, does not know how to get interfaces ---'

    def get_interface_stats(self,interface):
        return (0,0,0,0)

 
#===================================================================================
#---- Class to hold information about an IOS network device --------
class NetworkDeviceIOS(NetworkDevice):

    #---- Initialization ---------------------------------------
    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)
        self.os_type = 'ios'

    #---- Connect -----------------------------------------------
    def connect(self):
        print '--- connecting IOS: telnet '+self.ip_address

        self.session = pexpect.spawn('telnet '+self.ip_address, timeout=20)
        result = self.session.expect(['Username:', pexpect.TIMEOUT])

        self.session.sendline(self.username)
        result = self.session.expect('Password:')

        # Successfully got password prompt, logging in with password
        self.session.sendline(self.password)
        self.session.expect('>')
 
    #---- Get Stats ---------------------------------------------
    def get_interface_stats(self, interface):

        stats_cmd = 'show interface ' + interface + ' accounting' \
                                      + ' | include IP'

        # Execute the show interface accounting command
        self.session.sendline(stats_cmd)
        result = self.session.expect('>')

        stats_output = (self.session.before).splitlines()

        for stats_line in stats_output:

            stats = stats_line.split()
            if stats[0] == 'IP':  # We only care about 'IP' stats
                return (stats[1],stats[2],stats[3],stats[4])

        print '--- unexpected show interface output'
        return (0,0,0,0)