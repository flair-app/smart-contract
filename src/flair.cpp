#include <eosio/eosio.hpp>
#include <eosio/name.hpp>
#include <eosio/asset.hpp>
#include <eosio/print.hpp>
#include <eosio/crypto.hpp>
#include <eosio/system.hpp>
#include <string>
#include <map>

using namespace eosio;

class [[eosio::contract("flair")]] flair : public contract {
  public:
      using contract::contract;

      /*
         CREATE CATEGORY
      */
      [[eosio::action]]
      void createcat(name id,  std::string name, uint32_t maxVideoLength) {
         require_auth( _self );

         category_index categories( _self, _self.value );

         categories.emplace(_self, [&](category& row) {
            row.id = id;
            row.name = name;
            row.maxVideoLength = maxVideoLength;
            row.archived = false;
         });
      }

      /*
         EDIT CATEGORY
      */
      struct editcatargs {
         std::string name;
         uint32_t maxVideoLength;
         bool archived;
      };

      [[eosio::action]]
      void editcat(name id,  editcatargs data) {
         require_auth( _self );

         category_index categories( _self, _self.value );

         auto iterator = categories.find(id.value);
         categories.modify(iterator, _self, [&](category& row) {
            row.id = id;
            row.name = data.name;
            row.maxVideoLength = data.maxVideoLength;
            row.archived = data.archived;
         });
      }

      /*
         CREATE LEVEL
      */
      struct createlvlargs {
         name id;
         name categoryId;
         std::string name;
         uint32_t price;
         uint32_t participantLimit;
         uint32_t submissionPeriod;
         uint32_t votePeriod;
      };

      [[eosio::action]]
      void createlevel(createlvlargs params) {
         require_auth( _self );

         level_index levels( _self, _self.value );

         levels.emplace(_self, [&](level& row) {
            row.id = params.id;
            row.categoryId = params.categoryId;
            row.name = params.name;
            row.price = params.price;
            row.participantLimit = params.participantLimit;
            row.submissionPeriod = params.submissionPeriod;
            row.votePeriod = params.votePeriod;
            row.archived = false;
         });
      }

      /*
         EDIT LEVEL
      */
      struct editlevelargs {
         std::string name;
         bool archived;
         uint32_t price;
         uint32_t participantLimit;
         uint32_t submissionPeriod;
         uint32_t votePeriod;
      };

      [[eosio::action]]
      void editlevel(name id,  editlevelargs data) {
         require_auth( _self );

         level_index levels( _self, _self.value );

         auto iterator = levels.find(id.value);
         levels.modify(iterator, _self, [&](level& row) {
            row.id = id;
            row.name = data.name;
            row.archived = data.archived;
            row.price = data.price;
            row.participantLimit = data.participantLimit;
            row.submissionPeriod = data.submissionPeriod;
            row.votePeriod = data.votePeriod;
         });
      }

      /*
         ADD PROFILE
      */
      struct addprofargs {
         name id;
         std::string username;
         checksum256 imgHash;
         name account;
         bool active;
      };

      [[eosio::action]]
      void addprofile(addprofargs params) {
         require_auth( _self );

         check(checkusername(params.username), "Invalid Username");

         profile_index profiles( _self, _self.value );
         
         checksum256 usernameHash = sha256(&params.username[0], params.username.size());

         auto byUsernameHashIdx = profiles.get_index<name("byusername")>();
         auto itr = byUsernameHashIdx.find(usernameHash);

         check(itr->username != params.username, "Username already exists.");

         profiles.emplace(_self, [&](profile& row) {
            row.id = params.id;
            row.username = params.username;
            row.usernameHash = usernameHash;
            row.imgHash = params.imgHash;
            row.account = params.account;
            row.active = params.active;
         });
      }

      /*
         EDIT PROFILE USER
      */
      struct editprofargsu {
         std::string username;
         checksum256 imgHash;
      };

