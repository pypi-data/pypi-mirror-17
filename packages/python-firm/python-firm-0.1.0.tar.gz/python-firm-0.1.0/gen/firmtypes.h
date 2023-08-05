typedef unsigned long ir_visited_t;
typedef unsigned long ir_label_t;
typedef unsigned optimization_state_t;
typedef struct dbg_info             dbg_info;
typedef struct type_dbg_info        type_dbg_info;
typedef const char                  ident;
typedef struct ir_node              ir_node;
typedef struct ir_op                ir_op;
typedef struct ir_mode              ir_mode;
typedef struct ir_edge_t            ir_edge_t;
typedef struct ir_heights_t         ir_heights_t;
typedef struct ir_tarval            ir_tarval;
typedef struct ir_type              ir_type;
typedef struct ir_graph             ir_graph;
typedef struct ir_prog              ir_prog;
typedef struct ir_loop              ir_loop;
typedef struct ir_entity            ir_entity;
typedef struct ir_cdep              ir_cdep;
typedef union  ir_initializer_t     ir_initializer_t;
typedef void irg_walk_func(ir_node *, void *);
typedef struct ir_switch_table  ir_switch_table;

typedef enum firm_kind {
  k_BAD,
  k_entity,
  k_type,
  k_ir_graph,
  k_ir_node,
  k_ir_mode,
  k_tarval,
  k_ir_loop,
  k_ir_max
} firm_kind;

typedef enum ir_relation {
  ir_relation_false,
  ir_relation_equal,
  ir_relation_less,
  ir_relation_greater,
  ir_relation_unordered,
  ir_relation_less_equal,
  ir_relation_greater_equal,
  ir_relation_less_greater,
  ir_relation_less_equal_greater,
  ir_relation_unordered_equal,
  ir_relation_unordered_less,
  ir_relation_unordered_less_equal,
  ir_relation_unordered_greater,
  ir_relation_unordered_greater_equal,
  ir_relation_unordered_less_greater,
  ir_relation_true
} ir_relation;

typedef enum ir_cons_flags {
  cons_none,
  cons_volatile,
  cons_unaligned,
  cons_floats,
  cons_throws_exception,
} ir_cons_flags;

typedef enum op_pin_state {
  op_pin_state_floats,
  op_pin_state_pinned,
  op_pin_state_exc_pinned,
} op_pin_state;

typedef enum cond_jmp_predicate {
  COND_JMP_PRED_NONE,
  COND_JMP_PRED_TRUE,
  COND_JMP_PRED_FALSE
} cond_jmp_predicate;

typedef enum mtp_additional_properties {
  mtp_no_property,
  mtp_property_no_write,
  mtp_property_pure,
  mtp_property_noreturn,
  mtp_property_terminates,
  mtp_property_nothrow,
  mtp_property_naked,
  mtp_property_malloc,
  mtp_property_returns_twice,
  mtp_property_private,
  mtp_property_always_inline,
  mtp_property_noinline,
  mtp_property_inline_recommended,
  mtp_temporary
} mtp_additional_properties;

typedef struct ir_asm_constraint {
	unsigned pos;
	ident    *constraint;
	ir_mode  *mode;
} ir_asm_constraint;

typedef enum ir_builtin_kind {
  ir_bk_trap,
  ir_bk_debugbreak,
  ir_bk_return_address,
  ir_bk_frame_address,
  ir_bk_prefetch,
  ir_bk_ffs,
  ir_bk_clz,
  ir_bk_ctz,
  ir_bk_popcount,
  ir_bk_parity,
  ir_bk_bswap,
  ir_bk_inport,
  ir_bk_outport,
  ir_bk_saturating_increment,
  ir_bk_compare_swap,
  ir_bk_may_alias,
  ir_bk_va_start,
  ir_bk_va_arg,
  ir_bk_last
} ir_builtin_kind;

typedef enum {
  volatility_non_volatile,
  volatility_is_volatile
} ir_volatility;

