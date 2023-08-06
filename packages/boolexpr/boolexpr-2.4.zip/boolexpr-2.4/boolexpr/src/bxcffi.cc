// Copyright 2016 Chris Drake
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


#include <cassert>
#include <cstring>

#include "boolexpr/boolexpr.h"
#include "bxcffi.h"


using std::static_pointer_cast;
using std::string;
using std::vector;

using boolexpr::Array;
using boolexpr::BoolExpr;
using boolexpr::BoolExprProxy;
using boolexpr::CofactorIterProxy;
using boolexpr::Constant;
using boolexpr::Context;
using boolexpr::DfsIterProxy;
using boolexpr::DomainIterProxy;
using boolexpr::Literal;
using boolexpr::LiteralProxy;
using boolexpr::MapProxy;
using boolexpr::Operator;
using boolexpr::PointsIterProxy;
using boolexpr::SatIterProxy;
using boolexpr::SetProxy;
using boolexpr::SolnProxy;
using boolexpr::TermsIterProxy;
using boolexpr::Variable;
using boolexpr::VecProxy;

using boolexpr::bx_t;
using boolexpr::const_t;
using boolexpr::illogical;
using boolexpr::logical;
using boolexpr::one;
using boolexpr::point_t;
using boolexpr::var_t;
using boolexpr::var2bx_t;
using boolexpr::zero;


DllExport CONTEXT
boolexpr_Context_new()
{
    return new Context();
}


DllExport void
boolexpr_Context_del(CONTEXT c_self)
{
    auto self = reinterpret_cast<Context * const>(c_self);
    delete self;
}


DllExport BX
boolexpr_Context_get_var(CONTEXT c_self, STRING c_name)
{
    auto self = reinterpret_cast<Context * const>(c_self);
    string name { c_name };

    auto var = self->get_var(name);
    auto bx = static_pointer_cast<BoolExpr const>(var);
    return new BoolExprProxy(bx);
}


DllExport void
boolexpr_String_del(STRING c_str)
{
    delete [] c_str;
}


DllExport void
boolexpr_Vec_del(VEC c_self)
{
    auto self = reinterpret_cast<VecProxy<bx_t> * const>(c_self);
    delete self;
}


DllExport void
boolexpr_Vec_iter(VEC c_self)
{
    auto self = reinterpret_cast<VecProxy<bx_t> * const>(c_self);
    self->iter();
}


DllExport void
boolexpr_Vec_next(VEC c_self)
{
    auto self = reinterpret_cast<VecProxy<bx_t> * const>(c_self);
    self->next();
}


DllExport BX
boolexpr_Vec_val(VEC c_self)
{
    auto self = reinterpret_cast<VecProxy<bx_t> * const>(c_self);
    return self->val();
}


DllExport void
boolexpr_VarSet_del(VARSET c_self)
{
    auto self = reinterpret_cast<SetProxy<var_t> * const>(c_self);
    delete self;
}


DllExport void
boolexpr_VarSet_iter(VARSET c_self)
{
    auto self = reinterpret_cast<SetProxy<var_t> * const>(c_self);
    self->iter();
}


DllExport void
boolexpr_VarSet_next(VARSET c_self)
{
    auto self = reinterpret_cast<SetProxy<var_t> * const>(c_self);
    self->next();
}


DllExport BX
boolexpr_VarSet_val(VARSET c_self)
{
    auto self = reinterpret_cast<SetProxy<var_t> * const>(c_self);
    return self->val();
}


DllExport void
boolexpr_Point_del(POINT c_self)
{
    auto self = reinterpret_cast<MapProxy<var_t, const_t> * const>(c_self);
    delete self;
}


DllExport void
boolexpr_Point_iter(POINT c_self)
{
    auto self = reinterpret_cast<MapProxy<var_t, const_t> * const>(c_self);
    self->iter();
}


DllExport void
boolexpr_Point_next(POINT c_self)
{
    auto self = reinterpret_cast<MapProxy<var_t, const_t> * const>(c_self);
    self->next();
}


