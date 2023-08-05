extern "Python" {
  void plf_merge_pair(ir_node *new_node, ir_node *old_node,
                      dbg_action action);
  void plf_merge_sets(ir_node *const *new_node_array,
                      int new_num_entries,
                      ir_node *const *old_node_array,
                      int old_num_entries, dbg_action action);
  src_loc_t plf_retrieve_dbg(dbg_info const *dbg);
  void plf_retrieve_type_dbg(char *buffer, size_t buffer_size,
                               const type_dbg_info *tdbgi);
}

void dbg_init(void(*dbg_info_merge_pair)(ir_node *new_node, ir_node *old_node,
                                         dbg_action action),
              void(*dbg_info_merge_sets)(ir_node *const *new_node_array,
                                         int new_num_entries,
                                         ir_node *const *old_node_array,
                                         int old_num_entries,
                                         dbg_action action));

void ir_set_debug_retrieve(src_loc_t(*func)(dbg_info const *dbg));
void ir_set_type_debug_retrieve(void(*func)(char *buffer, size_t buffer_size,
                                            const type_dbg_info *tdbgi));
