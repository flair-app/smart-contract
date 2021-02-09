import unittest, sys, json, hashlib, time, random
from eosfactory.eosf import *
import eosfactory.core.setup as setup

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG, Verbosity.ERROR])

CONTRACT_WORKSPACE = sys.path[0] + "/../"
TOKEN_CONTRACT_WORKSPACE = "_iqhgcqllgnpkirjwwkms"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
TOKENHOST = Account()
ALICE = Account()
BOB = Account()

class randomDebugUnitTest(unittest.TestCase):

    def run(self, result=None):
        super().run(result)

    @classmethod
    def setUpClass(cls):
        reset()
        create_master_account("MASTER")
        
        create_account("TOKENHOST", MASTER, account_name='eosio.token')
        tokSmart = Contract(TOKENHOST, project_from_template(TOKEN_CONTRACT_WORKSPACE, template="eosio_token", remove_existing=True))
        tokSmart.build()
        tokSmart.deploy()

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

        create_account("ALICE", MASTER)
        create_account("BOB", MASTER)

        # create EOS tokens
        TOKENHOST.push_action(
            "create",
            {
                "issuer": MASTER,
                "maximum_supply": "1000000000.0000 EOS",
                "can_freeze": "0",
                "can_recall": "0",
                "can_whitelist": "0"
            },
            force_unique=True,
            permission=[(MASTER, Permission.ACTIVE), (TOKENHOST, Permission.ACTIVE)],
        )

        #issue tokens
        TOKENHOST.push_action(
            "issue",
            {
                "to": ALICE, "quantity": "10000.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "issue",
            {
                "to": BOB, "quantity": "10000.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )

        cls.userId = 'username123'

        HOST.push_action(
            "addprofile",
            [{
                "id":cls.userId,
                "username":cls.userId,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": ALICE,
                "active": True,
                "link": "",
                "bio": "",
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        cls.userId2 = 'username124'

        HOST.push_action(
            "addprofile",
            [{
                "id":cls.userId2,
                "username":cls.userId2,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": BOB,
                "active": True,
                "link": "",
                "bio": "",
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        HOST.push_action(
            "createcat", 
            {
                "id":"music",
                "name":"Music",
                "maxVideoLength": 30,
            }, 
            permission=(HOST, Permission.ACTIVE)
        )

        HOST.push_action(
            "setentryexp",
            [12 * 3600],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        HOST.push_action(
            "setcurrency",
            ["EOS"],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        HOST.push_action(
            "setpricefrsh",
            [12 * 3600],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        HOST.push_action(
            "addcurhigh",
            {
                "openTime": int(time.time()),
                "usdHigh": 30000, # $3.0000
                "intervalSec": 300, # 2 seconds
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

    def setUp(self):
        pass

    def randomEOSIOId(self):
        allowChar = "abcdefghijklmnopqrstuvwxyz12345."
        
        randomId = ""
        for i in range(0, 11):
            randomCharIndex = random.randrange(0,31,1)
            randomId += allowChar[randomCharIndex]
        
        return randomId

    def test_start(self):
        self.levelId = self.randomEOSIOId()
        
        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "1000.0000 EOS", 
                "memo": "prizefund",
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        HOST.push_action(
            "createlevel", 
            [{
                "id":self.levelId,
                "name":"Gold",
                "categoryId": "music",
                "price": 0,
                "participantLimit": 100,
                "submissionPeriod": 0,
                "votePeriod": 86400,
                "fee": 0,
                "prizes": [100],
                "fixedPrize": 100,
                "allowedSimultaneousContests": 1,
                "voteStartUTCHour": 17,
            }], 
            permission=(HOST, Permission.ACTIVE)
        )

        id = "contestentry"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        time.sleep(3)

        id2 = "contestentry2"
        videoHash720p2 = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb0"
        videoHash1080p2 = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb0"
        coverHash2 = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb0"

        HOST.push_action(
            "entercontest",
            [{
                "id":id2,
                "userId": self.userId2,
                "levelId": self.levelId,
                "videoHash720p": videoHash720p2,
                "videoHash1080p": videoHash1080p2,
                "coverHash": coverHash2,
            }],
            permission=(BOB, Permission.ACTIVE)
        )

        tableRes = HOST.table("entries", HOST,)

if __name__ == "__main__":
    unittest.main()
