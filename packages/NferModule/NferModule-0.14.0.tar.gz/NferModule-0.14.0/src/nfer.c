/*
 * nfer.c
 *
 *  Created on: Jan 19, 2017
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
#include <stdio.h>
#include <inttypes.h>

#include "nfer.h"
#include "dict.h"
#include "pool.h"
#include "stack.h"
#include "log.h"
#include "expression.h"
#include "memory.h"

#define PURGE_THRESHOLD 0.5

// We are using the hated global here, because there really is no reason why you would
// ever have different values in a process, and they are read only except from whatever
// user interface is being used
timestamp opt_window_size = NO_WINDOW;
bool opt_full = false;

#ifndef NO_DYNAMIC_MEMORY
void initialize_specification(nfer_specification *spec, unsigned int rule_space) {
    // initialize everything to zero
    spec->space = 0;
    spec->rules = NULL;
    spec->size = 0;
    // initialize label equivalence
    initialize_map(&spec->equivalent_labels);

    if (rule_space > 0) {
        spec->rules = (nfer_rule *) malloc(sizeof(nfer_rule) * rule_space);
        if (spec->rules != NULL) {
            spec->space = rule_space;
            clear_memory(spec->rules, sizeof(nfer_rule) * rule_space);
        }
    }
}
void destroy_specification(nfer_specification *spec) {
    rule_id i;
    nfer_rule *rule;
    map_iterator mit;
    map_key key;
    map_value value;

    // go through all the rules in the list and free the pools
    if (spec->rules != NULL) {

        for (i = 0; i < spec->size; i++) {
            rule = &spec->rules[i];

            destroy_pool(&rule->new_intervals);
            destroy_pool(&rule->left_cache);
            destroy_pool(&rule->right_cache);
            destroy_pool(&rule->produced);
            // support exclusion
            rule->exclusion = false;

            // support the dsl data structures
            destroy_expression_input(&rule->where_expression);
            destroy_expression_input(&rule->begin_expression);
            destroy_expression_input(&rule->end_expression);
            get_map_iterator(&rule->map_expressions, &mit);
            while(has_next_map_key(&mit)) {
                key = next_map_key(&mit);
                map_get(&rule->map_expressions, key, &value);
                if (value.type == pointer_type) {
                    destroy_expression_input((expression_input **)(&value.value.pointer));
                }
            }
            destroy_map(&rule->map_expressions);
            destroy_stack(&rule->expression_stack);
        }
        free(spec->rules);
        spec->rules = NULL;
    }
    spec->size = 0;
    spec->space = 0;
    // get rid of the equivalence map
    destroy_map(&spec->equivalent_labels);
}

/**
 * Move an nfer rule from one location to another.
 * This function is destructive, meaning that the src rule is unusable but can
 * be safely destroyed using the destroy_specification function. It also
 * overwrites anything in the dest rule without checking first.  This means
 * that the dest rule should NOT be initialized (via add, normally) prior
 * to calling this function.
 * 
 * This function handles expressions from the DSL by shallow copying the 
 * pointers and setting the src rule to NULL, which should be safe since
 * expression destruction checks for it.
 * The map expressions map is deep copied and the source is DESTROYED so
 * that the destroy_specification function doesn't go in and destroy the
 * still-referenced expression inputs.
 **/
void move_rule(nfer_rule *dest, nfer_rule *src) {
    // just go through in order of the struct
    // this part isn't destructive
    dest->op_code = src->op_code;
    dest->left_label = src->left_label;
    dest->right_label = src->right_label;
    dest->result_label = src->result_label;
    dest->exclusion = src->exclusion;
    // this is a pointer to a struct that is handled outside of nfer code
    dest->phi = src->phi;
    dest->hidden = src->hidden;
    // below is destructive
    dest->where_expression = src->where_expression;
    src->where_expression = NULL;
    dest->begin_expression = src->begin_expression;
    src->begin_expression = NULL;
    dest->end_expression = src->end_expression;
    src->end_expression = NULL;
    // be careful - src map needs destroyed so the expressions get left intact
    initialize_map(&dest->map_expressions);
    copy_map(&dest->map_expressions, &src->map_expressions, COPY_MAP_DEEP);
    destroy_map(&src->map_expressions);
    // below here we don't need to copy, just initialize
    // set up the pools
    initialize_pool(&dest->new_intervals);
    // note we don't have to do anything with the pool iterator
    initialize_pool(&dest->left_cache);
    initialize_pool(&dest->right_cache);
    initialize_pool(&dest->produced);
    // this only gets called in dynamic mode, so the expression stack can just
    // be initialized and it will be resized as needed
    initialize_stack(&dest->expression_stack);
    // clear the cycle root since we cannot know any longer if it's accurate
    dest->cycle_size = 0;
}
#endif // no dynamic memory

// nfer operators
static bool before(timestamp UNUSED(s1), timestamp e1, timestamp s2, timestamp UNUSED(e2)) {
    return e1 < s2;
}
static bool meet(timestamp UNUSED(s1), timestamp e1, timestamp s2, timestamp UNUSED(e2)) {
    return e1 == s2;
}
static bool during(timestamp s1, timestamp e1, timestamp s2, timestamp e2) {
    return s1 >= s2 && e1 <= e2;
}
static bool coincide(timestamp s1, timestamp e1, timestamp s2, timestamp e2) {
    return s1 == s2 && e1 == e2;
}
static bool start(timestamp s1, timestamp UNUSED(e1), timestamp s2, timestamp UNUSED(e2)) {
    return s1 == s2;
}
static bool finish(timestamp UNUSED(s1), timestamp e1, timestamp UNUSED(s2), timestamp e2) {
    return e1 == e2;
}
static bool overlap(timestamp s1, timestamp e1, timestamp s2, timestamp e2) {
    return s1 < e2 && s2 < e1;
} // also used for slice