      [[eosio::action]]
      void editprofuser(name id, editprofargsu data) {
         profile_index profiles(_self, _self.value);
         auto userProfile = profiles.find(id.value);

         require_auth( userProfile->account );

         checksum256 usernameHash = sha256(&data.username[0], data.username.size());

         auto byUsernameHashIdx = profiles.get_index<name("byusername")>();
         auto existingUsernameProfile = byUsernameHashIdx.find(usernameHash);
         check(existingUsernameProfile->username != data.username, "Username already exists.");

         profiles.modify(userProfile, _self, [&](profile& row) {
            row.id = id;
            row.username = data.username;
            row.usernameHash = usernameHash;
            row.imgHash = data.imgHash;
         });
      }

      /*
         EDIT PROFILE ADMIN
      */
      struct editprofargsa {
         std::string username;
         checksum256 imgHash;
         name account;
         bool active;
      };

      [[eosio::action]]
      void editprofadm(name id, editprofargsa data) {
         require_auth(_self);

         profile_index profiles(_self, _self.value);
         auto userProfile = profiles.find(id.value);
         checksum256 usernameHash = sha256(&data.username[0], data.username.size());

         auto byUsernameHashIdx = profiles.get_index<name("byusername")>();
         auto existingUsernameProfile = byUsernameHashIdx.find(usernameHash);
         check(existingUsernameProfile->username != data.username, "Username already exists.");

         profiles.modify(userProfile, _self, [&](profile& row) {
            row.id = id;
            row.username = data.username;
            row.usernameHash = usernameHash;
            row.imgHash = data.imgHash;
            row.account = data.account;
            row.active = data.active;
         });
      }

      /*
         SET EOS 12 HOUR HIGH
      */
      [[eosio::action]]
      void addeoshigh(uint32_t openTime, uint32_t usdHigh, uint32_t intervalSec) {
         require_auth(_self);

         uint32_t curEpoch = eosio::current_time_point().sec_since_epoch();
         uint32_t EOSPriceStoreLifeSec = 12 * 3600;
         uint32_t EOSPriceExpTime = curEpoch - EOSPriceStoreLifeSec;

         check(openTime > EOSPriceExpTime, "Open time must be within last 12 hours");

         eosprice_index eosprices(_self, _self.value);
         
         // DELETE EXPIRED PRICES
         auto oldPriceIter = eosprices.lower_bound(EOSPriceExpTime);
         bool done = false;
         while(
            !done
            && oldPriceIter != eosprices.end()
         ) {
            if (oldPriceIter == eosprices.begin()) {
               done = true;
            }

            bool isPriceExpired = oldPriceIter->openTime < EOSPriceExpTime;
            if(isPriceExpired) {
               print("(Notice) Expired EOS Price found: erase ", oldPriceIter->openTime, "\n");
               oldPriceIter = eosprices.erase(oldPriceIter);
            } else if(oldPriceIter != eosprices.begin()) {
               oldPriceIter--;
            }
         }

         // ADD NEW PRICE
         eosprices.emplace(_self, [&]( eosprice& row ) {
            row.openTime = openTime;
            row.usdHigh = usdHigh;
            row.intervalSec = intervalSec;
         });
      }

      /*
         SET ENTRY EXPIRATION
      */
      [[eosio::action]]
      void setentryexp(uint64_t exp) {
         require_auth( _self );

         entry_exp_index entry_exp_table( _self, _self.value );

         if (entry_exp_table.begin() != entry_exp_table.end()) {
            entry_exp_table.erase(entry_exp_table.begin());
         }

         entry_exp_table.emplace(_self, [&](entryexp& row) {
            row.exp = exp;
         });
      }

      /*
         SET PRICE FRESHNESS
      */
      [[eosio::action]]
      void setpricefrsh(uint64_t freshness) {
         require_auth( _self );

         price_fresh_index price_fresh_table( _self, _self.value );

         if (price_fresh_table.begin() != price_fresh_table.end()) {
            price_fresh_table.erase(price_fresh_table.begin());
         }

         price_fresh_table.emplace(_self, [&](pricefresh& row) {
            row.freshness = freshness;
         });
      }

