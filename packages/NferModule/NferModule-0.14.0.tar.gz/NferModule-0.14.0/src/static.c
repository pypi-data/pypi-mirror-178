/*
 * static.c
 *
 *  Created on: Dec 10, 2021
 *      Author: skauffma
 *
 *   nfer - a system for inferring abstractions of event streams
 *   Copyright (C) 2021  Sean Kauffman
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

#include <assert.h>
#include <stdlib.h>

#include "types.h"
#include "ast.h"
#include "dsl.tab.h"
#include "dict.h"
#include "static.h"
#include "nfer.h"
#include "log.h"



/**
 * Determine if any rule defines custom begin or end timestamps that refer to anything
 * apart from the four input begin and end timestamps.  This is strictly not permitted
 * if one relies on the known complexity classes.
 **/
bool check_computes_ts(ast_node *node) {
    bool does_compute_ts;

    // if we hit a null pointer (end of a list), return
    if (node == NULL) {
        return false;
    }

    /* no preconditions - there are too many node types to make it worth checking */

    // doesn't do it unless we find otherwise
    does_compute_ts = false;

    switch (node->type) {
    case type_time_field:
        // users are allowed to specify end points are just a timestamp from the input
        does_compute_ts = false;
        break;
    case type_end_points:
        does_compute_ts = check_computes_ts(node->end_points.begin_expr) ||
                          check_computes_ts(node->end_points.end_expr);
        break;
    case type_rule:
        does_compute_ts = check_computes_ts(node->rule.end_points);

        break;
    case type_rule_list:
        does_compute_ts = check_computes_ts(node->rule_list.head) ||
                          check_computes_ts(node->rule_list.tail);
        break;
    case type_module_list:
        /* skip any non-imported modules */
        if (node->module_list.imported) {
            does_compute_ts = check_computes_ts(node->module_list.rules);
        }
        does_compute_ts = does_compute_ts || check_computes_ts(node->module_list.tail);
        break;
    default:
        // if we get here, it's because we hit some arithmetic expression in the end points
        // therefore, we got some computation
        does_compute_ts = true;
        filter_log_msg(LOG_LEVEL_DEBUG, "    Found possible arithmetic in end point expression: %d\n", (int)node->type);
        break;
    }
    return does_compute_ts;
}