// exclusion operators
static bool after(timestamp s1, timestamp UNUSED(e1), timestamp UNUSED(s2), timestamp e2)  {
    return s1 > e2;
}
static bool follow(timestamp s1, timestamp UNUSED(e1), timestamp UNUSED(s2), timestamp e2) {
    return s1 == e2;
}
static bool contain(timestamp s1, timestamp e1, timestamp s2, timestamp e2) {
    return s2 >= s1 && e2 <= e1;
}

// start and end time functions
static timestamp start_end_1(timestamp t1, timestamp UNUSED(t2)) {
    return t1;
}
static timestamp start_end_2(timestamp UNUSED(t1), timestamp t2) {
    return t2;
}
static timestamp start_end_min(timestamp t1, timestamp t2) {
    if (t1 < t2) {
        return t1;
    } else {
        return t2;
    }
}
static timestamp start_end_max(timestamp t1, timestamp t2) {
    if (t1 > t2) {
        return t1;
    } else {
        return t2;
    }
}
/**********
 * Nfer operators as predefined, including negations
 **********/
nfer_operator operators[] = {
        { "also", NULL, start_end_1, start_end_1, false }, // default to using ends from the left-hand interval, since also is used for atomic rules
        { "before", before, start_end_1, start_end_2, false },
        { "meet", meet, start_end_1, start_end_2, false },
        { "during", during, start_end_2, start_end_2, false },
        { "coincide", coincide, start_end_1, start_end_2, false },
        { "start", start, start_end_1, start_end_max, false },
        { "finish", finish, start_end_min, start_end_2, false },
        { "overlap", overlap, start_end_min, start_end_max, false },
        { "slice", overlap, start_end_max, start_end_min, false },
        // negations
        { "after", after, start_end_1, start_end_1, true },
        { "follow", follow, start_end_1, start_end_1, true },
        { "contain", contain, start_end_1, start_end_1, true }
};

/**
 * Add a rule to the specification, returning a pointer to the rule for further setup.
 * This allocates space in the specification, sets up some initial settings, intitializes some
 * pointers, and generally makes the rule safe to use.  It does not do a lot of the work
 * for the caller, though, who will need to manually used the returned pointer to set up
 * the rest of the data structure.  This is maybe not ideal and should be modified, but 
 * for now it works well enough and makes testing easier.
 */
nfer_rule * add_rule_to_specification(
        nfer_specification *spec,
        label result_label_index, 
        label left_label_index, 
        operator_code op_code, 
        label right_label_index, 
        phi_function *phi) {

    nfer_rule *rule = NULL, *new_rules;
    rule_id id = MISSING_RULE_ID;

#ifndef NO_DYNAMIC_MEMORY
    // check to make sure there is room...
    if (spec->space <= spec->size) {
        filter_log_msg(LOG_LEVEL_DEBUG, "Not enough space for rule (%u <= %u), allocating more.\n", spec->space, spec->size);

        // there isn't enough room.  Allocate more.
        if (spec->rules == NULL) {
            // we have to now consider when nothing has been allocated yet
            new_rules = malloc(sizeof(nfer_rule) * RULE_LIST_SIZE_ON_EMPTY);
            if (new_rules != NULL) {
                spec->rules = new_rules;
                spec->space = RULE_LIST_SIZE_ON_EMPTY;
                // clear the memory
                clear_memory(spec->rules, sizeof(nfer_rule) * spec->space);
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Couldn't allocate new memory for rule!\n");
            }
        } else {
            new_rules = realloc(spec->rules, sizeof(nfer_rule) * spec->space * 2);
            if (new_rules != NULL) {
                spec->rules = new_rules;
                spec->space = spec->space * 2;
                // clear anything above size to the end
                clear_memory(spec->rules + spec->size, sizeof(nfer_rule) * (spec->space - spec->size));
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Couldn't allocate new memory for rule!\n");
            }
        }
    }
#endif
    if (spec->rules != NULL && spec->size < spec->space) {
        id = spec->size;
        rule = &spec->rules[id];

        // initialize the pools
        initialize_pool(&rule->new_intervals);
        initialize_pool(&rule->left_cache);
        initialize_pool(&rule->right_cache);
        initialize_pool(&rule->produced);

        // set the operator
        if (op_code > 0 && op_code < N_OPERATORS) {
            rule->op_code = op_code;
            rule->exclusion = operators[op_code].exclusion;
        } else {
            // default to also
            rule->op_code = ALSO_OPERATOR;
            rule->exclusion = false;
        }

        // set phi function
        rule->phi = phi;

        // set all the fields for DSL support to empty by default
        // default to not being hidden
        rule->hidden = false;
        rule->where_expression = NULL;
        rule->begin_expression = NULL;
        rule->end_expression = NULL;
        rule->map_expressions = EMPTY_MAP;
        initialize_stack(&rule->expression_stack);

        // clear the cycle root - this will be set by setup_rule_order
        rule->cycle_size = 0;

        // then set the common fields
        rule->left_label = left_label_index;
        rule->right_label = right_label_index;
        rule->result_label = result_label_index;

        // increment the size
        spec->size++;
    }

    return rule;
}