typedef enum {
  align_is_aligned = 0,
  align_non_aligned,
} ir_align;

typedef struct hook_entry hook_entry_t;

typedef enum ir_edge_kind_t {
  EDGE_KIND_NORMAL,
  EDGE_KIND_FIRST,
  EDGE_KIND_BLOCK,
  EDGE_KIND_LAST
} ir_edge_kind_t;

typedef enum {
  dump_verbosity_onlynames,
  dump_verbosity_fields,
  dump_verbosity_methods,
  dump_verbosity_nostatic,
  dump_verbosity_typeattrs,
  dump_verbosity_entattrs,
  dump_verbosity_entconsts,
  dump_verbosity_accessStats,
  dump_verbosity_max
} ir_dump_verbosity_t;

typedef enum {
  ir_dump_flag_blocks_as_subgraphs,
  ir_dump_flag_with_typegraph,
  ir_dump_flag_disable_edge_labels,
  ir_dump_flag_consts_local,
  ir_dump_flag_idx_label,
  ir_dump_flag_number_label,
  ir_dump_flag_keepalive_edges,
  ir_dump_flag_out_edges,
  ir_dump_flag_dominance,
  ir_dump_flag_loops,
  ir_dump_flag_back_edges,
  ir_dump_flag_iredges,
  ir_dump_flag_all_anchors,
  ir_dump_flag_show_marks,
  ir_dump_flag_no_entity_values,
  ir_dump_flag_ld_names,
  ir_dump_flag_entities_in_hierarchy,
} ir_dump_flags_t;

typedef enum {
  irop_flag_none,
  irop_flag_commutative,
  irop_flag_cfopcode,
  irop_flag_fragile,
  irop_flag_forking,
  irop_flag_constlike,
  irop_flag_keep,
  irop_flag_start_block,
  irop_flag_uses_memory,
  irop_flag_dump_noblock,
  irop_flag_unknown_jump,
  irop_flag_const_memory
} irop_flags;

typedef enum {
  oparity_invalid,
  oparity_binary,
  oparity_variable,
  oparity_dynamic,
  oparity_any
} op_arity;

typedef enum ir_resources_t {
  IR_RESOURCE_NONE,
  IR_RESOURCE_BLOCK_VISITED,
  IR_RESOURCE_BLOCK_MARK,
  IR_RESOURCE_IRN_VISITED,
  IR_RESOURCE_IRN_LINK,
  IR_RESOURCE_LOOP_LINK,
  IR_RESOURCE_PHI_LIST
} ir_resources_t;

typedef enum ir_alias_relation {
  ir_no_alias,
  ir_may_alias,
  ir_sure_alias
} ir_alias_relation;

typedef enum ir_entity_usage_computed_state {
  ir_entity_usage_not_computed,
  ir_entity_usage_computed
} ir_entity_usage_computed_state;

typedef enum ir_disambiguator_options {
  aa_opt_none,
  aa_opt_always_alias,
  aa_opt_type_based,
  aa_opt_byte_type_may_alias,
  aa_opt_no_alias,
  aa_opt_inherited,
} ir_disambiguator_options;

typedef enum {
  ir_usage_none,
  ir_usage_address_taken,
  ir_usage_write,
  ir_usage_read,
  ir_usage_reinterpret_cast,
  ir_usage_unknown,
} ir_entity_usage;

typedef enum ptr_access_kind {
  ptr_access_none,
  ptr_access_read,
  ptr_access_write,
  ptr_access_rw,
  ptr_access_store,
  ptr_access_all,
} ptr_access_kind;

typedef enum ir_graph_constraints_t {
  IR_GRAPH_CONSTRAINT_ARCH_DEP,
  IR_GRAPH_CONSTRAINT_MODEB_LOWERED,
  IR_GRAPH_CONSTRAINT_NORMALISATION2,
  IR_GRAPH_CONSTRAINT_OPTIMIZE_UNREACHABLE_CODE,
  IR_GRAPH_CONSTRAINT_CONSTRUCTION,
  IR_GRAPH_CONSTRAINT_TARGET_LOWERED,
  IR_GRAPH_CONSTRAINT_BACKEND,
} ir_graph_constraints_t;

