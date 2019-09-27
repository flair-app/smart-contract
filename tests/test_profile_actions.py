import unittest, sys, json, hashlib
from eosfactory.eosf import *
import eosfactory.core.setup as setup

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG, Verbosity.ERROR])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
BOB = Account()

class ProfileActionsUnitTest(unittest.TestCase):

    def run(self, result=None):
        super().run(result)

    @classmethod
    def setUpClass(cls):
        reset()
        create_master_account("MASTER")

        create_account("HOST", MASTER)
        smart = Contract(HOST, CONTRACT_WORKSPACE)
        smart.build(force=True)
        smart.deploy()

        create_account("ALICE", MASTER)
        create_account("BOB", MASTER)

    def setUp(self):
        pass

    def test_create_profile_saves_fields_into_table(self):
        SCENARIO('''
        test_create_profile_saves_fields_into_table
        ''')

        id = "31a55254b3521"
        username = "cryptocat123"
        imgHash = "950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        HOST.push_action(
            "addprofile",
            [{
                "id":id,
                "username":username,
                "imgHash":imgHash,
                "account": ALICE,
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        usernameHash = hashlib.sha256(username.encode())
        
        tableRes = HOST.table("profiles", HOST, lower=id, key_type="name", limit=1)
        tableData = json.loads(tableRes.out_msg)

        self.assertEqual(tableData["rows"], [{
            "id":id,
            "username":username,
            "usernameHash":usernameHash.hexdigest(),
            "imgHash":imgHash,
            "account": str(ALICE),
            "active": 1,
        }])

    def test_create_profile_requires_auth_of_self(self):
        pass
        SCENARIO('''
        test_create_profile_requires_auth_of_self
        ''')

        with self.assertRaises(MissingRequiredAuthorityError):
            id = "31a55254b3522"
            username = "cryptocat1235"
            imgHash = "950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

            HOST.push_action(
                "addprofile",
                [{
                    "id":id,
                    "username":username,
                    "imgHash":imgHash,
                    "account": ALICE,
                    "active": True,
                }],
                permission=(ALICE, Permission.ACTIVE)
            )

    def test_create_profile_must_be_unique_username(self):
        pass
        SCENARIO('''
        test_create_profile_must_be_unique_username
        ''')

        HOST.push_action(
            "addprofile",
            [{
                "id":"1111111111111",
                "username":"tester1",
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account":ALICE,
                "active":True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        with self.assertRaises(Error):
            HOST.push_action(
                "addprofile",
                [{
                    "id":"1111111111112",
                    "username":"tester1",
                    "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                    "account":BOB,
                    "active":True,
                }],
                permission=(HOST, Permission.ACTIVE)
            )

    def test_create_profile_ensures_valid_username(self):
        pass
        SCENARIO('''
        test_create_profile_ensures_valid_username
        ''')

        validUsernames = [
            "tester", #min 6 char
            "t.e.s.t.e.r", # can contain dots
            "1test1", # can contain numbers & start and end with numbers
            "TeStEr", # can contain capital numbers
            "abcdefghijkmnopqrstuvxz1234789", # can contain upto 30 char
        ]
        invalidUsernames = [
            "caleb", # can not contain less than 6 char
            "abcdefghijkmnopqrstuvxz12347890", # can not contain more than 30 char
            "t_e_s_t_e_r", # can not contain understores
            "t-e-s-t-e-r", # can not contain dashes
            "test&test", # can not contain ampersand
            "test+test", # can not contain plus
            "test,test", # can not contain comma
            "test<test", # can not contain brackets
            "test>test", # can not contain brackets
            "t.e..s.t.e.r", # can not contain double dot
            "t.e.s.t.e.r.", # can not end with dot
            ".t.e.s.t.e.r", # can not start with dot
        ]

        idPostfix = ""
        idIndex = 0

        for validUsername in validUsernames:
            idIndex += 1
            if (idIndex > 5):
                    idPostfix = idPostfix + "5"
                    idIndex = 1
            accountname = "acct" + idPostfix + str(idIndex)
            create_account(accountname, MASTER, accountname)

            COMMENT(
                '''
                accountname: {accountname}
                username: {username}
                '''
                .format(
                    accountname=accountname, 
                    username=validUsername,
                )
            )

            HOST.push_action(
                "addprofile",
                [{
                    "id":idPostfix+str(idIndex),
                    "username":validUsername,
                    "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                    "account":accountname,
                    "active":True,
                }],
                permission=(HOST, Permission.ACTIVE)
            )
        
        for invalidUsername in invalidUsernames:
            with self.assertRaises(Error):
                idIndex += 1
                if (idIndex > 5):
                        idPostfix = idPostfix + "5"
                        idIndex = 1
                accountname = "acct" + idPostfix + str(idIndex)
                create_account(accountname, MASTER, accountname)

                COMMENT(
                    '''
                    accountname: {accountname}
                    username: {username}
                    '''
                    .format(
                        accountname=accountname, 
                        username=invalidUsername,
                    )
                )

                HOST.push_action(
                    "addprofile",
                    [{
                        "id":idPostfix+str(idIndex),
                        "username":invalidUsername,
                        "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                        "account":accountname,
                        "active":True,
                    }],
                    permission=(HOST, Permission.ACTIVE)
                )
                
    
    def test_create_profile_require_account_to_be_uniquely_active(self):
        pass

    def test_profile_lookup_by_username(self):
        pass

    def test_edit_profile_modifies_table_when_user_auth(self):
        pass

    def test_edit_profile_modifies_table_when_admin_auth(self):
        pass

    def test_edit_profile_requires_auth_self_when_editing_account_or_active(self):
        pass

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
