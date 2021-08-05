#include <eosio/eosio.hpp>
#include <eosio/name.hpp>
#include <eosio/asset.hpp>
#include <eosio/print.hpp>
#include <eosio/crypto.hpp>
#include <eosio/system.hpp>
#include <string>
#include <map>
#include "safeint.hpp"

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
         uint32_t fee;
         std::list<uint32_t> prizes;
         uint32_t fixedPrize;
         uint32_t allowedSimultaneousContests;
         uint32_t voteStartUTCHour;
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
            row.fee = params.fee;
            row.prizes = params.prizes;
            row.fixedPrize = params.fixedPrize;
            row.allowedSimultaneousContests = params.allowedSimultaneousContests;
            row.voteStartUTCHour = params.voteStartUTCHour;
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
         uint32_t fee;
         std::list<uint32_t> prizes;
         uint32_t fixedPrize;
         uint32_t allowedSimultaneousContests;
         uint32_t voteStartUTCHour;
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
            row.fee = data.fee;
            row.prizes = data.prizes;
            row.fixedPrize = data.fixedPrize;
            row.allowedSimultaneousContests = data.allowedSimultaneousContests;
            row.voteStartUTCHour = data.voteStartUTCHour;
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
         std::string link;
         std::string bio;
         bool active;
      };

      [[eosio::action]]
      void addprofile(addprofargs params) {
         require_auth( _self );

         check(checkusername(params.username), "Invalid Username");
         checkUsernameExists(params.username);
         checkAndSanitizeLink(params.link);
         checkAndSanitizeBio(params.bio);

         profile_index profiles( _self, _self.value );
         checksum256 usernameHash = hashUsername(params.username);
         profiles.emplace(_self, [&](profile& row) {
            row.id = params.id;
            row.username = params.username;
            row.usernameHash = usernameHash;
            row.imgHash = params.imgHash;
            row.account = params.account;
            row.active = params.active;
            row.link = params.link;
            row.bio = params.bio;
         });
      }

      /*
         EDIT PROFILE USER
      */
      struct editprofargsu {
         std::string username;
         checksum256 imgHash;
         std::string link;
         std::string bio;
      };

      [[eosio::action]]
      void editprofuser(name id, editprofargsu data) {
         profile_index profiles(_self, _self.value);
         auto userProfile = profiles.find(id.value);

         require_auth( userProfile->account );

         if (userProfile->username != data.username) {
            checkUsernameExists(data.username);
         }
         checkAndSanitizeLink(data.link);
         checkAndSanitizeBio(data.bio);

         checksum256 usernameHash = hashUsername(data.username);
         profiles.modify(userProfile, _self, [&](profile& row) {
            row.id = id;
            row.username = data.username;
            row.usernameHash = usernameHash;
            row.imgHash = data.imgHash;
            row.link = data.link;
            row.bio = data.bio;
         });
      }

      /*
         EDIT PROFILE ADMIN
      */
      struct editprofargsa {
         std::string username;
         checksum256 imgHash;
         name account;
         std::string link;
         std::string bio;
         bool active;
      };

      [[eosio::action]]
      void editprofadm(name id, editprofargsa data) {
         require_auth(_self);

         profile_index profiles(_self, _self.value);
         auto userProfile = profiles.find(id.value);
         checksum256 usernameHash = hashUsername(data.username);

         if (userProfile->username != data.username) {
            checkUsernameExists(data.username);
         }

         checkAndSanitizeLink(data.link);
         checkAndSanitizeBio(data.bio);

         profiles.modify(userProfile, _self, [&](profile& row) {
            row.id = id;
            row.username = data.username;
            row.usernameHash = usernameHash;
            row.imgHash = data.imgHash;
            row.account = data.account;
            row.active = data.active;
            row.link = data.link;
            row.bio = data.bio;
         });
      }

      /*
         SET CURRENCY 12 HOUR HIGH
      */
      [[eosio::action]]
      void addcurhigh(uint32_t openTime, uint32_t usdHigh, uint32_t intervalSec) {
         require_auth(_self);

         uint32_t curEpoch = eosio::current_time_point().sec_since_epoch();
         uint32_t CurPriceStoreLifeSec = get_option_int(name{"entryexp"});
         uint32_t CurPriceExpTime = curEpoch - CurPriceStoreLifeSec;

         check(openTime > CurPriceExpTime, "Open time must be within last 12 hours");

         curprice_index curprices(_self, _self.value);
         
         // DELETE EXPIRED PRICES
         auto oldPriceIter = curprices.lower_bound(CurPriceExpTime);
         bool done = false;
         while(
            !done
            && oldPriceIter != curprices.end()
         ) {
            if (oldPriceIter == curprices.begin()) {
               done = true;
            }

            bool isPriceExpired = oldPriceIter->openTime < CurPriceExpTime;
            if(isPriceExpired) {
               print("(Notice) Expired Currency Price found: erase ", oldPriceIter->openTime, "\n");
               oldPriceIter = curprices.erase(oldPriceIter);
            } else if(oldPriceIter != curprices.begin()) {
               oldPriceIter--;
            }
         }

         // ADD NEW PRICE
         curprices.emplace(_self, [&]( curprice& row ) {
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
         set_option(name{"entryexp"}, exp);
      }

      /*
         SET PRICE FRESHNESS
      */
      [[eosio::action]]
      void setpricefrsh(uint64_t freshness) {
         require_auth( _self );
         set_option(name{"pricefresh"}, freshness);
      }

      /*
         ENTER CONTEST
      */
      struct contestargs {
         name id;
         name userId;
         name levelId;
         checksum256 videoHash720p;
         checksum256 videoHash1080p;
         checksum256 coverHash;
      };

      [[eosio::action]]
      void entercontest(contestargs params) {
         profile_index profiles(_self, _self.value);
         auto userProfile = profiles.find(params.userId.value);

         level_index levels(_self, _self.value);
         auto levelItr = levels.find(params.levelId.value);

         require_auth( userProfile->account );
         check(userProfile->active, "Profile must be active to enter a contest");
         check(levelItr->archived == 0, "Level must be active to enter a contest");

         uint32_t levelContestCount = countOpenContestForLevel(levelItr->id);
         print("levelAllowedSimultaneousContests:", levelItr->allowedSimultaneousContests, "\n");
         print("levelContestCount:", levelContestCount, "\n");
         check(levelItr->allowedSimultaneousContests == 0 || levelContestCount < levelItr->allowedSimultaneousContests, "This level is full");

         if (levelItr->fixedPrize > 0) {
            auto prizefund = get_option_int(name{"prizefund"});
            check(prizefund >= usdToCurrencyAmount(levelItr->fixedPrize), "Not enough money in prize fund to pay out prize.");
         }

         entries_index entries(_self, _self.value);

         auto byUserIdAndLevelIdIdx = entries.get_index<name("byuserandlvl")>();         
         auto itr = byUserIdAndLevelIdIdx.find(composite_key(params.userId.value, params.levelId.value, true));
         
         contest_index contests(_self, _self.value);

         // 1. get by index with UserId, LevelId, and open = 1
         // 2. check if is actually open or not, mark open = 0 if so
         if(itr != byUserIdAndLevelIdIdx.end() && itr->contestId > 0) {
            auto contestItr = contests.find(itr->contestId);
            if (contestItr != contests.end()) {
               uint32_t now = eosio::current_time_point().sec_since_epoch();
               check(now > contestItr->votestarttime(), "You've already entered this contest. You can only submit one entry per contest. (entryId: " + params.id.to_string() + ")");

               byUserIdAndLevelIdIdx.modify(itr, _self, [&](contestEntry& row) {
                  row.open = false;
               });
            }
         } else if(itr != byUserIdAndLevelIdIdx.end()) {
            byUserIdAndLevelIdIdx.modify(itr, _self, [&](contestEntry& row) {
               row.open = false;
            });
         }

         auto entryItr = entries.emplace(_self, [&]( contestEntry& row ) {
            row.id = params.id;
            row.userId = params.userId;
            row.levelId = params.levelId;
            row.videoHash720p = params.videoHash720p;
            row.videoHash1080p = params.videoHash1080p;
            row.coverHash = params.coverHash;
            
            row.createdAt = eosio::current_time_point().sec_since_epoch();
            row.contestId = 0;
            row.amount = 0;
            row.votes = 0;
            row.open = true;
         });

         if(levelItr->price == 0) {
            activateEntry<decltype(entries), decltype(entryItr)>(entries, entryItr);
         }
      }

      /*
         On Payment
      */
      [[eosio::on_notify("eosio.token::transfer")]]
      void deposit(name from, name to, asset quantity, std::string memo) {
         std::string currency = get_option(name{'currency'});
         if (to != _self || quantity.symbol.code().to_string() != currency) {
            if (quantity.symbol.code().to_string() != currency) {
               print("Currency doesn't match: ", quantity.symbol.code().to_string(), " != ", currency);
            }
            return;
         }

         if (memo == "prizefund") {
            auto prizefund = get_option_int(name{"prizefund"});
            print("prizefund before:", prizefund, "\n");
            prizefund = (safeint{prizefund} + safeint{quantity.amount}).amount;
            print("prizefund after:", prizefund, "\n");
            set_option(name{"prizefund"}, prizefund);
         } else {
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
               row.amount = (safeint{row.amount} + safeint{quantity.amount}).amount;
            });
            
            activateEntry<decltype(entries), decltype(entryItr)>(entries, entryItr);
         }
      }

      /*
         Refund Entry
      */
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
         symbol s = symbol{get_option(name{'currency'}), 4};
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

      /*
         Block Entry
      */
      [[eosio::action]]
      void blkentry(name id) {
         require_auth(_self);

         entries_index entries(_self, _self.value);
         auto entryItr = entries.find(id.value);

         check(entryItr->contestId > 0, "Cannot block an entry that is not in a contest.");
         check(entryItr->block == 0, "Entry is already blocked.");

         contest_index contests(_self, _self.value);
         auto contestItr = contests.find(entryItr->contestId);

         entries.modify(entryItr, _self, [&](contestEntry& row) {
            row.block = 1;
         });

         contests.modify(contestItr, _self, [&](contest& row) {
            row.participantCount--;
         });

         symbol s(get_option(name{'currency'}), 4);

         if (!entryItr->prizeRevoked && entryItr->prizeGiven.amount > 0 && entryItr->prizeGiven > asset{0, s}) {
            profile_index profiles(_self, _self.value);
            auto profileItr = profiles.find(entryItr->userId.value);

            if (profileItr->winnings >= entryItr->prizeGiven) { 
               profiles.modify(profileItr, _self, [&](profile& row) {
                  row.winnings = row.winnings - entryItr->prizeGiven;
               });

               entries.modify(entryItr, _self, [&](contestEntry& row) {
                  row.prizeRevoked = 1;
               });
            }          
         }
         
      }

     /*
         Unblock Entry
      */
      void unblkentry(name id) {
         require_auth(_self);
         
         entries_index entries(_self, _self.value);
         auto entryItr = entries.find(id.value);

         check(entryItr->contestId > 0, "Cannot unblock an entry that is not in a contest");
         check(entryItr->block == 1, "Cannot unblock an entry that is not blocked.");

         contest_index contests(_self, _self.value);
         auto contestItr = contests.find(entryItr->contestId);


         entries.modify(entryItr, _self, [&](contestEntry& row) {
            row.block = 0;
         });

         contests.modify(contestItr, _self, [&](contest& row) {
            row.participantCount++;
         });
      }

      /*
         Vote
      */
      [[eosio::action]]
      void vote(name voterUserId, name entryId) {
         profile_index profiles( _self, _self.value );
         auto userItr = profiles.find(voterUserId.value);

         check(userItr != profiles.end(), "User could not be found.");

         require_auth(userItr->account);

         check(userItr->active, "User must be active.");

         entries_index entries(_self, _self.value);
         auto entryItr = entries.find(entryId.value);

         check(entryItr != entries.end(), "Entry could not be found.");

         // ensure within voting period
         contest_index contests(_self, _self.value);
         auto contestItr = contests.find(entryItr->contestId);
         uint32_t now = eosio::current_time_point().sec_since_epoch();

         print("votestarttime: ", contestItr->votestarttime(), "\n");
         print("endtime: ", contestItr->endtime(), "\n");
         check(now > contestItr->votestarttime(), "Voting has not begun yet.");
         check(now <= contestItr->endtime(), "Voting has ended for this contest.");

         // determine if already voted
         vote_index votes(_self, _self.value);
         auto votesByUserContest = votes.get_index<name("byusrcontest")>();
         auto voteItr = votesByUserContest.find(composite_key(entryItr->contestId, voterUserId.value));
         check(voteItr == votesByUserContest.end(), "You've already voted in this contest.");

         // update entry vote count
         entries.modify(entryItr, _self, [&](contestEntry& row) {
            row.votes = (safeint{row.votes} + 1).amount;
         });

         // add to votes table
         uint64_t newVoteId = votes.available_primary_key();
         if (newVoteId == 0) { newVoteId++; }
         print("newVoteId: ", newVoteId, "\n");
         
         votes.emplace(_self, [&](entryvote& row) {
            row.id = newVoteId;
            row.contestId = entryItr->contestId;
            row.entryId = entryId;
            row.voterUserId = voterUserId;
            row.createdAt = eosio::current_time_point().sec_since_epoch();
         });
      }

      /*
         Claim
      */
      [[eosio::action]]
      void claim(name profileId, asset amount, name to, std::string memo) {
         profile_index profiles(_self, _self.value);
         auto profileItr = profiles.find(profileId.value);
         check(profileItr->id == profileId, "Cannot find profile");
         require_auth(profileItr->account);
         check(profileItr->active, "Profile must be active to claim winnings");
         check(profileItr->winnings.amount >= amount.amount, "Amount greater than prize winnings");

         profiles.modify(profileItr, _self, [&](profile& row) {
            row.winnings = row.winnings - amount;
         });

         action{
            permission_level{get_self(), name("active")},
            name("eosio.token"),
            name("transfer"),
            std::make_tuple(get_self(), to, amount, memo)
         }.send();
      }

      /*
         Claim USD
      */
      [[eosio::action]]
      void claimusd(name profileId, name claimId, asset amount) {
         profile_index profiles(_self, _self.value);
         auto profileItr = profiles.find(profileId.value);
         check(profileItr->id == profileId, "Cannot find profile");
         require_auth(profileItr->account);
         check(profileItr->active, "Profile must be active to claim winnings");
         check(profileItr->winnings.amount >= amount.amount, "Amount greater than prize winnings");

         profiles.modify(profileItr, _self, [&](profile& row) {
            row.winnings = row.winnings - amount;
         });

         std::string claimusdacct = get_option(name{"claimusdacct"});
         std::string claimusdmemo = get_option(name{"claimusdmemo"});

         openclaim_index openclaims(_self, _self.value);
         openclaims.emplace(_self, [&](openclaim& row) {
            row.id = claimId;
            row.profileId = profileId;
            row.to = name{claimusdacct};
            row.toMemo = claimusdmemo;
            row.amount = amount;
         });

         action{
            permission_level{get_self(), name("active")},
            name("eosio.token"),
            name("transfer"),
            std::make_tuple(get_self(), name{claimusdacct}, amount, claimusdmemo)
         }.send();
      }

      /*
         Claim USD
      */
      [[eosio::action]]
      void deleteclaim(name claimId) {
         require_auth( _self );
         openclaim_index openclaims(_self, _self.value);
         auto openclaim = openclaims.find(claimId.value);
         openclaims.erase(openclaim);
      }

      /*
         Set Fee Account
      */
      [[eosio::action]]
      void setclaimacct(name account, std::string memo) {
         require_auth( _self );
         set_option(name{"claimusdacct"}, account.to_string());
         set_option(name{"claimusdmemo"}, memo);
      }

      /*
         Set Fee Account
      */
      [[eosio::action]]
      void setfeeacct(name account, std::string memo) {
         require_auth( _self );
         set_option(name{"feeacct"}, account.to_string());
         set_option(name{"feeacctmemo"}, memo);
      }

      /*
         Set Currency
      */
      [[eosio::action]]
      void setcurrency(std::string curSymbol) {
         require_auth( _self );
         set_option(name{'currency'}, curSymbol);
         print("setcurrency", name{'currency'}, " ", curSymbol);
      }

      /*
         Set Entry Archive Seconds
      */
      [[eosio::action]]
      void setentryarch(uint64_t sec) {
         require_auth( _self );
         set_option(name{"entryarchsec"}, sec);
      }

      /*
         Update
      */
      [[eosio::action]]
      void update() {
         require_auth( _self );
         print("hello from update \n");
         distributeContestWinnings();
         print("distributeContestWinnings completed \n");
         checkUnavailablePriceEntries();
         print("checkUnavailablePriceEntries completed \n");
         archiveContests();
         print("archiveContests completed \n");
      }

      [[eosio::action]]
      void paycpu() {
         // noop
      }

   private:
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
         uint32_t fee;
         std::list<uint32_t> prizes;
         uint32_t fixedPrize;
         uint32_t allowedSimultaneousContests;
         uint32_t voteStartUTCHour;

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
         std::string link;
         std::string bio;
         name account;
         bool active;
         asset winnings;

         uint64_t primary_key() const { return id.value; }
         checksum256 by_username_hash() const { return usernameHash; }
      };

      typedef eosio::multi_index<
         name("profiles"), 
         profile,
         indexed_by<name("byusername"), const_mem_fun<profile, checksum256, &profile::by_username_hash>>
      > profile_index;

      /*
         TABLE: openclaims
      */
      struct [[eosio::table]] openclaim {
         name id;
         name profileId;
         name to;
         std::string toMemo;
         asset amount;

         uint64_t primary_key() const { return id.value; }
      };

      typedef eosio::multi_index<
         name("openclaims"), 
         openclaim
      > openclaim_index;

      /*
         TABLE: options
      */
      struct [[eosio::table]] option {
         name id;
         std::string value;
         uint64_t primary_key() const { return id.value; }
      };

      typedef eosio::multi_index<name("options"), option> option_index;

      /*
         TABLE: curprices
      */
      struct [[eosio::table]] curprice {
         uint64_t openTime;
         uint32_t usdHigh; // represented as one hundredth of a cent ($1.00 * 1000)
         uint32_t intervalSec;

         uint64_t primary_key() const { return openTime; }
         uint64_t endtime_key() const { return (safeint{openTime} + safeint{intervalSec}).amount; }
      };

      typedef eosio::multi_index<
         name("curprices"),
         curprice,
         indexed_by<name("byendtime"), const_mem_fun<curprice, uint64_t, &curprice::endtime_key>>
      > curprice_index;

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
         bool block;
         bool prizeRevoked;
         asset prizeGiven;
         checksum256 videoHash720p;
         checksum256 videoHash1080p;
         checksum256 coverHash;
         uint32_t createdAt;
         uint32_t votes;
         
         uint64_t primary_key() const { return id.value; }
         checksum256 by_userid_levelid() const {
            return composite_key(userId.value, levelId.value, open);
         }
         uint64_t bycontest() const {
            return contestId;
         }
         uint64_t bypriceunavail() const {
            return priceUnavailable;
         }
         checksum256 byvidhashsm() const {
            return videoHash720p;
         }
         checksum256 byvidhashlg() const {
            return videoHash1080p;
         }
         uint64_t bycreatedat() const {
            return createdAt;
         }
      };

      typedef eosio::multi_index<
         name("entries"), 
         contestEntry,
         indexed_by<name("byuserandlvl"), const_mem_fun<contestEntry, checksum256, &contestEntry::by_userid_levelid>>,
         indexed_by<name("bycontest"), const_mem_fun<contestEntry, uint64_t, &contestEntry::bycontest>>,
         indexed_by<name("bynoprice"), const_mem_fun<contestEntry, uint64_t, &contestEntry::bypriceunavail>>,
         indexed_by<name("byvidhashsm"), const_mem_fun<contestEntry, checksum256, &contestEntry::byvidhashsm>>,
         indexed_by<name("byvidhashlg"), const_mem_fun<contestEntry, checksum256, &contestEntry::byvidhashlg>>,
         indexed_by<name("bycreatedat"), const_mem_fun<contestEntry, uint64_t, &contestEntry::bycreatedat>>
      > entries_index;

      /*
         TABLE: contests
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
         uint32_t fixedPrize;
         uint32_t voteStartUTCHour;
         bool paid;

         uint64_t primary_key() const { return id; }
         uint128_t bylevel() const { return composite_key(levelId.value, submissionsClosed); }
         uint64_t votestarttime() const {
            if (voteStartUTCHour == 0) {
               return (safeint{createdAt} + safeint{submissionPeriod}).amount;
            }

            auto hours = (createdAt / 3600) % 24;
            auto minutes = (createdAt / 60) % 60;
            auto seconds = createdAt % 60;
            if (hours < voteStartUTCHour) {
               return createdAt - (minutes * 60) - seconds + ((voteStartUTCHour - hours) * 3600);
            } else {
               return createdAt - (minutes * 60) - seconds + ((24 + voteStartUTCHour - hours) * 3600);
            }
         }
         uint64_t endtime() const { return (safeint{votestarttime()} + safeint{votePeriod}).amount; }
         uint128_t level_and_start() const { 
            return composite_key(levelId.value, votestarttime());
         }
      };

      typedef eosio::multi_index<
         name("contests"),
         contest,
         indexed_by<name("bylevel"), const_mem_fun<contest, uint128_t, &contest::bylevel>>,
         indexed_by<name("byendtime"), const_mem_fun<contest, uint64_t, &contest::endtime>>,
         indexed_by<name("bylevelstart"), const_mem_fun<contest, uint128_t, &contest::level_and_start>>
      > contest_index;

      /*
         TABLE: votes
      */
      struct [[eosio::table]] entryvote {
         uint64_t id;
         uint64_t contestId;
         name entryId;
         name voterUserId;
         uint32_t createdAt;

         uint64_t primary_key() const { return id; }
         uint128_t byusercontest() const { return composite_key(contestId, voterUserId.value); }
         uint64_t byentryid() const { return entryId.value; }
      };

      typedef eosio::multi_index<
         name("votes"), 
         entryvote,
         indexed_by<name("byusrcontest"), const_mem_fun<entryvote, uint128_t, &entryvote::byusercontest>>,
         indexed_by<name("byentryid"), const_mem_fun<entryvote, uint64_t, &entryvote::byentryid>>
      > vote_index;

      /*
         Distribute Contest Winnings - used within update
      */
      void distributeContestWinnings() {
         print("distributeContestWinnings \n");
         contest_index contests( _self, _self.value );
         auto contestsByEndtime = contests.get_index<name("byendtime")>();
         uint64_t now = eosio::current_time_point().sec_since_epoch();
         auto contestItrEndTime = contestsByEndtime.upper_bound(now - 1);

         if (contestItrEndTime == contestsByEndtime.begin()) {
            print("no unpaid contests ending at or before ", now - 1, "\n");
            return;
         } else {
            contestItrEndTime--;
         }

         auto contestItr = contestItrEndTime;

         bool hitBeginning = false;
         while(!hitBeginning && contestItr->paid == false) {
            auto winnerResults = getContestWinners<decltype(contestItr)>(contestItr);
            auto winnersArr = std::get<0>(winnerResults);
            auto prizeRemainder = std::get<1>(winnerResults);

            for (auto const& winnerTuple : winnersArr) {
               auto winner = std::get<0>(winnerTuple);
               auto entryId = std::get<1>(winnerTuple);
               auto winnerPrize = std::get<2>(winnerTuple);

               profile_index profiles(_self, _self.value);
               auto profileItr = profiles.find(winner);
               if (profileItr == profiles.end()) {
                  continue;
               }

               entries_index entries(_self, _self.value);
               auto entryItr = entries.find(entryId);
               if (entryItr == entries.end()) {
                  continue;
               }

               if (winnerPrize.amount > 0) { 
                  profiles.modify(profileItr, _self, [&](profile& row) {
                     if (row.winnings.amount > 0) {
                        row.winnings = row.winnings + winnerPrize;
                     } else {
                        row.winnings = winnerPrize;
                     }
                  });

                  entries.modify(entryItr, _self, [&](contestEntry& row) {
                     row.prizeGiven = winnerPrize;
                  });
               }
            }

            name feeacct(get_option(name{"feeacct"}));
            std::string feeacctmemo = get_option(name{"feeacctmemo"});
            print("feeacct: ", feeacct, ", memo: ", feeacctmemo, ", amount: ", prizeRemainder, "\n");
            if (prizeRemainder.amount > 0) {
               action{
                  permission_level{get_self(), name("active")},
                  name("eosio.token"),
                  name("transfer"),
                  std::make_tuple(get_self(), feeacct, prizeRemainder, feeacctmemo)
               }.send();
            }

            contestsByEndtime.modify(contestItr, _self, [&](contest& row) {
               row.paid = true;
            });

            hitBeginning = contestItr == contestsByEndtime.begin();
            if (!hitBeginning) {
               contestItr--;
            }
         }              
      }

      template <typename contestItrT>
      std::tuple<std::list<std::tuple<uint64_t, uint64_t, asset>>, asset> getContestWinners(contestItrT contestItr) {
         print("getContestWinners contest id: ", contestItr->id, "\n");
         entries_index entries(_self, _self.value);
         auto entriesByContest = entries.get_index<name("bycontest")>();
         auto contestEntriesItr = entriesByContest.lower_bound(contestItr->id);
         level_index levels(_self, _self.value);
         auto levelItr = levels.find(contestItr->levelId.value);

         symbol s(get_option(name{'currency'}), 4);

         asset contestPrize(0, s);
         std::map<uint64_t, std::list<std::tuple<uint64_t, uint64_t>>> winners;
         uint64_t votes = 0;

         if (contestItr->fixedPrize > 0) {
            contestPrize = asset{contestItr->fixedPrize, s};
         }

         // sum amount of all entry within contest & find winner(s)
         for (auto entryItr = contestEntriesItr; entryItr->contestId == contestItr->id && entryItr != entriesByContest.end(); entryItr++) {
            if (entryItr->block) { continue; }

            print("user: ", entryItr->userId, " votes: ", entryItr->votes, " amount: ", entryItr->amount, "\n");
            if (contestItr->fixedPrize == 0) {
               contestPrize += asset(entryItr->amount, s);
            }
            std::list<std::tuple<uint64_t, uint64_t>> winnersByVotes; 
            if(winners.find(entryItr->votes) != winners.end()) {
               winnersByVotes = winners[entryItr->votes];
               winnersByVotes.push_back(std::make_tuple(entryItr->userId.value, entryItr->id.value));
            } else {
               winnersByVotes = {std::make_tuple(entryItr->userId.value, entryItr->id.value)};
            }
            winners[entryItr->votes] = winnersByVotes;
         }

         print("level fee: ", levelItr->fee, "\n");
         check(levelItr->fee < 1000, "interval error: fee is too large, must be below 100%");
         asset feeAmount = contestPrize * levelItr->fee / 1000;
         if (contestItr->fixedPrize > 0) {
            feeAmount.set_amount(0);
         }
         asset winTotal = contestPrize - feeAmount;
         asset prizeRemainder = contestPrize;

         safeint totalWinnersWeight(0);

         auto rank = 1;
         auto prize = levelItr->prizes.begin();
         for(auto rankWinners = winners.rbegin(); rankWinners != winners.rend(); ++rankWinners) {
            if (rank > levelItr->prizes.size()) {
               break;
            }

            for (auto const& winner : rankWinners->second) {
               totalWinnersWeight = totalWinnersWeight + safeint{*prize};
            }

            ++rank;
            ++prize;
         }

         print("totalWinnersWeight: ", totalWinnersWeight.amount, ", winTotal: ", winTotal, ", fee: ", feeAmount, "\n");

         std::list<std::tuple<uint64_t, uint64_t, asset>> results;

         if (winTotal.amount > 0 && totalWinnersWeight > 0) {
            rank = 1;
            prize = levelItr->prizes.begin();
            for(auto rankWinners = winners.rbegin(); rankWinners != winners.rend(); ++rankWinners) {
               if (rank > levelItr->prizes.size()) {
                  break;
               }

               for (auto const& winnerRes : rankWinners->second) {
                  auto winner = std::get<0>(winnerRes);
                  auto entryId = std::get<1>(winnerRes);
                  safeint total = safeint{winTotal.amount} * safeint{*prize} / safeint{totalWinnersWeight};
                  asset winnerPrize(total.amount, s);
                  prizeRemainder -= winnerPrize;

                  results.push_back(std::make_tuple(winner, entryId, winnerPrize));
               }

               ++rank;
               ++prize;
            }
         }

         return std::make_tuple(results, prizeRemainder);
      }

      /*
         Re-check Entries marked as UnavailablePrice  - used within update
      */
      void checkUnavailablePriceEntries() {
         entries_index entries(_self, _self.value);
         auto entriesByNoPrice = entries.get_index<name("bynoprice")>();
         auto noPriceEntriesItr = entriesByNoPrice.lower_bound(true);

         int limitIndex = 0;
         auto entryItr = noPriceEntriesItr;
         while(entryItr != entriesByNoPrice.end() && limitIndex < 500) {
            auto thisEntryItr = entryItr; // prevent activate entry from resorting after modification
            limitIndex++;
            ++entryItr;
            activateEntry<decltype(entriesByNoPrice), decltype(thisEntryItr)>(entriesByNoPrice, thisEntryItr);
         }
      }

      /*
         Archive Contests
      */
      void archiveContests() {
         contest_index contests( _self, _self.value );
         auto contestsByEndtime = contests.get_index<name("byendtime")>();

         vote_index votes(_self, _self.value);
         auto votesByEntry = votes.get_index<name("byentryid")>();

         entries_index entries(_self, _self.value);
         auto entriesByContest = entries.get_index<name("bycontest")>();
         auto entriesByCreatedAt = entries.get_index<name("bycreatedat")>();

         uint64_t now = eosio::current_time_point().sec_since_epoch();
         uint64_t archSec = get_option_int(name{"entryarchsec"});

         int limitIndex = 0;
         int limitMax = 500;
         auto contestItr = contestsByEndtime.begin();
         while(contestItr != contestsByEndtime.end() && limitIndex < limitMax && now > contestItr->endtime() + archSec) {
            if (!contestItr->paid) continue;

            print("archiving contest ", contestItr->id, "\n");
            auto entryItr = entriesByContest.lower_bound(contestItr->id);

            while(entryItr != entriesByContest.end() && limitIndex < limitMax && entryItr->contestId == contestItr->id) {
               print("archiving entry ", entryItr->id, "\n");

               auto voteItr = votesByEntry.lower_bound(entryItr->id.value);
               while(voteItr != votesByEntry.end() && limitIndex < limitMax && voteItr->entryId == entryItr->id) {
                  print("archive vote ", voteItr->id, "\n");
                  voteItr = votesByEntry.erase(voteItr);
                  limitIndex++;
               }

               if (limitIndex < limitMax) {
                  print("archive entry ", entryItr->id, "\n");
                  entryItr = entriesByContest.erase(entryItr);
                  limitIndex++;
               }
            }

            if (limitIndex < limitMax) {
               print("archive contest ", contestItr->id, "\n");
               contestItr = contestsByEndtime.erase(contestItr);
               limitIndex++;
            }
         }

         auto entryItr2 = entriesByContest.begin();
         while(entryItr2 != entriesByContest.end() && entryItr2->contestId == 0 && limitIndex < limitMax && entryItr2->createdAt + (24 * 60 * 60) <= now) {
            if (entryItr2->contestId == 0 && entryItr2->amount == 0) {
               print("archive entry without contest ", entryItr2->id, "\n");
               entryItr2 = entriesByContest.erase(entryItr2);
               limitIndex++;
            } else {
               entryItr2++;
            }
         }
      }

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

      template <typename entriesT, typename entryItrT>
      bool activateEntry(entriesT& entries, entryItrT& entryItr) {      
         print("activate entry \n");
         if(entryItr == entries.end()) {
            print("Cannot activate entry: invalid entry");
            return false;
         }

         // ensure entry is not closed
         if(!entryItr->open) {
            print("Cannot activate entry: entry is closed.\n");
            return false;
         }

         // ensure entry is already assigned to contest
         if(entryItr->contestId != 0) {
            print("Entry already paid & assigned to contest.\n");
            return false;
         }

         uint32_t now = eosio::current_time_point().sec_since_epoch();

         // ensure entry is not expired
         uint64_t entryexpTime = get_option_int(name{"entryexp"});

         if (now > (safeint{entryItr->createdAt} + safeint{entryexpTime}).amount) {
            print("Entry is expired, please initiate refund to recieve money back.\n");
            entries.modify(entryItr, _self, [&](contestEntry& row) {
               row.priceUnavailable = false;
            });
            return false;
         }

         // get level interator
         level_index levels(_self, _self.value);
         auto levelItr = levels.find(entryItr->levelId.value);

         if (levelItr == levels.end()) {
            print("Error Creating Contest: could not find level with that id.", "\n");
            return false;
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
            && now <= curContestItr->votestarttime()
         );
         print("ae: test1");
         if (curContestValid) {
            contestPrice = curContestItr->price;
         } else {
            contestPrice = levelItr->price;
            if (levelItr->fixedPrize > 0) {
               auto prizefund = get_option_int(name{"prizefund"});
               check(prizefund >= usdToCurrencyAmount(levelItr->fixedPrize), "Not enough money in prize fund to pay out prize.");
            }
         }
         print("ae: test2");
         if (contestPrice != 0) {
            // determine eos price high since entry created
            curprice_index curprices(_self, _self.value);
            auto pricesByEndTime = curprices.get_index<name("byendtime")>();
            auto priceItr = pricesByEndTime.lower_bound(entryItr->createdAt);

            uint64_t priceHigh = 0;

            for (auto itr = priceItr; itr != pricesByEndTime.end(); itr++) {
               print("debug price high: ", itr->usdHigh, "\n");
               if(itr->usdHigh > priceHigh) {
                  priceHigh = itr->usdHigh;
               }
            }

            // mark entry as priceUnavailable if lastest currency price openTime + intervalSec is older than the set required price freshness
            uint64_t freshTime = get_option_int(name{"pricefresh"});
            auto lastPrice = --pricesByEndTime.end();

            bool freshPrice = (safeint{lastPrice->openTime} + safeint{lastPrice->intervalSec} + safeint{freshTime}).amount > now;
            print(
               "price fresh debug: freshPrice=", freshPrice,
               " lastEndTime=", (safeint{lastPrice->openTime} + safeint{lastPrice->intervalSec}).amount, 
               ", freshTime=", freshTime, " | ", (safeint{lastPrice->openTime} + safeint{lastPrice->intervalSec} + safeint{freshTime}).amount, " > ", now, 
               "\n"
            );
            if(priceHigh <= 0 || !freshPrice) {
               entries.modify(entryItr, _self, [&](contestEntry& row) {
                  row.priceUnavailable = true;
               });

               print("Currency Price Unavailable: run update action to recheck once price has been updated.\n");
               return false;
            }

            // fail if quantity is not enough
            print("debug price 1: ", priceHigh, " ", entryItr->amount, " ", contestPrice, "\n");
            // paid in cents
            auto paidAmt = (safeint{priceHigh} * safeint{entryItr->amount} / 1000000.0).amount;
            print("debug price 2: paidAmt: ¢", paidAmt, ", contestPrice: ¢", contestPrice, "\n");
            if (paidAmt < contestPrice) {
               print("Payment not enough only ¢", paidAmt,".\n");
               return false;
            }
         }

         if (curContestValid) {
            entries.modify(entryItr, _self, [&](contestEntry& row) {
               row.contestId = curContestItr->id;
               row.priceUnavailable = false;
            });
            byLevelIdx.modify(curContestItr, _self, [&](contest& row) {
               row.participantCount++;
            });

            print(entryItr->id, " activated with contest id of ", curContestItr->id, "\n");
            return true;
         } else {
            uint32_t levelContestCount = countOpenContestForLevel(entryItr->levelId);
            print("levelAllowedSimultaneousContests:", levelItr->allowedSimultaneousContests, "\n");
            print("levelContestCount:", levelContestCount, "\n");
            check(levelItr->allowedSimultaneousContests == 0 || levelContestCount < levelItr->allowedSimultaneousContests, "This level is full");

            safeint levelFixedPrizeCurrency = 0;
            if (levelItr->fixedPrize > 0) {
               auto prizefund = get_option_int(name{"prizefund"});
               levelFixedPrizeCurrency = usdToCurrencyAmount(levelItr->fixedPrize);
               prizefund = (safeint{prizefund} - levelFixedPrizeCurrency).amount;
               set_option(name{"prizefund"}, prizefund);
            }

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
               row.fixedPrize = levelFixedPrizeCurrency.amount;
               row.voteStartUTCHour = levelItr->voteStartUTCHour;
               row.paid = false;
            });

            if(curContestItr != byLevelIdx.end()) {
               byLevelIdx.modify(curContestItr, _self, [&](contest& row) {
                  row.submissionsClosed = 1;
               });
            }

            entries.modify(entryItr, _self, [&](contestEntry& row) {
               row.contestId = newContestId;
               row.priceUnavailable = false;
            });

            print(entryItr->id, " activated with contest id of ", newContestId, "\n");
            return true;
         }

         return false;
      }

      safeint usdToCurrencyAmount(uint32_t usd) {
         curprice_index curprices(_self, _self.value);
         auto pricesByEndTime = curprices.get_index<name("byendtime")>();
         auto priceItr = pricesByEndTime.rbegin();
         return (safeint{usd} * 1000000) / safeint{priceItr->usdHigh};
      }

      void set_option(name id, std::string value) {
         option_index options(_self, _self.value);
         auto optionItr = options.find(id.value);
         if (optionItr == options.end()) {
            options.emplace(_self, [&](option& row) {
               row.id = id;
               row.value = value;
            });
         } else {
            options.modify(optionItr, _self, [&](option& row) {
               row.value = value;
            });
         }
      }

      void set_option(name id, uint64_t value) {
         set_option(id, std::to_string(value));
      }

      std::string get_option(name id) {
         option_index options(_self, _self.value);
         auto optionItr = options.find(id.value);
         if (optionItr == options.end()) {
            return "";
         } else {
            return optionItr->value;
         }
      }

      uint64_t get_option_int(name id) {
         std::string str = get_option(id);
         if (str == "") { return 0; }
         return std::stoi(str);
      }

      void htmlspecialchars(std::string& data) {
         std::string buffer;
         buffer.reserve(data.size());
         for(size_t pos = 0; pos != data.size(); ++pos) {
            switch(data[pos]) {
                  case '&':  buffer.append("&amp;");       break;
                  case '\"': buffer.append("&quot;");      break;
                  case '\'': buffer.append("&apos;");      break;
                  case '<':  buffer.append("&lt;");        break;
                  case '>':  buffer.append("&gt;");        break;
                  default:   buffer.append(&data[pos], 1); break;
            }
         }
         data.swap(buffer);
      }

      void checkAndSanitizeLink(std::string& data) {
         if (data.length() == 0) { 
            return; 
         }

         bool isHttp = data.rfind("http:", 0) >= 0 || data.rfind("https:", 0) >= 0;
         check(isHttp, "Link must start with http or https");
         check(data.length() <= 2000, "Link is too long, must be 2000 characters or less");
         htmlspecialchars(data);
      }

      void checkAndSanitizeBio(std::string& data) {
         check(data.length() <= 150, "Bio is too long, must be 150 characters or less");
         htmlspecialchars(data);
      }

      char tolower(char c) {
         std::map<char, char> lowercaseMap({
            {'A', 'a'}, {'B', 'b'}, {'C', 'c'}, {'D', 'd'}, {'E', 'e'}, {'F', 'f'},
            {'G', 'g'}, {'H', 'h'}, {'I', 'i'}, {'J', 'j'}, {'K', 'k'}, {'L', 'l'}, {'M', 'm'}, {'N', 'n'},
            {'O', 'o'}, {'P', 'p'}, {'Q', 'q'}, {'R', 'r'}, {'S', 's'}, {'T', 't'}, {'U', 'u'}, {'V', 'v'},
            {'W', 'w'}, {'X', 'x'}, {'Y', 'y'}, {'Z', 'z'},
         });

         auto it = lowercaseMap.find(c);
         if(it == lowercaseMap.end()) {
            return c;
         }

         return it->second;
      }

      checksum256 hashUsername(std::string username) {
         std::transform(username.begin(), username.end(), username.begin(),
            [&](unsigned char c){ return tolower(c); });
         print("lowercase", username, "\n");
         return sha256(&username[0], username.size());
      }

      void checkUsernameExistsSingle(std::string username) {
         checksum256 usernameHash = hashUsername(username);
         profile_index profiles(_self, _self.value);
         auto byUsernameHashIdx = profiles.get_index<name("byusername")>();
         auto itr = byUsernameHashIdx.find(usernameHash);

         check(itr->usernameHash != usernameHash, "Username already exists.");
      }

      void checkUsernameExists(std::string username) {
         std::map<char, char> lookAlikeChars({
            {'l', 'I'},
            {'I', 'l'},
            {'O', '0'},
            {'0', 'O'},
         });

         checkUsernameExistsSingle(username);

         for (std::string::size_type i = 0; i < username.size(); i++) {
            auto it = lookAlikeChars.find(username[i]);
            if(it == lookAlikeChars.end()) {
               continue;
            }
            std::string lookAlike = username;
            lookAlike[i] = it->second;
            checkUsernameExistsSingle(lookAlike);
         }
      }

      uint32_t countOpenContestForLevel(name levelId) {
         auto now = eosio::current_time_point().sec_since_epoch();
         contest_index contests(_self, _self.value);
         auto contestByLevelAndStart = contests.get_index<name("bylevelstart")>();
         auto contestOpenItr = contestByLevelAndStart.upper_bound(composite_key(levelId.value, now));

         uint32_t levelContestCount = 0;
         auto itr = contestOpenItr;

         if (itr != contestByLevelAndStart.begin() && itr != contestByLevelAndStart.end()) {
            itr--;
         }

         if (contestOpenItr->levelId == levelId) {
            while(itr->endtime() >= now) {
               print("contest: id=", itr->id, " | endtime=", itr->endtime(), " | now=", now, "\n");
               if (itr->participantLimit == itr->participantCount) {
                  levelContestCount++;
               }

               if (itr == contestByLevelAndStart.begin()) {
                  break;
               }
               itr--;
            }
         }

         return levelContestCount;
      }
};
