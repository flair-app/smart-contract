#pragma once

#include <eosio/eosio.hpp>
#include <eosio/check.hpp>

#include <tuple>
#include <limits>

struct safeint {
    /**
     * The amount of the safeint
     */
    int64_t      amount = 0;

    /**
     * Maximum amount possible for this safeint. It's capped to 2^62 - 1
     */
    static constexpr int64_t max_amount    = (1LL << 62) - 1;

    safeint() {}

    /**
     * Construct a new safeint given the amount
     *
     * @param a - The amount of the safeint
     */
    safeint( int64_t a)
    :amount(a)
    {
        eosio::check( is_amount_within_range(), "magnitude of safeint amount must be less than 2^62" );
    }

    /**
     * Check if the amount doesn't exceed the max amount
     *
     * @return true - if the amount doesn't exceed the max amount
     * @return false - otherwise
     */
    bool is_amount_within_range()const { return -max_amount <= amount && amount <= max_amount; }

    /**
     * Check if the safeint is valid. %A valid safeint has its amount <= max_amount
     *
     * @return true - if the safeint is valid
     * @return false - otherwise
     */
    bool is_valid()const               { return is_amount_within_range(); }

    /**
     * Set the amount of the safeint
     *
     * @param a - New amount for the safeint
     */
    void set_amount( int64_t a ) {
        amount = a;
        eosio::check( is_amount_within_range(), "magnitude of safeint amount must be less than 2^62" );
    }

    /// @cond OPERATORS

    /**
     * Unary minus operator
     *
     * @return safeint - New safeint with its amount is the negative amount of this safeint
     */
    safeint operator-()const {
        safeint r = *this;
        r.amount = -r.amount;
        return r;
    }

    /**
     * Subtraction assignment operator
     *
     * @param a - Another safeint to subtract this safeint with
     * @return safeint& - Reference to this safeint
     * @post The amount of this safeint is subtracted by the amount of safeint a
     */
    safeint& operator-=( const safeint& a ) {
        amount -= a.amount;
        eosio::check( -max_amount <= amount, "subtraction underflow" );
        eosio::check( amount <= max_amount,  "subtraction overflow" );
        return *this;
    }

    /**
     * Addition Assignment  operator
     *
     * @param a - Another safeint to subtract this safeint with
     * @return safeint& - Reference to this safeint
     * @post The amount of this safeint is added with the amount of safeint a
     */
    safeint& operator+=( const safeint& a ) {
        amount += a.amount;
        eosio::check( -max_amount <= amount, "addition underflow" );
        eosio::check( amount <= max_amount,  "addition overflow" );
        return *this;
    }

    /**
     * Addition operator
     *
     * @param a - The first safeint to be added
     * @param b - The second safeint to be added
     * @return safeint - New safeint as the result of addition
     */
    inline friend safeint operator+( const safeint& a, const safeint& b ) {
        safeint result = a;
        result += b;
        return result;
    }

    /**
     * Subtraction operator
     *
     * @param a - The safeint to be subtracted
     * @param b - The safeint used to subtract
     * @return safeint - New safeint as the result of subtraction of a with b
     */
    inline friend safeint operator-( const safeint& a, const safeint& b ) {
        safeint result = a;
        result -= b;
        return result;
    }

    /**
     * Multiplication assignment operator, with a number
     *
     * @details Multiplication assignment operator. Multiply the amount of this safeint with a number and then assign the value to itself.
     * @param a - The multiplier for the safeint's amount
     * @return safeint - Reference to this safeint
     * @post The amount of this safeint is multiplied by a
     */
    safeint& operator*=( int64_t a ) {
        int128_t tmp = (int128_t)amount * (int128_t)a;
        eosio::check( tmp <= max_amount, "multiplication overflow" );
        eosio::check( tmp >= -max_amount, "multiplication underflow" );
        amount = (int64_t)tmp;
        return *this;
    }

    /**
     * Multiplication operator, with a number proceeding
     *
     * @brief Multiplication operator, with a number proceeding
     * @param a - The safeint to be multiplied
     * @param b - The multiplier for the safeint's amount
     * @return safeint - New safeint as the result of multiplication
     */
    friend safeint operator*( const safeint& a, int64_t b ) {
        safeint result = a;
        result *= b;
        return result;
    }


