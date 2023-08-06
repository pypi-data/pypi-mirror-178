/*
 * pool.c
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

#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#include "types.h"
#include "pool.h"
#include "dict.h"
#include "map.h"
#include "log.h"
#include "memory.h"


void initialize_pool(pool *p) {
    p->space = 0;
    p->size = 0;
    p->removed = 0;
    p->intervals = NULL;

#ifndef NO_DYNAMIC_MEMORY
    p->intervals = (interval_node *) malloc(sizeof(interval_node) * INITIAL_POOL_SIZE);
    if (p->intervals != NULL) {
        p->space = INITIAL_POOL_SIZE;
        clear_memory(p->intervals, p->space * sizeof(interval_node));
    }
#endif

    p->start = END_OF_POOL;
    p->end = END_OF_POOL;
}

void destroy_pool(pool *p) {
    unsigned int i;

    // if p is null, be safe and do nothing
    if (p != NULL) {
        // we have to destroy all the interval maps first
        for (i = 0; i < p->size; i++) {
            destroy_map(&p->intervals[i].i.map);
        }

#ifndef NO_DYNAMIC_MEMORY
        if (p->intervals != NULL) {
            free(p->intervals);
        }
        // destroying a static pool needs to not reset the interval storage
        p->space = 0;
        p->intervals = NULL;
#endif

        p->size = 0;
        p->removed = 0;
        p->start = END_OF_POOL;
        p->end = END_OF_POOL;
    }
}

/**
 * Gets the a pointer to the next spot an interval should go and sets up the
 * linked list for that interval to be used.  This basically adds a blank
 * interval that the calling code can then fill in with details.
 *
 * This is both more efficient than having the calling code allocate an interval
 * to then copy into the pool, and also it avoids the problem of how calling
 * code can know how big maps should be in the case of static pool allocation.
 */
interval * allocate_interval(pool *p) {
    int new_space;
    interval *result;
    interval_node *interval_alloc;

    // by default, return null
    result = NULL;

    if (p->size >= p->space) {
        // first check to see if space can be recovered
        // purge_pool is O(n) so this may slow things down some
        if (p->removed > 0) {
            purge_pool(p);
        }

#ifndef NO_DYNAMIC_MEMORY
        else if (p->intervals != NULL) {
            filter_log_msg(LOG_LEVEL_SUPERDEBUG, "Growing pool %p from %u to %u\n", p, p->space, p->space * 2);
            new_space = p->space * 2;
            interval_alloc = realloc(p->intervals, sizeof(interval_node) * new_space);
            if (interval_alloc != NULL) {
                p->intervals = interval_alloc;
                clear_memory(p->intervals + p->space, p->space * sizeof(interval_node));
                p->space = new_space;
            }
        }
#endif
    }

    if (p->intervals != NULL && p->size < p->space) {
        result = &p->intervals[p->size].i;

        // adjust the double-linked-list
        if (p->start == END_OF_POOL) {
            // it's the first entry
            p->start = p->size;
        } else {
            p->intervals[p->end].next = p->size;
        }
        p->intervals[p->size].prior = p->end;
        p->intervals[p->size].next = END_OF_POOL;
        p->end = p->size;
        p->size++;

        // initialize the map here, since it must always be done
        initialize_map(&result->map);
    } else {
        filter_log_msg(LOG_LEVEL_WARN, "Could not allocate space in pool at %x for new interval (space = %d)!\n", p, p->space);
    }

    return result;
}

void add_interval(pool *p, interval *add) {
    interval *new;

    // get a new interval and adjust the linked list pointers
    new = allocate_interval(p);

    if (new != NULL) {
        // names are now just indices, so we don't actually care how they are made unique
        new->name = add->name;
        new->start = add->start;
        new->end = add->end;
        new->hidden = add->hidden;

        // deep copy the map
        copy_map(&new->map, &add->map, COPY_MAP_DEEP);
    }
}

