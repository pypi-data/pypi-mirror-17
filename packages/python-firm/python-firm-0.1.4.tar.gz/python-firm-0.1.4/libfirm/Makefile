# libfirm Makefile
#
# This is currently experimental and not fully supported, but we plan to replace
# the jambuild with this at some point in the future.
#
# Most variable names are similar to the names used by autoconf...
-include config.mak

# Some build configuration defaults
top_srcdir   ?= .
top_builddir ?= build
variant      ?= debug

srcdir       ?= $(top_srcdir)
builddir     ?= $(top_builddir)/$(variant)
gendir       ?= $(top_builddir)/gen
docdir       ?= $(top_builddir)/doc

# This hides the noisy commandline outputs. Show them with "make V=1"
ifneq ($(V),1)
Q ?= @
endif

# Tools
CC ?= cc
DOXYGEN ?= doxygen
LINK ?= $(CC)
AR ?= ar
DLLEXT ?= .so

# Variants
CFLAGS_debug       = -O0 -g3 -DDEBUG_libfirm
CFLAGS_profile     = -O3 -pg -DNDEBUG -fno-inline
CFLAGS_coverage    = -O0 --coverage -DDEBUG_libfirm
CFLAGS_optimize    = -O3 -fomit-frame-pointer -DNDEBUG
LINKFLAGS_debug    =
LINKFLAGS_profile  = -pg
LINKFLAGS_coverage = --coverage

# General flags
CPPFLAGS  ?=
CFLAGS    += $(CFLAGS_$(variant)) -std=c99 -fPIC -DHAVE_FIRM_REVISION_H
CFLAGS    += -Wall -W -Wextra -Wstrict-prototypes -Wmissing-prototypes -Wwrite-strings
LINKFLAGS += $(LINKFLAGS_$(variant)) -lm
VPATH = $(srcdir) $(gendir)

all: firm
.PHONY: all

# disable make builtin suffix rules
.SUFFIXES:

