void add_Block_phi(ir_node *block, ir_node *phi);
void add_immBlock_pred(ir_node *immblock, ir_node *jmp);
void add_irg_constraints(ir_graph *irg,
                         ir_graph_constraints_t constraints);
void add_irg_properties(ir_graph *irg, ir_graph_properties_t props);
void assure_irg_properties(ir_graph *irg, ir_graph_properties_t props);
void clear_irg_constraints(ir_graph *irg,
                           ir_graph_constraints_t constraints);
void clear_irg_properties(ir_graph *irg, ir_graph_properties_t props);
void confirm_irg_properties(ir_graph *irg, ir_graph_properties_t props);
ir_entity *create_Block_entity(ir_node *block);
void free_ir_graph(ir_graph *irg);
ir_node *get_idx_irn(const ir_graph *irg, unsigned idx);

ir_node *get_irg_args(const ir_graph *irg);
ir_visited_t get_irg_block_visited(const ir_graph *irg);
ir_entity *get_irg_entity(const ir_graph *irg);
ir_node *get_irg_end(const ir_graph *irg);
ir_node *get_irg_end_block(const ir_graph *irg);
ir_node *get_irg_frame(const ir_graph *irg);
ir_type *get_irg_frame_type(ir_graph *irg);
long get_irg_graph_nr(const ir_graph *irg);
ir_node *get_irg_initial_mem(const ir_graph *irg);
unsigned get_irg_last_idx(const ir_graph *irg);
void *get_irg_link(const ir_graph *irg);
void *get_irg_loc_description(ir_graph *irg, int n);
int get_irg_n_locs(ir_graph *irg);
ir_node *get_irg_no_mem(const ir_graph *irg);
op_pin_state get_irg_pinned(const ir_graph *irg);
ir_node *get_irg_start(const ir_graph *irg);
ir_node *get_irg_start_block(const ir_graph *irg);
ir_visited_t get_irg_visited(const ir_graph *irg);

ir_visited_t get_max_irg_visited(void);
ir_node *get_r_cur_block(ir_graph *irg);
ir_node *get_r_store(ir_graph *irg);
ir_node *get_r_value(ir_graph *irg, int pos, ir_mode *mode);
/* missing: has_irg_properties */
void inc_irg_visited(ir_graph *irg);
ir_visited_t inc_max_irg_visited(void);
void ir_free_resources(ir_graph *irg, ir_resources_t resources);
void ir_reserve_resources(ir_graph *irg, ir_resources_t resources);
ir_resources_t ir_resources_reserved(const ir_graph *irg);
void irg_finalize_cons(ir_graph *irg);
int irg_is_constrained(const ir_graph *irg,
                       ir_graph_constraints_t constraints);
int irg_verify(ir_graph *irg);
void mature_immBlock(ir_node *block);
ir_graph *new_ir_graph(ir_entity *ent, int n_loc);

void set_irg_args(ir_graph *irg, ir_node *node);
void set_irg_block_visited(ir_graph *irg, ir_visited_t i);
void set_irg_entity(ir_graph *irg, ir_entity *ent);
void set_irg_end(ir_graph *irg, ir_node *node);
void set_irg_end_block(ir_graph *irg, ir_node *node);
void set_irg_frame_type(ir_graph *irg, ir_type *ftp);
void set_irg_frame(ir_graph *irg, ir_node *node);
void set_irg_initial_mem(ir_graph *irg, ir_node *node);
void set_irg_link(ir_graph *irg, void *thing);
void set_irg_loc_description(ir_graph *irg, int n, void *description);
void set_irg_no_mem(ir_graph *irg, ir_node *node);
void set_irg_start(ir_graph *irg, ir_node *node);
void set_irg_start_block(ir_graph *irg, ir_node *node);
void set_irg_visited(ir_graph *irg, ir_visited_t i);

void set_max_irg_visited(int val);
void set_r_cur_block(ir_graph *irg, ir_node *target);
void set_r_store(ir_graph *irg, ir_node *store);
void set_r_value(ir_graph *irg, int pos, ir_node *value);