DllExport BX
boolexpr_Point_key(POINT c_self)
{
    auto self = reinterpret_cast<MapProxy<var_t, const_t> * const>(c_self);
    return self->key();
}


DllExport BX
boolexpr_Point_val(POINT c_self)
{
    auto self = reinterpret_cast<MapProxy<var_t, const_t> * const>(c_self);
    return self->val();
}


DllExport void
boolexpr_Soln_del(SOLN c_self)
{
    auto self = reinterpret_cast<SolnProxy * const>(c_self);
    delete self;
}


DllExport bool
boolexpr_Soln_first(SOLN c_self)
{
    auto self = reinterpret_cast<SolnProxy * const>(c_self);
    return self->soln.first;
}


DllExport POINT
boolexpr_Soln_second(SOLN c_self)
{
    auto self = reinterpret_cast<SolnProxy * const>(c_self);
    auto point = *(self->soln.second);
    return new MapProxy<var_t, const_t>(std::move(point));
}


DllExport DFS_ITER
boolexpr_DfsIter_new(BX c_bxp)
{
    auto bxp = reinterpret_cast<BoolExprProxy const * const>(c_bxp);
    return new DfsIterProxy(bxp->bx);
}


DllExport void
boolexpr_DfsIter_del(DFS_ITER c_self)
{
    auto self = reinterpret_cast<DfsIterProxy * const>(c_self);
    delete self;
}


DllExport void
boolexpr_DfsIter_next(DFS_ITER c_self)
{
    auto self = reinterpret_cast<DfsIterProxy * const>(c_self);
    self->next();
}


DllExport BX
boolexpr_DfsIter_val(DFS_ITER c_self)
{
    auto self = reinterpret_cast<DfsIterProxy * const>(c_self);
    return self->val();
}


DllExport SAT_ITER
boolexpr_SatIter_new(BX c_bxp)
{
    auto bxp = reinterpret_cast<BoolExprProxy const * const>(c_bxp);
    return new SatIterProxy(bxp->bx);
}


DllExport void
boolexpr_SatIter_del(SAT_ITER c_self)
{
    auto self = reinterpret_cast<SatIterProxy * const>(c_self);
    delete self;
}


DllExport void
boolexpr_SatIter_next(SAT_ITER c_self)
{
    auto self = reinterpret_cast<SatIterProxy * const>(c_self);
    self->next();
}


DllExport POINT
boolexpr_SatIter_val(SAT_ITER c_self)
{
    auto self = reinterpret_cast<SatIterProxy * const>(c_self);
    return self->val();
}


DllExport POINTS_ITER
boolexpr_PointsIter_new(size_t n, VARS c_varps)
{
    vector<var_t> vars(n);
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        vars[i] = var;
    }
    return new PointsIterProxy(vars);
}


DllExport void
boolexpr_PointsIter_del(POINTS_ITER c_self)
{
    auto self = reinterpret_cast<PointsIterProxy * const>(c_self);
    delete self;
}


DllExport void
boolexpr_PointsIter_next(POINTS_ITER c_self)
{
    auto self = reinterpret_cast<PointsIterProxy * const>(c_self);
    self->next();
}


DllExport POINT
boolexpr_PointsIter_val(POINTS_ITER c_self)
{
    auto self = reinterpret_cast<PointsIterProxy * const>(c_self);
    return self->val();
}


DllExport TERMS_ITER
boolexpr_TermsIter_new(size_t n, BXS c_args)
{
    vector<bx_t> _args(n);
    for (size_t i = 0; i < n; ++i) {
        auto arg = reinterpret_cast<BoolExprProxy const * const>(c_args[i]);
        _args[i] = arg->bx;
    }
    return new TermsIterProxy(_args);
}


DllExport void
boolexpr_TermsIter_del(TERMS_ITER c_self)
{
    auto self = reinterpret_cast<TermsIterProxy * const>(c_self);
    delete self;
}


DllExport void
boolexpr_TermsIter_next(TERMS_ITER c_self)
{
    auto self = reinterpret_cast<TermsIterProxy * const>(c_self);
    self->next();
}


