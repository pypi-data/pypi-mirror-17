/* Warning: Automatically generated file */

typedef enum ir_opcode {
        iro_ASM,
        iro_Add,
        iro_Address,
        iro_Align,
        iro_Alloc,
        iro_Anchor,
        iro_And,
        iro_Bad,
        iro_Bitcast,
        iro_Block,
        iro_Builtin,
        iro_Call,
        iro_Cmp,
        iro_Cond,
        iro_Confirm,
        iro_Const,
        iro_Conv,
        iro_CopyB,
        iro_Deleted,
        iro_Div,
        iro_Dummy,
        iro_End,
        iro_Eor,
        iro_Free,
        iro_IJmp,
        iro_Id,
        iro_Jmp,
        iro_Load,
        iro_Member,
        iro_Minus,
        iro_Mod,
        iro_Mul,
        iro_Mulh,
        iro_Mux,
        iro_NoMem,
        iro_Not,
        iro_Offset,
        iro_Or,
        iro_Phi,
        iro_Pin,
        iro_Proj,
        iro_Raise,
        iro_Return,
        iro_Sel,
        iro_Shl,
        iro_Shr,
        iro_Shrs,
        iro_Size,
        iro_Start,
        iro_Store,
        iro_Sub,
        iro_Switch,
        iro_Sync,
        iro_Tuple,
        iro_Unknown,
} ir_opcode;

ir_node *get_ASM_mem(const ir_node *node);
void set_ASM_mem(ir_node *node, ir_node *mem);
int get_ASM_n_inputs(ir_node const *node);
ir_node *get_ASM_input(ir_node const *node, int pos);
void set_ASM_input(ir_node *node, int pos, ir_node *input);
ir_node **get_ASM_input_arr(ir_node *node);
ir_asm_constraint* get_ASM_input_constraints(const ir_node *node);

ir_asm_constraint* get_ASM_output_constraints(const ir_node *node);

ident** get_ASM_clobbers(const ir_node *node);

ident* get_ASM_text(const ir_node *node);
ir_op *get_op_ASM(void);

