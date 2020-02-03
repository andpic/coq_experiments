Goal forall X : Prop, ~~~X -> ~X.

(*** ~X is defined as X -> False ***)
Print not.

Proof.
  (*** Introduce the proposition X and the premise ***)
  intros X.
  intros prove_of_triple_not_X.
Admitted.