DllExport VEC
boolexpr_TermsIter_val(TERMS_ITER c_self)
{
    auto self = reinterpret_cast<TermsIterProxy * const>(c_self);
    return self->val();
}


DllExport DOM_ITER
boolexpr_DomainIter_new(BX c_bxp)
{
    auto bxp = reinterpret_cast<BoolExprProxy const * const>(c_bxp);
    return new DomainIterProxy(bxp->bx);
}


DllExport void
boolexpr_DomainIter_del(DOM_ITER c_self)
{
    auto self = reinterpret_cast<DomainIterProxy * const>(c_self);
    delete self;
}


DllExport void
boolexpr_DomainIter_next(DOM_ITER c_self)
{
    auto self = reinterpret_cast<DomainIterProxy * const>(c_self);
    self->next();
}


DllExport POINT
boolexpr_DomainIter_val(DOM_ITER c_self)
{
    auto self = reinterpret_cast<DomainIterProxy * const>(c_self);
    return self->val();
}


DllExport CF_ITER
boolexpr_CofactorIter_new(BX c_bxp, size_t n, VARS c_varps)
{
    auto bxp = reinterpret_cast<BoolExprProxy const * const>(c_bxp);
    vector<var_t> vars(n);
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        vars[i] = var;
    }
    return new CofactorIterProxy(bxp->bx, vars);
}


DllExport void
boolexpr_CofactorIter_del(CF_ITER c_self)
{
    auto self = reinterpret_cast<CofactorIterProxy * const>(c_self);
    delete self;
}


DllExport void
boolexpr_CofactorIter_next(CF_ITER c_self)
{
    auto self = reinterpret_cast<CofactorIterProxy * const>(c_self);
    self->next();
}


DllExport BX
boolexpr_CofactorIter_val(CF_ITER c_self)
{
    auto self = reinterpret_cast<CofactorIterProxy * const>(c_self);
    return self->val();
}


DllExport BX
boolexpr_zero()
{
    return new BoolExprProxy(zero());
}


DllExport BX
boolexpr_one()
{
    return new BoolExprProxy(one());
}


DllExport BX
boolexpr_logical()
{
    return new BoolExprProxy(logical());
}


DllExport BX
boolexpr_illogical()
{
    return new BoolExprProxy(illogical());
}


DllExport BX
boolexpr_not(BX c_arg)
{
    auto arg = reinterpret_cast<BoolExprProxy const * const>(c_arg);
    return new BoolExprProxy(~arg->bx);
}


DllExport LIT
boolexpr_abs(LIT c_arg)
{
    auto arg = reinterpret_cast<LiteralProxy const * const>(c_arg);
    return new LiteralProxy(abs(arg->lit));
}


static vector<bx_t>
_convert_args(size_t n, BXS c_args)
{
    vector<bx_t> _args(n);
    for (size_t i = 0; i < n; ++i) {
        auto arg = reinterpret_cast<BoolExprProxy const * const>(c_args[i]);
        _args[i] = arg->bx;
    }
    return _args;
}


DllExport BX
boolexpr_nor(size_t n, BXS c_args)
{ return new BoolExprProxy(nor(_convert_args(n, c_args))); }

DllExport BX
boolexpr_or(size_t n, BXS c_args)
{ return new BoolExprProxy(or_(_convert_args(n, c_args))); }

DllExport BX
boolexpr_nand(size_t n, BXS c_args)
{ return new BoolExprProxy(nand(_convert_args(n, c_args))); }

DllExport BX
boolexpr_and(size_t n, BXS c_args)
{ return new BoolExprProxy(and_(_convert_args(n, c_args))); }

DllExport BX
boolexpr_xnor(size_t n, BXS c_args)
{ return new BoolExprProxy(xnor(_convert_args(n, c_args))); }

DllExport BX
boolexpr_xor(size_t n, BXS c_args)
{ return new BoolExprProxy(xor_(_convert_args(n, c_args))); }

DllExport BX
boolexpr_neq(size_t n, BXS c_args)
{ return new BoolExprProxy(neq(_convert_args(n, c_args))); }

