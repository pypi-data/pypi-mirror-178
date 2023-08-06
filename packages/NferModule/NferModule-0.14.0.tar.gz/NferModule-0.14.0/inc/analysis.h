/*
 * analysis.h
 *
 *  Created on: Jun 2, 2017
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

#ifndef INC_ANALYSIS_H_
#define INC_ANALYSIS_H_

#include "pool.h"
#include "nfer.h"

void log_event_groups(nfer_specification *, dictionary *);

/*** Compute specification cycles ***/
typedef struct _rule_digraph_vertex {
    nfer_rule     *rule;
    unsigned int  index;    /* unique index of the vertex */
    unsigned int  lowlink;  /* smallest index of vertex on stack known to be reachable */
    bool          on_stack; /* is the vertex on the stack */
    bool          visited;  /* track if the vertex has been visited yet */
} rule_digraph_vertex;

typedef struct _rule_digraph_edge {
    struct _rule_digraph_vertex    *from;
    struct _rule_digraph_vertex    *to;
} rule_digraph_edge;

bool compute_sccs(nfer_rule *, rule_digraph_vertex *, unsigned int, rule_digraph_edge *, unsigned int);
bool setup_rule_order(nfer_specification *);
bool exclusive_cycle(nfer_specification *);

#endif /* INC_ANALYSIS_H_ */
