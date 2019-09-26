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

   private:
      struct [[eosio::table]] category {
         name id;
         std::string name;
         bool archived;

         uint64_t primary_key() const { return id.value; }
      };

      typedef eosio::multi_index<"categories"_n, category> category_index;
};
