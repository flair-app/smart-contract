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

        cls.username = '123'
        cls.levelId = 'music_gold'

    def setUp(self):
        pass

    def test_enter_contest_saves_fields_into_table(self):
        SCENARIO('''
        test_enter_contest_saves_fields_into_table
        ''')

        id = "123"
        videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
        coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

        HOST.push_action(
            "entercontest",
            {
                "username": self.username,
                "id":id,
                "levelId": self.levelId,
                "videoHash360p": videoHash360p,
                "videoHash480p": videoHash480p,
                "videoHash720p": videoHash720p,
                "videoHash1080p": videoHash1080p,
                "coverHash": coverHash,
            },
            permission=(HOST, Permission.ACTIVE)
        )

        tableRes = HOST.table("entries", HOST, lower=id, key_type="name")
        tableData = json.loads(tableRes.out_msg)

        self.assertEqual(tableData["rows"], [{
            "username": self.username,
            "id": id,
            "levelId": self.levelId,
            "contestId": "",
            "amount": 0,
            "videoHash360p": videoHash360p,
            "videoHash480p": videoHash480p,
            "videoHash720p": videoHash720p,
            "videoHash1080p": videoHash1080p,
            "coverHash": coverHash,
        }])

    def test_enter_contest_requires_auth_of_user(self):
        pass
        SCENARIO('''
        test_enter_contest_requires_auth_of_user
        ''')

        with self.assertRaises(MissingRequiredAuthorityError):
            id = "123"
            videoHash360p = "150fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
            videoHash480p = "250fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
            videoHash720p = "350fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
            videoHash1080p = "450fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"
            coverHash = "550fe755a7ef10e2dfdca952bb877cc023e9a4f3f2d896455e62cb6a442f5bb9"

            HOST.push_action(
                "entercontest",
                {
                    "username": self.username,
                    "id":id,
                    "levelId": self.levelId,
                    "videoHash360p": videoHash360p,
                    "videoHash480p": videoHash480p,
                    "videoHash720p": videoHash720p,
                    "videoHash1080p": videoHash1080p,
                    "coverHash": coverHash,
                },
                permission=(ALICE, Permission.ACTIVE)
            )

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