# libFirm
libfirm_SOURCES     = $(subst $(srcdir)/,,$(wildcard $(srcdir)/ir/*/*.c))
libfirm_GEN_SOURCES =
libfirm_DIRS        = $(sort $(dir $(libfirm_SOURCES))) include/libfirm include/libfirm/adt
libfirm_GEN_DIRS    = $(sort $(dir $(libfirm_GEN_SOURCES)))
libfirm_INCLUDEDIRS = $(addprefix $(srcdir)/, $(libfirm_DIRS)) $(addprefix $(gendir)/, $(libfirm_GEN_DIRS))
libfirm_a           = $(builddir)/libfirm.a
libfirm_dll         = $(builddir)/libfirm$(DLLEXT)
libfirm_CPPFLAGS    = $(foreach dir,$(libfirm_INCLUDEDIRS),-I$(dir))
libfirm_OBJECTS     = $(libfirm_SOURCES:%.c=$(builddir)/%.o) $(libfirm_GEN_SOURCES:%.c=$(builddir)/%.o)
libfirm_DEPS        = $(libfirm_OBJECTS:%.o=%.d)
libfirm_BUILDDIRS   = $(sort $(dir $(libfirm_OBJECTS))) $(addprefix $(gendir)/, $(libfirm_GEN_DIRS))

.PHONY: firm
firm: $(libfirm_dll) $(libfirm_a)

# backends
backends = amd64 arm ia32 sparc TEMPLATE

EMITTER_GENERATOR = $(srcdir)/ir/be/scripts/generate_emitter.pl
REGALLOC_IF_GENERATOR = $(srcdir)/ir/be/scripts/generate_regalloc_if.pl
OPCODES_GENERATOR = $(srcdir)/ir/be/scripts/generate_new_opcodes.pl

define backend_template
$(1)_SOURCES = $$(subst $$(srcdir)/,,$$(wildcard $$(srcdir)/ir/be/$(1)/*.c))
$(1)_GEN_HEADERS =

$(1)_SPEC = ir/be/$(1)/$(1)_spec.pl

$$(gendir)/ir/be/$(1)/gen_$(1)_emitter.h $$(gendir)/ir/be/$(1)/gen_$(1)_emitter.c: $$($(1)_SPEC) $$(EMITTER_GENERATOR)
	@echo GEN $$@
	$(Q)$$(EMITTER_GENERATOR) $$< $$(gendir)/ir/be/$(1)
$(1)_GEN_SOURCES += ir/be/$(1)/gen_$(1)_emitter.c
$(1)_GEN_HEADERS += $$(gendir)/ir/be/$(1)/gen_$(1)_emitter.h

$$(gendir)/ir/be/$(1)/gen_$(1)_regalloc_if.h $$(gendir)/ir/be/$(1)/gen_$(1)_regalloc_if.c: $$($(1)_SPEC) $$(REGALLOC_IF_GENERATOR)
	@echo GEN $$@
	$(Q)$$(REGALLOC_IF_GENERATOR) $$< $$(gendir)/ir/be/$(1)
$(1)_GEN_SOURCES += ir/be/$(1)/gen_$(1)_regalloc_if.c
$(1)_GEN_HEADERS += $$(gendir)/ir/be/$(1)/gen_$(1)_regalloc_if.h

$$(gendir)/ir/be/$(1)/gen_$(1)_new_nodes.h $$(gendir)/ir/be/$(1)/gen_$(1)_new_nodes.c: $$($(1)_SPEC) $$(OPCODES_GENERATOR)
	@echo GEN $$@
	$(Q)$$(OPCODES_GENERATOR) $$< $$(gendir)/ir/be/$(1)
$(1)_GEN_SOURCES += ir/be/$(1)/gen_$(1)_new_nodes.c
$(1)_GEN_HEADERS += $$(gendir)/ir/be/$(1)/gen_$(1)_new_nodes.h

# We need to inform make of the headers it doesn't know yet...
$(1)_OBJECTS = $$($(1)_SOURCES:%.c=$$(builddir)/%.o) $$($(1)_GEN_SOURCES:%.c=$$(builddir)/%.o)
$$($(1)_OBJECTS): $$($(1)_GEN_HEADERS)

libfirm_GEN_SOURCES += $$($(1)_GEN_SOURCES)
libfirm_SOURCES += $$($1_SOURCES)
endef

$(foreach backend,$(backends),$(eval $(call backend_template,$(backend))))

# generators
IR_SPEC_GENERATED_INCLUDES := \
	$(gendir)/include/libfirm/nodes.h \
	$(gendir)/ir/ir/gen_proj_names.h  \
	$(gendir)/ir/ir/gen_irnode.h
IR_SPEC_GENERATOR := $(srcdir)/scripts/gen_ir.py
IR_SPEC_GENERATOR_DEPS := $(IR_SPEC_GENERATOR) $(srcdir)/scripts/jinjautil.py $(srcdir)/scripts/irops.py $(srcdir)/scripts/filters.py
IR_SPEC := $(srcdir)/scripts/ir_spec.py
libfirm_BUILDDIRS += $(gendir)/include/libfirm

libfirm_GEN_SOURCES += \
	ir/ir/gen_irnode.c \
	ir/ir/gen_irio.c
$(builddir)/ir/ir/gen_irnode.o: $(gendir)/ir/ir/gen_irnode.c
$(builddir)/ir/ir/gen_irio.o: $(gendir)/ir/ir/gen_irio.c

$(gendir)/ir/ir/% : scripts/templates/% $(IR_SPEC_GENERATOR_DEPS) $(IR_SPEC)
	@echo GEN $@
	$(Q)$(IR_SPEC_GENERATOR) $(IR_SPEC) "$<" > "$@"

$(gendir)/include/libfirm/% : scripts/templates/% $(IR_SPEC_GENERATOR_DEPS) $(IR_SPEC)
	@echo GEN $@
	$(Q)$(IR_SPEC_GENERATOR) $(IR_SPEC) "$<" > "$@"

libfirm_GEN_DIRS += ir/ir include/libfirm

$(libfirm_a): $(libfirm_OBJECTS)
	@echo AR $@
	$(Q)rm -f $@
	$(Q)$(AR) -crs $@ $^

$(libfirm_dll): $(libfirm_OBJECTS)
	@echo LINK $@
	$(Q)$(LINK) -shared $^ -o $@ $(LINKFLAGS)

# Determine if we can use cparser-beta for quickcheck
QUICKCHECK_DEFAULT := $(shell which cparser-beta 2> /dev/null || echo true) -fsyntax-only
QUICKCHECK ?= $(QUICKCHECK_DEFAULT)
QUICKCHECK_FLAGS ?= -m32 -Wno-compat-option -Wno-shadow -Wno-shadow-local -Wunreachable-code

$(builddir)/%.o: %.c $(IR_SPEC_GENERATED_INCLUDES)
	@echo CC $@
	$(Q)$(QUICKCHECK) $(QUICKCHECK_FLAGS) $(CFLAGS) $(CPPFLAGS) $(libfirm_CPPFLAGS) $(QUICKCHECK_FLAGS) $<
	$(Q)$(CC) $(CFLAGS) $(CPPFLAGS) $(libfirm_CPPFLAGS) -MP -MMD -c -o $@ $<

$(docdir)/libfirm.tag: doc/Doxyfile doc/logo.png $(IR_SPEC_GENERATED_INCLUDES) $(wildcard include/libfirm/*.h) $(wildcard include/libfirm/adt/*.h)
	@echo Doxygen $@
	$(Q)$(DOXYGEN) $<

DOCU_TEMPLATE = $(srcdir)/scripts/templates/nodes.html
DOCU_TEMPLATE_DEPS = $(srcdir)/scripts/templates/style.css
$(docdir)/html/nodes.html: $(docdir)/libfirm.tag $(IR_SPEC_GENERATOR) $(IR_SPEC_GENERATOR_DEPS) $(IR_SPEC) $(DOCU_TEMPLATE) $(DOCU_TEMPLATE_DEPS)
	@echo GEN $@
	$(Q)$(IR_SPEC_GENERATOR) $(IR_SPEC) $(DOCU_TEMPLATE) --tagfile $(docdir)/libfirm.tag > $@
	$(Q)cp $(DOCU_TEMPLATE_DEPS) $(docdir)/html

NODES_TEMPLATE = firm-homepage/nodes_templates/Nodes
$(docdir)/Nodes: $(docdir)/libfirm.tag $(IR_SPEC_GENERATOR) $(IR_SPEC_GENERATOR_DEPS) $(IR_SPEC) $(NODES_TEMPLATE)
	@echo GEN $@
	$(Q)$(IR_SPEC_GENERATOR) $(IR_SPEC) $(NODES_TEMPLATE) --tagfile $(docdir)/libfirm.tag -I $(dir $(NODES_TEMPLATE)) > $@

.PHONY: doc
doc: $(docdir)/libfirm.tag $(docdir)/html/nodes.html

.PHONY: clean
clean:
	@echo CLEAN
	$(Q)rm -fr $(builddir) $(gendir) $(docdir)

.PHONY: install
PREFIX ?= /usr/local
INSTALL ?= install
INSTALLPREFIX = $(DESTDIR)$(PREFIX)
install: $(libfirm_a) $(libfirm_dll)
	$(INSTALL) -d "$(INSTALLPREFIX)/include/libfirm"
	$(INSTALL) -m0644 include/libfirm/*.h "$(INSTALLPREFIX)/include/libfirm"
	$(INSTALL) -m0644 "$(gendir)"/include/libfirm/*.h "$(INSTALLPREFIX)/include/libfirm"
	$(INSTALL) -d "$(INSTALLPREFIX)/include/libfirm/adt"
	$(INSTALL) -m0644 include/libfirm/adt/*.h "$(INSTALLPREFIX)/include/libfirm/adt"
	$(INSTALL) -d "$(INSTALLPREFIX)/lib"
	$(INSTALL) -m0644 $^ "$(INSTALLPREFIX)/lib"

# Ensure all output directories are created
UNUSED1 := $(shell mkdir -p $(libfirm_BUILDDIRS))

REVISION ?= $(shell git --git-dir $(top_srcdir)/.git describe --abbrev=40 --always --dirty --match '')

# Update revision.h if necessary
REVISIONH = $(gendir)/firm_revision.h
libfirm_INCLUDEDIRS += $(gendir)
UNUSED2 := $(shell \
	REV="\#define libfirm_VERSION_REVISION \"$(REVISION)\""; \
	echo "$$REV" | cmp -s - "$(REVISIONH)" 2> /dev/null || echo "$$REV" > "$(REVISIONH)" \
)

# Unit tests
UNITTESTS_SOURCES = $(subst $(srcdir)/unittests/,,$(wildcard $(srcdir)/unittests/*.c))
UNITTESTS         = $(UNITTESTS_SOURCES:%.c=$(builddir)/%.exe)
UNITTESTS_OK      = $(UNITTESTS_SOURCES:%.c=$(builddir)/%.ok)

$(builddir)/%.exe: $(srcdir)/unittests/%.c $(libfirm_a)
	@echo LINK $<
	$(Q)$(LINK) $(CFLAGS) $(CPPFLAGS) $(libfirm_CPPFLAGS) "$<" $(libfirm_a) -lm -o "$@"

$(builddir)/%.ok: $(builddir)/%.exe
	@echo EXEC $<
	$(Q)$< && touch "$@"

.PRECIOUS: $(UNITTESTS)
.PHONY: test
test: $(UNITTESTS_OK)

-include $(libfirm_DEPS)