DllExport BX
boolexpr_eq(size_t n, BXS c_args)
{ return new BoolExprProxy(eq(_convert_args(n, c_args))); }

DllExport BX
boolexpr_nimpl(BX c_p, BX c_q)
{
    auto p = reinterpret_cast<BoolExprProxy const * const>(c_p);
    auto q = reinterpret_cast<BoolExprProxy const * const>(c_q);
    return new BoolExprProxy(nimpl(p->bx, q->bx));
}

DllExport BX
boolexpr_impl(BX c_p, BX c_q)
{
    auto p = reinterpret_cast<BoolExprProxy const * const>(c_p);
    auto q = reinterpret_cast<BoolExprProxy const * const>(c_q);
    return new BoolExprProxy(impl(p->bx, q->bx));
}

DllExport BX
boolexpr_nite(BX c_s, BX c_d1, BX c_d0)
{
    auto s = reinterpret_cast<BoolExprProxy const * const>(c_s);
    auto d1 = reinterpret_cast<BoolExprProxy const * const>(c_d1);
    auto d0 = reinterpret_cast<BoolExprProxy const * const>(c_d0);
    return new BoolExprProxy(nite(s->bx, d1->bx, d0->bx));
}

DllExport BX
boolexpr_ite(BX c_s, BX c_d1, BX c_d0)
{
    auto s = reinterpret_cast<BoolExprProxy const * const>(c_s);
    auto d1 = reinterpret_cast<BoolExprProxy const * const>(c_d1);
    auto d0 = reinterpret_cast<BoolExprProxy const * const>(c_d0);
    return new BoolExprProxy(ite(s->bx, d1->bx, d0->bx));
}


DllExport BX
boolexpr_onehot0(size_t n, BXS c_args)
{ return new BoolExprProxy(onehot0(_convert_args(n, c_args))); }

DllExport BX
boolexpr_onehot(size_t n, BXS c_args)
{ return new BoolExprProxy(onehot(_convert_args(n, c_args))); }


DllExport BX
boolexpr_nor_s(size_t n, BXS c_args)
{ return new BoolExprProxy(nor_s(_convert_args(n, c_args))); }

DllExport BX
boolexpr_or_s(size_t n, BXS c_args)
{ return new BoolExprProxy(or_s(_convert_args(n, c_args))); }

DllExport BX
boolexpr_nand_s(size_t n, BXS c_args)
{ return new BoolExprProxy(nand_s(_convert_args(n, c_args))); }

DllExport BX
boolexpr_and_s(size_t n, BXS c_args)
{ return new BoolExprProxy(and_s(_convert_args(n, c_args))); }

DllExport BX
boolexpr_xnor_s(size_t n, BXS c_args)
{ return new BoolExprProxy(xnor_s(_convert_args(n, c_args))); }

DllExport BX
boolexpr_xor_s(size_t n, BXS c_args)
{ return new BoolExprProxy(xor_s(_convert_args(n, c_args))); }

DllExport BX
boolexpr_neq_s(size_t n, BXS c_args)
{ return new BoolExprProxy(neq_s(_convert_args(n, c_args))); }

DllExport BX
boolexpr_eq_s(size_t n, BXS c_args)
{ return new BoolExprProxy(eq_s(_convert_args(n, c_args))); }

DllExport BX
boolexpr_nimpl_s(BX c_p, BX c_q)
{
    auto p = reinterpret_cast<BoolExprProxy const * const>(c_p);
    auto q = reinterpret_cast<BoolExprProxy const * const>(c_q);
    return new BoolExprProxy(nimpl_s(p->bx, q->bx));
}

DllExport BX
boolexpr_impl_s(BX c_p, BX c_q)
{
    auto p = reinterpret_cast<BoolExprProxy const * const>(c_p);
    auto q = reinterpret_cast<BoolExprProxy const * const>(c_q);
    return new BoolExprProxy(impl_s(p->bx, q->bx));
}

