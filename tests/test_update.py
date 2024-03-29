import unittest, sys, json, random, time
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG, Verbosity.ERROR])

CONTRACT_WORKSPACE = sys.path[0] + "/../"
TOKEN_CONTRACT_WORKSPACE = "_iqhgcqllgnpkirjwwkms"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
TOKENHOST = Account()

def extract_profile_winnings(rows):
    if (len(rows) == 0):
        return 0
    return float(rows[0]['winnings'].split(' ')[0])

class UpdateActionsUnitTest(unittest.TestCase):

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
            "setcurrency",
            ["EOS"],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
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

        #issue tokens
        TOKENHOST.push_action(
            "issue",
            {
                "to": self.ALICE, "quantity": "100.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "issue",
            {
                "to": self.BOB, "quantity": "100.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "issue",
            {
                "to": self.CAROL, "quantity": "100.0000 EOS", "memo": ""
            },
            force_unique=True,
            permission=(MASTER, Permission.ACTIVE)
        )
        
        self.userId = self.randomEOSIOId()

        HOST.push_action(
            "addprofile",
            [{
                "id":self.userId,
                "username":self.userId,
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": self.ALICE,
                "active": True,
                "link": "",
                "bio": "",
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
                "link": "",
                "bio": "",
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
                "link": "",
                "bio": "",
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
                "link": "",
                "bio": "",
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        HOST.push_action(
            "setfeeacct", 
            {
                "account":self.FEEACCT,
                "memo":"my memo",
            }, 
            permission=(HOST, Permission.ACTIVE)
        )

        self.levelId = self.randomEOSIOId()
        
        HOST.push_action(
            "createlevel", 
            [{
                "id":self.levelId,
                "name":"Gold",
                "categoryId": "music",
                "price": 1000,
                "participantLimit": 4,
                "submissionPeriod": 4,
                "votePeriod": 4,
                "fee": 45, # = 4.5%
                "prizes": [70, 30],
                "fixedPrize": 0,
                "allowedSimultaneousContests": 0,
                "voteStartUTCHour": 0,
            }], 
            permission=(HOST, Permission.ACTIVE)
        )

        self.levelId2 = self.randomEOSIOId()
        
        HOST.push_action(
            "createlevel", 
            [{
                "id":self.levelId2,
                "name":"Gold",
                "categoryId": "music",
                "price": 0,
                "participantLimit": 4,
                "submissionPeriod": 4,
                "votePeriod": 4,
                "fee": 0, # = 4.5%
                "prizes": [100],
                "fixedPrize": 1000,
                "allowedSimultaneousContests": 0,
                "voteStartUTCHour": 0,
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
            "setentryarch",
            [50],
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
            "addcurhigh",
            {
                "openTime": int(time.time()),
                "usdHigh": 50000, # $5.0000
                "intervalSec": 2, # 2 seconds
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        self.videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        self.videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        self.videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        self.videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        self.coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        self.entryId = self.randomEOSIOId()
        HOST.push_action(
            "entercontest",
            [{
                "id": self.entryId,
                "userId": self.userId,
                "levelId": self.levelId,
                "videoHash360p": self.videoHash360p,
                "videoHash480p": self.videoHash480p,
                "videoHash720p": self.videoHash720p,
                "videoHash1080p": self.videoHash1080p,
                "coverHash": self.coverHash,
            }],
            permission=(self.ALICE, Permission.ACTIVE)
        )

        self.entryId2 = self.randomEOSIOId()
        HOST.push_action(
            "entercontest",
            [{
                "id": self.entryId2,
                "userId": self.userId2,
                "levelId": self.levelId,
                "videoHash360p": self.videoHash360p,
                "videoHash480p": self.videoHash480p,
                "videoHash720p": self.videoHash720p,
                "videoHash1080p": self.videoHash1080p,
                "coverHash": self.coverHash,
            }],
            permission=(self.BOB, Permission.ACTIVE)
        )

        self.entryId3 = self.randomEOSIOId()
        HOST.push_action(
            "entercontest",
            [{
                "id": self.entryId3,
                "userId": self.userId3,
                "levelId": self.levelId,
                "videoHash360p": self.videoHash360p,
                "videoHash480p": self.videoHash480p,
                "videoHash720p": self.videoHash720p,
                "videoHash1080p": self.videoHash1080p,
                "coverHash": self.coverHash,
            }],
            permission=(self.CAROL, Permission.ACTIVE)
        )

    def test_update_action_sends_winnings_to_winner_and_flair_only_once(self):
        SCENARIO("test_update_action_sends_winnings_to_winner_and_flair_only_once")
        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId,
            },
            force_unique=True,
            permission=(self.ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.BOB,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId2,
            },
            force_unique=True,
            permission=(self.BOB, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.CAROL,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId3,
            },
            force_unique=True,
            permission=(self.CAROL, Permission.ACTIVE)
        )

        time.sleep(5)    

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId,
                "voterUserId": self.userId,
            },
            permission=(self.ALICE, Permission.ACTIVE)
        )

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId2,
                "voterUserId": self.userId2,
            },
            permission=(self.BOB, Permission.ACTIVE)
        )

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId2,
                "voterUserId": self.userId3,
            },
            permission=(self.CAROL, Permission.ACTIVE)
        )

        time.sleep(4)
        
        feeBeforeBal = float(self.getEOSBalance(self.FEEACCT))
        aliceBeforeBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId, key_type="name").json["rows"])
        bobBeforeBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId2, key_type="name").json["rows"])

        HOST.table("contests", HOST)

        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))
        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))

        feeAfterBal = float(self.getEOSBalance(self.FEEACCT))
        aliceAfterBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId, key_type="name").json["rows"])
        bobAfterBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId2, key_type="name").json["rows"])
        
        self.assertAlmostEqual(feeAfterBal - feeBeforeBal, 0.27)
        self.assertAlmostEqual(aliceAfterBal - aliceBeforeBal, 1.719)
        self.assertAlmostEqual(bobAfterBal - bobBeforeBal, 4.011)

    def test_update_action_sends_winnings_to_winners_when_tied_and_flair_only_once(self):
        SCENARIO("test_update_action_sends_winnings_to_winners_when_tied_and_flair_only_once")
        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId,
            },
            force_unique=True,
            permission=(self.ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.BOB,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId2,
            },
            force_unique=True,
            permission=(self.BOB, Permission.ACTIVE)
        )

        time.sleep(5)    

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId2,
                "voterUserId": self.userId3,
            },
            permission=(self.CAROL, Permission.ACTIVE)
        )

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId,
                "voterUserId": self.userId4,
            },
            permission=(self.ELLIOT, Permission.ACTIVE)
        )

        time.sleep(4)
        
        feeBeforeBal = float(self.getEOSBalance(self.FEEACCT))
        aliceBeforeBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId, key_type="name").json["rows"])
        bobBeforeBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId2, key_type="name").json["rows"])

        HOST.table("contests", HOST)

        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))
        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))

        feeAfterBal = float(self.getEOSBalance(self.FEEACCT))
        aliceAfterBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId, key_type="name").json["rows"])
        bobAfterBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId2, key_type="name").json["rows"])
        
        self.assertAlmostEqual(bobAfterBal - bobBeforeBal, 1.91)
        self.assertAlmostEqual(aliceAfterBal - aliceBeforeBal, 1.91)
        self.assertAlmostEqual(feeAfterBal - feeBeforeBal, 0.18)

    def test_update_action_doesnt_send_winnings_before_contest_ends(self):
        SCENARIO("test_update_action_doesnt_send_winnings_before_contest_ends")
        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId,
            },
            force_unique=True,
            permission=(self.ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.BOB,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId2,
            },
            force_unique=True,
            permission=(self.BOB, Permission.ACTIVE)
        )

        time.sleep(5)    

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId2,
                "voterUserId": self.userId3,
            },
            permission=(self.CAROL, Permission.ACTIVE)
        )
        
        feeBeforeBal = float(self.getEOSBalance(self.FEEACCT))
        bobBeforeBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId2, key_type="name").json["rows"])

        HOST.table("contests", HOST)

        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))
        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))

        feeAfterBal = float(self.getEOSBalance(self.FEEACCT))
        bobAfterBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId2, key_type="name").json["rows"])
        
        self.assertAlmostEqual(feeAfterBal, feeBeforeBal)
        self.assertAlmostEqual(bobAfterBal, bobBeforeBal)

        # go ahead payout now to prevent from having side effects on later tests. 
        time.sleep(5)
        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))

    def test_update_action_activates_priceUnavailable_entries_that_have_prices(self):
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

        time.sleep(5)

        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS",
                "memo": self.entryId,
            },
            force_unique=True,
            permission=(self.ALICE, Permission.ACTIVE)
        )

        HOST.push_action(
            "addcurhigh",
            {
                "openTime": int(time.time()),
                "usdHigh": 50000, # $5.0000
                "intervalSec": 2, # 2 seconds
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )
        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))

        entriesRes = HOST.table("entries", HOST, lower=self.entryId, key_type="name")
        print(entriesRes)
        entry = entriesRes.json["rows"][0]
        self.assertEqual(entry["id"], self.entryId)
        self.assertEqual(entry["priceUnavailable"], 0)
        self.assertEqual(entry["amount"], 20000)
        contestId = entry["contestId"]
        self.assertGreater(contestId, 0)

        # go ahead payout now to prevent from having side effects on later tests. 
        time.sleep(5)
        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))

    def test_update_action_archives_entries(self):
        return
        HOST.push_action(
            "setentryarch",
            [5],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId,
            },
            force_unique=True,
            permission=(self.ALICE, Permission.ACTIVE)
        )

        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.BOB,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": self.entryId2,
            },
            force_unique=True,
            permission=(self.BOB, Permission.ACTIVE)
        )

        HOST.table("contests", HOST)
        HOST.table("entries", HOST)

        time.sleep(5)

        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE)) 
        HOST.table("contests", HOST)
        HOST.table("entries", HOST)

        entriesRes = HOST.table("entries", HOST, lower=self.entryId, key_type="name")
        try:
            self.assertNotEqual(entriesRes.json["rows"][0]['id'], self.entryId)
        except IndexError:
            pass

        entriesRes = HOST.table("entries", HOST, lower=self.entryId2, key_type="name")
        try:
            self.assertNotEqual(entriesRes.json["rows"][0]['id'], self.entryId2)
        except IndexError:
            pass

        entriesRes = HOST.table("entries", HOST, lower=self.entryId3, key_type="name")
        try:
            self.assertNotEqual(entriesRes.json["rows"][0]['id'], self.entryId3)
        except IndexError:
            pass

    def test_update_action_sends_fixed_prize_winnings_to_winner_and_flair_only_once(self):
        return
        SCENARIO("test_update_action_sends_winnings_to_winner_and_flair_only_once")

        print("test \n")
        TOKENHOST.push_action(
            "transfer",
            {
                "from": self.ALICE,
                "to": HOST,
                "quantity": "2.0000 EOS", 
                "memo": "prizefund",
            },
            force_unique=True,
            permission=(self.ALICE, Permission.ACTIVE)
        )
        print("test 2 \n")
        self.entryId4 = self.randomEOSIOId()
        HOST.push_action(
            "entercontest",
            [{
                "id": self.entryId4,
                "userId": self.userId,
                "levelId": self.levelId2,
                "videoHash360p": self.videoHash360p,
                "videoHash480p": self.videoHash480p,
                "videoHash720p": self.videoHash720p,
                "videoHash1080p": self.videoHash1080p,
                "coverHash": self.coverHash,
            }],
            permission=(self.ALICE, Permission.ACTIVE)
        )
        print("test 3 \n")

        self.entryId5 = self.randomEOSIOId()
        HOST.push_action(
            "entercontest",
            [{
                "id": self.entryId5,
                "userId": self.userId2,
                "levelId": self.levelId2,
                "videoHash360p": self.videoHash360p,
                "videoHash480p": self.videoHash480p,
                "videoHash720p": self.videoHash720p,
                "videoHash1080p": self.videoHash1080p,
                "coverHash": self.coverHash,
            }],
            permission=(self.BOB, Permission.ACTIVE)
        )

        self.entryId6 = self.randomEOSIOId()
        HOST.push_action(
            "entercontest",
            [{
                "id": self.entryId6,
                "userId": self.userId3,
                "levelId": self.levelId2,
                "videoHash360p": self.videoHash360p,
                "videoHash480p": self.videoHash480p,
                "videoHash720p": self.videoHash720p,
                "videoHash1080p": self.videoHash1080p,
                "coverHash": self.coverHash,
            }],
            permission=(self.CAROL, Permission.ACTIVE)
        )

        time.sleep(5)    

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId4,
                "voterUserId": self.userId,
            },
            permission=(self.ALICE, Permission.ACTIVE)
        )

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId5,
                "voterUserId": self.userId2,
            },
            permission=(self.BOB, Permission.ACTIVE)
        )

        HOST.push_action(
            "vote",
            {
                "entryId": self.entryId5,
                "voterUserId": self.userId3,
            },
            permission=(self.CAROL, Permission.ACTIVE)
        )

        time.sleep(4)

        HOST.push_action(
            "addcurhigh",
            {
                "openTime": int(time.time()),
                "usdHigh": 50000, # $5.0000
                "intervalSec": 2, # 2 seconds
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )
        
        feeBeforeBal = float(self.getEOSBalance(self.FEEACCT))
        aliceBeforeBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId, key_type="name").json["rows"])
        bobBeforeBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId2, key_type="name").json["rows"])


        HOST.table("contests", HOST)

        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))
        HOST.push_action("update", force_unique=True, permission=(HOST, Permission.ACTIVE))

        feeAfterBal = float(self.getEOSBalance(self.FEEACCT))
        aliceAfterBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId, key_type="name").json["rows"])
        bobAfterBal = extract_profile_winnings(HOST.table("profiles", HOST, lower=self.userId2, key_type="name").json["rows"])

        
        self.assertAlmostEqual(feeAfterBal - feeBeforeBal, 0.0)
        self.assertAlmostEqual(aliceAfterBal - aliceBeforeBal, 0.0)
        self.assertAlmostEqual(bobAfterBal - bobBeforeBal, 2.0)

        HOST.table("options", HOST)

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
