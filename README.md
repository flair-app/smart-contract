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

## **archiveCategory**
**Authorization:** Requires `_self` auth

**Parameters:**
- `string` id

**Example Data:**
    
    ["music"]

## **archiveParentCategory**
**Authorization:** Requires `_self` auth

**Parameters:**
- `string` id

**Example Data:**
    
    ["music"]

## **claimFunds**
Transfer user's winnings to specified destination.

**Authorization:** Requires auth of the parameter `user`

**Parameters:**
- `string` user
- `account` to
- `string` memo

**Example Data:**
    
    ["bob", "coinbase", "12398712"]

## **createCategory**
**Authorization:** Requires `_self` auth

**Parameters:**
- `createCategoryParams` params
  - `string` id
  - `string` parentId
  - `string` name
  - `uint8` maxVideoLength *(specified as seconds)*
  - `uint64` price *(specified in USD as cents)*
  - `uint64` participantLimit
  - `uint64` submissionPeriod *(specified as hours)*
  - `uint64` votePeriod *(specified as hours)*

**Example Data:**
    
    [
        {
            id: 'music_gold',
            parentId: 'music',
            name: 'Gold',
            maxVideoLength: 30,
            price: 1000,
            participantLimit: 100,
            submissionPeriod: 12,
            votePeriod: 12
        }
    ]

## **createContestEntry**
**Authorization:** 
- Requires auth of the account associated to `username` parameter 
- Asserts that the user has an active profile

**Parameters:**
- `createContestEntry` params
  - `string` username
  - `string` id
  - `string` contestId
  - `checksum256` videoHash360p
  - `checksum256` videoHash480p
  - `checksum256` videoHash720p
  - `checksum256` videoHash1080p

**Example Data:**
    
    [
        {
            username: 'cryptoCat123',
            id: 'd68c1257-e9a0-47c0-b82f-c67affd6b631',
            contestId: 'e74988a5-efb4-4e92-a5e2-25ea718c56ec',
            videoHash360p: '7e074460435747efe...',
            videoHash480p: '61fa79bd6c8ab8593...',
            videoHash720p: 'fa5546d484d063b85...',
            videoHash1080p: 'd7328edbe89e6e12...,
        }
    ]

## **createProfile**
**Authorization:** Requires `_self` auth

**Parameters:**
- `createProfileParams` params
  - `string` id
  - `string` username
  - `checksum256` imgHash
  - `name` account
  - `bool` active

**Example Data:**
    
    [
        {
            id: '7f945fdb-50d3-48d2-96e2-30a65268b762',
            username: 'cryptoCat123',
            imgHash: 'fbea88977ed96d4b1...'
            account: 'bob',
            active: true',
        }
    ]

## **editCategory**
**Authorization:** Requires `_self` auth

**Parameters:**
- `string` id
- `editCategoryParams` params
  - `string` parentId
  - `string` name
  - `uint8` maxVideoLength *(specified as seconds)*
  - `uint64` price *(specified in USD as cents)*
  - `uint64` participantLimit
  - `uint64` submissionPeriod *(specified as hours)*
  - `uint64` votePeriod *(specified as hours)*

**Example Data:**
    
    [
        id: 'music_gold',
        {
            parentId: 'music',
            name: 'Gold',
            maxVideoLength: 30,
            price: 1000,
            participantLimit: 100,
            submissionPeriod: 12,
            votePeriod: 12
        }
    ]

## **setParentCategory**
**Authorization:** Requires `_self` auth

**Parameters:**
- `string` id
- `string` name

**Example Data:**
    
    ["id", "Music"]

## **updateEOS12HourHigh**

The 12hr high is used to calculate the amount of EOS needed for entries.

**Authorization:** Requires `_self` auth

**Parameters:**
- `uint64` time *(ms since epoch)*
- `uint64` usdHigh

**Example Data:**
    
    [1568751673935, 4.18]

## **updateProfile**

**Authorization:**
- Requires auth of `_self` or the `account` associated to the `uuid` parameter.
- Forces auth of `_self` when parameter `account` or `active` are not null.

**Parameters:**
- `string` uuid
- `updateProfileData` data
  - `name` account *(requires auth of _self)*
  - `bool` active *(requires auth of _self)*
  - `string` username
  - `checksum256` imgHash

**Example Data:**
    
    [
        '7f945fdb-50d3-48d2-96e2-30a65268b762',
        {
            username: 'cryptoCat123',
            imgHash: 'fbea88977ed96d4b1a43b...'
            account: 'bob',
            active: true',
        }
    ]

## **vote**

**Authorization:** 
- Requires auth of account associated to `username` parameter 
- Asserts that the user has an active profile
- Asserts hasn't yet voted for entry within contest

**Parameters:**
- `string` username
- `id` entryId

**Example Data:**
    
    ['bob', '89d1989d-7261-4454-b63b-fc370e290a0f']