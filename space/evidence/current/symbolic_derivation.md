# Independent symbolic reconstruction

This document reconstructs the five universal statements from the hashed
arXiv source. Numerical checks are corroboration only. The executable
dependency certificate rejects a missing or reordered step; the mathematics
of each accepted step is given here.

## Claim 1: nonexpansive MLP Euler step

For

\[
F(x)=x-\tau W^\top\operatorname{ReLU}(Wx+b),
\qquad
0\leq\tau\leq 2/\lVert W\rVert_2^2,
\]

fix a line segment between two inputs. Away from the finitely many ReLU
breakpoints its Jacobian is

\[
J_D=I-\tau W^\top D W,\qquad 0\preceq D\preceq I,
\]

where `D` is diagonal with entries zero or one. Thus
\(0\preceq W^\top D W\preceq \lVert W\rVert_2^2I\). Every eigenvalue of
`J_D` is \(1-\tau\lambda\) for
\(0\leq\lambda\leq\lVert W\rVert_2^2\), hence lies in `[-1,1]`.
Integrating the segment derivative across its finitely many pieces proves
\(\lVert F(x)-F(x')\rVert_2\leq\lVert x-x'\rVert_2\) in every dimension.
If `W=0`, `F` is the identity and the reciprocal endpoint is not evaluated.
The potential
\(g(x)=\sum_i\frac12\operatorname{ReLU}((Wx+b)_i)^2\)
has gradient \(W^\top\operatorname{ReLU}(Wx+b)\), proving the Euler identity.

## Claim 2: shallow attention bounds

Let \(v(y)=Ay\), \(Z_x(\mu)=\int e^{\langle x,v(y)\rangle}d\mu(y)\), and

\[
\Gamma(\mu,x)=x-\eta\nabla_x\log Z_x(\mu).
\]

For fixed `mu`, the Hessian of `log Z` is the covariance of `v(Y)` under the
exponentially tilted measure. It is positive semidefinite and, for every unit
vector `q`,

\[
q^\top\operatorname{Cov}(v(Y))q
\leq E\lVert v(Y)\rVert_2^2
\leq\beta:=\sup_{y\in\Omega}\lVert Ay\rVert_2^2.
\]

Therefore `log Z` is convex and beta-smooth. Cocoercivity gives
\(\langle\nabla f(x)-\nabla f(x'),x-x'\rangle
\geq\lVert\nabla f(x)-\nabla f(x')\rVert^2/\beta\).
Expanding the squared distance after the gradient step proves
nonexpansiveness for \(0\leq\eta\leq2/\beta\). The `beta=0` case is the
identity.

For the measure argument, put
\(R=\sup_{\Omega}\lVert y\rVert_2\),
\(B=\lVert A\rVert_2R^2\), and
\(L_f=\lVert A\rVert_2R\). Kantorovich--Rubinstein duality gives

\[
|Z_x(\mu)-Z_x(\nu)|\leq e^B L_f W_1(\mu,\nu)
\]

and, for \(N_x(\mu)=\int e^{\langle x,Ay\rangle}Ay\,d\mu(y)\),

\[
\lVert N_x(\mu)-N_x(\nu)\rVert
\leq e^B\lVert A\rVert_2(1+RL_f)W_1(\mu,\nu).
\]

Since \(Z_x\geq e^{-B}\) and
\(\lVert N_x(\nu)\rVert\leq e^B\lVert A\rVert_2R\), the quotient identity
gives the explicit finite bound

\[
\operatorname{Lip}_{W_1}\Gamma(\cdot,x)
\leq\eta\left[
e^{2B}\lVert A\rVert_2(1+RL_f)
+e^{4B}\lVert A\rVert_2R L_f
\right].
\]

This constant is for fixed `(A, eta)`. It is not uniform over all parameter
choices; the paper appendix also retains this dependence.

## Claim 3: finite-depth composition

For a layer with query constant `q_l <= 1` and context constant `c_l < inf`,
let `r_l` bound the Wasserstein change in the propagated measure and let `s_l`
bound the output-query change caused by the original context. A coupling gives

\[
r_l\leq(q_l+c_l)r_{l-1},\qquad
s_l\leq q_l s_{l-1}+c_l r_{l-1}.
\]

MLP layers have `c_l=0`. With `r_0=1` and `s_0=0`, induction makes both
constants finite for every finite depth. For fixed context, the query
constant is \(\prod_l q_l\leq1\). This proves the exact Lemma 6 scope:
depth-independent query nonexpansiveness and a context constant that may
depend on depth.

## Claim 5: restricted Stone--Weierstrass lemma

This claim precedes Claim 4 in the dependency order. Given a target `g` and
tolerance `epsilon`, scale it by

\[
\rho=1-\frac{\varepsilon}{2(1+\lVert g\rVert_\infty)}<1.
\]

Then `rho g` differs from `g` by at most `epsilon/2`, while every distinct
two-point target gap is strictly below the product Lipschitz budget. Strict
separation supplies an interpolant for a fixed base point and every second
point. The open sets on which each interpolant lies below
`rho g + epsilon/2` cover the compact product domain. A finite subcover and
the lattice minimum produce a global upper envelope touching the base point.
Those touching neighborhoods form a second open cover. A finite subcover and
the lattice maximum produce `G` with

\[
\rho g-\varepsilon/2<G<\rho g+\varepsilon/2.
\]

The triangle inequality proves \(\lVert G-g\rVert_\infty<\varepsilon\).
No chosen basis or finite sample enters this argument.

## Claim 4: Transformer density

Apply Claim 5 to `L = G_C`. The two premises are reconstructed separately.

1. **Lattice.** Parallel MLP blocks are block-diagonal Euler layers. Two
   attention blocks are implemented sequentially on the product feature
   space using block matrices, preserving their respective coordinates.
   A final admissible ReLU Euler block realizes max/min from
   \(\max(a,b)=\operatorname{ReLU}(a-b)+b\). Pointwise max/min preserve the
   `(1,C)` bounds, so the constructed network remains in `G_C`.
2. **Strict separation.** A normalized Kantorovich--Rubinstein optimizer
   exists by Arzela--Ascoli on compact `Omega`. The scalar 1-Lipschitz ResNet
   density theorem of Murari et al. approximates that witness uniformly.
   An added constant coordinate makes the attention scores zero, so one
   attention layer computes its uniform context integral. Combining this
   context primitive with the unit query direction yields a gap approaching
   \(\lVert x-x'\rVert_2+C W_1(\mu,\nu)\). The strict premise leaves room to
   choose the approximation tolerance and rescale by a coefficient with
   absolute value at most one to interpolate the requested values. A negative
   coefficient is handled by the final linear projection; positivity is not
   required.

If the approximating witness is identically zero, either the desired
Wasserstein lower bound is nonpositive (and the zero primitive suffices) or
uniform approximation of a positive KR gap rules that case out. The singleton
domain is constant and is handled directly. Consequently both premises of
Claim 5 hold, proving the uniform theorem over
`P(Omega) x Omega`; token count never appears.

The residual validation risk is explicit: this reconstruction imports Murari
et al., Theorem 3.1 rather than formalizing that antecedent in a proof
assistant.