/**
 * Checks if a label has been subscribed to by a specification
 */
bool is_subscribed(nfer_specification *spec, label name) {
    rule_id i;
    nfer_rule *rule;

    // as there is no longer a subscription data structure, we have to iterate
    for (i = 0; i < spec->size; i++) {
        rule = &spec->rules[i];
        if (rule->left_label == name || rule->right_label == name) {
            return true;
        }
    }

    return false;
}

/**
 * Checks if a label may be published by a specification
 */
bool is_published(nfer_specification *spec, label name) {
    rule_id i;
    nfer_rule *rule;

    for (i = 0; i < spec->size; i++) {
        rule = &spec->rules[i];
        if (rule->result_label == name && !rule->hidden) {
            return true;
        }
    }
    return false;
}

/**
 * Checks if a map key is produced by any rules in the specification
 */
bool is_mapped(nfer_specification *spec, map_key key) {
    rule_id i;
    nfer_rule *rule;

    for (i = 0; i < spec->size; i++) {
        rule = &spec->rules[i];
        // skip hidden rules and look for the key
        if (!rule->hidden && map_has_key(&rule->map_expressions, key)) {
            return true;
        }
    }

    return false;
}

/**
 * Remove any non-minimal intervals from the pool of potential new intervals.
 * This function implements the minimality selection function.  It takes two pools, the first
 * is the new potential intervals and the second is the already produced intervals from previous
 * calls of apply_rule.
 * 
 * The function removes intervals from the potential pool in the following cases:
 * 1) There is an interval in the prior pool with equal or smaller timestamps
 * 2) There is an interval in the potentials pool with equal or smaller timestamps
 * 
 * Technically, case 2 treat strictly smaller or equal timestamps differently and, in the
 * case of equal timestamps, compare the maps to ensure the choice is deterministic. 
 * In practice, this does not really matter and we just keep whatever one is produced later.
 */
#ifndef TEST
static
#endif
void select_minimal(pool *potentials, pool *prior) {
    interval *new, *old;
    pool_iterator new_pit, old_pit;
    bool removed;

    if (potentials->size > 0) {
        // perform a minimality check
        get_pool_iterator(potentials, &new_pit);
        while (has_next_interval(&new_pit)) {
            new = next_interval(&new_pit);
            removed = false;

            // first check against the other potentials
            get_pool_iterator(potentials, &old_pit);
            while (has_next_interval(&old_pit)) {
                old = next_interval(&old_pit);
                if (old != new) {
                    if (old->start >= new->start && old->end <= new->end) {
                        // remove the candidate
                        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Removing non-minimal interval (%d,%" PRIu64 ",%" PRIu64 ") due to conflict in new pool (%d,%" PRIu64 ",%" PRIu64 ")\n", new->name, new->start, new->end, old->name, old->start, old->end);
                        remove_from_pool(&new_pit);
                        removed = true;
                        break;
                    }
                }
            }

            // then check against the prior intervals
            // skip it if we already removed
            if (!removed) {
                get_pool_iterator(prior, &old_pit);
                while (has_next_interval(&old_pit)) {
                    old = next_interval(&old_pit);
                    if (old->start >= new->start && old->end <= new->end) {
                        // remove the candidate
                        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Removing non-minimal interval (%d,%" PRIu64 ",%" PRIu64 ") due to conflict in prior pool (%d,%" PRIu64 ",%" PRIu64 ")\n", new->name, new->start, new->end, old->name, old->start, old->end);
                        remove_from_pool(&new_pit);
                        break;
                    }
                }
            }
        }
    } // if potentials is non-empty
}

/**
 * Given a rule and two intervals, return true if the rule matches those intervals.
 * This function checks all constraints, both temporal and data, to determine if the
 * two passed intervals match.
 * 
 * All of the constraints must match (conjunction) for the function to return true.
 * The constaints may be:
 * 1) the operator (temporal)
 * 2) a C (phi) function (deprecated)
 * 3) a where expression from the DSL (data + temporal)
 * 
 * This function is used for both inclusive and exclusive rules: for inclusive rules,
 * a match means a new interval should be produced and for exclusive rules, it means
 * a new interval should _not_ be produced.
 * 
 * In the case of an atomic rule, the caller should pass the left-hand-side interval
 * for both the lhs and rhs parameters.
 */
#ifndef TEST
static
#endif
bool interval_match(nfer_rule *rule, interval *lhs, interval *rhs) {
    nfer_operator *op;
    bool op_succeeded, phi_succeeded;
    typed_value where_succeeded;

    // we should be able to safely assume that there is an op_code
    op = &operators[rule->op_code];
    op_succeeded = true;
    // if there is a test function, use it, otherwise default to true
    if (op->test != NULL) {
        // test the operator to see if it is met
        op_succeeded = op->test(lhs->start, lhs->end, rhs->start, rhs->end);
    }

    // if there's a phi function, test it, otherwise default to success
    phi_succeeded = true;
    if (rule->phi != NULL && rule->phi->test != NULL) {
        phi_succeeded = rule->phi->test(lhs->start, lhs->end, &lhs->map, rhs->start, rhs->end, &rhs->map);
    }

    // if there is a where clause from the DSL, use it, otherwise default to success
    where_succeeded.type = boolean_type;
    where_succeeded.value.boolean = true;

    if (rule->where_expression != NULL) {
        evaluate_expression(rule->where_expression, &where_succeeded, &rule->expression_stack,
                lhs->start, lhs->end, &lhs->map,
                rhs->start, rhs->end, &rhs->map);
    }

    // the op, phi, and where clause must all succeed to match an interval
    // We're just using the boolean value of where_succeeded without type checking at runtime
    // we assume that static type checking worked.
    return op_succeeded && phi_succeeded && where_succeeded.value.boolean;
}

