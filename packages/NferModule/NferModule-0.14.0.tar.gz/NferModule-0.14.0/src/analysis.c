/*
 * analysis.c
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

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "types.h"
#include "dict.h"
#include "nfer.h"
#include "log.h"
#include "analysis.h"
#include "memory.h"


void log_event_groups(nfer_specification *spec, dictionary *name_dict) {
    int i, j, new_group_num, *group_assignments, *group_counts, num_labels;
    rule_id id;
    nfer_rule *rule;
    bool first;

    if (spec->size > 0) {
        filter_log_msg(LOG_LEVEL_DEBUG, "Number of rules %d\n", spec->size);

        // find the number of subscribed names
        num_labels = name_dict->size;

        // find event groups
        group_assignments = malloc(sizeof(int) * num_labels);
        clear_memory(group_assignments, sizeof(int) * num_labels);
        // can't have more groups than num_labels
        group_counts = malloc(sizeof(int) * num_labels);
        clear_memory(group_counts, sizeof(int) * num_labels);
        new_group_num = 0;

        // iterate over the rules
        for (id = 0; id < spec->size; id++) {
            // get the rule
            rule = &spec->rules[id];

            // if neither left or right side has been assigned a group
            // then pick a new group number and assign it to both
            if (group_assignments[rule->left_label] == 0 && group_assignments[rule->right_label] == 0) {
                new_group_num++;
                group_assignments[rule->left_label]  = new_group_num;
                group_assignments[rule->right_label] = new_group_num;
                group_counts[new_group_num - 1] = 1;
            } else {
                // otherwise, at least one of them is assigned a group alread so copy that

                // mark right side
                if (group_assignments[rule->right_label] == 0) {
                    group_assignments[rule->right_label] = group_assignments[rule->left_label];
                    group_counts[group_assignments[rule->left_label] - 1]++;
                }

                // mark left side
                if (group_assignments[rule->left_label] == 0) {
                    group_assignments[rule->left_label] = group_assignments[rule->right_label];
                    group_counts[group_assignments[rule->right_label] - 1]++;
                }
            }
        }

        for (j = 1; j <= new_group_num; j++) {
            if (group_counts[j - 1] > 1) {
                log_msg("Group %d:", j);
                first = true;

                for (i = 0; i < num_labels; i++) {
                    if (group_assignments[i] == j) {
                        if (!first) {
                            log_msg(",");
                        }
                        log_msg(" %s", get_word(name_dict, i));
                        first = false;
                    }
                }
                log_msg("\n");
            }
        }
        free(group_assignments);
        free(group_counts);
    }
}

/**
 * Compute a digraph from a specification where vertices are rules and edges
 * point from a rule that produces an interval label to one that consumes it.
 * Takes a specification as input along with pointers to the vertices and
 * edges that will be allocated by this function and to their counts that 
 * will be populated by this function.
 * 
 * Returns true on success, false on failure.
 */
#ifndef TEST
static
#endif
bool generate_rule_digraph(nfer_specification *spec, 
                           rule_digraph_vertex **parent_vertices,
                           unsigned int *vertex_count,
                           rule_digraph_edge **parent_edges,
                           unsigned int *edge_count) {
    unsigned int i, j;
    rule_digraph_vertex *vertices, *vertex, *from, *to;
    rule_digraph_edge *edges;

    // we know immediately how many vertices we need, so we can just allocate
    // space and set those up right away.
    *vertex_count = spec->size;
    vertices = (rule_digraph_vertex *)malloc(sizeof(rule_digraph_vertex) * (*vertex_count));

    // fail if allocation fails
    if (vertices == NULL) {
        return false;
    }
    // actually pass up the pointer
    *parent_vertices = vertices;

    // iterate over the vertices and set them up, pointing at the equivalent rule
    for (i = 0; i < *vertex_count; i++) {
        vertex = &vertices[i];
        vertex->rule = &spec->rules[i];
        // set up the important flags
        vertex->visited = false;
        vertex->on_stack = false;
        // set the other values too, just for funsies
        vertex->index = 0;
        vertex->lowlink = 0;
    }

    // now we need to set up the edges
    // this will be quick and dirty - we know the maximum number of edges is n^2
    // where n is the number of vertices, so just allocate that much space so we 
    // don't have to realloc.  In practice this should be fine since there should
    // never be so many rules as to make this a problem.
    *edge_count = 0;
    edges = (rule_digraph_edge *)malloc(sizeof(rule_digraph_edge) * (*vertex_count) * (*vertex_count));

    // make sure to clean up if there's an error
    if (edges == NULL) {
        free(vertices);
        return false;
    }
    // actually pass up the pointer
    *parent_edges = edges;

    // again, quick and dirty
    // just iterate over all possible edges and add them if they should exist
    for (i = 0; i < *vertex_count; i++) {
        from = &vertices[i];
        for (j = 0; j < *vertex_count; j++) {
            to = &vertices[j];

            // if from produces the same interval that to consumes
            if (from->rule->result_label == to->rule->left_label || 
                from->rule->result_label == to->rule->right_label) {
                // add the edge
                edges[*edge_count].from = from;
                edges[*edge_count].to   = to;
                (*edge_count)++;
            }
        }
    }
    return true;
}