      /*
         ENTER CONTEST
      */
      struct contestargs {
         name id;
         name userId;
         name levelId;
         checksum256 videoHash360p;
         checksum256 videoHash480p;
         checksum256 videoHash720p;
         checksum256 videoHash1080p;
         checksum256 coverHash;
      };

      [[eosio::action]]
      void entercontest(contestargs params) {
         profile_index profiles(_self, _self.value);
         auto userProfile = profiles.find(params.userId.value);

         require_auth( userProfile->account );

         entries_index entries(_self, _self.value);

         auto byUserIdAndLevelIdIdx = entries.get_index<name("byuserandlvl")>();         
         auto itr = byUserIdAndLevelIdIdx.find(composite_key(params.userId.value, params.levelId.value, true));
         
         // 1. get by index with UserId, LevelId, and open = 1
         // 2. check if is actually open or not, mark open = 0 if so
         if(itr != byUserIdAndLevelIdIdx.end() && itr->contestId > 0) {
            contest_index contests(_self, _self.value);
            auto contestItr = contests.find(itr->contestId);
            if (contestItr != contests.end()) {
               uint32_t now = eosio::current_time_point().sec_since_epoch();
               uint64_t contestEndTime = contestItr->createdAt + contestItr->submissionPeriod + contestItr->votePeriod;
               
               check(now > contestEndTime, "entryId: " + params.id.to_string() + ", You already have a running entry within this contest level.");

               byUserIdAndLevelIdIdx.modify(itr, _self, [&](contestEntry& row) {
                  row.open = false;
               });
            }
         } else if(itr != byUserIdAndLevelIdIdx.end()) {
            byUserIdAndLevelIdIdx.erase(itr);
         }

         entries.emplace(_self, [&]( contestEntry& row ) {
            row.id = params.id;
            row.userId = params.userId;
            row.levelId = params.levelId;
            row.videoHash360p = params.videoHash360p;
            row.videoHash480p = params.videoHash480p;
            row.videoHash720p = params.videoHash720p;
            row.videoHash1080p = params.videoHash1080p;
            row.coverHash = params.coverHash;
            
            row.createdAt = eosio::current_time_point().sec_since_epoch();
            row.contestId = 0;
            row.amount = 0;
            row.open = true;
         });
      }