/**
 * Removes the most recently fetched interval from a pool using an iterator.
 * This is the only method to remove intervals individually from pools.
 * It only works using a pool iterator, and only using the regular iteration
 * functions (not the queue functions).  To use it, pass the pool iterator 
 * _after_ the interval to remove has been fetched using next_interval.
 * This allows the calling code to test that the interval in question is
 * the one to remove, and then to remove it (since next_interval updates
 * the iterator).  After this is called, the next call to next_interval
 * will still return the interval that came after the removed one so that
 * the caller should still be able to keep all the other code constant in a 
 * loop.
 */
void remove_from_pool(pool_iterator *remove) {
    interval_node *node;

    node = &remove->p->intervals[remove->last];
    if (node->prior != END_OF_POOL) {
        remove->p->intervals[node->prior].next = node->next;
    }
    if (node->next != END_OF_POOL) {
        remove->p->intervals[node->next].prior = node->prior;
    }
    if (remove->p->start == remove->last) {
        remove->p->start = node->next;
    }
    if (remove->p->end == remove->last) {
        remove->p->end = node->prior;
    }
    // go ahead and destroy any associated map
    destroy_map(&node->i.map);
    // this is how we know it is removed
    node->next = END_OF_POOL;
    node->prior = END_OF_POOL;
    // we also count how many have been removed
    remove->p->removed++;
}

/**
 * Removes all the hidden intervals from a pool.
 * The purpose of this function is to iterate over the passed pool,
 * finding all the hidden intervals and removing them.  Subsequent
 * iteration over the pool will not fetch the removed intervals.
 */
void remove_hidden(pool *p) {
    pool_iterator pit;
    interval *i;

    // iterate over the pool
    get_pool_iterator(p, &pit);
    while (has_next_interval(&pit)) {
        i = next_interval(&pit);
        // it it's marked as hidden, remove it
        if (i->hidden) {
            remove_from_pool(&pit);
        }
    }
}


void get_pool_iterator(pool *p, pool_iterator *pit) {
    pit->p = p;
    pit->current = p->start;
    pit->last = END_OF_POOL;
}
interval * next_interval(pool_iterator *pit) {
    interval_node *node;

    node = &pit->p->intervals[pit->current];
    pit->last = pit->current;
    pit->current = node->next;
    return &node->i;
}
bool has_next_interval(pool_iterator *pit) {
    return pit->current != END_OF_POOL;
}

/**
 * Get an iterator that treats the pool as an empty FIFO.
 * This function can be called on any pool, regardless of its emptiness.
 * It will set the passed iterator either to the beginning of the pool
 * or to the location where the next added interval will be placed in 
 * the pool.  The purpose of the iterator is to walk through added 
 * intervals in the order THEY WERE INSERTED instead of in their sort 
 * order.  
 * 
 * The last parameter sets the starting location of the queue.
 * If it is set to QUEUE_FROM_BEGINNING it will start from the very 
 * beginning, causing iteration to include everything already present.
 * If it is set to QUEUE_FROM_END it will only get intervals
 * added AFTER get_pool_queue was called!
 * 
 * 
 * These functions MUST NOT be mixed up with the above iterator
 * functions for walking the pool in sort order!  The queue
 * iterator returned by this function may refer to unallocated space, 
 * but the normal iterator functions will misinterpret this and
 * try to read it!
 */
void get_pool_queue(pool *p, pool_iterator *pqueue, bool end) {
    pqueue->p = p;
    if (end) {
        pqueue->current = p->size;
    } else {
        pqueue->current = 0;
    }
    pqueue->last = END_OF_POOL;
}
/**
 * Given a pool queue (iterator) that has intervals in the queue, 
 * return the next interval (in insertion order).
 * This function will get the next interval in the queue and 
 * update the queue (iterator) to point to the next interval.
 * 
 * has_next_queue_interval must return true for the queue prior
 * to calling next_queue_interval!
 */
interval * next_queue_interval(pool_iterator *pqueue) {
    interval_node *node;

    node = &pqueue->p->intervals[pqueue->current];
    pqueue->current = pqueue->current + 1;
    // careful here - this really should not be used but we'll
    // keep it set to something that should work - essentially
    // this iterator should still work to remove an interval but 
    // it gets dicey and should not be relied on.
    pqueue->last = node->prior;
    
    return &node->i;
}
/**
 * Check to see if any intervals have been added to the passed
 * queue (iterator) since it was allocated.  Returns true if
 * so, false if not.
 * 
 * TODO: think about if this needs to skip removed intervals...
 */
