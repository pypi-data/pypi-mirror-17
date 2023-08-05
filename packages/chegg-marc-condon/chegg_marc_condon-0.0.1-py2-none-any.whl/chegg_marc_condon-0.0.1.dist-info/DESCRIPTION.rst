==================================
Chegg Code Challenge - Marc Condon
==================================

---
USE
---

pip install chegg-marc-condon

cat input-file | chegg-marc-condon

pip uninstall chegg-marc-condon

----------------
Algorithmic Cost
----------------

This program has an O2 algorithmic cost, meaning there an N**2 steps for solution.  Where N is appoximately
(Number of Patterns + Number of Paths)/2. I optimized the solution by making sure all the patterns are unique
and immediately exclude patterns that cannot match because the of matching terms do not match.