      /*
         On Payment
      */
      [[eosio::on_notify("eosio.token::transfer")]]
      void deposit(name from, name to, asset quantity, std::string memo) {
         if (to != _self || quantity.symbol.code().to_string() != "EOS") {
            return;
         }

         // use memo as id to lookup entry
         name entryId = name(memo);
         entries_index entries(_self, _self.value);
         auto entryItr = entries.find(entryId.value);

         if(entryItr == entries.end()) {
            print("No entry found - payment invalid, memo: ", memo, " from: ", from, ", amount: ", quantity.to_string(), "\n");
            return;
         }

         // increment entry by asset amount
         entries.modify(entryItr, _self, [&](contestEntry& row) {
            row.amount = row.amount + quantity.amount;
         });
         
         // ensure entry is already assigned to contest
         if(entryItr->contestId != 0) {
            print("Entry already paid & assigned to contest.\n");
            return;
         }

         uint32_t now = eosio::current_time_point().sec_since_epoch();

         // ensure entry is not expired
         entry_exp_index entry_exp_table( _self, _self.value );
         uint64_t entryexpTime = entry_exp_table.begin()->exp;

         if (now > entryItr->createdAt + entryexpTime) {
            print("Entry is expired, please initiate refund to recieve money back.\n");
            return;
         }

         // get level interator
         level_index levels(_self, _self.value);
         auto levelItr = levels.find(entryItr->levelId.value);

         if (levelItr == levels.end()) {
            print("Error Creating Contest: could not find level with that id.", "\n");
            return;
         }

         // get contest interator
         contest_index contests(_self, _self.value);
         auto byLevelIdx = contests.get_index<name("bylevel")>();
         uint64_t submissionsClosed = false;
         auto curContestItr = byLevelIdx.lower_bound(composite_key(entryItr->levelId.value, submissionsClosed));

         uint64_t contestPrice = 0;
         
         // print("curContest: ", curContestItr->id, " ", curContestItr->levelId, " ", curContestItr->participantCount, "\n");
         // print("curContest Not End: ", curContestItr != byLevelIdx.end(), "\n");
         // print("levelId Matches: ", curContestItr->levelId == entryItr->levelId, "\n");
         // print("contest not full: ", curContestItr->participantCount < curContestItr->participantLimit, "\n");
         bool curContestValid = (
            curContestItr != byLevelIdx.end()
            && curContestItr->levelId == entryItr->levelId
            && curContestItr->participantCount < curContestItr->participantLimit
            && now <= curContestItr->createdAt + curContestItr->submissionPeriod
         );

         if (curContestValid) {
            contestPrice = curContestItr->price;
         } else {
            contestPrice = levelItr->price;
         }

         // determine eos price high since entry created
         eosprice_index eosprices(_self, _self.value);
         auto pricesByEndTime = eosprices.get_index<name("byendtime")>();
         auto priceItr = pricesByEndTime.lower_bound(entryItr->createdAt);

         uint64_t priceHigh = 0;

         for (auto itr = priceItr; itr != pricesByEndTime.end(); itr++) {
            print("debug price high: ", itr->usdHigh, "\n");
            if(itr->usdHigh > priceHigh) {
               priceHigh = itr->usdHigh;
            }
         }

         // mark entry as priceUnavailable if lastest EOS price openTime + intervalSec is older than the set required price freshness
         price_fresh_index price_fresh_table( _self, _self.value );
         uint64_t freshTime = price_fresh_table.begin()->freshness;
         auto lastPrice = --pricesByEndTime.end();
         bool freshPrice = (lastPrice->openTime + lastPrice->intervalSec) + freshTime > now;
         print("price fresh debug: freshPrice=", freshPrice," lastEndTime=", lastPrice->openTime + lastPrice->intervalSec, ", freshTime=", freshTime, " | ", lastPrice->openTime + lastPrice->intervalSec + freshTime, " > ", now, "\n");
         if(priceHigh <= 0 || !freshPrice) {
            entries.modify(entryItr, _self, [&](contestEntry& row) {
               row.priceUnavailable = true;
            });

            print("EOS Price Unavailable: run update action to recheck once price has been updated.\n");
            return;
         }

         // fail if quantity is not enough.
         print("debug price: ", priceHigh, " ", quantity.amount, " ", contestPrice, "\n");
         if (priceHigh * quantity.amount < contestPrice * 1000000) {
            print("Payment not enough only $", (float)(priceHigh * quantity.amount) / 100000000.0,".\n");
            return;
         }

         if (curContestValid) {
            entries.modify(entryItr, _self, [&](contestEntry& row) {
               row.contestId = curContestItr->id;
            });
            byLevelIdx.modify(curContestItr, _self, [&](contest& row) {
               row.participantCount++;
            });
         } else {
            uint64_t newContestId = contests.available_primary_key();
            if (newContestId == 0) { newContestId++; }
            print("newContestId: ", newContestId, "\n");
            
            contests.emplace(_self, [&](contest& row) {
               row.id = newContestId;
               row.levelId = entryItr->levelId;
               row.participantLimit = levelItr->participantLimit;
               row.participantCount = 1;
               row.price = levelItr->price;
               row.submissionPeriod = levelItr->submissionPeriod;
               row.submissionsClosed = false;
               row.votePeriod = levelItr->votePeriod;
               row.createdAt = eosio::current_time_point().sec_since_epoch();
            });

            if(curContestItr != byLevelIdx.end()) {
               byLevelIdx.modify(curContestItr, _self, [&](contest& row) {
                  row.submissionsClosed = 1;
               });
            }

            entries.modify(entryItr, _self, [&](contestEntry& row) {
               row.contestId = newContestId;
            });

            print(entryId, " activated with contest id of ", newContestId, "\n");
         }
      }