bool has_next_queue_interval(pool_iterator *pqueue) {
    return pqueue->current < pqueue->p->size;
}

/**
 * Check if the current position of the first iterator is equal 
 * or after the current positin of the second iterator.
 */
bool interval_added_after(pool_iterator *q1, pool_iterator *q2) {
    return q1->current >= q2->current;
}


void copy_pool(pool *dest, pool *src, bool append, bool include_hidden) {
    pool_iterator pit;
    interval *i;

    if (!append) {
        clear_pool(dest);
    }

    get_pool_iterator(src, &pit);
    while(has_next_interval(&pit)) {
        i = next_interval(&pit);
        if (include_hidden || !i->hidden) {
            add_interval(dest, i);
        }
    }
}

/**
 * Compare two intervals and return a number based on their relation.
 * Returns negative if i1 < i2
 * Returns 0 if i1 == i2
 * Returns positive if i1 > i2
 * 
 * Takes a map as a parameter that can map labels to each other.
 * This is needed due to rule generation that can split logical rules into
 * multiple internal rules with generated labels.
 * The equivalence only matters for equality testing.
 * If the map pointer is NULL then it is ignored and labels must match exactly.
 * 
 * Note that only the i1 name will be checked for in the equivalence map!
 */
int64_t compare_intervals(interval *i1, interval *i2, data_map *equivalent_labels) {
    map_value value;

    if (i1->end == i2->end) {
        if (i1->start == i2->start) {
            if (i1->name == i2->name) {
                return map_compare(&i1->map, &i2->map);
            } else if (equivalent_labels != NULL) {
                // if we have been passed a map of equivalent labels, check that
                // WE ONLY LOOK UP THE i1 NAME!!!  This is due to how the function is used.
                // Essentially, we know only the i1 name can be remapped so there's no reason to check.
                // Still, this is probably not following the principle of least astonishment...
                map_get(equivalent_labels, i1->name, &value);
                if (value.type == string_type && ((label)value.value.string) == i2->name) {
                    return map_compare(&i1->map, &i2->map);
                }
            }
            return i1->name - i2->name;
        }
        return i1->start - i2->start;
    }
    return i1->end - i2->end;
}
bool equal_intervals(interval *i1, interval *i2, data_map *equivalent_labels) {
    return compare_intervals(i1, i2, equivalent_labels) == 0;
}


/**
 * Actually perform the merge in merge sort.
 */
static pool_index merge(pool *p, pool_index a, pool_index b) {
    pool_index start, *forward;
    forward = &start;
    // some static analysis complains if start isn't initialized here
    start = a;

    while (a != END_OF_POOL && b != END_OF_POOL && a != b) {
        if (compare_intervals(&p->intervals[a].i, &p->intervals[b].i, NULL) < 0) {
            *forward = a;
            a = p->intervals[a].next;

        } else {
            *forward = b;
            b = p->intervals[b].next;

        }
        forward = &p->intervals[*forward].next;
    }
    if (a != END_OF_POOL) {
        *forward = a;
    }
    if (b != END_OF_POOL) {
        *forward = b;
    }
    return start;
}

/**
 * Iterative merge sort.  Returns the first element.  Only manipulates pointers instead of moving things around.  Doesn't recurse.
 * Requires the pool is purged before being called.
 */
