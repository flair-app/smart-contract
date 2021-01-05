import unittest, sys, json
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()

class LevelActionsUnitTest(unittest.TestCase):

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

        create_account("ALICE", MASTER)

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
        pass

    def test_create_level_saves_fields_into_table(self):
        HOST.push_action(
            "createlevel", 
            [{
                "id":"gold",
                "name":"Gold",
                "categoryId": "music",
                "price": 1000,
                "participantLimit": 100,
                "submissionPeriod": 12,
                "votePeriod": 12,
                "fee": 15, # = 1.5%
                "prizes": [70, 20, 10],
                "fixedPrize": 0,
                "allowedSimultaneousContests": 0,
                "voteStartUTCHour": 0,
            }], 
            permission=(HOST, Permission.ACTIVE)
        )

        catRes = HOST.table("levels", HOST, lower="gold", upper="gold")
        catData = json.loads(catRes.out_msg)

        self.assertEqual(catData["rows"], [{
            "id":"gold",
            "name":"Gold",
            "categoryId": "music",
            "price": 1000,
            "participantLimit": 100,
            "submissionPeriod": 12,
            "votePeriod": 12,
            "archived": False,
            "fee": 15, # = 1.5%
            "prizes": [70, 20, 10],
        }])
            
    def test_create_level_requires_auth_of_self(self):
        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "createlevel", 
                [{
                    "id":"gold",
                    "name":"Gold",
                    "categoryId": "music",
                    "price": 1000,
                    "participantLimit": 100,
                    "submissionPeriod": 12,
                    "votePeriod": 12,
                    "fee": 15, # = 1.5%
                    "prizes": [70, 20, 10],
                    "fixedPrize": 0,
                    "allowedSimultaneousContests": 0,
                    "voteStartUTCHour": 0,
                }], 
                permission=(ALICE, Permission.ACTIVE)
            )
    
    def test_create_level_requires_categoryId_to_exist(self):
        with self.assertRaises(Error):
            HOST.push_action(
                "createlevel", 
                [{
                    "id":"gold2",
                    "name":"Gold2",
                    "categoryId": "music2",
                    "price": 1000,
                    "participantLimit": 100,
                    "submissionPeriod": 12,
                    "votePeriod": 12,
                    "fee": 15, # = 1.5%
                    "prizes": [70, 20, 10],
                    "fixedPrize": 0,
                    "allowedSimultaneousContests": 0,
                    "voteStartUTCHour": 0,
                }], 
                permission=(HOST, Permission.ACTIVE)
            )

    def test_create_level_must_be_unique_id(self):
        HOST.push_action(
            "createlevel", 
            [{
                "id":"gold2",
                "name":"Gold 2a",
                "categoryId": "music",
                "price": 1000,
                "participantLimit": 100,
                "submissionPeriod": 12,
                "votePeriod": 12,
                "fee": 15, # = 1.5%
                "prizes": [70, 20, 10],
                "fixedPrize": 0,
                "allowedSimultaneousContests": 0,
                "voteStartUTCHour": 0,
            }], 
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        with self.assertRaises(Error):
            HOST.push_action(
                "createlevel", 
                {
                    "id":"gold2",
                    "name":"Gold 2b",
                    "categoryId": "music",
                    "price": 1000,
                    "participantLimit": 100,
                    "submissionPeriod": 12,
                    "votePeriod": 12,
                    "fee": 15, # = 1.5%
                    "prizes": [70, 20, 10],
                    "fixedPrize": 0,
                    "allowedSimultaneousContests": 0,
                    "voteStartUTCHour": 0,
                }, 
                permission=(HOST, Permission.ACTIVE),
                force_unique=1
            )

    def test_edit_level_modifies_table(self):
        HOST.push_action(
            "createlevel", 
            [{
                "id":"editexample",
                "name":"Edit Example 1",
                "categoryId": "music",
                "price": 1000,
                "participantLimit": 100,
                "submissionPeriod": 12,
                "votePeriod": 12,
                "fee": 15, # = 1.5%
                "prizes": [70, 20, 10],
                "fixedPrize": 0,
                "allowedSimultaneousContests": 0,
                "voteStartUTCHour": 0,
            }],
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )
        
        HOST.push_action(
            "editlevel", 
            {
                "id":"editexample",
                "data": {
                    "name":"Edit Example 2",
                    "archived": True,
                    "price": 1001,
                    "participantLimit": 101,
                    "submissionPeriod": 13,
                    "votePeriod": 13,
                    "fee": 15, # = 1.5%
                    "prizes": [70, 30],
                },
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        catRes = HOST.table("levels", HOST, lower="editexample", upper="editexample")
        catData = json.loads(catRes.out_msg)

        self.assertEqual(catData["rows"], [{
            "id":"editexample",
            "name":"Edit Example 2",
            "categoryId": "music",
            "archived": 1,
            "price": 1001,
            "participantLimit": 101,
            "submissionPeriod": 13,
            "votePeriod": 13,
            "fee": 15, # = 1.5%
            "prizes": [70, 30],
        }])

    def test_edit_level_requires_auth_self(self):
        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "editlevel", 
                {
                    "id":"gold",
                    "data": {
                        "name":"Gold",
                        "archived": False,
                        "price": 1001,
                        "participantLimit": 101,
                        "submissionPeriod": 13,
                        "votePeriod": 13,
                        "fee": 15, # = 1.5%
                        "prizes": [70, 20, 10],
                    },
                },
                permission=(ALICE, Permission.ACTIVE),
                force_unique=1
            )

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
