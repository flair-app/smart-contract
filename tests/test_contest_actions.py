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
CAROL = Account()
DAN = Account()
ELLIOT = Account()

class ContestActionsUnitTest(unittest.TestCase):

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
        create_account("CAROL", MASTER)
        create_account("DAN", MASTER)
        create_account("ELLIOT", MASTER)

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
                "to": ALICE, "quantity": "100.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "issue",
            {
                "to": BOB, "quantity": "100.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "issue",
            {
                "to": CAROL, "quantity": "100.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "issue",
            {
                "to": DAN, "quantity": "100.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "issue",
            {
                "to": ELLIOT, "quantity": "100.0000 EOS", "memo": ""
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
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        cls.userId3 = 'username125'

        HOST.push_action(
            "addprofile",
            [{
                "id":cls.userId3,
                "username":cls.userId3,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": CAROL,
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        cls.userId4 = 'username131'

        HOST.push_action(
            "addprofile",
            [{
                "id":cls.userId4,
                "username":cls.userId4,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": DAN,
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        cls.userId5 = 'username133'

        HOST.push_action(
            "addprofile",
            [{
                "id":cls.userId5,
                "username":cls.userId5,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": ELLIOT,
                "active": True,
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

    def setUp(self):
        time.sleep(1)

        allowChar = "abcdefghijklmnopqrstuvwxyz12345."
        
        randomId = ""
        for i in range(0, 11):
            randomCharIndex = random.randrange(0,31,1)
            randomId += allowChar[randomCharIndex]
        
        self.levelId = randomId
        
        HOST.push_action(
            "createlevel", 
            [{
                "id":self.levelId,
                "name":"Gold",
                "categoryId": "music",
                "price": 1000,
                "participantLimit": 2,
                "submissionPeriod": 2,
                "votePeriod": 2
            }], 
            permission=(HOST, Permission.ACTIVE)
        )

        HOST.push_action(
            "setentryexp",
            [2],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        HOST.push_action(
            "setpricefrsh",
            [2],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        HOST.push_action(
            "addeoshigh",
            {
                "openTime": int(time.time()),
                "usdHigh": 50000, # $5.0000
                "intervalSec": 2, # 2 seconds
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )
    
    def test_enter_contest_saves_fields_into_table(self):
        id = "contestentry"
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        tableRes = HOST.table("entries", HOST, lower=id, key_type="name", limit=1)

        entry = tableRes.json["rows"][0]
        now = int(time.time())
        self.assertGreaterEqual(entry["createdAt"], now - 1)
        del entry["createdAt"]
        self.assertEqual(entry, {
            "id": id,
            "userId": self.userId,
            "levelId": self.levelId,
            "contestId": 0,
            "amount": 0,
            "videoHash360p": videoHash360p,
            "videoHash480p": videoHash480p,
            "videoHash720p": videoHash720p,
            "videoHash1080p": videoHash1080p,
            "coverHash": coverHash,
            "priceUnavailable": 0,
            "open": 1,
        })

    def test_enter_contest_requires_auth_of_user(self):
        with self.assertRaises(MissingRequiredAuthorityError):
            id = "contestentry2"
            videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
            videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
            videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
            videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
            coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

            HOST.push_action(
                "entercontest",
                [{
                    "userId": self.userId,
                    "id":id,
                    "levelId": self.levelId,
                    "videoHash360p": videoHash360p,
                    "videoHash480p": videoHash480p,
                    "videoHash720p": videoHash720p,
                    "videoHash1080p": videoHash1080p,
                    "coverHash": coverHash,
                }],
                permission=(BOB, Permission.ACTIVE)
            )

    def test_enter_contest_overwrites_current_pending_entry_with_new(self):
        id = "contestentry4"
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        id = "contestentry5"
        videoHash360p = "151fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "251fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "351fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "451fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "551fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        tableRes = HOST.table("entries", HOST, lower="contestentry4", key_type="name")

        entry = tableRes.json["rows"][0]
        now = int(time.time())
        self.assertGreaterEqual(entry["createdAt"], now - 1)
        del entry["createdAt"]
        self.assertEqual(entry, {
            "id": id,
            "userId": self.userId,
            "levelId": self.levelId,
            "contestId": 0,
            "amount": 0,
            "videoHash360p": videoHash360p,
            "videoHash480p": videoHash480p,
            "videoHash720p": videoHash720p,
            "videoHash1080p": videoHash1080p,
            "coverHash": coverHash,
            "priceUnavailable": 0,
            "open": 1,
        })

    def test_entry_payment_activates_entry_in_contest(self):
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        # verify activates and creates contest when no existing contest
        id = "myentry1"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 20000)
        contestId1 = contestId = entry["contestId"]
        self.assertNotEqual(contestId, 0)

        contestsRes = HOST.table("contests", HOST, lower=str(contestId))
        contestData = contestsRes.json["rows"][0]
        self.assertEqual(contestData["id"], contestId)
        self.assertEqual(contestData["levelId"], self.levelId)
        self.assertEqual(contestData["price"], 1000)
        self.assertEqual(contestData["participantLimit"], 2)
        self.assertEqual(contestData["participantCount"], 1)
        self.assertEqual(contestData["submissionPeriod"], 2)
        self.assertEqual(contestData["votePeriod"], 2)

        now = int(time.time())
        self.assertLessEqual(contestData["createdAt"], now + 1)
        self.assertGreaterEqual(contestData["createdAt"], now - 1)
        
        # verify activates when existing contest
        id = "myentry2"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId2,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(BOB, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": BOB,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": id,
            },
            force_unique=True,
            permission=(BOB, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 20000)
        contestId = entry["contestId"]
        self.assertEqual(contestId1, contestId)

        contestsRes = HOST.table("contests", HOST, lower=str(contestId))
        contestData = contestsRes.json["rows"][0]
        self.assertEqual(contestData["id"], contestId)
        self.assertEqual(contestData["levelId"], self.levelId)
        self.assertEqual(contestData["price"], 1000)
        self.assertEqual(contestData["participantLimit"], 2)
        self.assertEqual(contestData["participantCount"], 2)
        self.assertEqual(contestData["submissionPeriod"], 2)
        self.assertEqual(contestData["votePeriod"], 2)

        now = int(time.time())
        self.assertLessEqual(contestData["createdAt"], now + 1)
        self.assertGreaterEqual(contestData["createdAt"], now - 1)

        # verify creates new contest when existing is full
        id = "myentry3"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId3,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(CAROL, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": CAROL,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": id,
            },
            force_unique=True,
            permission=(CAROL, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 20000)
        contestId2 = contestId = entry["contestId"]
        self.assertNotEqual(contestId, contestId1)
        self.assertNotEqual(contestId, 0)

        contestsRes = HOST.table("contests", HOST, lower=str(contestId))
        contestData = contestsRes.json["rows"][0]
        self.assertEqual(contestData["id"], contestId)
        self.assertEqual(contestData["levelId"], self.levelId)
        self.assertEqual(contestData["price"], 1000)
        self.assertEqual(contestData["participantLimit"], 2)
        self.assertEqual(contestData["participantCount"], 1)
        self.assertEqual(contestData["submissionPeriod"], 2)
        self.assertEqual(contestData["votePeriod"], 2)

        now = int(time.time())
        self.assertLessEqual(contestData["createdAt"], now + 1)
        self.assertGreaterEqual(contestData["createdAt"], now - 1)

        # verify creates new contest when existing is no longer accepting submissions
        time.sleep(3)

        HOST.push_action(
            "addeoshigh",
            {
                "openTime": int(time.time()),
                "usdHigh": 50000, # $5.0000
                "intervalSec": 2, # 2 seconds
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        id = "myentry4"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId4,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(DAN, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": DAN,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": id,
            },
            force_unique=True,
            permission=(DAN, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 20000)
        contestId3 = contestId = entry["contestId"]
        self.assertNotEqual(contestId, contestId2)
        self.assertNotEqual(contestId, 0)

        contestsRes = HOST.table("contests", HOST, lower=str(contestId))
        contestData = contestsRes.json["rows"][0]
        self.assertEqual(contestData["id"], contestId)
        self.assertEqual(contestData["levelId"], self.levelId)
        self.assertEqual(contestData["price"], 1000)
        self.assertEqual(contestData["participantLimit"], 2)
        self.assertEqual(contestData["participantCount"], 1)
        self.assertEqual(contestData["submissionPeriod"], 2)
        self.assertEqual(contestData["votePeriod"], 2)

        now = int(time.time())
        entry4CreatedAt = contestData["createdAt"]
        self.assertLessEqual(contestData["createdAt"], now + 1)
        self.assertGreaterEqual(contestData["createdAt"], now - 1)

        TOKENHOST.push_action(
            "transfer",
            {
                "from": DAN,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": id,
            },
            force_unique=True,
            permission=(DAN, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 40000)
        contestId = entry["contestId"]
        self.assertEqual(contestId, contestId3)

        contestsRes = HOST.table("contests", HOST, lower=str(contestId))
        contestData = contestsRes.json["rows"][0]
        self.assertEqual(contestData["id"], contestId)
        self.assertEqual(contestData["levelId"], self.levelId)
        self.assertEqual(contestData["price"], 1000)
        self.assertEqual(contestData["participantLimit"], 2)
        self.assertEqual(contestData["participantCount"], 1)
        self.assertEqual(contestData["submissionPeriod"], 2)
        self.assertEqual(contestData["votePeriod"], 2)

        now = int(time.time())
        self.assertEqual(contestData["createdAt"], entry4CreatedAt)
    
    def test_entry_payment_doesnt_activate_when_entry_expired(self):
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        #set required price freshness forward to ensure entry expired check
        HOST.push_action(
            "setpricefrsh",
            [10],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        id = "myentry5"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        time.sleep(3)

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS",
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 20000)
        contestId = entry["contestId"]
        self.assertEqual(contestId, 0)

    def test_entry_payment_doesnt_activate_when_payment_not_enough(self):
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        #set required price freshness forward to ensure entry expired check
        HOST.push_action(
            "setpricefrsh",
            [10],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        id = "myentry54"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "1.0000 EOS",
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 10000)
        contestId = entry["contestId"]
        self.assertEqual(contestId, 0)
    
    def test_entry_payment_doesnt_activate_when_price_not_fresh(self):
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        #set entry exp forward from price freshness to ensure price freshness check
        HOST.push_action(
            "setentryexp",
            [2000],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        HOST.push_action(
            "setpricefrsh",
            [1],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        id = "myentry51"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        time.sleep(3)

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS",
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["priceUnavailable"], 1)
        self.assertEqual(entry["amount"], 20000)
        contestId = entry["contestId"]
        self.assertEqual(contestId, 0)
    
    def test_enter_contest_limits_to_one_active_within_level(self):
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        id = "myentry52"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        HOST.table("eosprices", HOST, limit=100)

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS",
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )
        
        with self.assertRaises(Error):
            id = "myentry53"
            HOST.push_action(
                "entercontest",
                [{
                    "id":id,
                    "userId": self.userId,
                    "levelId": self.levelId,
                    "videoHash360p": videoHash360p,
                    "videoHash480p": videoHash480p,
                    "videoHash720p": videoHash720p,
                    "videoHash1080p": videoHash1080p,
                    "coverHash": coverHash,
                }],
                permission=(ALICE, Permission.ACTIVE)
            )
    
    def test_entercontest_verify_success_when_has_past_submissions_within_level(self):
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        id = "myentry55"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS",
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        time.sleep(5)

        HOST.push_action(
            "addeoshigh",
            {
                "openTime": int(time.time()),
                "usdHigh": 50000, # $5.0000
                "intervalSec": 2, # 2 seconds
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        id = "myentry44"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS",
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 20000)
        contestId = entry["contestId"]
        self.assertNotEqual(contestId, 0)

    def test_refund_entry_payment_sends_funds(self):
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        id = "myentry11"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        accountsRes = TOKENHOST.table("accounts", ALICE)
        beforeBal = accountsRes.json["rows"][0]["balance"]

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "1.0000 EOS",
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        HOST.push_action(
            "refundentry",
            {
                "id":id,
                "to": ALICE,
                "memo": "test",
            },
            permission=(ALICE, Permission.ACTIVE)
        )

        entriesRes = HOST.table("entries", HOST, lower=id, key_type="name")
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], id)
        self.assertEqual(entry["amount"], 0)

        accountsRes = TOKENHOST.table("accounts", ALICE)
        self.assertEqual(accountsRes.json["rows"][0]["balance"], beforeBal)

    def test_refund_entry_payment_fails_when_contest_is_set(self):
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        id = "myentry12"
        HOST.push_action(
            "entercontest",
            [{
                "id":id,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            }],
            permission=(ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS",
                "memo": id,
            },
            force_unique=True,
            permission=(ALICE, Permission.ACTIVE)
        )

        with self.assertRaises(Error):
            HOST.push_action(
                "refundentry",
                {
                    "id":id,
                    "to": ALICE,
                    "memo": "test",
                },
                permission=(ALICE, Permission.ACTIVE)
            )

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
