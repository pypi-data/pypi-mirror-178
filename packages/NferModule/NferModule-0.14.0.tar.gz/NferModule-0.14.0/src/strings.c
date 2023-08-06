/*
 * strings.c
 *
 *  Created on: May 15, 2018
 *      Author: skauffma
 *
 *    nfer - a system for inferring abstractions of event streams
 *   Copyright (C) 2017  Sean Kauffman
 *
 *   This file is part of nfer.
 *   nfer is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <stdint.h>
#include "types.h"
#include "strings.h"

/**
 * Copy the second string to the first up to the max_length.
 * Assumes C strings and stops if a null byte is encountered.
 * The maximum length does not include the null byte, also,
 * meaning that max_length should always be one less than the 
 * size of dest.
 * 
 * This function copies one byte at a time, which may not be
 * optimal on many architectures.  Consider improving this
 * at some point.
 */
void copy_string(char *dest, const char *src, size_t max_length) {
    size_t index;

    // max length does not include the terminating null char
    index = 0;

    while (index < max_length && src[index] != '\0') {
        dest[index] = src[index];
        index++;
    }

    dest[index] = '\0';
}

/**
 * Compare two strings for equality up to max_length.
 * If any difference is found before the strings terminate or max_length
 * is reached, then return false.  If the strings are equal up to 
 * max_length, even if they aren't yet terminated, return true.
 */
bool string_equals(const char *left, const char *right, int max_length) {
    int count;

    count = 0;
    while (count++ < max_length) {
        if (*left != *right) {
            return false;
        }
        if (*left == '\0') {
            return true;
        }
        left++;
        right++;
    }

    return true;
}

/**
 * Compute the length of a C string, up to some maximum.
 * Find the end of the passed string in bytes and return it.
 * If max_length is reached without finding a null byte
 * just return the max_length.
 */
int string_length(const char *str, int max_length) {
    int count;

    if (!str) {
        return 0;
    }

    count = 0;
    while (count < max_length && str[count] != '\0') {
        count++;
    }

    return count;
}

/**
 * Parse a string containing a number into an unsigned 64-bit int.
 * Takes the string to parse and a maximum length.
 * Parses the string one byte at a time.  If the max length is reached
 * or a character is found that is not in the ASCII number range, then
 * the function terminates, returning the number parsed so far.
 * Returns zero if the string is NULL or not an ASCII number.
 */
uint64_t string_to_u64(const char *str, int max_length) {
    int count;
    uint64_t result;

    result = 0;

    if (!str) {
        return result;
    }

    count = 0;
    // loop over the number, calculating the resulting int
    while (count < max_length && str[count] >= '0' && str[count] <= '9') {
        result = (result * 10) + (str[count] - '0');
        count++;
    }
    return result;
}

/**
 * Parse a string containing a number into a signed 64-bit int.
 * Takes the string to parse and a maximum length.
 * If the string begins with a '-' character, calls string_to_u64
 * and negates it.  If not, just calls string_to_u64.
 */
int64_t string_to_i64(const char *str, int max_length) {
    if (!str) {
        return (int64_t)0;
    }

    if (str[0] == '-') {
        return ((int64_t)string_to_u64(&str[1], max_length - 1)) * -1;
    } else {
        return (int64_t)string_to_u64(str, max_length);
    }
}

/**
 * Parses a string containing a number into a double.
 * Takes the string to parse and a maximum length.
 * Assumes the string contains only ASCII numbers, - and period (.),
 * where . delineates the whole and fractional part of the number.
 * Returns zero if the string is NULL or not a number.
 * If an unexpected character is encountered, returns the number
 * up to that point.
 */
double string_to_double(const char *str, int max_length) {
    int count;
    double result;
    short negate;
    int fraction;

    result = 0.0;

    if (!str) {
        return result;
    }

    count = 0;
    negate = 1;
    fraction = 0;

    // check for negative values
    if (str[count] == '-') {
        negate = -1;
        count++;
    }

    // loop over the number, calculating the resulting float
    while (count < max_length && ((str[count] >= '0' && str[count] <= '9') || (fraction == 0 && str[count] == '.'))) {
        // first check if we found a dot
        if (str[count] == '.') {
            fraction = 10;
        } else {
            // if we haven't reached a dot, treat it as an int
            if (fraction == 0) {
                result = (result * 10) + (str[count] - '0');
            } else {
                // if this is the fraction portion, treat it as such
                result = result + ((double)(str[count] - '0') / (double)(fraction));
                fraction = fraction * 10;
            }
        }
        count++;
    }

    // make sure to negate it if needed
    return result * negate;
}
