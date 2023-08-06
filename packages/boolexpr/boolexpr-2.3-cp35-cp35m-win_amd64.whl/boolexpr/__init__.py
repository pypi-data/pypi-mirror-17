# Copyright 2016 Chris Drake
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
BoolExpr is an open source library for symbolic Boolean Algebra.

Data Types:

abstract syntax tree
   A nested tuple of entries that represents an expression.
   Unlike a ``BoolExpr`` object, an ast object is serializable.

   It is defined recursively::

      ast := (BoolExpr.Kind.zero, )
           | (BoolExpr.Kind.one, )
           | (BoolExpr.Kind.log, )
           | (BoolExpr.Kind.comp, ctx, name)
           | (BoolExpr.Kind.var, ctx, name)
           | (BoolExpr.Kind.nor, ast, ...)
           | (BoolExpr.Kind.or_, ast, ...)
           | (BoolExpr.Kind.nand, ast, ...)
           | (BoolExpr.Kind.and_, ast, ...)
           | (BoolExpr.Kind.xnor, ast, ...)
           | (BoolExpr.Kind.xor, ast, ...)
           | (BoolExpr.Kind.neq, ast, ...)
           | (BoolExpr.Kind.eq, ast, ...)
           | (BoolExpr.Kind.nimpl, ast, ast)
           | (BoolExpr.Kind.impl, ast, ast)
           | (BoolExpr.Kind.nite, ast, ast, ast)
           | (BoolExpr.Kind.ite, ast, ast, ast)

      ctx := int

      name := str

   The ``ctx`` int is a pointer to a C++ Context object.
   It must be re-cast to ``void *`` before being used.

point
   A dictionary of ``{Variable : Constant}`` mappings.
   For example, ``{a: False, b: True, c: 0, d: 'X'}``.

var2bx
   A dictionary of ``{Variable : BoolExpr}`` mappings.
   For example, ``{a: False, b: ~p | q}``.
"""


# pylint: skip-file


from cffi import FFI
import importlib


HEADER = """

typedef char const * const STRING;
typedef void * const CONTEXT;
typedef void const * const BX;
typedef void const * const LIT;
typedef void * const ARRAY;
typedef void * const ARRAY_PAIR;
typedef void const * const * const BXS;
typedef void const * const * const VARS;
typedef void const * const * const CONSTS;
typedef void * const VEC;
typedef void * const VARSET;
typedef void * const POINT;
typedef void * const SOLN;
typedef void * const DFS_ITER;
typedef void * const SAT_ITER;
typedef void * const POINTS_ITER;
typedef void * const TERMS_ITER;
typedef void * const DOM_ITER;
typedef void * const CF_ITER;

enum Kind {
    ZERO  = 0x00,   // 0 0000
    ONE   = 0x01,   // 0 0001
    LOG   = 0x04,   // 0 0100
    ILL   = 0x06,   // 0 0110
    COMP  = 0x08,   // 0 1000
    VAR   = 0x09,   // 0 1001
    NOR   = 0x10,   // 1 0000
    OR    = 0x11,   // 1 0001
    NAND  = 0x12,   // 1 0010
    AND   = 0x13,   // 1 0011
    XNOR  = 0x14,   // 1 0100
    XOR   = 0x15,   // 1 0101
    NEQ   = 0x16,   // 1 0110
    EQ    = 0x17,   // 1 0111
    NIMPL = 0x18,   // 1 1000
    IMPL  = 0x19,   // 1 1001
    NITE  = 0x1A,   // 1 1010
    ITE   = 0x1B,   // 1 1011
};

CONTEXT boolexpr_Context_new(void);
void boolexpr_Context_del(CONTEXT);
BX boolexpr_Context_get_var(CONTEXT, STRING);

void boolexpr_String_del(STRING);

void boolexpr_Vec_del(VEC);
void boolexpr_Vec_iter(VEC);
void boolexpr_Vec_next(VEC);
BX const boolexpr_Vec_val(VEC);

void boolexpr_VarSet_del(VARSET);
void boolexpr_VarSet_iter(VARSET);
void boolexpr_VarSet_next(VARSET);
BX const boolexpr_VarSet_val(VARSET);

void boolexpr_Point_del(POINT);
void boolexpr_Point_iter(POINT);
void boolexpr_Point_next(POINT);
BX const boolexpr_Point_key(POINT);
BX const boolexpr_Point_val(POINT);

void boolexpr_Soln_del(SOLN);
_Bool boolexpr_Soln_first(SOLN);
POINT boolexpr_Soln_second(SOLN);

DFS_ITER boolexpr_DfsIter_new(BX);
void boolexpr_DfsIter_del(DFS_ITER);
void boolexpr_DfsIter_next(DFS_ITER);
BX boolexpr_DfsIter_val(DFS_ITER);

