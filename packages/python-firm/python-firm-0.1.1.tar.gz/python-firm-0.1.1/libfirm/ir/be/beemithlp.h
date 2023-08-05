/*
 * This file is part of libFirm.
 * Copyright (C) 2016 University of Karlsruhe.
 */

/**
 * @file
 * @brief       Helper functions for emitting assembly from a firm graph.
 * @author      Matthias Braun
 *
 * You typically register an emission function for each node type of your
 * backend with be_set_emitter().
 */
#ifndef FIRM_BE_BEEMITHLP_H
#define FIRM_BE_BEEMITHLP_H

#include <assert.h>
#include "be.h"
#include "irop_t.h"
#include "irnode_t.h"

/**
 * Emit spaces until the comment position is reached.
 */
void be_emit_pad_comment(void);

/**
 * The type of a emitter function.
 */
typedef void emit_func(ir_node const *node);

static inline void be_set_emitter(ir_op *const op, emit_func *const func)
{
	set_generic_function_ptr(op, func);
}

void be_init_emitters(void);

void be_emit_nothing(ir_node const *node);

/**
 * Emit code for a node by calling a handler registeres with be_set_emitter().
 */
void be_emit_node(ir_node const *node);

/**
 * Set irn links of blocks to point to the predecessor blocks in the given
 * blockschedule and set irn_links of mode_X nodes to the block using them.
 * This function expects that you require the IR_RESOURCE_IRN_LINK prior
 * to using it.
 */
void be_emit_init_cf_links(ir_node **block_schedule);

/**
 * Returns the target block for a control flow node.
 * Requires a prior call to be_emit_init_cf_links().
 */
static inline ir_node *be_emit_get_cfop_target(ir_node const *const irn)
{
	assert(get_irn_mode(irn) == mode_X);
	return (ir_node*)get_irn_link(irn);
}

/**
 * Returns the previous block in the block schedule.
 * Requires a prior call to be_emit_get_cfop_target().
 */
static inline ir_node *be_emit_get_prev_block(ir_node const *const block)
{
	assert(is_Block(block));
	return (ir_node*)get_irn_link(block);
}

#endif