    /**
     * Multiplication operator, with a number preceeding
     *
     * @param a - The multiplier for the safeint's amount
     * @param b - The safeint to be multiplied
     * @return safeint - New safeint as the result of multiplication
     */
    friend safeint operator*( int64_t b, const safeint& a ) {
        safeint result = a;
        result *= b;
        return result;
    }

    /**
     * Multiplication operator, with a number preceeding
     *
     * @param a - safeint to be multiplied
     * @param b - safeint to be multiplied
     * @return safeint - New safeint as the result of multiplication
     */
    friend safeint operator*( const safeint& a, const safeint& b ) {
        safeint result = a;
        result *= b.amount;
        return result;
    }

    /**
     * @brief Division assignment operator, with a number
     *
     * @details Division assignment operator. Divide the amount of this safeint with a number and then assign the value to itself.
     * @param a - The divisor for the safeint's amount
     * @return safeint - Reference to this safeint
     * @post The amount of this safeint is divided by a
     */
    safeint& operator/=( int64_t a ) {
        eosio::check( a != 0, "divide by zero" );
        eosio::check( !(amount == std::numeric_limits<int64_t>::min() && a == -1), "signed division overflow" );
        amount /= a;
        return *this;
    }

    /**
     * Division operator, with a number proceeding
     *
     * @param a - The safeint to be divided
     * @param b - The divisor for the safeint's amount
     * @return safeint - New safeint as the result of division
     */
    friend safeint operator/( const safeint& a, int64_t b ) {
        safeint result = a;
        result /= b;
        return result;
    }

    /**
     * Division operator, with another safeint
     *
     * @param a - The safeint which amount acts as the dividend
     * @param b - The safeint which amount acts as the divisor
     * @return int64_t - the resulted amount after the division
     */
    friend int64_t operator/( const safeint& a, const safeint& b ) {
        eosio::check( b.amount != 0, "divide by zero" );
        return a.amount / b.amount;
    }

    /**
     * Equality operator
     *
     * @param a - The first safeint to be compared
     * @param b - The second safeint to be compared
     * @return true - if both safeint has the same amount
     * @return false - otherwise
     */
    friend bool operator==( const safeint& a, const safeint& b ) {
        return a.amount == b.amount;
    }

    /**
     * Inequality operator
     *
     * @param a - The first safeint to be compared
     * @param b - The second safeint to be compared
     * @return true - if both safeint doesn't have the same amount
     * @return false - otherwise
     */
    friend bool operator!=( const safeint& a, const safeint& b ) {
        return a.amount != b.amount;
    }

    /**
     * Less than operator
     *
     * @param a - The first safeint to be compared
     * @param b - The second safeint to be compared
     * @return true - if the first safeint's amount is less than the second safeint amount
     * @return false - otherwise
     */
    friend bool operator<( const safeint& a, const safeint& b ) {
        return a.amount < b.amount;
    }

    /**
     * Less or equal to operator
     *
     * @param a - The first safeint to be compared
     * @param b - The second safeint to be compared
     * @return true - if the first safeint's amount is less or equal to the second safeint amount
     * @return false - otherwise
     */
    friend bool operator<=( const safeint& a, const safeint& b ) {
        return a.amount <= b.amount;
    }

    /**
     * Greater than operator
     *
     * @param a - The first safeint to be compared
     * @param b - The second safeint to be compared
     * @return true - if the first safeint's amount is greater than the second safeint amount
     * @return false - otherwise
     */
    friend bool operator>( const safeint& a, const safeint& b ) {
        return a.amount > b.amount;
    }

    /**
     * Greater or equal to operator
     *
     * @param a - The first safeint to be compared
     * @param b - The second safeint to be compared
     * @return true - if the first safeint's amount is greater or equal to the second safeint amount
     * @return false - otherwise
     */
    friend bool operator>=( const safeint& a, const safeint& b ) {
        return a.amount >= b.amount;
    }

    /// @endcond
};