/**
 * Computes the strongly connected component for a single vertex.
 * Helper method for compute_sccs.
 * 
 * Takes a single vertex, the edges, the stack of vertices, and the
 * lowest unused index as inputs.
 * 
 * The rules pointer must be an array with enough space allocated to
 * hold all the rules.  It will be populated with the rules in 
 * topological order (of the strongly connected components).
 * 
 * Recursively calls itself.
 */
#ifndef TEST
static
#endif
void strongly_connected(nfer_rule *rules_dest,
                        rule_id *rules_index,
                        rule_digraph_vertex *vertex, 
                        rule_digraph_edge *edges, 
                        unsigned int edge_count, 
                        rule_digraph_vertex **stack, 
                        unsigned int *tos, // stack is empty ascending
                        unsigned int *unused_index) {
    unsigned int i;
    rule_digraph_edge *edge;
    rule_digraph_vertex *successor, *member;
    unsigned int cycle_count;

    /*** setup the vertex ***/
    
    // set the index and lowlink for the vertex
    vertex->index = *unused_index;
    vertex->lowlink = *unused_index;
    // increment the unused index
    (*unused_index)++;
    // push the vertex onto the stack
    stack[*tos] = vertex;
    // increment the top of stack
    (*tos)++;
    // mark that the vertex is on the stack
    vertex->on_stack = true;
    // mark that the vertex has been visited
    vertex->visited = true;

    filter_log_msg(LOG_LEVEL_SUPERDEBUG, "      Visiting vertex <%p> [%u,%u,%u,%u]\n", vertex, vertex->index, vertex->lowlink, vertex->on_stack, vertex->visited);

    /*** consider successors of the vertex ***/

    // iterate over the edges
    for (i = 0; i < edge_count; i++) {
        edge = &edges[i];
        // only consider outgoing edges from the vertex
        if (edge->from == vertex) {
            successor = edge->to;
            filter_log_msg(LOG_LEVEL_SUPERDEBUG, "      Found outgoing edge %u to <%p> : ", i, successor);

            // if the successor hasn't been visited yet, recurse
            if (!successor->visited) {
                filter_log_msg(LOG_LEVEL_SUPERDEBUG, "Not yet visited\n");
                // successor hasn't been visited
                strongly_connected(rules_dest, rules_index, successor, edges, edge_count, stack, tos, unused_index);
                // after recursing, set the lowlink to the lower of the two indices
                if (successor->lowlink < vertex->lowlink) {
                    vertex->lowlink = successor->lowlink;
                }
            } else if (successor->on_stack) {
                filter_log_msg(LOG_LEVEL_SUPERDEBUG, "On stack at %u\n", successor->index);
                // the successor is on the stack, so it's in the current SCC
                // we ignore the successor if it isn't on the stack as it's in
                // an already formed SCC that this SCC points to
                // set the lowlink to the minimum of its lowlink and the successor's index
                if (successor->index < vertex->lowlink) {
                    vertex->lowlink = successor->index;
                }
            }
        }
    }

    /*** output an SCC ***/

    // if the vertex is the root of an SCC, output it
    if (vertex->index == vertex->lowlink) {
        // we need to keep track of how many rules have been 
        // added to this cycle
        cycle_count = 0;
        // always pop at least the top of the stack
        do {
            // pop the top of stack - first decrement then read
            (*tos)--;
            member = stack[*tos];
            member->on_stack = false;
            // now write the rule to the output
            // decrement the rules index first
            (*rules_index)--;
            filter_log_msg(LOG_LEVEL_SUPERDEBUG, "      Writing rule %u <%p> [%u,%u,%u,%u] to index %u\n", member->index, member, member->index, member->lowlink, member->on_stack, member->visited, *rules_index);
            // note that this leaves the rule in the original data structure unusable!
            move_rule(&rules_dest[*rules_index], member->rule);
            // now set the cycle count and increment it
            rules_dest[*rules_index].cycle_size = cycle_count;
            cycle_count++;

        } while (member != vertex);
        // stop when the popped member is the root vertex
    }
    filter_log_msg(LOG_LEVEL_SUPERDEBUG, "      Returning\n");
}

