{% import '_macros/digital_logic.html' as m with context %}

{% markdown %}

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
<div class="page-header">
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# An Introduction to Digital Logic
## <small>OpenStax</small>

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
</div>
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Preface

Digital logic is the basis of every modern computer. Digital logic
takes binary inputs, valued at 1 or 0, and transforms them into useful
outputs using logic operations. This learning module will focus on
understanding the basic building blocks of digital logic circuits and
how these can be combined to produce more complicated logic circuits.

{% endmarkdown %}

{% markdown %}

[TOC]

Introductory Digital Logic {:.book-main}
========================================

Digital logic is a subarea of traditional algebra. Like algebra,
digital logic consists of variables and operations that can be carried
out on those variables. However, the variables and operations used in
digital logic are quite different than conventional algebra in both
the types of variables that are used and operations that allow us to
manipulate those variables.

Boolean Variables
-----------------

Traditional algebraic variables can take on a wide array of values. For
example, $x=7$, $t=-7.3$, and $z=57$ are perfectly acceptable
variables.  In Boolean algebra, variables can take on only one of two
(or binary) values: $0$ or $1$. These values have a logical
interpretation in digital logic, with $0$ corresponding to false and
$1$ corresponding to true.

**Boolean operations** receive binary values and return (or, output)
another binary value. The three primitive Boolean operations are:

-   AND

-   OR

-   NOT

The outputs of these operations will be discussed in the next section.
These primitive Boolean operations can be used together to produce
more complex functions. We use the term **Boolean experssion** when we
write these functions mathematically.

Logic Gates
-----------

**Logic gates** are the theoretical and physical electronic components
that execute Boolean operations. They are often used to provide a
pictorial representation of a boolean operation and are useful when
designing and interpreting digital logic circuits. Here we introduce
the primitive logic gates. For this section, let A and B be Boolean
variables.

### AND

The **AND** logic gate takes two inputs. The output of the AND gate is
$1$ only if both inputs are $1$. For example, A AND B will only equal
1 if A = B = 1. For every other combination of inputs, A AND B will
equal $0$. In Boolean algebra, AND is represented as multiplication.

{% call m.equation() %}
A AND B = A$\cdot$B = AB
{% endcall %}

#### **Example 1** {:.exercise}

Evaluate 1 AND 1.

**Solution**

Since AND evaluates to 1 when both inputs are 1, 1 AND 1 = 1.

#### **Example 2** {:.exercise}

Lisa will go to the movies only if she has money and free time.  Model
this situation with a Boolean expression.


**Solution**

Let G denote whether Lisa will go to the movies.  Further, let M
denote whether she has money, and let T denote whether she has free
time.  Then we can write G = M AND T = MT.  If either M is false (Lisa
does not have money) or T is false (she does not have any free time),
then Lisa will not go (G) to the movies.

It is very easy to understand the behavior of the AND gate when we
think of a binary value 1 denoting true and the binary value 0
denoting false.  In this case, the output of the AND gate is true only
if the first input **and** the second input are true.

{% call m.figure("AND.PNG", "AND logic gate") %}

**Figure 1** The electronic symbol for the AND logic gate. It takes
  as input A and B and outputs AB.
  
{% endcall %}

{% endmarkdown %}