/**
 * Given a rule and the two intervals it matches, produce the new begin and end timestamps.
 * This function generates the new timestamps for produced intervals by either using the operator
 * or evaluating the begin and end expressions from the DSL.
 * 
 * When used to generate timestamps for an atomic or exclusive rule (where there is no right-hand-side)
 * interval, the caller should pass the left-hand-side interval for both the lhs and rhs parameters.
 * 
 * This function uses the non-threadsafe rule->expression_stack for expression evaluation.
 */
#ifndef TEST
static
#endif
void set_end_times(nfer_rule *rule, interval *lhs, interval *rhs, interval *result) {
    typed_value time_result;
    nfer_operator *op;
    op = &operators[rule->op_code];

    // begin and end expressions from the DSL override operator begin and end times
    if (rule->begin_expression != NULL) {
        evaluate_expression(rule->begin_expression, &time_result, &rule->expression_stack,
                lhs->start, lhs->end, &lhs->map,
                rhs->start, rhs->end, &rhs->map);
        if (time_result.type == real_type) {
            result->start = (timestamp)time_result.value.real;
        } else {
            // this is relying on static type checking from the DSL to work, otherwise we could get some randomness
            result->start = time_result.value.integer;
        }
    } else {
        // semantic analysis should guarantee that this is not null
        result->start = op->start_time(lhs->start, rhs->start);
    }
    if (rule->end_expression != NULL) {
        evaluate_expression(rule->end_expression, &time_result, &rule->expression_stack,
                lhs->start, lhs->end, &lhs->map,
                rhs->start, rhs->end, &rhs->map);
        if (time_result.type == real_type) {
            result->end = (timestamp)time_result.value.real;
        } else {
            // this is relying on static type checking from the DSL to work, otherwise we could get some randomness
            result->end = time_result.value.integer;
        }
    } else {
        // semantic analysis should guarantee that this is not null
        result->end = op->end_time(lhs->end, rhs->end);
    }
}

/**
 * Given a rule and the two intervals it matches, produce a new map by applying whatever map function.
 * This function generates the new maps for produced intervals by either calling C code (deprecated)
 * or evaluating the map expression from the DSL.
 * 
 * When used to generate a map for an atomic or exclusive rule (where there is no right-hand-side)
 * interval, the caller should pass the left-hand-side interval for both the lhs and rhs parameters.
 * 
 * This function uses the non-threadsafe rule->expression_stack for map expression evaluation.
 */
#ifndef TEST
static
#endif
void set_map(nfer_rule *rule, interval *lhs, interval *rhs, data_map *result) {
    map_iterator mit;
    map_key key_to_set;
    map_value map_expression, value_to_set;

    // if there's a phi function, use it first
    if (rule->phi != NULL && rule->phi->result != NULL) {
        // if the phi function exists
        // use it to set the map and then add
        rule->phi->result(result, lhs->start, lhs->end, &lhs->map, rhs->start, rhs->end, &rhs->map);
    }

    // if there are map expressions from the DSL, use them
    get_map_iterator(&rule->map_expressions, &mit);
    while (has_next_map_key(&mit)) {
        key_to_set = next_map_key(&mit);
        map_get(&rule->map_expressions, key_to_set, &map_expression);

        // it should (must) be a pointer to an expression_input
        evaluate_expression((expression_input *)map_expression.value.pointer, &value_to_set, &rule->expression_stack,
                lhs->start, lhs->end, &lhs->map,
                rhs->start, rhs->end, &rhs->map);
        // set the key to whatever was returned
        map_set(result, key_to_set, &value_to_set);
    }
}

/**
 * Implements the window optimization by discarding intervals from a pool with an end timestamp below the cutoff.
 * The idea is to pass a pool to this function and it will iterate over the intervals therein and remove any
 * that are too old.
 * 
 * If the number of intervals removed represents too high of a proportion of the total amount of allocated
 * storage then the pool will be purged.
 */
#ifndef TEST
static
#endif
void discard_older_events(pool *cache, timestamp cutoff) {
    pool_iterator pit;
    interval *i;

    get_pool_iterator(cache, &pit);
    while (has_next_interval(&pit)) {
        i = next_interval(&pit);
        if (i->end < cutoff) {
            remove_from_pool(&pit);
        }
    }
    // above some threshold, purge the pool to free up space
    // the threshold is if the number of removed items is at least some percent of the total size
    // purge_pool is O(n), so this isn't too expensive.  Maybe try decreasing the threshold.
    if ((float)cache->removed / (float)cache->size > PURGE_THRESHOLD) {
        filter_log_msg(LOG_LEVEL_INFO, "Purging pool %x due to removed reaching threshold %f\n", cache, PURGE_THRESHOLD);
        purge_pool(cache);
    }
}

