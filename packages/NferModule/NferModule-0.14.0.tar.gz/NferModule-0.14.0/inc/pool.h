/*
 * pool.h
 *
 *  Created on: Jan 22, 2017
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

#ifndef POOL_H_
#define POOL_H_

#include <stdint.h>
#include "types.h"
#include "dict.h"
#include "map.h"

typedef uint64_t timestamp;
typedef int label;

typedef unsigned int pool_index;

#define INITIAL_POOL_SIZE         16

#define COPY_POOL_OVERWRITE       0
#define COPY_POOL_APPEND          1
#define COPY_POOL_EXCLUDE_HIDDEN  0
#define COPY_POOL_INCLUDE_HIDDEN  1

#define QUEUE_FROM_BEGINNING 0
#define QUEUE_FROM_END       1

#define END_OF_POOL         ((pool_index)-1)

typedef struct _interval {
    label       name;
    timestamp   start;
    timestamp   end;
    data_map    map;
    bool        hidden;
} interval;

#define EMPTY_INTERVAL ((interval){WORD_NOT_FOUND,0,0,EMPTY_MAP})

typedef struct _interval_node {
    interval    i;
    pool_index  prior;
    pool_index  next;
} interval_node;

typedef struct _pool {
    pool_index      size;
    pool_index      space;
    pool_index      removed;
    interval_node   *intervals;
    pool_index      start;
    pool_index      end;
} pool;

typedef struct _pool_iterator {
    pool        *p;
    pool_index  current;
    pool_index  last;
} pool_iterator;

void initialize_pool(pool *);
void destroy_pool(pool *);

void add_interval(pool *, interval *);
interval * allocate_interval(pool *);
void copy_pool(pool *dest, pool *src, bool append, bool include_hidden);
void purge_pool(pool *);
void sort_pool(pool *);
void clear_pool(pool *);
void remove_from_pool(pool_iterator *);
void remove_hidden(pool *);

void get_pool_iterator(pool *, pool_iterator *);
interval * next_interval(pool_iterator *);
bool has_next_interval(pool_iterator *);

// These functions are for partial iteration in insertion order (pool queue, get it?).
// They still use the same iterator struct but the functions must not be mixed.
// get_pool_queue sets the iterator to where anything added after this is created will 
// be available to iterate over, but nothing before it the function was called.
void get_pool_queue(pool *, pool_iterator *, bool);
interval * next_queue_interval(pool_iterator *);
bool has_next_queue_interval(pool_iterator *);
// This checks if the current position of the first queue was added after the current 
// position of the second queue.
// This uses the insertion order of the pool, not the iteration order!
bool interval_added_after(pool_iterator *, pool_iterator *);

int64_t compare_intervals(interval *, interval *, data_map *);
bool equal_intervals(interval *, interval *, data_map *);
void log_interval(interval *);
void output_interval(interval *, dictionary *, dictionary *, dictionary *, int);
void output_pool(pool *, dictionary *, dictionary *, dictionary *, int);

#endif /* POOL_H_ */