      [[eosio::action]]
      void refundentry(name id, name to, std::string memo) {
         entries_index entries(_self, _self.value);
         auto entryItr = entries.find(id.value);

         profile_index profiles(_self, _self.value);
         auto userProfile = profiles.find(entryItr->userId.value);

         require_auth( userProfile->account );

         check(entryItr != entries.end(), "No entry found... id: " + id.to_string() + "memo: " + memo + " to: " + to.to_string());
         check(entryItr->contestId <= 0, "Entry cannot be refunded once it has been assigned to a contest.");
         check(entryItr->amount > 0, "Entry does not have any funds to refund.");

         print(id, " ", entryItr->contestId, " ", entryItr->amount, "\n");

         int64_t a = static_cast<int64_t>(entryItr->amount);
         symbol s = symbol{"EOS", 4};
         asset refundAmt = asset{a, s};

         print("refund amt: ", refundAmt, "a: ", a, "s: ", s, "\n");
         action{
            permission_level{get_self(), name("active")},
            name("eosio.token"),
            name("transfer"),
            std::make_tuple(get_self(), to, refundAmt, memo)
         }.send();

         // reset entry asset amount
         entries.modify(entryItr, _self, [&](contestEntry& row) {
            row.amount = 0;
         });
      }

   private:
      bool checkusername(std::string username) {
         print("checkusername ", username, "\n");

         // cannot be under 6 char
         if (username.size() < 6) {
            print("Username cannot be less than 6 characters.", "\n");
            return false;
         }

         // cannot be over 30 char
         if (username.size() > 30) {
            print("Username cannot be more than 30 characters.", "\n");
            return false;
         }

         // prevent starting with dot
         if (username.front() == '.') {
            print("Username cannot start with a dot.", "\n");
            return false;
         }

         // prevent ending with dot
         if (username.back() == '.') {
            print("Username cannot end with a dot.", "\n");
            return false;
         }

         // only allow alphanumeric and dots (A-Z a-z 0-9 .)
         std::map<char, char> allowedCharactersHash({
            {'a', 'a'}, {'b', 'b'}, {'c', 'c'}, {'d', 'd'}, {'e', 'e'}, {'f', 'f'}, {'g', 'g'}, {'h', 'h'},
            {'i', 'i'}, {'j', 'j'}, {'k', 'k'}, {'l', 'l'}, {'m', 'm'}, {'n', 'n'}, {'o', 'o'}, {'p', 'p'},
            {'q', 'q'}, {'r', 'r'}, {'s', 's'}, {'t', 't'}, {'u', 'u'}, {'v', 'v'}, {'w', 'w'}, {'x', 'x'},
            {'y', 'y'}, {'z', 'z'}, {'A', 'A'}, {'B', 'B'}, {'C', 'C'}, {'D', 'D'}, {'E', 'E'}, {'F', 'F'},
            {'G', 'G'}, {'H', 'H'}, {'I', 'I'}, {'J', 'J'}, {'K', 'K'}, {'L', 'L'}, {'M', 'M'}, {'N', 'N'},
            {'O', 'O'}, {'P', 'P'}, {'Q', 'Q'}, {'R', 'R'}, {'S', 'S'}, {'T', 'T'}, {'U', 'U'}, {'V', 'V'},
            {'W', 'W'}, {'X', 'X'}, {'Y', 'Y'}, {'Z', 'Z'}, {'1', '1'}, {'2', '2'}, {'3', '3'}, {'4', '4'},
            {'5', '5'}, {'6', '6'}, {'7', '7'}, {'8', '8'}, {'9', '9'}, {'0', '0'}, {'.', '.'}
         });

         char *prevChar = NULL;
         for (char &c: username) {
            if (allowedCharactersHash.count(c) == 0) {
               print("Username is limited to containing alphanumeric(A-Z a-z 0-9) and dots(.).", "\n");
               return false;
            }

            if (c == '.' && *prevChar == '.') {
               print("Username cannot contain double dots (..).", "\n");
               return false;
            }
            prevChar = &c;
         }

         print("username is valid", "\n");
         return true;
      }

      static uint128_t composite_key(uint64_t mostSignificantInt, uint64_t leastSignificantInt) {
         return (uint128_t) mostSignificantInt << 64 | leastSignificantInt;
      }