/**
 * Compute the strongly connected components of the rule graph.
 * This implements Tarjan's algorithm to find the strongly connected components 
 * and order them topologically.  The algorithm runs in linear time in the size 
 * of the graph.  It does recursively call strongly_connected, which would be
 * nice but not crucial to avoid, since this code is not included in static
 * monitors.
 * 
 * The vertices and edges must be precomputed.
 * The passed rules pointer must be an array with enough space allocated to hold
 * all of the rules.  It will be populated with the rules in the correct order
 * starting from index zero.
 * 
 * Returns true on success, false on failure.
 */
bool compute_sccs(nfer_rule *rules_dest, 
                  rule_digraph_vertex *vertices, unsigned int vertex_count, 
                  rule_digraph_edge *edges, unsigned int edge_count) {
    // set up the variables we need
    unsigned int index;
    rule_digraph_vertex **stack;
    unsigned int tos;
    unsigned int i;
    unsigned int rules_index;
    rule_digraph_vertex *vertex;

    // precondition: rules_dest needs to be allocated
    assert(rules_dest != NULL);

    // set starting index to zero
    index = 0;
    // allocate enough memory on the stack to hold every vertex, which is the worst case
    stack = (rule_digraph_vertex **)malloc(sizeof(rule_digraph_vertex *) * vertex_count);
    // if an error occurred, return failure
    if (stack == NULL) {
        return false;
    }
    // stack is empty ascending
    tos = 0;
    // start the rules at the maximum index, which is the same as the number of vertices
    // the reason is that the algorithm outputs the SCCs in _reverse_ topological order, so
    // we need to write them to the rules array in reverse order.
    // The index will be decremented before written to!
    rules_index = vertex_count;

    // loop over all the vertices, calling strongly_connected unless it has already been visited
    for (i = 0; i < vertex_count; i++) {
        vertex = &vertices[i];

        // if the vertex has not been visited, call strongly_connected
        if (!vertex->visited) {
            filter_log_msg(LOG_LEVEL_SUPERDEBUG, "    Starting with vertex %u <%p> [%u,%u,%u,%u]\n", i, vertex, vertex->index, vertex->lowlink, vertex->on_stack, vertex->visited);
            strongly_connected(rules_dest, &rules_index, vertex, edges, edge_count, stack, &tos, &index);
        }
    }

    // clean up the stack
    free(stack);

    // postconditions: the stack is empty, the index is the same as the vertex count and the rules
    //                 index is zero
    assert(tos == 0);
    assert(index == vertex_count);
    assert(rules_index == 0);

    return true;
}

/**
 * Set up the rule ordering to work with the fixed point algorithm that depends
 * on pre-computing strongly connected components and topologically sorting 
 * them.  As of nfer 1.8 this function MUST be called on a specification after
 * new rules are added before it can be applied.
 */
