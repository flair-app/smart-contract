import unittest, sys, json, random, time
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG, Verbosity.ERROR])

CONTRACT_WORKSPACE = sys.path[0] + "/../"
TOKEN_CONTRACT_WORKSPACE = "_iqhgcqllgnpkirjwwkms"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
TOKENHOST = Account()

class ProfileMigrateToTmpUnitTest(unittest.TestCase):

    def run(self, result=None):
        super().run(result)

    @classmethod
    def setUpClass(cls):
        reset()
        create_master_account("MASTER")

        create_account("HOST", MASTER)
        smart = Contract(HOST, CONTRACT_WORKSPACE)
        smart.build()
        smart.deploy()
            
        # set eosio.code permission to contract
        HOST.set_account_permission(
            permission_name=Permission.ACTIVE, 
            add_code=True,
            permission=(HOST, Permission.OWNER)
        )

    def randomEOSIOId(self):
        allowChar = "abcdefghijklmnopqrstuvwxyz12345."
        
        randomId = ""
        for i in range(0, 11):
            randomCharIndex = random.randrange(0,31,1)
            randomId += allowChar[randomCharIndex]
        
        return randomId
    
    def randomPythonVar(self):
        allowChar = "abcdefghijklmnopqrstuvwxyz12345"
        
        randomId = ""
        for i in range(0, 11):
            randomCharIndex = random.randrange(0,31,1)
            randomId += allowChar[randomCharIndex]
        
        return randomId

    def getEOSBalance(self, ACCT):
        try:
            accountsRes = TOKENHOST.table("accounts", ACCT)
            return accountsRes.json["rows"][0]["balance"].split()[0]
        except:
            return 0
    
    def createRandomGlobalUser(self, prefix = ""):
        uservar = prefix + self.randomPythonVar()
        create_account(uservar, MASTER)
        return globals()[uservar]

    def setUp(self):
        time.sleep(1) # prevent non unique error for timestamps in eos prices
        
        self.FEEACCT = self.createRandomGlobalUser("user_feeacct_")
        self.ALICE = self.createRandomGlobalUser("user_alice_")
        self.BOB = self.createRandomGlobalUser("user_bob_")
        self.CAROL = self.createRandomGlobalUser("user_carol_")
        self.ELLIOT = self.createRandomGlobalUser("user_elliot_")

        self.userId = self.randomEOSIOId()

        HOST.push_action(
            "addprofile",
            [{
                "id":self.userId,
                "username":self.userId,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": self.ALICE,
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        self.userId2 = self.randomEOSIOId()

        HOST.push_action(
            "addprofile",
            [{
                "id":self.userId2,
                "username":self.userId2,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": self.BOB,
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        self.userId3 = self.randomEOSIOId()

        HOST.push_action(
            "addprofile",
            [{
                "id":self.userId3,
                "username":self.userId3,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": self.CAROL,
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        self.userId4 = self.randomEOSIOId()

        HOST.push_action(
            "addprofile",
            [{
                "id":self.userId4,
                "username":self.userId4,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": self.ELLIOT,
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

    def test_migrates_to_tmp(self):
        SCENARIO("test_migrates_to_tmp") 

        oldTableRes = HOST.table("profiles", HOST, limit=100)
        oldTableData = json.loads(oldTableRes.out_msg)

        HOST.push_action(
            "migrateprof",
            {
                "limit": 100,
            },
            permission=(HOST, Permission.ACTIVE)
        )

        oldTableAfterRes = HOST.table("profiles", HOST, limit=100)
        oldTableAfterData = json.loads(oldTableAfterRes.out_msg)

        newTableRes = HOST.table("profilestmp", HOST, limit=100)
        newTableData = json.loads(newTableRes.out_msg)

        self.assertEqual(len(oldTableAfterData["rows"]), 0)
        def stripLinkAndBio(row):
            newrow = row.copy()
            del newrow['link']
            del newrow['bio']
            return newrow
        self.assertEqual(oldTableData["rows"], list(map(stripLinkAndBio, newTableData["rows"])))

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
