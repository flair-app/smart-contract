#include <eosio/eosio.hpp>
#include <eosio/print.hpp>
#include <eosio/crypto.hpp>
#include <string>

using namespace eosio;

class [[eosio::contract("flair")]] flair : public contract {
  public:
      using contract::contract;

      /*
         CREATE CATEGORY
      */
      [[eosio::action]]
      void createcat(name id,  std::string name) {
         require_auth( _self );

         category_index categories( _self, _self.value );

         categories.emplace(_self, [&](category& row) {
            row.id = id;
            row.name = name;
            row.archived = false;
         });
      }

      /*
         EDIT CATEGORY
      */
      struct editcatargs {
         std::string name;
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
         uint32_t maxVideoLength;
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
            row.maxVideoLength = params.maxVideoLength;
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
         uint32_t maxVideoLength;
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
            row.maxVideoLength = data.maxVideoLength;
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

         auto byUsernameHashIdx = profiles.get_index<"byusername"_n>();
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

   private:
      /*
         checkusername
      */
      bool checkusername(std::string username) {
         print("checkusername ", username, "\n");
         // cannot be under 6 char
         if (username.size() < 6) {
            print("Username cannot be less than 6 characters.", "\n");
            return false;
         }
         //check(username.size() >= 6, "Username cannot be less than 6 characters.");

         // cannot be over 30 char
         if (username.size() > 30) {
            print("Username cannot be more than 30 characters.", "\n");
            return false;
         }
         // check(username.size() <= 30, "Username cannot be more than 30 characters.");

         // only allow alphanumeric and dots (A-Z a-z 0-9 .)
         // std::regex reg("[\w.]+");
         // if (std::regex_match(username, reg)) {
         //    print("Username is limited to containing alphanumeric(A-Z a-z 0-9) and dots(.).");
         //    return false;
         // }
         // check(std::regex_match(username, reg), "Username is limited to containing alphanumeric(A-Z a-z 0-9) and dots(.).");

         // prevent starting or ending with dot
         if (username.front() == '.') {
            print("Username cannot start with a dot.", "\n");
            return false;
         }
         // check(username.front() != '.', "Username cannot start with a dot.");

         if (username.back() == '.') {
            print("Username cannot end with a dot.", "\n");
            return false;
         }
         // check(username.back() != '.', "Username cannot end with a dot.");

         // prevent double dots
         // std::regex doubleDotReg("(\.\.)");
         // if (std::regex_match(username, doubleDotReg)) {
         //    print("Username cannot contain double dots (..).");
         //    return false;
         // }
         // check(!std::regex_match(username, doubleDotReg), "Username cannot contain double dots (..).");

         print("checkusername valid", "\n");
         return true;
      }

      /*
         TABLE: categories
      */
      struct [[eosio::table]] category {
         name id;
         std::string name;
         bool archived;

         uint64_t primary_key() const { return id.value; }
      };

      typedef eosio::multi_index<"categories"_n, category> category_index;

      /*
         TABLE: levels
      */
      struct [[eosio::table]] level {
         name id;
         name categoryId;
         std::string name;
         bool archived;
         uint32_t maxVideoLength;
         uint32_t price;
         uint32_t participantLimit;
         uint32_t submissionPeriod;
         uint32_t votePeriod;

         uint64_t primary_key() const { return id.value; }
      };

      typedef eosio::multi_index<"levels"_n, level> level_index;

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
         "profiles"_n, 
         profile,
         indexed_by<"byusername"_n, const_mem_fun<profile, checksum256, &profile::by_username_hash>>
      > profile_index;
};
