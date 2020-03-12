import unittest, sys, json, hashlib, time
from eosfactory.eosf import *
import eosfactory.core.setup as setup

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG, Verbosity.ERROR])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
BOB = Account()

class addcurhighUnitTest(unittest.TestCase):

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
        create_account("BOB", MASTER)

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

    def setUp(self):
        pass

    def test_add_currency_high_saves_fields_into_table_and_deletes_existings_rows_older_than_12_hours(self):
        SCENARIO('''
        test_add_currency_high_saves_fields_into_table_and_deletes_existings_rows_older_than_12_hours
        ''')

        ts = int(time.time())
        usdHigh = 45678 # $4.5678
        intervalSec = 900

        HOST.push_action(
            "addcurhigh",
            {
                "openTime":ts,
                "usdHigh":usdHigh,
                "intervalSec": intervalSec,
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        hourSec = 3600
        ts2 = (ts - (hourSec * 12)) + 5
        usdHigh2 = usdHigh + 10000 # + $1.0000

        HOST.push_action(
            "addcurhigh",
            {
                "openTime":ts2,
                "usdHigh":usdHigh2,
                "intervalSec": intervalSec,
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        # second expired price to confirm looping functionality
        HOST.push_action(
            "addcurhigh",
            {
                "openTime":ts2 - 1,
                "usdHigh":usdHigh2,
                "intervalSec": intervalSec,
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )

        time.sleep(5)

        ts3 = ts + intervalSec
        usdHigh3 = usdHigh + 10000 # + $1.0000

        HOST.push_action(
            "addcurhigh",
            {
                "openTime":ts3,
                "usdHigh":usdHigh3,
                "intervalSec": intervalSec,
            },
            permission=(HOST, Permission.ACTIVE),
            force_unique=1
        )
        
        tableRes = HOST.table("curprices", HOST)

        tableData = json.loads(tableRes.out_msg)

        self.assertEqual(
            tableData["rows"], 
            [
                {
                    "openTime":ts,
                    "usdHigh":usdHigh,
                    "intervalSec": intervalSec,
                },
                {
                    "openTime":ts3,
                    "usdHigh":usdHigh3,
                    "intervalSec": intervalSec,
                },
            ]
        )

    def test_add_currency_high_saves_fails_when_not_within_12_hour_period(self):
        SCENARIO('''
        test_add_currency_high_saves_fails_when_not_within_12_hour_period
        ''')

        hourSec = 3600
        ts = int(time.time() - (hourSec * 12))
        usdHigh = 45678 # $4.5678
        intervalSec = 900

        with self.assertRaises(Error):
            HOST.push_action(
                "addcurhigh",
                {
                    "openTime":ts,
                    "usdHigh":usdHigh,
                    "intervalSec": intervalSec,
                },
                permission=(HOST, Permission.ACTIVE),
                force_unique=1
            )

    def test_add_currency_high_requires_auth_of_self(self):
        SCENARIO('''
        test_add_currency_high_requires_auth_of_self
        ''')

        with self.assertRaises(MissingRequiredAuthorityError):
            ts = int(time.time())
            usdHigh = 45678 # $4.5678
            intervalSec = 900

            HOST.push_action(
                "addcurhigh",
                {
                    "openTime":ts,
                    "usdHigh":usdHigh,
                    "intervalSec": intervalSec,
                },
                permission=(ALICE, Permission.ACTIVE),
                force_unique=1
            )

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