static pool_index iterative_merge_sort(pool *p, pool_index start) {
    pool_index block_size, block_start, middle, end, begin, last;
    bool first_pass, first_block;

    // short circuit for pools that are zero or one interval long
    if (start == END_OF_POOL || p->intervals[start].next == END_OF_POOL) {
        return start;
    }

    filter_log_msg(LOG_LEVEL_DEBUG, "Performing merge sort on pool %x from start index %d\n", p, start);

    // start by splitting the pool into blocks of size 1
    // we will then merge these into blocks of 2, then 4, then 8, etc.
    // the trick is how to keep track of where the blocks start
    // to do this, we can use the _prior_ pointers, as they are unused in this algorithm and must be rewritten after
    // the first time through, though, they aren't set but the information is available via the next pointers
    // so, we set a flag to mark if we should use the prior pointers or not
    first_pass = true;

    // divide the pool into blocks, starting with the smallest size and working up
    // note that we don't actually use the block_size value in the loop, it's just to make sure we stop at the right place
    for (block_size = 1; block_size < p->size; block_size = 2*block_size) {
        // for the first block, we store its beginning in the start variable since there's no previous block
        first_block = true;
        block_start = start;

        // we iterate until we get to the end, then increase the block size
        while (block_start != END_OF_POOL) {
            // if it's the first time through, we want to break up the pool and use its initial structure to get
            // the middle and end pointers (which are the next block and the one after that)
            end = END_OF_POOL;
            if (first_pass) {
                middle = p->intervals[block_start].next;
                p->intervals[block_start].next = END_OF_POOL;
                p->intervals[block_start].prior = END_OF_POOL;

                // get the beginning of the next block too, and break after it as well
                if (middle != END_OF_POOL) {
                    end = p->intervals[middle].next;
                    p->intervals[middle].next = END_OF_POOL;
                    p->intervals[middle].prior = END_OF_POOL;
                }
            } else {
                // we have to find the middle and end using the prior pointers
                // the middle is now set on the the prior of the beginning
                middle = p->intervals[block_start].prior;
                // don't go overwriting the pointers now that we're set up
                if (middle != END_OF_POOL) {
                    end = p->intervals[middle].prior;
                }
            }

            // actually merge the two blocks
            begin = merge(p, block_start, middle);

            // if this is the first block, set its beginning to start (we'll use it to start the next pass)
            if (first_block) {
                start = begin;
            } else {
                // if it isn't the first block, set its beginning on the prior of the beginning of the last block
                p->intervals[last].prior = begin;
            }

            // no longer the first block
            first_block = false;
            // overwrite last
            last = begin;
            
            // set the beginning of the next block
            block_start = end;
        }
        // no longer the first pass - now the prior pointers are to be used for finding the next block
        first_pass = false;
    }
    return start;
} 