      static checksum256 composite_key(uint64_t a, uint64_t b, uint64_t c) {
         return checksum256::make_from_word_sequence<uint64_t>(
            0ULL, a, b, c
         );
      }

      /*
         TABLE: categories
      */
      struct [[eosio::table]] category {
         name id;
         std::string name;
         uint32_t maxVideoLength;
         bool archived;

         uint64_t primary_key() const { return id.value; }
      };

      typedef eosio::multi_index<name("categories"), category> category_index;

      /*
         TABLE: levels
      */
      struct [[eosio::table]] level {
         name id;
         name categoryId;
         std::string name;
         bool archived;
         uint32_t price;
         uint32_t participantLimit;
         uint32_t submissionPeriod;
         uint32_t votePeriod;

         uint64_t primary_key() const { return id.value; }
      };

      typedef eosio::multi_index<name("levels"), level> level_index;

      /*
         TABLE: profiles
      */
      struct [[eosio::table]] profile {
         name id;
         std::string username;
         checksum256 usernameHash;
         checksum256 imgHash;
         name account;
         bool active;

         uint64_t primary_key() const { return id.value; }
         checksum256 by_username_hash() const { return usernameHash; }
      };

      typedef eosio::multi_index<
         name("profiles"), 
         profile,
         indexed_by<name("byusername"), const_mem_fun<profile, checksum256, &profile::by_username_hash>>
      > profile_index;

      /*
         TABLE: entryexp
      */
      struct [[eosio::table]] entryexp {
         uint64_t exp;
         uint64_t primary_key() const { return exp; }
      };

      typedef eosio::multi_index<name("entryexp"), entryexp> entry_exp_index;

      /*
         TABLE: pricefresh
      */
      struct [[eosio::table]] pricefresh {
         uint64_t freshness;
         uint64_t primary_key() const { return freshness; }
      };

      typedef eosio::multi_index<name("pricefresh"), pricefresh> price_fresh_index;

      /*
         TABLE: eosprices
      */
      struct [[eosio::table]] eosprice {
         uint64_t openTime;
         uint32_t usdHigh; // represented as one hundredth of a cent ($1.00 * 1000)
         uint32_t intervalSec;

         uint64_t primary_key() const { return openTime; }
         uint64_t endtime_key() const { return openTime + intervalSec; }
      };

      typedef eosio::multi_index<
         name("eosprices"), 
         eosprice,
         indexed_by<name("byendtime"), const_mem_fun<eosprice, uint64_t, &eosprice::endtime_key>>
      > eosprice_index;

      /*
         TABLE: entries
      */
      struct [[eosio::table]] contestEntry {
         name id;
         name userId;
         name levelId;
         uint64_t contestId;
         uint64_t amount;
         bool priceUnavailable;
         bool open;
         checksum256 videoHash360p;
         checksum256 videoHash480p;
         checksum256 videoHash720p;
         checksum256 videoHash1080p;
         checksum256 coverHash;
         uint32_t createdAt;
         
         uint64_t primary_key() const { return id.value; }
         checksum256 by_userid_levelid() const {
            return composite_key(userId.value, levelId.value, open);
         }
      };
      
      typedef eosio::multi_index<
         name("entries"), 
         contestEntry,
         indexed_by<name("byuserandlvl"), const_mem_fun<contestEntry, checksum256, &contestEntry::by_userid_levelid>>
      > entries_index;

      /*
         TABLE: contest
      */
      struct [[eosio::table]] contest {
         uint64_t id;
         name levelId;
         uint64_t price;
         uint32_t participantLimit;
         uint32_t participantCount;
         bool submissionsClosed;
         uint32_t submissionPeriod;
         uint32_t votePeriod;
         uint32_t createdAt;

         uint64_t primary_key() const { return id; }
         uint128_t bylevel() const { return composite_key(levelId.value, submissionsClosed); }
      };

      typedef eosio::multi_index<
         name("contests"), 
         contest,
         indexed_by<name("bylevel"), const_mem_fun<contest, uint128_t, &contest::bylevel>>
      > contest_index;
};
