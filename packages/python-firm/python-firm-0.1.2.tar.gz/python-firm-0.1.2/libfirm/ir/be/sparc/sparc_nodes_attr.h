/*
 * This file is part of libFirm.
 * Copyright (C) 2012 University of Karlsruhe.
 */

/**
 * @file
 * @brief   attributes attached to all sparc nodes
 * @author  Hannes Rapp, Matthias Braun
 */
#ifndef FIRM_BE_SPARC_SPARC_NODES_ATTR_H
#define FIRM_BE_SPARC_SPARC_NODES_ATTR_H

#include <stdint.h>

#include "be_types.h"
#include "firm_types.h"
#include "irnode_t.h"

typedef struct sparc_attr_t  sparc_attr_t;

/**
 * base SPARC attribute
 */
struct sparc_attr_t
{
	except_attr                 exc;                /**< the exception attribute. MUST be the first one. */
	int32_t                     immediate_value;    /* immediate values */
	ir_entity                  *immediate_value_entity;
};

enum sparc_arch_irn_flags_t {
	sparc_arch_irn_flag_needs_64bit_spillslot = arch_irn_flag_backend << 0,
	sparc_arch_irn_flag_immediate_form        = arch_irn_flag_backend << 1,
	sparc_arch_irn_flag_aggregate_return      = arch_irn_flag_backend << 2,
	sparc_arch_irn_flag_has_delay_slot        = arch_irn_flag_backend << 3,
};

/**
 * attribute for Call instruction
 */
typedef struct sparc_call_attr_t sparc_call_attr_t;
struct sparc_call_attr_t {
	sparc_attr_t  base;
	ir_type      *call_type; /**< The call type, copied from the original Call node. */
};

/**
 * attribute for FP immediate instruction
 */
typedef struct sparc_fp_attr_t sparc_fp_attr_t;
struct sparc_fp_attr_t {
	sparc_attr_t  base;         /**< generic attribute */
	ir_mode      *fp_mode;
};

typedef struct sparc_fp_conv_attr_t sparc_fp_conv_attr_t;
struct sparc_fp_conv_attr_t {
	sparc_attr_t  base;
	ir_mode      *src_mode;
	ir_mode      *dest_mode;
};

/**
 * attributes for load/store addressing modes
 */
typedef struct sparc_load_store_attr_t sparc_load_store_attr_t;
struct sparc_load_store_attr_t {
	sparc_attr_t  base;    /**< generic attribute */
	ir_mode      *load_store_mode;
	bool          is_frame_entity : 1;
	bool          is_reg_reg      : 1;
};

/**
 * attributes for conditional jumps
 */
typedef struct sparc_jmp_cond_attr_t sparc_jmp_cond_attr_t;
struct sparc_jmp_cond_attr_t {
	sparc_attr_t base;    /**< generic attribute */
	ir_relation  relation;
	bool         is_unsigned      : 1;
	bool         annul_delay_slot : 1;
};

/**
 * attributes for switch jumps
 */
typedef struct sparc_switch_jmp_attr_t sparc_switch_jmp_attr_t;
struct sparc_switch_jmp_attr_t {
	sparc_attr_t           base;
	const ir_switch_table *table;
	ir_entity             *table_entity;
};

typedef enum operand_kind_t {
	ASM_OPERAND_INPUT_VALUE,
	ASM_OPERAND_OUTPUT_VALUE,
	ASM_OPERAND_IMMEDIATE,
	ASM_OPERAND_MEMORY,
} operand_kind_t;

typedef struct sparc_asm_operand_t {
	operand_kind_t kind;
	unsigned       pos;
	int32_t        immediate_value;
	ir_entity     *immediate_value_entity;
} sparc_asm_operand_t;

#endif