void purge_pool(pool *p) {
    pool_index src_i, dest_i, extra_i;
    interval_node *src, *dest = NULL, *extra = NULL;

    filter_log_msg(LOG_LEVEL_DEBUG, "Purging pool %x size %d with %d removed intervals\n", p, p->size, p->removed);

    // if nothing has been removed, don't bother to do any work
    if (p->removed == 0) {
        return;
    }

    // src has the next element in the linked list
    src_i = p->start;
    // dest just iterates the storage space
    dest_i = 0;
    // Walk the linked list and move elements to whatever the next spot in the storage is.
    // We have to be careful to destroy anything that is in the storage but isn't linked.
    while (src_i != END_OF_POOL) {
        // get the actual intervals
        src = &p->intervals[src_i];
        dest = &p->intervals[dest_i];

        // find the next hole in storage
        // skip over the index if the following is true:
        // 1) within the possible size AND
        // 2) at least one of the following is true:
        //    a) start or end of the pool
        //    b) one of the linked list pointers points to something
        // the check for the start/end are because of edge cases like a single element pool
        while (dest_i < p->size &&
                (p->start == dest_i || p->end == dest_i ||
                dest->next != END_OF_POOL || dest->prior != END_OF_POOL)) {
            dest_i++;
            dest = &p->intervals[dest_i];
        }
        // make sure we're not off the end of the used area
        // if we are then we are done
        if (dest_i >= p->size) {
            break;
        }
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Found hole at %d\n", dest_i);

        // find the first interval that occurs after the hole
        // this iterates using the sort order which may not be accurate
        while (src_i < dest_i) {
            src_i = src->next;
            if (src_i != END_OF_POOL) {
                src = &p->intervals[src_i];
            }
        }
        // bail out if src hit the end of the list
        if (src_i == END_OF_POOL) {
            break;
        }
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Found interval to move at %d\n", src_i);

        // copy the interval in src over the interval in dest
        // the map was freed in remove_from_pool
        dest->i.name = src->i.name;
        dest->i.start = src->i.start;
        dest->i.end = src->i.end;
        dest->i.hidden = src->i.hidden;
        // just copy the pointer for the map
        copy_map(&dest->i.map, &src->i.map, COPY_MAP_SHALLOW);
        dest->next = src->next;
        dest->prior = src->prior;

        // fix the linked list
        if (src->next != END_OF_POOL) {
            p->intervals[src->next].prior = dest_i;
        }
        if (src->prior != END_OF_POOL) {
            p->intervals[src->prior].next = dest_i;
        }
        if (p->start == src_i) {
            p->start = dest_i;
        }
        if (p->end == src_i) {
            p->end = dest_i;
        }
        // get the next src_i before we zero out src's pointers
        src_i = src->next;
        src->next = END_OF_POOL;
        src->prior = END_OF_POOL;
#ifndef NO_DYNAMIC_MEMORY
        // overwrite the pointer to the map, since we copied it
        src->i.map = EMPTY_MAP;
#endif
    }
    // make sure we're at the end
    extra_i = dest_i;
    while (extra_i < p->size) {
        extra = &p->intervals[extra_i];

        // filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Looking for end - checking %d where start:%d, end:%d, next:%d, prior:%d\n", extra_i, p->start, p->end, extra->next, extra->prior);

        if (p->start == extra_i || p->end == extra_i ||
                extra->next != END_OF_POOL || extra->prior != END_OF_POOL) {
            // increment dest_i so we find the real end of the pool
            dest_i = extra_i + 1;
        } else {
            break;
        }
        extra_i++;
    }
    // fix the length
    p->size = dest_i;
    // reset removed
    p->removed = 0;
}

void sort_pool(pool *p) {
    pool_index previous, current;

    // destroy removed entries and compress the pool
    purge_pool(p);
    // sort the remaining entries by their timestamps
    p->start = iterative_merge_sort(p, p->start);

    // fix the backwards pointers, since sorting doesn't adjust them right now
    previous = END_OF_POOL;
    current = p->start;
    p->intervals[current].prior = END_OF_POOL;
    while (current != END_OF_POOL) {
        previous = current;
        current = p->intervals[current].next;
        if (current != END_OF_POOL) {
            p->intervals[current].prior = previous;
        }
    }
    p->end = previous;
}

void clear_pool(pool *p) {
    pool_index i;
    // free any maps
    for (i = 0; i < p->size; i++) {
        p->intervals[i].next = 0;
        p->intervals[i].prior = 0;
        p->intervals[i].i.name = 0;
        p->intervals[i].i.start = 0;
        p->intervals[i].i.end = 0;
        p->intervals[i].i.hidden = false;
        destroy_map(&p->intervals[i].i.map);
#ifndef NO_DYNAMIC_MEMORY
        p->intervals[i].i.map = EMPTY_MAP;
#endif
    }
    p->size = 0;
    p->removed = 0;
    p->start = END_OF_POOL;
    p->end = END_OF_POOL;
}

void log_interval(interval *i) {
    log_msg("(%d, %" PRIu64 ", %" PRIu64 ", ", i->name, i->start, i->end);
    log_map(&i->map);
    log_msg(")\n");
}

void output_interval(interval *intv, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict, int log_to) {
    write_msg(log_to, "%s|%" PRIu64 "|%" PRIu64, get_word(name_dict, intv->name), intv->start, intv->end);
    output_map_strings(&intv->map, key_dict, val_dict, log_to);
    write_msg(log_to, "\n");
}

void output_pool(pool *p, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict, int log_to) {
    pool_iterator pit;
    interval *intv;

    //log_msg("Pool(%d,%d,%p)\n", p->space, p->size, p->intervals);
    get_pool_iterator(p, &pit);
    while (has_next_interval(&pit)) {
        intv = next_interval(&pit);
        output_interval(intv, name_dict, key_dict, val_dict, log_to);
    }
}