/**
 * Apply a rule to an input pool, producing an output pool.
 * This matches the R[] semantics given in various papers defining the nfer language.
 * Previous versions of the tool organized the work differently because the focus was on monitoring and
 * there was an assumption that mostly intervals would be added one at a time.
 * This version takes a rule and a pool as inputs and populates a pool as outputs.
 * 
 * precondition: rule->input_queue must have been intialized to point at the
 * first interval in input_pool that has not yet been handled by this rule.
 **/
void apply_rule(nfer_rule *rule, pool_iterator *input_queue, pool *output_pool, data_map *equivalent_labels) {
    interval *rhs, *lhs, *new, *accepted;
    pool_iterator left_pit, right_pit, new_pit;
    bool exclude;
    timestamp window_cutoff, latest_window_cutoff;
    interval *add;
    // for iterating over the new intervals in each cache
    pool_iterator new_left_queue, new_right_queue;

    // clear the potential new interval pool
    // we need to do this at the beginning - unfortunately we can't find out if this 
    // work can be skipped because the pool may have arbitrary numbers of intervals
    clear_pool(&rule->new_intervals);

    // set window cutoff initial values
    window_cutoff = 0;
    // this is used at the end of the function to prune the produced pool if 
    // windowing is enabled
    latest_window_cutoff = 0;

    // this is the main idea of the algorithm here which attempts to capture the fact
    // that there may be more than one interval in the input pool that may change
    // specifically what happens with exclusive rules.
    // 1. get pool queues from the ends of both left and right caches
    //    -- these will be used to iterate over the new intervals
    // 2. add the new intervals to either/both cache if the label matches
    // 3. use the queue to iterate over the new intervals in the left cache
    //    -- the crucial difference here from just using the input pool to iterate
    //       is that the other cache already has the new intervals in it
    //    -- HOWEVER to avoid duplicates we want to make sure that we don't check
    //       the new intervals in the right cache unless it's an exclusive rule.
    //       This avoids double counting.  For exclusive rules we don't iterate
    //       over the right cache, so we don't avoid them here.
    // 4. use the queue to iterate over the new intervals in the right cache
    // 5. do any filtering or copying needed to eliminate, for example, non-minimal intervals


    // the first part of this function iterates over the new intervals in input_pool
    // importantly, we treat the pool as a queue here - we get the intervals that have been
    // added since the last time this rule was called.
    // ALSO, crucially, the input_queue has to have been initialized already.

    // first initialize the queues for the left and right caches
    get_pool_queue(&rule->left_cache, &new_left_queue, QUEUE_FROM_END);
    get_pool_queue(&rule->right_cache, &new_right_queue, QUEUE_FROM_END);
    // now copy the intervals from the input into those queues
    while(has_next_queue_interval(input_queue)) {
        add = next_queue_interval(input_queue);
        if (should_log(LOG_LEVEL_SUPERDEBUG)) {
            log_msg("    Adding interval to rule (%d,%" PRIu64 ",%" PRIu64 ",", add->name, add->start, add->end);
            log_map(&add->map);
            log_msg(")\n");
        }
        if (add->name == rule->left_label) {
            add_interval(&rule->left_cache, add);
        }
        if (add->name == rule->right_label) {
            add_interval(&rule->right_cache, add);
        }
    }

    // now we can iterate over the new intervals in the left cache
    while (has_next_queue_interval(&new_left_queue)) {
        add = next_queue_interval(&new_left_queue);

        // pre-compute because we need to check if it's the latest
        if (opt_window_size != NO_WINDOW && add->end > opt_window_size) {
            window_cutoff = add->end - opt_window_size;
            if (window_cutoff > latest_window_cutoff) {
                latest_window_cutoff = window_cutoff;
            }
        }

        // handle exclusions first
        if (rule->exclusion) {
            exclude = false;
            // go through the rhs cache to see if something has occurred to negate this interval
            get_pool_iterator(&rule->right_cache, &right_pit);
            while (has_next_interval(&right_pit)) {
                rhs = next_interval(&right_pit);
                filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Checking exclusion rhs [%" PRIu64 ",%" PRIu64 "]\n", rhs->start, rhs->end);

                // if a window is used, remove the interval if it is too old
                if (opt_window_size != NO_WINDOW) {
                    if (rhs->end < window_cutoff) {
                        remove_from_pool(&right_pit);
                        continue;
                    }
                }

                // check the exclusion conditions just like any other operator
                if (interval_match(rule, add, rhs)) {
                    // if we get here, check for equality between the two intervals
                    // we do not want an interval to exclude itself!
                    if (!equal_intervals(add, rhs, equivalent_labels)) {
                        // if the conditions hold, exclude the match
                        exclude = true;

                        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Exclusion matched: included lhs [%" PRIu64 ",%" PRIu64 "] excluded rhs [%" PRIu64 ",%" PRIu64 "]\n", add->start, add->end, rhs->start, rhs->end);

                        // we don't need to continue iterating over the rhs since we know we'll exclude
                        break;
                    }
                }
            }
            // the interval is not negated
            if (!exclude) {
                // get a new interval from the new_intervals pool
                new = allocate_interval(&rule->new_intervals);

                // set the end times using the helper function
                // use add as the rhs as semantic analysis should guarantee it doesn't matter
                set_end_times(rule, add, add, new);
                new->name = rule->result_label;

                // again, add is rhs and it doesn't matter
                set_map(rule, add, add, &new->map);
            }

        } else { // not an exclusion

            // if this isn't an atomic rule
            if (rule->right_label != WORD_NOT_FOUND) {
                // go through the rhs cache for matches
                get_pool_iterator(&rule->right_cache, &right_pit);
                while (has_next_interval(&right_pit)) {

                    // Don't go past the where the new intervals start on the rhs!
                    // If we do we'll double count everything.
                    // We do want to go past for exclusive rules so we are sure to exclude 
                    // everything - this works because we skip exclusive rules when iterating
                    // the rhs cache.
                    // IMPORTANT: this relies on the cache not being sorted or purged!
                    // if the cache were to be purged it could change the indices and break 
                    // the comparison
                    if (interval_added_after(&right_pit, &new_right_queue)) {
                        // break this while loop over the right cache
                        break;
                    }


                    rhs = next_interval(&right_pit);
                    filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Checking inclusion rhs [%" PRIu64 ",%" PRIu64 "]\n", rhs->start, rhs->end);

                    // if a window is used, remove the interval if it is too old
                    if (opt_window_size != NO_WINDOW) {
                        if (rhs->end < window_cutoff) {
                            remove_from_pool(&right_pit);
                            continue;
                        }
                    }

                    // the op, phi, and where clause must all succeed to match an interval
                    if (interval_match(rule, add, rhs)) {
                        // get a new interval from the new_intervals pool
                        new = allocate_interval(&rule->new_intervals);

                        // set the end times using the helper function
                        set_end_times(rule, add, rhs, new);
                        new->name = rule->result_label;

                        set_map(rule, add, rhs, &new->map);
                    }
                } // for right_cache

            } else {
                // this is an atomic rule, so just test
                // set rhs to add just to it doesn't segfault -- the values shouldn't matter
                if (interval_match(rule, add, add)) {
                    // get a new interval from the new_intervals pool
                    new = allocate_interval(&rule->new_intervals);

                    // set the end times using the helper function
                    // again use add as the rhs, again it shouldn't matter
                    set_end_times(rule, add, add, new);

                    new->name = rule->result_label;

                    // again, add is rhs and it doesn't matter
                    set_map(rule, add, add, &new->map);
                }
            }
        } // end of inclusion rule for lhs match

    } // end of iterating over the new left side matches

    // now iterate over the new rules in the right side cache
    while (has_next_queue_interval(&new_right_queue)) {
        add = next_queue_interval(&new_right_queue);

        // pre-compute because we need to check if it's the latest
        if (opt_window_size != NO_WINDOW && add->end > opt_window_size) {
            window_cutoff = add->end - opt_window_size;
            if (window_cutoff > latest_window_cutoff) {
                latest_window_cutoff = window_cutoff;
            }
        }

        // skip this rhs match if the rule is a negation
        if (!rule->exclusion) {

            // go through the lhs cache for matches
            get_pool_iterator(&rule->left_cache, &left_pit);
            while (has_next_interval(&left_pit)) {
                lhs = next_interval(&left_pit);
                filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Checking lhs [%" PRIu64 ",%" PRIu64 "]\n", lhs->start, lhs->end);

                // if a window is used, remove the interval if it is too old
                if (opt_window_size != NO_WINDOW) {
                    if (lhs->end < window_cutoff) {
                        remove_from_pool(&left_pit);
                        continue;
                    }
                }

                // the op, phi, and where clause must all succeed to match an interval
                if (interval_match(rule, lhs, add)) {
                    // get a new interval from the new_intervals pool
                    new = allocate_interval(&rule->new_intervals);

                    // set the end times using the helper function
                    set_end_times(rule, lhs, add, new);
                    new->name = rule->result_label;

                    set_map(rule, lhs, add, &new->map);
                }
            } // for left_cache
        } // rule is not exclusion

    } // end of the loop over the new intervals in the right cache

    // check if we need to purge the caches
    if (opt_window_size != NO_WINDOW) {
        // above some threshold, purge the pool to free up space
        // the threshold is if the number of removed items is at least some percent of the total size
        // purge_pool is O(n), so this isn't too expensive.  Maybe try decreasing the threshold.
        if ((float)(rule->left_cache.removed) / (float)(rule->left_cache.size) > PURGE_THRESHOLD) {
            filter_log_msg(LOG_LEVEL_INFO, "Purging left cache of rule %x due to removed reaching threshold %f\n", rule, PURGE_THRESHOLD);
            purge_pool(&rule->left_cache);
        }
        if ((float)(rule->right_cache.removed) / (float)(rule->right_cache.size) > PURGE_THRESHOLD) {
            filter_log_msg(LOG_LEVEL_INFO, "Purging right cache of rule %x due to removed reaching threshold %f\n", rule, PURGE_THRESHOLD);
            purge_pool(&rule->right_cache);
        }
    }

    // skip this work if not testing for minimality
    if (!opt_full) {
        // before testing minimality, if a window is used, remove anything from the produced pool that is too old
        // if there's no minimality checking, then the produced pool is empty
        // also, if latest is set to 0 then there's no point in calling this
        if (opt_window_size != NO_WINDOW && latest_window_cutoff > 0) {
            discard_older_events(&rule->produced, latest_window_cutoff);
        }

        // now check for minimality and remove anything that isn't
        select_minimal(&rule->new_intervals, &rule->produced);
    }
    // finally add anything left to the produced pool, and to the output if the rule isn't hidden
    // TODO: figure out if we should just build new intervals in output and then remove/hide them 
    // alternatively we could do this in produced!  It may be worth trying to figure out how to 
    // even share somehow between the two pools.
    get_pool_iterator(&rule->new_intervals, &new_pit);
    while(has_next_interval(&new_pit)) {
        accepted = next_interval(&new_pit);
        /* set the hidden flag */
        accepted->hidden = rule->hidden;

        // skip adding to the produced pool if not using minimality
        if (!opt_full) {
            add_interval(&rule->produced, accepted);
        }
        
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Adding interval to output pool (%d,%" PRIu64 ",%" PRIu64 ")\n", accepted->name, accepted->start, accepted->end);
        add_interval(output_pool, accepted);
    }
}

