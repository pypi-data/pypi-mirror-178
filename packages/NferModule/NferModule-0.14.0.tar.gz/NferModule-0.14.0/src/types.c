/*
 * types.c
 *
 *  Created on: Jun 7, 2017
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

// we need float.h for the DBL constants...
#include <float.h>

#include "types.h"

/**
 * Returns the absolute value of a double, r.
 * Needed for the nearly_equals function below.
 **/
static double dabs(double r) {
    if (r < 0) {
        return -r;
    }
    return r;
}

/**
 * Returns the lesser of the two values.
 * Needed for the nearly_equals function below.
 **/
static double dmin(double a, double b) {
    if (a < b) {
        return a;
    }
    return b;
}

/**
 * Adapted from https://floating-point-gui.de nearlyEqual.
 * Two things to note:
 *   1) We ignore the guidance to provide an epsilon parameter, hard-coding a value.
 *      This isn't great!  But I don't want to provide a mechanism to give an epsilon in various APIs for now.
 *   2) We use double because that's the type used in the typed_value for reals.
 **/
static bool nearly_equals(double a, double b) {
    double abs_a = dabs(a);
    double abs_b = dabs(b);
    double diff  = dabs(a - b);
    double epsilon = 0.00001f;

    if (a == b) { // shortcut, handles infinities
        return true;

    } else if (a == 0 || b == 0 || ((abs_a + abs_b) < DBL_MIN)) {
        // a or b is zero or both are extremely close to it
        // relative error is less meaningful here
        return diff < (epsilon * DBL_MIN);
    } else { // use relative error
        return (diff / dmin((abs_a + abs_b), DBL_MAX)) < epsilon;
    }
}

/**
 * Returns true if the two typed values are equal(ish), false if not.
 * If the types are not equal, then the values are not considered
 * equal, even if they might be considered comparable (int/real).
 * For reals, equality uses the nearly_equals function.
 */
bool equals(typed_value *left, typed_value *right) {
    return (compare_typed_values(left, right) == 0);
}
/**
 * Compare two typed values, returning a value depending on their order.
 * Returns negative if left < right
 * Returns 0 if left == right
 * Returns positive if left > right
 */
int64_t compare_typed_values(typed_value *left, typed_value *right) {
    // if both are null pointers, then I suppose they're equal?
    if (left == NULL && right == NULL) {
        return 0;
    }

    // if one is a null pointer, though, then they're definitely not equal
    if (left == NULL) {
        // left < right
        return -1;
    } else if (right == NULL) {
        // left > right
        return 1;
    }

    // if their types aren't equal, then they aren't equal
    if (left->type != right->type) {
        // just subtract, which is fine since these are enums
        return (int64_t)left->type - (int64_t)right->type;
    }

    // types are equal
    switch(left->type) {
    case null_type:
        // both are null, so they are equal
        return 0;
        break;
    case boolean_type:
        // true > false -- subtraction is okay because these are just chars
        return left->value.boolean - right->value.boolean;
        break;
    case integer_type:
        // just compare the integer values
        return left->value.integer - right->value.integer;
        break;
    case real_type:
        // we have to be careful here that we don't get into trouble with reals
        if (nearly_equals(left->value.real, right->value.real)) {
            return 0;
        } else {
            if (left->value.real > right->value.real) {
                return 1;
            } else {
                return -1;
            }
        }
        break;
    case string_type:
        // just compare the string values, which are unsigned ints
        return (int)left->value.string - (int)right->value.string;
        break;
    case pointer_type:
        // just compare the pointer values - this shouldn't be used, actually
        return (((int64_t)left->value.pointer) - ((int64_t)right->value.pointer));
        break;
    }

    // provide a default case to make the compiler happy
    return 0;
}
// leave a blank line at the end...