DllExport BX
boolexpr_nite_s(BX c_s, BX c_d1, BX c_d0)
{
    auto s = reinterpret_cast<BoolExprProxy const * const>(c_s);
    auto d1 = reinterpret_cast<BoolExprProxy const * const>(c_d1);
    auto d0 = reinterpret_cast<BoolExprProxy const * const>(c_d0);
    return new BoolExprProxy(nite_s(s->bx, d1->bx, d0->bx));
}

DllExport BX
boolexpr_ite_s(BX c_s, BX c_d1, BX c_d0)
{
    auto s = reinterpret_cast<BoolExprProxy const * const>(c_s);
    auto d1 = reinterpret_cast<BoolExprProxy const * const>(c_d1);
    auto d0 = reinterpret_cast<BoolExprProxy const * const>(c_d0);
    return new BoolExprProxy(ite_s(s->bx, d1->bx, d0->bx));
}


DllExport void
boolexpr_BoolExpr_del(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    delete self;
}


DllExport uint8_t
boolexpr_BoolExpr_kind(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return static_cast<uint8_t>(self->bx->kind);
}


DllExport STRING
boolexpr_BoolExpr_to_string(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto str = self->bx->to_string();
    auto c_str = new char[str.length() + 1];
    std::strcpy(c_str, str.c_str());
    return c_str;
}


DllExport STRING
boolexpr_BoolExpr_to_dot(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto str = self->bx->to_dot();
    auto c_str = new char[str.length() + 1];
    std::strcpy(c_str, str.c_str());
    return c_str;
}


DllExport uint32_t
boolexpr_BoolExpr_depth(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return self->bx->depth();
}


DllExport uint32_t
boolexpr_BoolExpr_size(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return self->bx->size();
}


DllExport bool
boolexpr_BoolExpr_is_cnf(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return self->bx->is_cnf();
}


DllExport bool
boolexpr_BoolExpr_is_dnf(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return self->bx->is_dnf();
}


DllExport BX
boolexpr_BoolExpr_simplify(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new BoolExprProxy(self->bx->simplify());
}


DllExport BX
boolexpr_BoolExpr_to_binop(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new BoolExprProxy(self->bx->to_binop());
}


DllExport BX
boolexpr_BoolExpr_to_latop(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new BoolExprProxy(self->bx->to_latop());
}


DllExport BX
boolexpr_BoolExpr_to_posop(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new BoolExprProxy(self->bx->to_posop());
}


DllExport BX
boolexpr_BoolExpr_tseytin(BX c_self, CONTEXT c_ctx, STRING c_auxvarname)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto ctx = reinterpret_cast<Context * const>(c_ctx);
    string auxvarname { c_auxvarname };
    return new BoolExprProxy(self->bx->tseytin(*ctx, auxvarname));
}


DllExport BX
boolexpr_BoolExpr_compose(BX c_self, size_t n, VARS c_varps, BXS c_bxps)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto var2bx = var2bx_t();
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto bxp = reinterpret_cast<BoolExprProxy const * const>(c_bxps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        auto bx = bxp->bx;
        var2bx.insert({var, bx});
    }
    return new BoolExprProxy(self->bx->compose(var2bx));
}


DllExport BX
boolexpr_BoolExpr_restrict(BX c_self, size_t n, VARS c_varps, CONSTS c_constps)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto point = point_t();
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto constp = reinterpret_cast<BoolExprProxy const * const>(c_constps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        auto const_ = static_pointer_cast<Constant const>(constp->bx);
        point.insert({var, const_});
    }
    return new BoolExprProxy(self->bx->restrict_(point));
}


DllExport BX
boolexpr_BoolExpr_sat(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new SolnProxy(self->bx->sat());
}


DllExport BX
boolexpr_BoolExpr_to_cnf(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new BoolExprProxy(self->bx->to_cnf());
}


DllExport BX
boolexpr_BoolExpr_to_dnf(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new BoolExprProxy(self->bx->to_dnf());
}


DllExport BX
boolexpr_BoolExpr_to_nnf(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new BoolExprProxy(self->bx->to_nnf());
}


DllExport bool
boolexpr_BoolExpr_equiv(BX c_self, BX c_other)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto other = reinterpret_cast<BoolExprProxy const * const>(c_other);
    return self->bx->equiv(other->bx);
}