SAT_ITER boolexpr_SatIter_new(BX);
void boolexpr_SatIter_del(SAT_ITER);
void boolexpr_SatIter_next(SAT_ITER);
POINT boolexpr_SatIter_val(SAT_ITER);

POINTS_ITER boolexpr_PointsIter_new(size_t, VARS);
void boolexpr_PointsIter_del(POINTS_ITER);
void boolexpr_PointsIter_next(POINTS_ITER);
POINT boolexpr_PointsIter_val(POINTS_ITER);

TERMS_ITER boolexpr_TermsIter_new(size_t, VARS);
void boolexpr_TermsIter_del(TERMS_ITER);
void boolexpr_TermsIter_next(TERMS_ITER);
VEC boolexpr_TermsIter_val(TERMS_ITER);

DOM_ITER boolexpr_DomainIter_new(BX);
void boolexpr_DomainIter_del(DOM_ITER);
void boolexpr_DomainIter_next(DOM_ITER);
POINT boolexpr_DomainIter_val(DOM_ITER);

CF_ITER boolexpr_CofactorIter_new(BX, size_t, VARS);
void boolexpr_CofactorIter_del(CF_ITER);
void boolexpr_CofactorIter_next(CF_ITER);
BX boolexpr_CofactorIter_val(CF_ITER);

BX boolexpr_zero(void);
BX boolexpr_one(void);
BX boolexpr_logical(void);
BX boolexpr_illogical(void);

BX boolexpr_not(BX);
LIT boolexpr_abs(LIT);
BX boolexpr_nor(size_t, BXS);
BX boolexpr_or(size_t, BXS);
BX boolexpr_nand(size_t, BXS);
BX boolexpr_and(size_t, BXS);
BX boolexpr_xnor(size_t, BXS);
BX boolexpr_xor(size_t, BXS);
BX boolexpr_neq(size_t, BXS);
BX boolexpr_eq(size_t, BXS);
BX boolexpr_nimpl(BX, BX);
BX boolexpr_impl(BX, BX);
BX boolexpr_nite(BX, BX, BX);
BX boolexpr_ite(BX, BX, BX);

BX boolexpr_onehot0(size_t, BXS);
BX boolexpr_onehot(size_t, BXS);

BX boolexpr_nor_s(size_t, BXS);
BX boolexpr_or_s(size_t, BXS);
BX boolexpr_nand_s(size_t, BXS);
BX boolexpr_and_s(size_t, BXS);
BX boolexpr_xnor_s(size_t, BXS);
BX boolexpr_xor_s(size_t, BXS);
BX boolexpr_neq_s(size_t, BXS);
BX boolexpr_eq_s(size_t, BXS);
BX boolexpr_nimpl_s(BX, BX);
BX boolexpr_impl_s(BX, BX);
BX boolexpr_nite_s(BX, BX, BX);
BX boolexpr_ite_s(BX, BX, BX);

void boolexpr_BoolExpr_del(BX);
uint8_t boolexpr_BoolExpr_kind(BX);
STRING boolexpr_BoolExpr_to_string(BX);
STRING boolexpr_BoolExpr_to_dot(BX);
uint32_t boolexpr_BoolExpr_depth(BX);
uint32_t boolexpr_BoolExpr_size(BX);
_Bool boolexpr_BoolExpr_is_cnf(BX);
_Bool boolexpr_BoolExpr_is_dnf(BX);
BX boolexpr_BoolExpr_simplify(BX);
BX boolexpr_BoolExpr_to_binop(BX);
BX boolexpr_BoolExpr_to_latop(BX);
BX boolexpr_BoolExpr_to_posop(BX);
BX boolexpr_BoolExpr_tseytin(BX, CONTEXT, STRING);
BX boolexpr_BoolExpr_compose(BX, size_t, VARS, BXS);
BX boolexpr_BoolExpr_restrict(BX, size_t, VARS, CONSTS);
BX boolexpr_BoolExpr_sat(BX);
BX boolexpr_BoolExpr_to_cnf(BX);
BX boolexpr_BoolExpr_to_dnf(BX);
BX boolexpr_BoolExpr_to_nnf(BX);
_Bool boolexpr_BoolExpr_equiv(BX, BX);
VARSET boolexpr_BoolExpr_support(BX);
uint32_t boolexpr_BoolExpr_degree(BX);

BX boolexpr_BoolExpr_expand(BX, size_t, VARS);

BX boolexpr_BoolExpr_smoothing(BX, size_t, VARS);
BX boolexpr_BoolExpr_consensus(BX, size_t, VARS);
BX boolexpr_BoolExpr_derivative(BX, size_t, VARS);

