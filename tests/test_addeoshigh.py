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

class SeteoshighUnitTest(unittest.TestCase):

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

    def test_add_eos_high_saves_fields_into_table(self):
        SCENARIO('''
        test_add_eos_high_saves_fields_into_table
        ''')

        time = 1568751673935
        usdHigh = 45678 # $4.5678

        HOST.push_action(
            "seteoshigh",
            {
                "time":time,
                "usdHigh":usdHigh,
            },
            permission=(HOST, Permission.ACTIVE)
        )

        time = time + 1
        usdHigh = usdHigh + 1

        HOST.push_action(
            "seteoshigh",
            {
                "time":time,
                "usdHigh":usdHigh,
            },
            permission=(HOST, Permission.ACTIVE)
        )

        COMMENT('''
            get eosprices table {time}
        '''.format(
            time=time
        ))
        
        tableRes = HOST.table("eosprices", HOST, lower=str(time), key_type="i64")
        
        COMMENT('''
            tableRes: {tableRes}
        '''.format(
            tableRes=tableRes.out_msg
        ))

        tableData = json.loads(tableRes.out_msg)

        self.assertEqual(tableData["rows"], [{
            "time":str(time),
            "usdHigh":usdHigh,
        }])

    def test_add_eos_high_requires_auth_of_self(self):
        pass
        SCENARIO('''
        test_add_eos_high_requires_auth_of_self
        ''')

        with self.assertRaises(MissingRequiredAuthorityError):
            time = 1568751673935
            usdHigh = 41128 # $4.1128

            HOST.push_action(
                "seteoshigh",
                {
                    "time":time,
                    "usdHigh":usdHigh,
                },
                permission=(ALICE, Permission.ACTIVE)
            )

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
