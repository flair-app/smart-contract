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
            "t.e.s.t.e.r.", # can not end with dot
            ".t.e.s.t.e.r", # can not start with dot
            "t.e..s.t.e.r", # can not contain double dot
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

    def test_profile_lookup_by_username(self):
        # username = "tester1"

        usernames = [
            "tester2",
            "t.e.s.t.e.r2",
            "1test3",
            "TeStEr2",
            "abcdefghijkmnopqrstuvxz1234781",
        ]

        idPostfix = "123"
        idIndex = 0

        for username in usernames: 
            idIndex += 1
            if (idIndex > 5):
                idPostfix = idPostfix + "5"
                idIndex = 1
            accountname = "acct" + idPostfix + str(idIndex)
            create_account(accountname, MASTER, accountname)

            HOST.push_action(
                "addprofile",
                [{
                    "id":idPostfix+str(idIndex),
                    "username":username,
                    "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                    "account":accountname,
                    "active":True,
                }],
                permission=(HOST, Permission.ACTIVE)
            )

            usernameHash = hashlib.sha256(username.encode())

            COMMENT(
                '''
                usernameHash    : {usernameHash}
                '''
                .format(
                    usernameHash=usernameHash.hexdigest(), 
                )
            )

            def hexLittleEndian(str):
                hexLE = ""

                for i in reversed(range(0, 30, 2)):
                    iEnd = i + 1
                    str[i:iEnd]
                    hexLE = hexLE + str

                return hexLE

            def shaKeyEncoding(str):
                return hexLittleEndian(str[0:15]) + hexLittleEndian(str[16:31])
            
            # tableRes = HOST.table("profiles", HOST, lower=shaKeyEncoding(usernameHash.hexdigest()), limit=1, key_type="sha256", index=2)
            tableRes = HOST.table("profiles", HOST, lower=usernameHash.hexdigest(), upper=usernameHash.hexdigest(), limit=1, key_type="sha256", index=2)
            tableData = json.loads(tableRes.out_msg)

            print(usernameHash.hexdigest(), shaKeyEncoding(usernameHash.hexdigest()))
            self.assertEqual(tableData["rows"], [{
                "id":idPostfix+str(idIndex),
                "username":username,
                "usernameHash":usernameHash.hexdigest(),
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": accountname,
                "active": 1,
            }])

    def test_edit_profile_modifies_table_when_user_auth(self):
        SCENARIO('''
        test_edit_profile_modifies_table_when_user_auth
        ''')

        id = "cryptocat234"
        username = "cryptocat234"
        imgHash = "950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        usernameEdit = "cryptocat345"
        imgHashEdit = "850fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        HOST.push_action(
            "addprofile",
            [{
                "id":id,
                "username":username,
                "imgHash":imgHash,
                "account": str(ALICE),
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        HOST.push_action(
            "editprofuser",
            [
                id,
                {
                    "username":usernameEdit,
                    "imgHash":imgHashEdit,
                }
            ],
            permission=(ALICE, Permission.ACTIVE)
        )

        usernameHash = hashlib.sha256(usernameEdit.encode())
        
        tableRes = HOST.table("profiles", HOST, lower=id, key_type="name", limit=1)
        tableData = json.loads(tableRes.out_msg)

        self.assertEqual(tableData["rows"], [{
            "id":id,
            "username":usernameEdit,
            "usernameHash":usernameHash.hexdigest(),
            "imgHash":imgHashEdit,
            "account": str(ALICE),
            "active": 1,
        }])

    def test_edit_profile_as_user_requires_auth_user(self):
        id = "testing444"
        HOST.push_action(
            "addprofile",
            [{
                "id":id,
                "username":"testing444",
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": str(ALICE),
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "editprofuser",
                [
                    id,
                    {
                        "username":"testing444b",
                        "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                    }
                ],
                force_unique=1,
                permission=(BOB, Permission.ACTIVE)
            )
    
    def test_edit_profile_as_user_ensures_unique_username(self):
        id = "testing333"
        HOST.push_action(
            "addprofile",
            [{
                "id":id,
                "username":"testing333",
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": str(ALICE),
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        idb = "testing333b"
        HOST.push_action(
            "addprofile",
            [{
                "id":idb,
                "username":"testing333b",
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": str(BOB),
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        with self.assertRaises(Error):
            HOST.push_action(
                "editprofuser",
                [
                    id,
                    {
                        "username":"testing333b",
                        "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                    }
                ],
                force_unique=1,
                permission=(ALICE, Permission.ACTIVE)
            )

    def test_edit_profile_modifies_table_when_admin_auth(self):
        SCENARIO('''
        test_edit_profile_modifies_table_when_user_auth
        ''')

        id = "555"
        username = "cryptocat456"
        imgHash = "950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        usernameEdit = "cryptocat567"
        imgHashEdit = "850fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        HOST.push_action(
            "addprofile",
            [{
                "id":id,
                "username":username,
                "imgHash":imgHash,
                "account": str(ALICE),
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        HOST.push_action(
            "editprofadm",
            [
                id,
                {
                    "username":usernameEdit,
                    "imgHash":imgHashEdit,
                    "account": str(BOB),
                    "active": False,
                }
            ],
            permission=(HOST, Permission.ACTIVE)
        )

        usernameHash = hashlib.sha256(usernameEdit.encode())
        
        tableRes = HOST.table("profiles", HOST, lower=id, key_type="name", limit=1)
        tableData = json.loads(tableRes.out_msg)

        self.assertEqual(tableData["rows"], [{
            "id":id,
            "username":usernameEdit,
            "usernameHash":usernameHash.hexdigest(),
            "imgHash":imgHashEdit,
            "account": str(BOB),
            "active": 0,
        }])

    def test_edit_profile_as_admin_requires_auth_self(self):
        id = "testing555"
        HOST.push_action(
            "addprofile",
            [{
                "id":id,
                "username":"testing555",
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": str(ALICE),
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "editprofadm",
                [
                    id,
                    {
                        "username":"testing555b",
                        "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                        "account": str(BOB),
                        "active": False,
                    }
                ],
                force_unique=1,
                permission=(ALICE, Permission.ACTIVE)
            )
    
    def test_edit_profile_as_admin_ensures_unique_username(self):
        id = "testing222"
        HOST.push_action(
            "addprofile",
            [{
                "id":id,
                "username":"testing222",
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": str(ALICE),
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        idb = "testing222b"
        HOST.push_action(
            "addprofile",
            [{
                "id":idb,
                "username":"testing222b",
                "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                "account": str(BOB),
                "active": True,
            }],
            permission=(HOST, Permission.ACTIVE)
        )

        with self.assertRaises(Error):
            HOST.push_action(
                "editprofadm",
                [
                    id,
                    {
                        "username":"testing222b",
                        "imgHash":"950fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9",
                        "account": str(ALICE),
                        "active": True,
                    }
                ],
                force_unique=1,
                permission=(HOST, Permission.ACTIVE)
            )

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