DllExport VARSET
boolexpr_BoolExpr_support(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return new SetProxy<var_t>(self->bx->support());
}


DllExport uint32_t
boolexpr_BoolExpr_degree(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    return self->bx->degree();
}


DllExport BX
boolexpr_BoolExpr_expand(BX c_self, size_t n, VARS c_varps)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    vector<var_t> vars(n);
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        vars[i] = var;
    }
    return new BoolExprProxy(self->bx->expand(vars));
}


DllExport BX
boolexpr_BoolExpr_smoothing(BX c_self, size_t n, VARS c_varps)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    vector<var_t> vars(n);
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        vars[i] = var;
    }
    return new BoolExprProxy(self->bx->smoothing(vars));
}


DllExport BX
boolexpr_BoolExpr_consensus(BX c_self, size_t n, VARS c_varps)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    vector<var_t> vars(n);
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        vars[i] = var;
    }
    return new BoolExprProxy(self->bx->consensus(vars));
}


DllExport BX
boolexpr_BoolExpr_derivative(BX c_self, size_t n, VARS c_varps)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    vector<var_t> vars(n);
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        vars[i] = var;
    }
    return new BoolExprProxy(self->bx->derivative(vars));
}


DllExport CONTEXT
boolexpr_Literal_ctx(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto lit = static_pointer_cast<Literal const>(self->bx);
    return lit->ctx;
}


DllExport uint32_t
boolexpr_Literal_id(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto lit = static_pointer_cast<Literal const>(self->bx);
    return lit->id;
}


DllExport bool
boolexpr_Operator_simple(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto op = static_pointer_cast<Operator const>(self->bx);
    return op->simple;
}


DllExport VEC
boolexpr_Operator_args(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto op = static_pointer_cast<Operator const>(self->bx);
    return new VecProxy<bx_t>(op->args);
}


DllExport bool
boolexpr_Operator_is_clause(BX c_self)
{
    auto self = reinterpret_cast<BoolExprProxy const * const>(c_self);
    auto op = static_pointer_cast<Operator const>(self->bx);
    return op->is_clause();
}


DllExport ARRAY
boolexpr_Array_new(size_t n, BXS c_args)
{
    return new Array(_convert_args(n, c_args));
}


DllExport void
boolexpr_Array_del(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    delete self;
}


DllExport size_t
boolexpr_Array_size(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return self->size();
}


DllExport BX
boolexpr_Array_getitem(ARRAY c_self, size_t index)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    assert(index < self->size());
    return new BoolExprProxy((*self)[index]);
}


DllExport void
boolexpr_Array_setitem(ARRAY c_self, size_t index, BX c_item)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto item = reinterpret_cast<BoolExprProxy const * const>(c_item);
    assert(index < self->size());
    (*self)[index] = item->bx;
}


DllExport ARRAY
boolexpr_Array_getslice(ARRAY c_self, size_t start, size_t stop)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    assert((0 <= start) && (start <= stop) && (stop <= self->size()));
    auto items = vector<bx_t>(self->begin() + start,
                              self->begin() + stop);
    return new Array(std::move(items));
}


DllExport ARRAY
boolexpr_Array_invert(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return (~(*self)).release();
}


DllExport ARRAY
boolexpr_Array_or(ARRAY c_self, ARRAY c_other)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto other = reinterpret_cast<Array * const>(c_other);
    return (*self | *other).release();
}


DllExport ARRAY
boolexpr_Array_and(ARRAY c_self, ARRAY c_other)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto other = reinterpret_cast<Array * const>(c_other);
    return (*self & *other).release();
}


DllExport ARRAY
boolexpr_Array_xor(ARRAY c_self, ARRAY c_other)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto other = reinterpret_cast<Array * const>(c_other);
    return (*self ^ *other).release();
}


DllExport ARRAY
boolexpr_Array_plus(ARRAY c_self, ARRAY c_other)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto other = reinterpret_cast<Array * const>(c_other);
    return (*self + *other).release();
}