bool setup_rule_order(nfer_specification *spec) {
    rule_digraph_vertex *vertices;
    rule_digraph_edge *edges;
    unsigned int vertex_count, edge_count;
    nfer_specification new_spec;
    bool success;

    filter_log_msg(LOG_LEVEL_INFO, "Setting up rule order for %u rules in spec <%p>\n", spec->size, spec);

    // skip this whole procedure if the size of the spec is zero or one
    if (spec->size < 2) {
        filter_log_msg(LOG_LEVEL_INFO, "  Skipping rule ordering as there are too few\n");
        return true;
    }

    // first, we need to calculate the digraph
    success = generate_rule_digraph(spec, &vertices, &vertex_count, &edges, &edge_count);
    filter_log_msg(LOG_LEVEL_INFO, "  Computed rule graph has %u vertices and %u edges\n", vertex_count, edge_count);

    if (!success) {
        filter_log_msg(LOG_LEVEL_ERROR, "Error computing rule graph!\n");

        // there was a problem generating the graph - bail out
        return false;
    }

    // now make room for the reordered rules
    initialize_specification(&new_spec, spec->size);

    // there is no explicit failure for initializing a spec so check its space
    if (new_spec.space != spec->size) {
        filter_log_msg(LOG_LEVEL_ERROR, "Error initializing new specification!\n");
        destroy_specification(&new_spec);
        // clean up the graph
        free(vertices);
        free(edges);
        return false;
    }

    // we can now populate it with the SCCs
    success = compute_sccs(new_spec.rules, vertices, vertex_count, edges, edge_count);
    filter_log_msg(LOG_LEVEL_INFO, "  Computed graph components.\n");

    // we have to clean these up anyway regardless of whether or not the call succeeded
    free(vertices);
    free(edges);

    if (!success) {
        filter_log_msg(LOG_LEVEL_ERROR, "Error computing rule graph components!\n");
        // if computing the SCCs fails, we have to ditch the new rules
        destroy_specification(&new_spec);
        return false;
    }

    // if we get here, everything succeeded
    // replace the internals of the specification with the new one
    // first, copy the equivalent_labels map to preserve it - deep so we don't need to 
    // mess around with how to preserve the data in the old spec
    copy_map(&new_spec.equivalent_labels, &spec->equivalent_labels, COPY_MAP_DEEP);
    // then we can destroy the old spec
    destroy_specification(spec);
    // now we can copy over the internals
    spec->rules    = new_spec.rules;
    spec->size     = vertex_count;
    spec->space    = vertex_count;
    // and shallow copy the equivalent_lable map back
    // shallow copy it since we don't destroy the data structures from the new spec
    copy_map(&spec->equivalent_labels, &new_spec.equivalent_labels, COPY_MAP_SHALLOW);

    // all is good
    return true;
}

/**
 * Checks if a specification contains a cycle with an exclusive rule.
 * This function only works if it has been called _after_ setup_rule_order.
 * Exclusive rules are not permitted inside cycles, so this function detects
 * if that is the case.
 * 
 * The cycles are detected by setup_rule_order, so this function only 
 * needs to iterate over the cycles and make sure none of them contain
 * exclusive rules.
 */
bool exclusive_cycle(nfer_specification *spec) {
    rule_id id;
    bool in_cycle;
    nfer_rule *rule;

    in_cycle = false;
    // iterate over the rules - if an exclusive rule is detected, make
    // sure it isn't in a cycle.  The only trick is that this requires
    // keeping track of if the loop is currently in a cycle, since
    // non-cycles and last-rules-in-cycles both have cycle_size = 0.
    for (id = 0; id < spec->size; id++) {
        rule = &spec->rules[id];
        // mark that this is a cycle if we see cycle_size above zero
        if (rule->cycle_size > 0) {
            in_cycle = true;
        }
        // then check for exclusive + in cycle
        if (in_cycle && rule->exclusion) {
            // problem detected
            return true;
        }
        // now that we tested for the exclusive / cycle condition
        // we can reset in_cycle if the cycle_size is zero
        if (rule->cycle_size == 0) {
            in_cycle = false;
        }
    }

    return false;
}