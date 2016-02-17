# Warehouses-orders

On note :

- $O$ l'ensemble des *orders*, $W$ l'ensemble des *warehouses*, $T$ l'ensemble des types de produits ;
- $x_{wot}$ le nombre de produits de type $t$ que $w$ donne à $o$ ;
- $r_{ot}$ le nombre de produits de type $t$ que requiert $o$ ;
- $s_{wt}$ le nombre de produits de type $t$ que stocke $w$.

Sous les contraintes suivantes :

$$ \forall o \in O, \forall t \in T, \sum_{w \in W} x_{wot} = r_{ot} \qquad \forall w \in W, \forall t \in T, \sum_{o \in O} x_{wot} \leqslant s_{wt} $$

Il faut minimiser :

$$ \sum_{w \in W, o \in O, t \in T} x_{wot} \cdot d(w, o). $$