/**
 * Apply a list of rules (a partial specification) one time to an input pool to produce an output pool.
 * Each rule, applied in order, is passed both the original input and the output from previous 
 * rule applications.
 * The input pool should contain the new intervals to add while the output pool may contain anything.
 * Both pools will be augmented with the produced intervals.
 * 
 * This is equivalent to the S[] function from nfer semantics.
 * 
 * Crucially, the function will modify both the input and output pools, with both having the 
 * same intervals added with the exception of the final rule output which does not need to be
 * added to the input.  The reason for this is that each rule gets the union of the input 
 * and the already produced intervals as its input.
 * 
 * The rules are passed in the spec along with the start and ending indices of the rules to apply.
 * This is done so that sub-specifications can be run.  The spec is passed instead of just the
 * rule list so we have access to any metadata stored at the spec level.
 * 
 * Assumes the rule list and input pool are non-empty.
 * 
 */
void apply_rule_list(nfer_specification *spec, rule_id start_id, rule_id end_id, pool *input_pool, pool *output_pool) {
    rule_id id;
    nfer_rule *rule;
    pool_iterator output_queue;
    interval *to_copy;

    // iterate over the rules, applying them to the input
    // note that end_id might equal start_id
    for (id = start_id; id <= end_id; id++) {
        rule = &spec->rules[id];

        // set up the queue on output_pool
        // this will be used to copy intervals into input_pool
        get_pool_queue(output_pool, &output_queue, QUEUE_FROM_END);

        filter_log_msg(LOG_LEVEL_DEBUG, "  Applying %d of (%d - %d) rule %d :- %d %s %d\n", id, start_id, end_id, rule->result_label, rule->left_label, operators[rule->op_code].name, rule->right_label);
        // apply one rule, putting the output directly into the output pool
        // pass through the equivalent labels map for making sure exclusive 
        // rules don't allow intervals to exclude themselves
        apply_rule(rule, &rule->input_queue, output_pool, &spec->equivalent_labels);

        // now set up the queue on input_pool
        // this will be used the next time the same rule is called
        // the trouble is that we need a handle to what intervals the rule
        // has already seen so it doesn't get passed the same ones twice
        get_pool_queue(input_pool, &rule->input_queue, QUEUE_FROM_END);

        // we need to copy any created intervals from this rule into the input pool
        // this is so the next rule application gets them sort of for free
        while (has_next_queue_interval(&output_queue)) {
            to_copy = next_queue_interval(&output_queue);
            filter_log_msg(LOG_LEVEL_SUPERDEBUG, "  -- Copying interval to input pool (%d,%" PRIu64 ",%" PRIu64 ")\n", to_copy->name, to_copy->start, to_copy->end);
            add_interval(input_pool, to_copy);
        }
    }
}

