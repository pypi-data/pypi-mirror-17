int is_alias_entity(const ir_entity *ent);
int is_compound_entity(const ir_entity *ent);
int is_method_entity(const ir_entity *ent);
int is_parameter_entity(const ir_entity *entity);
int is_unknown_entity(const ir_entity *entity);

ir_entity *new_entity(ir_type *owner, ident *name, ir_type *tp);
ir_entity *new_global_entity(ir_type *segment, ident *name, ir_type *tp,
                             ir_visibility vis, ir_linkage linkage);
int check_entity(const ir_entity *ent);
ir_entity *clone_entity(ir_entity const *old, ident *name, ir_type *owner);
int entity_has_definition(const ir_entity *entity);
int entity_has_ld_ident(const ir_entity *entity);
int entity_has_additional_properties(const ir_entity *entity);
int entity_is_externally_visible(const ir_entity *entity);
void free_entity(ir_entity *ent);

mtp_additional_properties get_entity_additional_properties(const ir_entity *ent);
ir_entity *get_entity_alias(const ir_entity *alias);
ir_align get_entity_aligned(const ir_entity *ent);
unsigned get_entity_alignment(const ir_entity *entity);
unsigned get_entity_bitfield_offset(const ir_entity *entity);
unsigned get_entity_bitfield_size(const ir_entity *entity);
dbg_info *get_entity_dbg_info(const ir_entity *ent);
ident *get_entity_ident(const ir_entity *ent);
ir_graph *get_entity_irg(const ir_entity *ent);
ir_label_t get_entity_label(const ir_entity *ent);
ident *get_entity_ld_ident(const ir_entity *ent);
const char *get_entity_ld_name(const ir_entity *ent);
ir_linkage get_entity_linkage(const ir_entity *entity);
const char *get_entity_name(const ir_entity *ent);
int get_entity_offset(const ir_entity *entity);
ir_type *get_entity_owner(const ir_entity *ent);
size_t get_entity_parameter_number(const ir_entity *entity);
ir_type *get_entity_type(const ir_entity *ent);
ir_entity_usage get_entity_usage(const ir_entity *ent);
ir_visibility get_entity_visibility(const ir_entity *entity);
ir_visited_t get_entity_visited(const ir_entity *ent);
ir_volatility get_entity_volatility(const ir_entity *ent);
unsigned get_entity_vtable_number(const ir_entity *ent);
ir_entity *get_unknown_entity(void);

void mark_entity_visited(ir_entity *ent);

void set_entity_additional_properties(ir_entity *ent,
                                      mtp_additional_properties prop);
void set_entity_alias(ir_entity *alias, ir_entity *aliased);
void set_entity_alignment(ir_entity *entity, unsigned alignment);
void set_entity_aligned(ir_entity *ent, ir_align a);
void set_entity_bitfield_offset(ir_entity *entity, unsigned offset);
void set_entity_dbg_info(ir_entity *ent, dbg_info *db);
void set_entity_ident(ir_entity *ent, ident *id);
/* missing: set_entity_irg */
void set_entity_label(ir_entity *ent, ir_label_t label);
void set_entity_ld_ident(ir_entity *ent, ident *ld_ident);
void set_entity_linkage(ir_entity *entity, ir_linkage linkage);
void set_entity_offset(ir_entity *entity, int offset);
void set_entity_owner(ir_entity *ent, ir_type *owner);
void set_entity_parameter_number(ir_entity *entity, size_t n);
void set_entity_type(ir_entity *ent, ir_type *tp);
void set_entity_usage(ir_entity *ent, ir_entity_usage flag);
void set_entity_visibility(ir_entity *entity, ir_visibility visibility);
void set_entity_visited(ir_entity *ent, ir_visited_t num);
void set_entity_volatility(ir_entity *ent, ir_volatility vol);
void set_entity_vtable_number(ir_entity *ent, unsigned vtable_number);