ir_node *new_rd_Add(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Add_left(const ir_node *node);
void set_Add_left(ir_node *node, ir_node *left);
ir_node *get_Add_right(const ir_node *node);
void set_Add_right(ir_node *node, ir_node *right);
ir_op *get_op_Add(void);

ir_node *new_rd_Address(dbg_info *dbgi, ir_graph *irg, ir_entity* entity);


ir_entity* get_Address_entity(const ir_node *node);
ir_op *get_op_Address(void);

ir_node *new_rd_Align(dbg_info *dbgi, ir_graph *irg, ir_mode * mode, ir_type* type);


ir_type* get_Align_type(const ir_node *node);
ir_op *get_op_Align(void);

ir_node *new_rd_Alloc(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_size, unsigned alignment);

ir_node *get_Alloc_mem(const ir_node *node);
void set_Alloc_mem(ir_node *node, ir_node *mem);
ir_node *get_Alloc_size(const ir_node *node);
void set_Alloc_size(ir_node *node, ir_node *size);

unsigned get_Alloc_alignment(const ir_node *node);
ir_op *get_op_Alloc(void);

ir_node *get_Anchor_end_block(const ir_node *node);
void set_Anchor_end_block(ir_node *node, ir_node *end_block);
ir_node *get_Anchor_start_block(const ir_node *node);
void set_Anchor_start_block(ir_node *node, ir_node *start_block);
ir_node *get_Anchor_end(const ir_node *node);
void set_Anchor_end(ir_node *node, ir_node *end);
ir_node *get_Anchor_start(const ir_node *node);
void set_Anchor_start(ir_node *node, ir_node *start);
ir_node *get_Anchor_frame(const ir_node *node);
void set_Anchor_frame(ir_node *node, ir_node *frame);
ir_node *get_Anchor_initial_mem(const ir_node *node);
void set_Anchor_initial_mem(ir_node *node, ir_node *initial_mem);
ir_node *get_Anchor_args(const ir_node *node);
void set_Anchor_args(ir_node *node, ir_node *args);
ir_node *get_Anchor_no_mem(const ir_node *node);
void set_Anchor_no_mem(ir_node *node, ir_node *no_mem);
ir_op *get_op_Anchor(void);

ir_node *new_rd_And(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_And_left(const ir_node *node);
void set_And_left(ir_node *node, ir_node *left);
ir_node *get_And_right(const ir_node *node);
void set_And_right(ir_node *node, ir_node *right);
ir_op *get_op_And(void);

ir_node *new_rd_Bad(dbg_info *dbgi, ir_graph *irg, ir_mode * mode);

ir_op *get_op_Bad(void);

ir_node *new_rd_Bitcast(dbg_info *dbgi, ir_node *block, ir_node * irn_op, ir_mode * mode);

ir_node *get_Bitcast_op(const ir_node *node);
void set_Bitcast_op(ir_node *node, ir_node *op);
ir_op *get_op_Bitcast(void);

ir_node *new_rd_Block(dbg_info *dbgi, ir_graph *irg, int arity, ir_node *const * in);

int get_Block_n_cfgpreds(ir_node const *node);
ir_node *get_Block_cfgpred(ir_node const *node, int pos);
void set_Block_cfgpred(ir_node *node, int pos, ir_node *cfgpred);
ir_node **get_Block_cfgpred_arr(ir_node *node);
ir_entity* get_Block_entity(const ir_node *node);
ir_op *get_op_Block(void);

ir_node *new_rd_Builtin(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, int arity, ir_node *const * in, ir_builtin_kind kind, ir_type* type);

ir_node *get_Builtin_mem(const ir_node *node);
void set_Builtin_mem(ir_node *node, ir_node *mem);
int get_Builtin_n_params(ir_node const *node);
ir_node *get_Builtin_param(ir_node const *node, int pos);
void set_Builtin_param(ir_node *node, int pos, ir_node *param);
ir_node **get_Builtin_param_arr(ir_node *node);
ir_builtin_kind get_Builtin_kind(const ir_node *node);

ir_type* get_Builtin_type(const ir_node *node);
ir_op *get_op_Builtin(void);

ir_node *new_rd_Call(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_ptr, int arity, ir_node *const * in, ir_type* type);

ir_node *get_Call_mem(const ir_node *node);
void set_Call_mem(ir_node *node, ir_node *mem);
ir_node *get_Call_ptr(const ir_node *node);
void set_Call_ptr(ir_node *node, ir_node *ptr);
int get_Call_n_params(ir_node const *node);
ir_node *get_Call_param(ir_node const *node, int pos);
void set_Call_param(ir_node *node, int pos, ir_node *param);
ir_node **get_Call_param_arr(ir_node *node);
ir_type* get_Call_type(const ir_node *node);
ir_op *get_op_Call(void);

ir_node *new_rd_Cmp(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right, ir_relation relation);

ir_node *get_Cmp_left(const ir_node *node);
void set_Cmp_left(ir_node *node, ir_node *left);
ir_node *get_Cmp_right(const ir_node *node);
void set_Cmp_right(ir_node *node, ir_node *right);

ir_relation get_Cmp_relation(const ir_node *node);
ir_op *get_op_Cmp(void);

ir_node *new_rd_Cond(dbg_info *dbgi, ir_node *block, ir_node * irn_selector);

ir_node *get_Cond_selector(const ir_node *node);
void set_Cond_selector(ir_node *node, ir_node *selector);

cond_jmp_predicate get_Cond_jmp_pred(const ir_node *node);
ir_op *get_op_Cond(void);

ir_node *new_rd_Confirm(dbg_info *dbgi, ir_node *block, ir_node * irn_value, ir_node * irn_bound, ir_relation relation);

ir_node *get_Confirm_value(const ir_node *node);
void set_Confirm_value(ir_node *node, ir_node *value);
ir_node *get_Confirm_bound(const ir_node *node);
void set_Confirm_bound(ir_node *node, ir_node *bound);

ir_relation get_Confirm_relation(const ir_node *node);
ir_op *get_op_Confirm(void);

ir_node *new_rd_Const(dbg_info *dbgi, ir_graph *irg, ir_tarval* tarval);


ir_tarval* get_Const_tarval(const ir_node *node);
ir_op *get_op_Const(void);

ir_node *new_rd_Conv(dbg_info *dbgi, ir_node *block, ir_node * irn_op, ir_mode * mode);

ir_node *get_Conv_op(const ir_node *node);
void set_Conv_op(ir_node *node, ir_node *op);
ir_op *get_op_Conv(void);

ir_node *new_rd_CopyB(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_dst, ir_node * irn_src, ir_type* type, ir_cons_flags flags);

ir_node *get_CopyB_mem(const ir_node *node);
void set_CopyB_mem(ir_node *node, ir_node *mem);
ir_node *get_CopyB_dst(const ir_node *node);
void set_CopyB_dst(ir_node *node, ir_node *dst);
ir_node *get_CopyB_src(const ir_node *node);
void set_CopyB_src(ir_node *node, ir_node *src);

ir_type* get_CopyB_type(const ir_node *node);

ir_volatility get_CopyB_volatility(const ir_node *node);
ir_op *get_op_CopyB(void);

ir_op *get_op_Deleted(void);

ir_node *new_rd_Div(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_left, ir_node * irn_right, int pinned);

ir_node *get_Div_mem(const ir_node *node);
void set_Div_mem(ir_node *node, ir_node *mem);
ir_node *get_Div_left(const ir_node *node);
void set_Div_left(ir_node *node, ir_node *left);
ir_node *get_Div_right(const ir_node *node);
void set_Div_right(ir_node *node, ir_node *right);

ir_mode* get_Div_resmode(const ir_node *node);

int get_Div_no_remainder(const ir_node *node);
ir_op *get_op_Div(void);

ir_node *new_rd_Dummy(dbg_info *dbgi, ir_graph *irg, ir_mode * mode);

ir_op *get_op_Dummy(void);

ir_node *new_rd_End(dbg_info *dbgi, ir_graph *irg, int arity, ir_node *const * in);

int get_End_n_keepalives(ir_node const *node);
ir_node *get_End_keepalive(ir_node const *node, int pos);
void set_End_keepalive(ir_node *node, int pos, ir_node *keepalive);
ir_node **get_End_keepalive_arr(ir_node *node);ir_op *get_op_End(void);

ir_node *new_rd_Eor(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Eor_left(const ir_node *node);
void set_Eor_left(ir_node *node, ir_node *left);
ir_node *get_Eor_right(const ir_node *node);
void set_Eor_right(ir_node *node, ir_node *right);
ir_op *get_op_Eor(void);

ir_node *new_rd_Free(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_ptr);

ir_node *get_Free_mem(const ir_node *node);
void set_Free_mem(ir_node *node, ir_node *mem);
ir_node *get_Free_ptr(const ir_node *node);
void set_Free_ptr(ir_node *node, ir_node *ptr);
ir_op *get_op_Free(void);

ir_node *new_rd_IJmp(dbg_info *dbgi, ir_node *block, ir_node * irn_target);

ir_node *get_IJmp_target(const ir_node *node);
void set_IJmp_target(ir_node *node, ir_node *target);
ir_op *get_op_IJmp(void);

ir_node *get_Id_pred(const ir_node *node);
void set_Id_pred(ir_node *node, ir_node *pred);
ir_op *get_op_Id(void);

ir_node *new_rd_Jmp(dbg_info *dbgi, ir_node *block);

ir_op *get_op_Jmp(void);

ir_node *new_rd_Load(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_ptr, ir_mode* mode, ir_type* type, ir_cons_flags flags);

ir_node *get_Load_mem(const ir_node *node);
void set_Load_mem(ir_node *node, ir_node *mem);
ir_node *get_Load_ptr(const ir_node *node);
void set_Load_ptr(ir_node *node, ir_node *ptr);

ir_mode* get_Load_mode(const ir_node *node);

ir_type* get_Load_type(const ir_node *node);

ir_volatility get_Load_volatility(const ir_node *node);

ir_align get_Load_unaligned(const ir_node *node);
ir_op *get_op_Load(void);

ir_node *new_rd_Member(dbg_info *dbgi, ir_node *block, ir_node * irn_ptr, ir_entity* entity);

ir_node *get_Member_ptr(const ir_node *node);
void set_Member_ptr(ir_node *node, ir_node *ptr);

ir_entity* get_Member_entity(const ir_node *node);
ir_op *get_op_Member(void);

ir_node *new_rd_Minus(dbg_info *dbgi, ir_node *block, ir_node * irn_op);

ir_node *get_Minus_op(const ir_node *node);
void set_Minus_op(ir_node *node, ir_node *op);
ir_op *get_op_Minus(void);

ir_node *new_rd_Mod(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_left, ir_node * irn_right, int pinned);

ir_node *get_Mod_mem(const ir_node *node);
void set_Mod_mem(ir_node *node, ir_node *mem);
ir_node *get_Mod_left(const ir_node *node);
void set_Mod_left(ir_node *node, ir_node *left);
ir_node *get_Mod_right(const ir_node *node);
void set_Mod_right(ir_node *node, ir_node *right);

ir_mode* get_Mod_resmode(const ir_node *node);
ir_op *get_op_Mod(void);

ir_node *new_rd_Mul(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Mul_left(const ir_node *node);
void set_Mul_left(ir_node *node, ir_node *left);
ir_node *get_Mul_right(const ir_node *node);
void set_Mul_right(ir_node *node, ir_node *right);
ir_op *get_op_Mul(void);

ir_node *new_rd_Mulh(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Mulh_left(const ir_node *node);
void set_Mulh_left(ir_node *node, ir_node *left);
ir_node *get_Mulh_right(const ir_node *node);
void set_Mulh_right(ir_node *node, ir_node *right);
ir_op *get_op_Mulh(void);

ir_node *new_rd_Mux(dbg_info *dbgi, ir_node *block, ir_node * irn_sel, ir_node * irn_false, ir_node * irn_true);

ir_node *get_Mux_sel(const ir_node *node);
void set_Mux_sel(ir_node *node, ir_node *sel);
ir_node *get_Mux_false(const ir_node *node);
void set_Mux_false(ir_node *node, ir_node *false_);
ir_node *get_Mux_true(const ir_node *node);
void set_Mux_true(ir_node *node, ir_node *true_);
ir_op *get_op_Mux(void);

ir_node *new_rd_NoMem(dbg_info *dbgi, ir_graph *irg);

ir_op *get_op_NoMem(void);

ir_node *new_rd_Not(dbg_info *dbgi, ir_node *block, ir_node * irn_op);

ir_node *get_Not_op(const ir_node *node);
void set_Not_op(ir_node *node, ir_node *op);
ir_op *get_op_Not(void);

ir_node *new_rd_Offset(dbg_info *dbgi, ir_graph *irg, ir_mode * mode, ir_entity* entity);


ir_entity* get_Offset_entity(const ir_node *node);
ir_op *get_op_Offset(void);

ir_node *new_rd_Or(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Or_left(const ir_node *node);
void set_Or_left(ir_node *node, ir_node *left);
ir_node *get_Or_right(const ir_node *node);
void set_Or_right(ir_node *node, ir_node *right);
ir_op *get_op_Or(void);

ir_node *new_rd_Phi(dbg_info *dbgi, ir_node *block, int arity, ir_node *const * in, ir_mode * mode);

int get_Phi_n_preds(ir_node const *node);
ir_node *get_Phi_pred(ir_node const *node, int pos);
void set_Phi_pred(ir_node *node, int pos, ir_node *pred);
ir_node **get_Phi_pred_arr(ir_node *node);
int get_Phi_loop(const ir_node *node);
ir_op *get_op_Phi(void);

ir_node *new_rd_Pin(dbg_info *dbgi, ir_node *block, ir_node * irn_op);

ir_node *get_Pin_op(const ir_node *node);
void set_Pin_op(ir_node *node, ir_node *op);
ir_op *get_op_Pin(void);

ir_node *new_rd_Proj(dbg_info *dbgi, ir_node * irn_pred, ir_mode * mode, unsigned num);

ir_node *get_Proj_pred(const ir_node *node);
void set_Proj_pred(ir_node *node, ir_node *pred);

unsigned get_Proj_num(const ir_node *node);
ir_op *get_op_Proj(void);

ir_node *new_rd_Raise(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_exo_ptr);

ir_node *get_Raise_mem(const ir_node *node);
void set_Raise_mem(ir_node *node, ir_node *mem);
ir_node *get_Raise_exo_ptr(const ir_node *node);
void set_Raise_exo_ptr(ir_node *node, ir_node *exo_ptr);
ir_op *get_op_Raise(void);

ir_node *new_rd_Return(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, int arity, ir_node *const * in);

ir_node *get_Return_mem(const ir_node *node);
void set_Return_mem(ir_node *node, ir_node *mem);
int get_Return_n_ress(ir_node const *node);
ir_node *get_Return_res(ir_node const *node, int pos);
void set_Return_res(ir_node *node, int pos, ir_node *res);
ir_node **get_Return_res_arr(ir_node *node);ir_op *get_op_Return(void);

ir_node *new_rd_Sel(dbg_info *dbgi, ir_node *block, ir_node * irn_ptr, ir_node * irn_index, ir_type* type);

ir_node *get_Sel_ptr(const ir_node *node);
void set_Sel_ptr(ir_node *node, ir_node *ptr);
ir_node *get_Sel_index(const ir_node *node);
void set_Sel_index(ir_node *node, ir_node *index);

ir_type* get_Sel_type(const ir_node *node);
ir_op *get_op_Sel(void);

ir_node *new_rd_Shl(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Shl_left(const ir_node *node);
void set_Shl_left(ir_node *node, ir_node *left);
ir_node *get_Shl_right(const ir_node *node);
void set_Shl_right(ir_node *node, ir_node *right);
ir_op *get_op_Shl(void);

ir_node *new_rd_Shr(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Shr_left(const ir_node *node);
void set_Shr_left(ir_node *node, ir_node *left);
ir_node *get_Shr_right(const ir_node *node);
void set_Shr_right(ir_node *node, ir_node *right);
ir_op *get_op_Shr(void);

ir_node *new_rd_Shrs(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Shrs_left(const ir_node *node);
void set_Shrs_left(ir_node *node, ir_node *left);
ir_node *get_Shrs_right(const ir_node *node);
void set_Shrs_right(ir_node *node, ir_node *right);
ir_op *get_op_Shrs(void);

ir_node *new_rd_Size(dbg_info *dbgi, ir_graph *irg, ir_mode * mode, ir_type* type);


ir_type* get_Size_type(const ir_node *node);
ir_op *get_op_Size(void);

ir_node *new_rd_Start(dbg_info *dbgi, ir_graph *irg);

ir_op *get_op_Start(void);

ir_node *new_rd_Store(dbg_info *dbgi, ir_node *block, ir_node * irn_mem, ir_node * irn_ptr, ir_node * irn_value, ir_type* type, ir_cons_flags flags);

ir_node *get_Store_mem(const ir_node *node);
void set_Store_mem(ir_node *node, ir_node *mem);
ir_node *get_Store_ptr(const ir_node *node);
void set_Store_ptr(ir_node *node, ir_node *ptr);
ir_node *get_Store_value(const ir_node *node);
void set_Store_value(ir_node *node, ir_node *value);

ir_type* get_Store_type(const ir_node *node);

ir_volatility get_Store_volatility(const ir_node *node);

ir_align get_Store_unaligned(const ir_node *node);
ir_op *get_op_Store(void);

ir_node *new_rd_Sub(dbg_info *dbgi, ir_node *block, ir_node * irn_left, ir_node * irn_right);

ir_node *get_Sub_left(const ir_node *node);
void set_Sub_left(ir_node *node, ir_node *left);
ir_node *get_Sub_right(const ir_node *node);
void set_Sub_right(ir_node *node, ir_node *right);
ir_op *get_op_Sub(void);

ir_node *new_rd_Switch(dbg_info *dbgi, ir_node *block, ir_node * irn_selector, unsigned n_outs, ir_switch_table* table);

ir_node *get_Switch_selector(const ir_node *node);
void set_Switch_selector(ir_node *node, ir_node *selector);

unsigned get_Switch_n_outs(const ir_node *node);

ir_switch_table* get_Switch_table(const ir_node *node);
ir_op *get_op_Switch(void);

ir_node *new_rd_Sync(dbg_info *dbgi, ir_node *block, int arity, ir_node *const * in);

int get_Sync_n_preds(ir_node const *node);
ir_node *get_Sync_pred(ir_node const *node, int pos);
void set_Sync_pred(ir_node *node, int pos, ir_node *pred);
ir_node **get_Sync_pred_arr(ir_node *node);ir_op *get_op_Sync(void);

ir_node *new_rd_Tuple(dbg_info *dbgi, ir_node *block, int arity, ir_node *const * in);

int get_Tuple_n_preds(ir_node const *node);
ir_node *get_Tuple_pred(ir_node const *node, int pos);
void set_Tuple_pred(ir_node *node, int pos, ir_node *pred);
ir_node **get_Tuple_pred_arr(ir_node *node);ir_op *get_op_Tuple(void);

ir_node *new_rd_Unknown(dbg_info *dbgi, ir_graph *irg, ir_mode * mode);

ir_op *get_op_Unknown(void);
