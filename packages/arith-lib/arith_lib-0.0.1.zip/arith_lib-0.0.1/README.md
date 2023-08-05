arith_lib: A set of functions for miscellaneous arithmetic calculation
======================================================================



List of implemented functions
-----------------------------


- gcd(*arg):    Greatest common divisor of a set of integers

- lcm(*arg):    Least common multiple of a set of integers

- bezout(a, b): Provides a particular solution to diophantine
                equation a.u+b.v=gcd(a, b)

- modulo_inv(a, b): inverse of a modulo b

- chinese_reminder(r, m): Solves the modular system:
                          x = r1 mod m1
                          x = r2 mod m2
                          ...
                          x = r_n mod m_n

- gene_pseudo_prime(): Generator which provides 2, 3, 5 and then
                       all non multiple of 2, 3, 5

- is_prime(n):         Check for n primality

- next_prime(n):       Provides the first prime greater or equal 
                       to n

- prime_factorization(n, frmt): Prime factorization of n
 
- divisors(n): Provides all divisors of n

- phi(n):      Euler indicator function

- moebius(n):  Moebius function

- to_base(n, **kwarg):  Conversion from base 10 to base B

- frobenius(*A, n=None): Solves a1.x1 + a2.x2 + .. + ap.xp = n
                         or provides the greatest n for which this
                         equation has no solution.
                         a1, a2, ... are positive integers
                         x1, x2, ... are the unknowns, positive integers

Installation
------------

pip install arith_lib