/**
 * Apply an nfer specification to a pool until a fixed point is reached.
 * This function implements the T[] function from nfer semantics.  It calls the S
 * function (apply_specification) until that function stops producing new intervals.
 * 
 * This implements the new semantics that include an optimization to skip iteration
 * if there is no cycle in the rules.  In that case, it will simply apply them
 * once and return, since there can be no more more intervals produced.
 * 
 * Assumes that the spec and input pool are non-empty.
 * Output pool will be purged and sorted at the end.
 */
void run_nfer(nfer_specification *spec, pool *input_pool, pool *output_pool) {
    pool_index previous_size;
    unsigned int loop_count;
    rule_id id, starting_id, ending_id;
    nfer_rule *rule, *starting_rule;
    bool is_cycle;

    // store the starting size, which should be zero but we don't need to require that
    previous_size = output_pool->size;

    // initialize the input_queues for all the rules to point at the beginning of input_pool
    // apply_rule uses the input queue to iterate over the input pool and it needs to be 
    // initialized outside of apply_specification since that function will be called multiple
    // times to reach a fixed point.  apply_specification will update the input_queues to
    // keep track of what intervals each rule has seen so far.
    for (id = 0; id < spec->size; id++) {
        rule = &spec->rules[id];
        get_pool_queue(input_pool, &rule->input_queue, QUEUE_FROM_BEGINNING);
    }

    // As of nfer 1.8 we implement the extended semantics that permit exclusive rules
    // in the same spec as cycles so long as the exclusive rules are not in cycles themselves.
    // To implement this, we have an outer loop over the cycles in the specification.
    // Each cycle is iterated over to a fixed point, unless it is a cycle of zero which means
    // it isn't a cycle and can be run just one time.  
    // Crucially, we also have to handle the special case of a cycle of just one rule
    // we can just check the result/left/right labels directly to find this case.
    for (starting_id = 0; starting_id < spec->size; starting_id = ending_id + 1) {
        starting_rule = &spec->rules[starting_id];
        // get the id of the last rule in the cycle (could be the same as starting_id)
        ending_id = starting_rule->cycle_size + starting_id;
        // is there a cycle?
        is_cycle = ending_id > starting_id || 
                   // look for self-loops
                   (starting_rule->result_label == starting_rule->left_label || starting_rule->result_label == starting_rule->right_label);
        // keep track of the number of times we have applied the rules
        loop_count = 0;
        
        filter_log_msg(LOG_LEVEL_DEBUG, "Running nfer rule cycle %u - %u\n", starting_id, ending_id);

        // always run at least once
        // if there is not a cycle, stop there
        // if there is a cycle, then keep going if new intervals were produced by the last application
        while (loop_count == 0 || (is_cycle && (output_pool->size - output_pool->removed) > previous_size)) {
            previous_size = output_pool->size - output_pool->removed;
            filter_log_msg(LOG_LEVEL_DEBUG, "  Iteration %d: applying spec to input pool size %d with partial output size %d\n", loop_count, input_pool->size, output_pool->size - output_pool->removed);
            apply_rule_list(spec, starting_id, ending_id, input_pool, output_pool);
            loop_count++;
        }
    }


    // sort the result
    // make sure to account for removed intervals, since they may be trimmed by a selection function
    if (output_pool->size - output_pool->removed > 0) {
        // remove any hidden intervals from the output before sorting
        remove_hidden(output_pool);
    }
    if (output_pool->size - output_pool->removed > 0) {
        // then sort, which also purges the removed hidden intervals
        sort_pool(output_pool);
    }
}

