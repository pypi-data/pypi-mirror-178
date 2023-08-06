/*
 * stack.c
 *
 *  Created on: Apr 29, 2017
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

#include <stdlib.h>

#include "log.h"
#include "stack.h"

/**
 * Set up a stack.
 * Must be called before a stack is used.
 * If dynamic memory is present, allocates some initial space.
 */
void initialize_stack(data_stack *stack) {
    stack->values = NULL;
#ifndef NO_DYNAMIC_MEMORY
    stack->values = malloc(sizeof(stack_value) * INITIAL_STACK_SPACE);
    if (stack->values != NULL) {
        stack->space = INITIAL_STACK_SPACE;
    }
#endif
    stack->tos = 0;
}

/**
 * Destroy an allocated stack.
 * Once initialize_stack has been called on a stack, destroy_stack 
 * must be called at some point before termination.
 * If dynamic memory is present this function is destructive.
 */
void destroy_stack(data_stack *stack) {
    // be safe around null pointers
    if (stack != NULL) {
        stack->space = 0;
        stack->tos = 0;
#ifndef NO_DYNAMIC_MEMORY
        if (stack->values != NULL) {
            free(stack->values);
            stack->values = NULL;
        }
#endif
    }
}

/**
 * Push a value (typed_value) onto the stack.
 * If the stack does not have enough room and dynamic memory is supported, 
 * it will be expanded.  If dynamic memory is not supported and there's
 * not enough room, the value will not be pushed.
 */
void push(data_stack *stack, stack_value *entry) {
#ifndef NO_DYNAMIC_MEMORY
    if (stack->tos >= stack->space) {
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "Growing stack %p from %u to %u\n", stack, stack->space, stack->space * 2);
        stack->values = realloc(stack->values, sizeof(stack_value) * stack->space * 2);

        if (stack->values != NULL) {
            stack->space = stack->space * 2;
        } else {
            stack->space = 0;
            stack->tos = 0;
            // bail out, since we failed to realloc
            return;
        }
    }
#endif

    if (stack->tos < stack->space) {
        stack->values[stack->tos].type = entry->type;
        switch(entry->type) {
        case null_type:
            stack->values[stack->tos].value.boolean = false;
            break;
        case boolean_type:
            stack->values[stack->tos].value.boolean = entry->value.boolean;
            break;
        case integer_type:
            stack->values[stack->tos].value.integer = entry->value.integer;
            break;
        case real_type:
            stack->values[stack->tos].value.real = entry->value.real;
            break;
        case string_type:
            stack->values[stack->tos].value.string = entry->value.string;
            break;
        case pointer_type:
            stack->values[stack->tos].value.pointer = entry->value.pointer;
            break;
        }
        stack->tos++;
    }
}

/**
 * Pop a (typed) value off the stack, copying it to the passed pointer.
 * If the stack is empty, the entry will be set to null.
 * This means the best way (right now) to tell if the stack
 * is empty when popping is to set the value argument to a different
 * data type, like Boolean.
 */
void pop(data_stack *stack, stack_value *entry) {
    if (stack->tos > 0) {
        stack->tos--;
        entry->type = stack->values[stack->tos].type;
        switch(entry->type) {
        case null_type:
            entry->value.boolean = false;
            break;
        case boolean_type:
            entry->value.boolean = stack->values[stack->tos].value.boolean;
            break;
        case integer_type:
            entry->value.integer = stack->values[stack->tos].value.integer;
            break;
        case real_type:
            entry->value.real = stack->values[stack->tos].value.real;
            break;
        case string_type:
            entry->value.string = stack->values[stack->tos].value.string;
            break;
        case pointer_type:
            entry->value.pointer = stack->values[stack->tos].value.pointer;
            break;
        }
    } else {
        entry->type = null_type;
        entry->value.boolean = false;
    }
}
