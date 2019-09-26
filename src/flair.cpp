#include <eosio/eosio.hpp>
#include <eosio/print.hpp>
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

   private:
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
};