/**
 * Write an nfer rule out in a format that should be parsable using this tool.
 * This function takes a rule in the internal format and, assuming it doesn't use any
 * specially linked C code, writes out the rule such that it could be reparsed into
 * the same rule data structure by the DSL code.
 * 
 * The function requires the three dictionaries for obvious reasons.
 * 
 * It writes using the write_msg function and passed the log_to parameter along to that.
 * This means it can potentially write to different file handles.
 * 
 * The output from the function does not have to exactly match what was parsed to
 * generate the rule, but it does have to match the semantics of that rule.
 * Of course, the DSL supports nested rules and this will only ever output a single,
 * binary (or atomic) rule.
 */
#ifndef TEST
static
#endif
void write_rule(nfer_rule *rule, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict, int log_to) {
    map_iterator mit;
    map_key key;
    map_value value;
    bool first;
    nfer_operator *op;

    op = &operators[rule->op_code];

    if (rule->exclusion) {
        // if it's an exclusion rule, the unless keyword appears
        write_msg(log_to, "%s :- %s unless %s %s",
                get_word(name_dict, rule->result_label),
                get_word(name_dict, rule->left_label),
                op->name,
                get_word(name_dict, rule->right_label));
    } else {
        write_msg(log_to, "%s :- %s %s %s",
                get_word(name_dict, rule->result_label),
                get_word(name_dict, rule->left_label),
                op->name,
                get_word(name_dict, rule->right_label));
    }
    // need to support both the C API and the DSL
    if (rule->phi) {
        write_msg(log_to, " phi %s", rule->phi->name);
    }
    #ifndef NO_DYNAMIC_MEMORY
    // skip all this if there's no dynamic memory, as write_expression won't be implemented
    if (rule->where_expression) {
        write_msg(log_to, " where ");
        write_expression(rule->where_expression, key_dict, val_dict, get_word(name_dict, rule->left_label), get_word(name_dict, rule->right_label), log_to);
    }
    get_map_iterator(&rule->map_expressions, &mit);
    if (has_next_map_key(&mit)) {
        write_msg(log_to, " map { ");
        first = true;
        while(has_next_map_key(&mit)) {
            if (first) {
                first = false;
            } else {
                log_msg(", ");
            }
            key = next_map_key(&mit);
            map_get(&rule->map_expressions, key, &value);
            write_msg(log_to, "%s -> ", get_word(key_dict, key));
            write_expression(value.value.pointer, key_dict, val_dict, get_word(name_dict, rule->left_label), get_word(name_dict, rule->right_label), log_to);
        }
        write_msg(log_to, " }");
    }
    if (rule->begin_expression) {
        write_msg(log_to, " begin ");
        write_expression(rule->begin_expression, key_dict, val_dict, get_word(name_dict, rule->left_label), get_word(name_dict, rule->right_label), log_to);
    }
    if (rule->end_expression) {
        write_msg(log_to, " end ");
        write_expression(rule->end_expression, key_dict, val_dict, get_word(name_dict, rule->left_label), get_word(name_dict, rule->right_label), log_to);
    }
    #endif // NO_DYNAMIC_MEMORY
}

void log_specification(nfer_specification *spec, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict) {
    rule_id i;
    filter_log_msg(LOG_LEVEL_DEBUG, "Specification(%d,%d,%p)\n",
            spec->space,
            spec->size,
            spec->rules);
    for (i = 0; i < spec->size; i++) {
        write_rule(&spec->rules[i], name_dict, key_dict, val_dict, WRITE_LOGGING);
        log_msg("\n");
    }
}

void output_specification(nfer_specification *spec, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict) {
    rule_id i;
    for (i = 0; i < spec->size; i++) {
        write_rule(&spec->rules[i], name_dict, key_dict, val_dict, WRITE_OUTPUT);
        write_msg(WRITE_OUTPUT, "\n");
    }
}

