ident *id_unique(const char *tag);
void ir_init(void);
ident *new_id_from_str(const char *str);
ident *new_id_from_chars(const char *str, size_t len);
ident *new_id_fmt(char const *fmt, ...);
const char *get_id_str(ident *id);
unsigned get_irn_opcode(const ir_node *node);
unsigned get_op_code(const ir_op *op);

/* used in extras.py,operations.py */
/* missing: get_ASM_n_input_ */

size_t get_ASM_n_clobbers(const ir_node *node);
size_t get_ASM_n_output_constraints(const ir_node *node);
ir_node *new_rd_ASM(dbg_info *db, ir_node *block, ir_node *mem,
                    int arity, ir_node *in[], ir_asm_constraint *inputs,
                    size_t n_outs, ir_asm_constraint *outputs,
                    size_t n_clobber, ident *clobber[],
                    ident *asm_text);
