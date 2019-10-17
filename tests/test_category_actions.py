import unittest, sys, json
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()

class CategoryActionsUnitTest(unittest.TestCase):

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

    def setUp(self):
        pass

    def test_create_category_saves_fields_into_table(self):
        HOST.push_action(
            "createcat", 
            {
                "id":"music",
                "name":"Music",
                "maxVideoLength": 30,
            }, 
            permission=(HOST, Permission.ACTIVE)
        )

        catRes = HOST.table("categories", HOST, lower="music", upper="music")
        catData = json.loads(catRes.out_msg)

        self.assertEqual(catData["rows"], [{
            "id":"music",
            "name":"Music",
            "maxVideoLength": 30,
            "archived": False,
        }])
            
    def test_create_category_requires_auth_of_self(self):
        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "createcat", 
                {
                    "id":"music",
                    "name":"Music",
                    "maxVideoLength": 30,
                }, 
                permission=(ALICE, Permission.ACTIVE)
            )

    def test_create_category_must_be_unique_id(self):
        HOST.push_action(
            "createcat", 
            {
                "id":"music2",
                "name":"Music 2a",
                "maxVideoLength": 30,
            }, 
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        with self.assertRaises(Error):
            HOST.push_action(
                "createcat", 
                {
                    "id":"music2",
                    "name":"Music 2b",
                    "maxVideoLength": 30,
                }, 
                permission=(HOST, Permission.ACTIVE),
                force_unique=1
            )

    def test_edit_category_modifies_table(self):
        HOST.push_action(
            "createcat", 
            {
                "id":"editexample",
                "name":"Edit Example 1",
                "maxVideoLength": 30,
            },
            permission=(HOST, Permission.ACTIVE)
        )
        
        HOST.push_action(
            "editcat", 
            {
                "id":"editexample",
                "data": {
                    "name":"Edit Example 2",
                    "maxVideoLength": 20,
                    "archived": True,
                },
            },
            permission=(HOST, Permission.ACTIVE)
        )

        catRes = HOST.table("categories", HOST, lower="editexample", upper="editexample")
        catData = json.loads(catRes.out_msg)

        self.assertEqual(catData["rows"], [{
            "id":"editexample",
            "name":"Edit Example 2",
            "maxVideoLength": 20,
            "archived": True,
        }])

    def test_edit_category_requires_auth_self(self):
        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "editcat", 
                {
                    "id":"music",
                    "data": {
                        "name":"Music",
                        "maxVideoLength": 20,
                        "archived": False,
                    },
                },
                permission=(ALICE, Permission.ACTIVE)
            )

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