CONTEXT boolexpr_Literal_ctx(BX);
uint32_t boolexpr_Literal_id(BX);

_Bool boolexpr_Operator_simple(BX);
VEC boolexpr_Operator_args(BX);
_Bool boolexpr_Operator_is_clause(BX);

ARRAY boolexpr_Array_new(size_t, BXS);
void boolexpr_Array_del(ARRAY);
size_t boolexpr_Array_size(ARRAY);
BX boolexpr_Array_getitem(ARRAY, size_t);
void boolexpr_Array_setitem(ARRAY, size_t, BX);
ARRAY boolexpr_Array_getslice(ARRAY, size_t, size_t);
ARRAY boolexpr_Array_invert(ARRAY);
ARRAY boolexpr_Array_or(ARRAY, ARRAY);
ARRAY boolexpr_Array_and(ARRAY, ARRAY);
ARRAY boolexpr_Array_xor(ARRAY, ARRAY);
ARRAY boolexpr_Array_plus(ARRAY, ARRAY);
ARRAY boolexpr_Array_mul(ARRAY, size_t);
ARRAY boolexpr_Array_simplify(ARRAY);
ARRAY boolexpr_Array_compose(ARRAY, size_t, VARS, BXS);
ARRAY boolexpr_Array_restrict(ARRAY, size_t, VARS, CONSTS);
_Bool boolexpr_Array_equiv(ARRAY, ARRAY);
ARRAY boolexpr_Array_zext(ARRAY, size_t);
ARRAY boolexpr_Array_sext(ARRAY, size_t);
BX boolexpr_Array_nor_reduce(ARRAY);
BX boolexpr_Array_or_reduce(ARRAY);
BX boolexpr_Array_nand_reduce(ARRAY);
BX boolexpr_Array_and_reduce(ARRAY);
BX boolexpr_Array_xnor_reduce(ARRAY);
BX boolexpr_Array_xor_reduce(ARRAY);
ARRAY boolexpr_ArrayPair_fst(ARRAY_PAIR);
ARRAY boolexpr_ArrayPair_snd(ARRAY_PAIR);
void boolexpr_ArrayPair_del(ARRAY_PAIR);
ARRAY_PAIR boolexpr_Array_lsh(ARRAY, ARRAY);
ARRAY_PAIR boolexpr_Array_rsh(ARRAY, ARRAY);
ARRAY_PAIR boolexpr_Array_arsh(ARRAY, size_t);

"""

ffi = FFI()
ffi.cdef(HEADER)
_spec = importlib.util.find_spec("boolexpr._boolexpr")
lib = ffi.dlopen(_spec.origin)


from .wrap import Context

from .wrap import BoolExpr
from .wrap import Atom
from .wrap import Constant
from .wrap import Known
from .wrap import Zero
from .wrap import One
from .wrap import Unknown
from .wrap import Logical
from .wrap import Illogical
from .wrap import Literal
from .wrap import Complement
from .wrap import Variable
from .wrap import Operator
from .wrap import NegativeOperator
from .wrap import LatticeOperator
from .wrap import Nor
from .wrap import Or
from .wrap import Nand
from .wrap import And
from .wrap import Xnor
from .wrap import Xor
from .wrap import Unequal
from .wrap import Equal
from .wrap import NotImplies
from .wrap import Implies
from .wrap import NotIfThenElse
from .wrap import IfThenElse

from .wrap import ZERO
from .wrap import ONE
from .wrap import LOGICAL
from .wrap import ILLOGICAL

from .wrap import iter_points
from .wrap import iter_terms

from .wrap import not_
from .wrap import nor
from .wrap import or_
from .wrap import nand
from .wrap import and_
from .wrap import xnor
from .wrap import xor
from .wrap import neq
from .wrap import eq
from .wrap import nimpl
from .wrap import impl
from .wrap import nite
from .wrap import ite

from .wrap import nor_s
from .wrap import or_s
from .wrap import nand_s
from .wrap import and_s
from .wrap import xnor_s
from .wrap import xor_s
from .wrap import neq_s
from .wrap import eq_s
from .wrap import nimpl_s
from .wrap import impl_s
from .wrap import nite_s
from .wrap import ite_s

from .wrap import onehot0
from .wrap import onehot

from .wrap import Array

from .wrap import zeros
from .wrap import ones
from .wrap import logicals
from .wrap import illogicals
from .wrap import uint2nda
from .wrap import int2nda
from .wrap import array

from .wrap import ndarray

from .misc import nhot
from .misc import majority
from .misc import achilles_heel
from .misc import mux
from .misc import exists
from .misc import forall
from .misc import cat


__version__ = "2.3"
