# Prerequisites 
You'll need the following items installed:
- [EOSIO v1.8.0](https://developers.eos.io/eosio-home/docs/setting-up-your-environment)
- [eosio.cdt v1.6.1](https://developers.eos.io/eosio-home/docs/installing-the-contract-development-toolkit)
- Python 3.5 or higher
- pip3 18.1 or higher
- CMake 3.5 or higher
- [EOSFactory](https://eosfactory.io/build/html/tutorials/01.InstallingEOSFactory.html)

# Tests
Tests are written utilizing EOSFactory which uses python3.

**Run All Tests**
```
cd tests
python3 -m unittest discover --pattern=*.py
```

**Run A Specific Test**
```
cd tests
python3 -m unittest discover --pattern=filename.py
```

# Building
Navigation to the root directory of repo run:
```
mkdir -p build
python3 -m eosfactory.build $(pwd)
```

# Deploying
After building, you can deploy the contract by running:
```
cleos set contract your_contract_account_name $(pwd)/build -p your_account@active
```

# Smart Contract Actions
  - [**addeoshigh (Update EOS 12 Hour High)**](#addeoshigh-update-eos-12-hour-high)
  - [**addprofile (Add/Create Profile)**](#addprofile-addcreate-profile)
  - [**claimfunds (Claim Funds)**](#claimfunds-claim-funds)
  - [**createcat (Create Category)**](#createcat-create-category)
  - [**createlevel (Create Level)**](#createlevel-create-level)
  - [**editcat (Edit Category)**](#editcat-edit-category)
  - [**editlevel (Edit Level)**](#editlevel-edit-level)
  - [**editprofile (Edit Profile)**](#editprofile-edit-profile)
  - [**entercontest (Enter Contest)**](#entercontest-enter-contest)
  - [**vote (Vote)**](#vote-vote)


## **addeoshigh (Update EOS 12 Hour High)**

The 12hr high is used to calculate the amount of EOS needed for entries.

**Authorization:** Requires `_self` auth

**Parameters:**
- `uint64` time *(ms since epoch)*
- `uint64` usdHigh

**Example Data:**
    
    {
        "time": 1568751673935, 
        "usdHigh": 4.18
    }

## **addprofile (Add/Create Profile)**
**Authorization:** Requires `_self` auth

**Parameters:**

- params
  - `string` id
  - `string` username
  - `checksum256` imgHash
  - `name` account
  - `bool` active

**Example Data:**
    
    {
        "params": {
            "id": "7f945fdb-50d3-48d2-96e2-30a65268b762",
            "username": "cryptocat1234",
            "imgHash": "fbea88977ed96d4b1...",
            "account": "bob",
            "active": "true"
        }
    }

## **claimfunds (Claim Funds)**
Transfer user's winnings to specified destination.

**Authorization:** Requires auth of the parameter `user`

**Parameters:**
- `string` user
- `name` to
- `string` memo

**Example Data:**
    
    {
        "user": "bob", 
        "to": "coinbase", 
        "memo": "12398712"
    }

## **createcat (Create Category)**
**Authorization:** Requires `_self` auth

**Parameters:**
- `name` id
- `string` name

**Example Data:**
    
    {
        "id": "music",
        "name": "Music"
    }

## **createlevel (Create Level)**
**Authorization:** Requires `_self` auth

**Parameters:**
- params
  - `name` id
  - `name` categoryId
  - `string` name
  - `uint8` maxVideoLength *(specified as seconds)*
  - `uint64` price *(specified in USD as cents)*
  - `uint64` participantLimit
  - `uint64` submissionPeriod *(specified as hours)*
  - `uint64` votePeriod *(specified as hours)*

**Example Data:**
    
    {
        "params": {
            "id": "music_gold",
            "categoryId": "music",
            "name": "Gold",
            "maxVideoLength": 30,
            "price": 1000,
            "participantLimit": 100,
            "submissionPeriod": 12,
            "votePeriod": 12
        }
    }

## **editcat (Edit Category)**

**Authorization:** Requires `_self` auth

**Parameters:**
*All parameters are required. To only edit a few parameters you must lookup existing values in table use them as values submitting action.*

- `name` id
- data
  - `string` name
  - `bool` archived
  

**Example Data:**
    
    {
        "id": "music",
        "data": {
            "name": "Music 2",
            "archived": false
        }
    }

## **editlevel (Edit Level)**

**Authorization:** Requires `_self` auth

**Parameters:**
*All parameters are required. To only edit a few parameters you must lookup existing values in table use them as values submitting action.*

- `name` id
- data
  - `name` categoryId
  - `string` name
  - `uint8` maxVideoLength *(specified as seconds)*
  - `uint64` price *(specified in USD as cents)*
  - `uint64` participantLimit
  - `uint64` submissionPeriod *(specified as hours)*
  - `uint64` votePeriod *(specified as hours)*

**Example Data:**
    
    {
        "id": "music_gold",
        "data": {
            "categoryId": "music",
            "name": "Gold",
            "maxVideoLength": 30,
            "price": 1000,
            "participantLimit": 100,
            "submissionPeriod": 12,
            "votePeriod": 12
        }
    }

## **editprofile (Edit Profile)**

**Authorization:**
- Requires auth of `_self` or the `account` associated to the `uuid` parameter.
- Forces auth of `_self` when parameter `account` or `active` are not null.

**Parameters:**
- `name` id
- data
  - `string` username
  - `checksum256` imgHash
  - `name` account *(requires auth of _self)*
  - `bool` active *(requires auth of _self)*

**Example Data:**
    
    {
        "id": "30a65268b762",
        "data": {
            "username": "cryptocat1234",
            "imgHash": "fbea88977ed96d4b1a43b...",
            "account": "bob",
            "active": true
        }
    }

## **entercontest (Enter Contest)**
**Authorization:** 
- Requires auth of the account associated to `username` parameter 
- Asserts that the user has an active profile

**Parameters:**
- params
  - `string` username
  - `name` id
  - `name` levelId
  - `checksum256` videoHash360p
  - `checksum256` videoHash480p
  - `checksum256` videoHash720p
  - `checksum256` videoHash1080p

**Example Data:**
    
    {
        "params": {
            "username": "cryptocat1234",
            "id": "c67affd6b631...",
            "contestId": "25ea718c56ec...",
            "videoHash360p": "7e074460435747efe...",
            "videoHash480p": "61fa79bd6c8ab8593...",
            "videoHash720p": "fa5546d484d063b85...",
            "videoHash1080p": "d7328edbe89e6e12..."
        }
    }

## **vote (Vote)**

**Authorization:** 
- Requires auth of account associated to `username` parameter 
- Asserts that the user has an active profile
- Asserts hasn't yet voted for entry within contest

**Parameters:**
- `string` username
- `string` entryId

**Example Data:**
    
    {
        "username": "bob", 
        "entryId": "fc370e290a0f"
    }