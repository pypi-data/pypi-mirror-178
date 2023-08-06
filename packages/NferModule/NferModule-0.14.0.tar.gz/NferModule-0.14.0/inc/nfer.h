/*
 * nfer.h
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

#ifndef NFER_H_
#define NFER_H_

#include "expression.h"
#include "types.h"
#include "dict.h"
#include "pool.h"
#include "map.h"
#include "stack.h"

#define NFER_VERSION "1.8"

typedef bool (*temporal_test)(timestamp, timestamp, timestamp, timestamp);
typedef timestamp (*start_end)(timestamp, timestamp);
typedef bool (*map_test)(timestamp, timestamp, data_map *, timestamp, timestamp, data_map *);
typedef void (*map_generator)(data_map *, timestamp, timestamp, data_map *, timestamp, timestamp, data_map *);

typedef unsigned int rule_id;
#define MISSING_RULE_ID      ((rule_id)-1)

#define RULE_LIST_SIZE_ON_EMPTY 2

// define some optimization flag settings
#define NO_WINDOW 0

// these correspond to the indices of the operators array
typedef enum {
    ALSO_OPERATOR,
    BEFORE_OPERATOR,
    MEET_OPERATOR,
    DURING_OPERATOR,
    COINCIDE_OPERATOR,
    START_OPERATOR,
    FINISH_OPERATOR,
    OVERLAP_OPERATOR,
    SLICE_OPERATOR,
    AFTER_OPERATOR,
    FOLLOW_OPERATOR,
    CONTAIN_OPERATOR,
    N_OPERATORS
} operator_code;

typedef struct _nfer_operator {
    char            *name;
    temporal_test   test;
    start_end       start_time;
    start_end       end_time;
    bool            exclusion;
} nfer_operator;

typedef struct _phi_function {
    char                *name;
    map_test            test;
    map_generator       result;
} phi_function;

typedef struct _nfer_rule {
    operator_code       op_code;           // lookup key for the temporal operator to use
    label               left_label;        // label matching left side of the operator
    label               right_label;       // label matching right side of the operator
    label               result_label;      // label for produced intervals on the left side of the rule
    bool                exclusion;         // set if this is an exclusive rule
    phi_function        *phi;              // supports C functions for while/map which are currently unused
    bool                hidden;            // set for a hidden rule, caused by nesting in specifications
    expression_input    *where_expression; // where expression set by DSL
    expression_input    *begin_expression; // begin expression set by DSL
    expression_input    *end_expression;   // end expression set by DSL
    data_map            map_expressions;   // map expressions where each key is set by the expression pointed to
    // below here are operational data structures used by the monitoring algorithm
    pool                new_intervals;     // used in apply_rule to temporarily store new intervals
    pool_iterator       input_queue;       // used to keep track of where the rule is in the input between calls to apply_rule
    pool                left_cache;        // used to store already seen intervals that match left_label
    pool                right_cache;       // used to store already seen intervals that match right_label
    pool                produced;          // used for minimality to store intervals produced by this rule
    data_stack          expression_stack;  // used for evaluating all expressions for this rule to avoid constant init/destroy
    unsigned int        cycle_size;        // holds the size of the _rest_ (rules with higher rule_ids) of the cycle in which this rule appears
} nfer_rule;

typedef struct _nfer_specification {
    nfer_rule       *rules;
    unsigned int    size;
    unsigned int    space;
    data_map        equivalent_labels;     // a map from remapped labels to the original labels they reference
} nfer_specification;

void initialize_specification(nfer_specification *spec, unsigned int size);
void destroy_specification(nfer_specification *spec);
void move_rule(nfer_rule *dest, nfer_rule *src);

nfer_rule * add_rule_to_specification(nfer_specification *spec,
        label result_label_index, label left_label_index, operator_code op_code, label right_label_index, phi_function *phi);
bool is_subscribed(nfer_specification *, label);
bool is_published(nfer_specification *, label);
bool is_mapped(nfer_specification *, map_key);

void apply_rule(nfer_rule *rule, pool_iterator *input_queue, pool *output_pool, data_map *equivalent_labels);
void apply_rule_list(nfer_specification *spec, rule_id start_id, rule_id end_id, pool *input_pool, pool *output_pool);
void run_nfer(nfer_specification *spec, pool *input_pool, pool *output_pool);

void log_specification(nfer_specification *, dictionary *, dictionary *, dictionary *);
void output_specification(nfer_specification *, dictionary *, dictionary *, dictionary *);

#endif /* NFER_H_ */