typedef enum ir_graph_properties_t {
  IR_GRAPH_PROPERTIES_NONE,
  IR_GRAPH_PROPERTY_NO_CRITICAL_EDGES,
  IR_GRAPH_PROPERTY_NO_BADS,
  IR_GRAPH_PROPERTY_NO_TUPLES,
  IR_GRAPH_PROPERTY_NO_UNREACHABLE_CODE,
  IR_GRAPH_PROPERTY_ONE_RETURN,
  IR_GRAPH_PROPERTY_CONSISTENT_DOMINANCE,
  IR_GRAPH_PROPERTY_CONSISTENT_POSTDOMINANCE,
  IR_GRAPH_PROPERTY_CONSISTENT_DOMINANCE_FRONTIERS,
  
  IR_GRAPH_PROPERTY_CONSISTENT_OUT_EDGES,
  IR_GRAPH_PROPERTY_CONSISTENT_OUTS,
  IR_GRAPH_PROPERTY_CONSISTENT_LOOPINFO,
  IR_GRAPH_PROPERTY_CONSISTENT_ENTITY_USAGE,
  IR_GRAPH_PROPERTY_MANY_RETURNS,
  
  IR_GRAPH_PROPERTIES_CONTROL_FLOW,
  IR_GRAPH_PROPERTIES_ALL,
} ir_graph_properties_t;

typedef enum {
  irp_callgraph_none,
  irp_callgraph_consistent,
  irp_callgraph_inconsistent,
  irp_callgraph_and_calltree_consistent
} irp_callgraph_state;

typedef enum {
  ir_visibility_external,
  ir_visibility_external_private,
  ir_visibility_external_protected,
  ir_visibility_local,
  ir_visibility_private,
} ir_visibility;

typedef enum ir_linkage {
  IR_LINKAGE_DEFAULT,
  IR_LINKAGE_CONSTANT,
  IR_LINKAGE_WEAK,
  IR_LINKAGE_GARBAGE_COLLECT,
  IR_LINKAGE_MERGE,
  IR_LINKAGE_HIDDEN_USER,
  IR_LINKAGE_NO_CODEGEN,
  IR_LINKAGE_NO_IDENTITY
} ir_linkage;

typedef enum {
  pn_Call_M, /**< memory result */
  pn_Call_T_result, /**< tuple containing all results */
  pn_Call_X_regular, /**< control flow when no exception occurs */
  pn_Call_X_except, /**< control flow when exception occured */
} pn_Call;

typedef enum ir_initializer_kind_t {
  IR_INITIALIZER_CONST,
  IR_INITIALIZER_TARVAL,
  IR_INITIALIZER_NULL,
  IR_INITIALIZER_COMPOUND
} ir_initializer_kind_t;

typedef enum {
  layout_undefined,
  layout_fixed
} ir_type_state;

typedef enum {
  dbg_error,
  dbg_opt_ssa,
  dbg_opt_auxnode,
  dbg_const_eval,
  dbg_opt_cse,
  dbg_straightening,
  dbg_if_simplification,
  dbg_algebraic_simplification,
  dbg_write_after_write,
  dbg_write_after_read,
  dbg_read_after_write,
  dbg_read_after_read,
  dbg_read_a_const,
  dbg_dead_code,
  dbg_opt_confirm,
  dbg_gvn_pre,
  dbg_combo,
  dbg_jumpthreading,
  dbg_backend,
  dbg_max
} dbg_action;

typedef struct src_loc_t {
  char const *file;
  unsigned line;
  unsigned column;
} src_loc_t;

typedef enum {
  cc_reg_param,
  cc_last_on_top,
  cc_callee_clear_stk,
  cc_this_call,
  cc_compound_ret,
  cc_frame_on_caller_stk,
  cc_fpreg_param,
} calling_convention;
