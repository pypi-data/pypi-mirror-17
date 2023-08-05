ir_initializer_kind_t get_initializer_kind(const ir_initializer_t *initializer);
const char *get_initializer_kind_name(ir_initializer_kind_t ini);
ir_initializer_t *get_initializer_null(void);
ir_initializer_t *create_initializer_const(ir_node *value);
ir_initializer_t *create_initializer_tarval(ir_tarval *tv);
ir_node *get_initializer_const_value(const ir_initializer_t *initializer);
ir_tarval *get_initializer_tarval_value(const ir_initializer_t *initialzier);
ir_initializer_t *create_initializer_compound(size_t n_entries);
size_t get_initializer_compound_n_entries(const ir_initializer_t *initializer);
void set_initializer_compound_value(ir_initializer_t *initializer,
                                    size_t index, ir_initializer_t *value);
ir_initializer_t *get_initializer_compound_value(
                const ir_initializer_t *initializer, size_t index);
void set_entity_initializer(ir_entity *entity, ir_initializer_t *initializer);
ir_initializer_t *get_entity_initializer(const ir_entity *entity);