DllExport ARRAY
boolexpr_Array_mul(ARRAY c_self, size_t num)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return (*self * num).release();
}


DllExport ARRAY
boolexpr_Array_simplify(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return self->simplify().release();
}


DllExport ARRAY
boolexpr_Array_compose(ARRAY c_self, size_t n, VARS c_varps, BXS c_bxps)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto var2bx = var2bx_t();
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto bxp = reinterpret_cast<BoolExprProxy const * const>(c_bxps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        auto bx = bxp->bx;
        var2bx.insert({var, bx});
    }
    return self->compose(var2bx).release();
}


DllExport ARRAY
boolexpr_Array_restrict(ARRAY c_self, size_t n, VARS c_varps, CONSTS c_constps)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto point = point_t();
    for (size_t i = 0; i < n; ++i) {
        auto varp = reinterpret_cast<BoolExprProxy const * const>(c_varps[i]);
        auto constp = reinterpret_cast<BoolExprProxy const * const>(c_constps[i]);
        auto var = static_pointer_cast<Variable const>(varp->bx);
        auto const_ = static_pointer_cast<Constant const>(constp->bx);
        point.insert({var, const_});
    }
    return self->restrict_(point).release();
}


DllExport bool
boolexpr_Array_equiv(ARRAY c_self, ARRAY c_other)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto other = reinterpret_cast<Array * const>(c_other);
    return self->equiv(*other);
}


DllExport ARRAY
boolexpr_Array_zext(ARRAY c_self, size_t num)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return self->zext(num).release();
}


DllExport ARRAY
boolexpr_Array_sext(ARRAY c_self, size_t num)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return self->sext(num).release();
}


DllExport BX
boolexpr_Array_nor_reduce(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return new BoolExprProxy(self->nor_reduce());
}


DllExport BX
boolexpr_Array_or_reduce(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return new BoolExprProxy(self->or_reduce());
}


DllExport BX
boolexpr_Array_nand_reduce(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return new BoolExprProxy(self->nand_reduce());
}


DllExport BX
boolexpr_Array_and_reduce(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return new BoolExprProxy(self->and_reduce());
}


DllExport BX
boolexpr_Array_xnor_reduce(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return new BoolExprProxy(self->xnor_reduce());
}


DllExport BX
boolexpr_Array_xor_reduce(ARRAY c_self)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    return new BoolExprProxy(self->xor_reduce());
}


DllExport ARRAY
boolexpr_ArrayPair_fst(ARRAY_PAIR c_self)
{
    auto self = reinterpret_cast<Array * const * const>(c_self);
    return self[0];
}

DllExport ARRAY
boolexpr_ArrayPair_snd(ARRAY_PAIR c_self)
{
    auto self = reinterpret_cast<Array * const * const>(c_self);
    return self[1];
}

DllExport void
boolexpr_ArrayPair_del(ARRAY_PAIR c_self)
{
    auto self = reinterpret_cast<Array * const * const>(c_self);
    delete [] self;
}


DllExport ARRAY_PAIR
boolexpr_Array_lsh(ARRAY c_self, ARRAY c_sin)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto si = reinterpret_cast<Array * const>(c_sin);

    auto p = self->lsh(*si);

    return new Array * [2] { p.first.release(), p.second.release() };
}


DllExport ARRAY_PAIR
boolexpr_Array_rsh(ARRAY c_self, ARRAY c_sin)
{
    auto self = reinterpret_cast<Array * const>(c_self);
    auto si = reinterpret_cast<Array * const>(c_sin);

    auto p = self->rsh(*si);

    return new Array * [2] { p.first.release(), p.second.release() };
}


DllExport ARRAY_PAIR
boolexpr_Array_arsh(ARRAY c_self, size_t n)
{
    auto self = reinterpret_cast<Array * const>(c_self);

    auto p = self->arsh(n);

    return new Array * [2] { p.first.release(), p.second.release() };
}


// Required to compile a Python extension for Windows
#ifdef _MSC_VER
DllExport void *
PyInit__boolexpr(void) { return NULL; }
#endif
