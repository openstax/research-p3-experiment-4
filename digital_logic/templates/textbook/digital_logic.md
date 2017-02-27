{% import '_macros/digital_logic.html' as m with context %}

{% extends 'layouts/base.html' %}

{% markdown %}

# Preface {:.preface}

Digital logic is the basis of every modern computer. Digital logic
takes binary inputs, valued at 1 or 0, and transforms them into useful
outputs using logic operations. This learning module will focus on
understanding the basic building blocks of digital logic circuits and
how these can be combined to produce more complicated logic circuits.


# Introductory Digital Logic {:.introduction}

Digital logic is a subarea of traditional algebra. Like algebra,
digital logic consists of variables and operations that can be carried
out on those variables. However, the variables and operations used in
digital logic are quite different than conventional algebra in both
the types of variables that are used and operations that allow us to
manipulate those variables.


# Boolean Variables {:.boolean-variables}

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
more complex functions. We use the term **Boolean expression** when we
write these functions mathematically.

## Logic Gates {:.logic-gates}


**Logic gates** are the theoretical and physical electronic components
that execute Boolean operations. They are often used to provide a
pictorial representation of a boolean operation and are useful when
designing and interpreting digital logic circuits. Here we introduce
the primitive logic gates. For this section, let A and B be Boolean
variables.

### AND {:.and}

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

## Truth Tables {:.truth-tables}

Now that we have seen our first Boolean expression, AB, let's learn
how to represent its behavior. **Truth tables** show the output of a
Boolean expression for every possible combination of inputs.

#### **Example 3** {:.exercise}

Draw a truth table for A AND B.

**Solution**

1.  Draw three columns: A, B, A AND B.
2.  Underneath A and B, write each possible combination of A and B.
3.  Underneath A AND B, write the value of A AND B based on the values
    of A and B in that row.

{% call m.figure("truth_table_A_AND_B.PNG", "truth table for A AND B", "restrict no-border responsive-img") %}

**Figure 2**  Truth table for A AND B.

{% endcall %}

## OR {:.or}

The **OR** logic gate takes two inputs. The output of the OR gate is 1
if at least one of the inputs is 1. A OR B only outputs 0 if A=B=0. In
Boolean algebra, OR is represented as addition.

{% call m.equation() %}
A OR B = A + B
{% endcall %}

{% call m.figure("OR.PNG", "OR Logic Gate") %}
**Figure 3** The electronic symbol for the OR logic gate.
{% endcall %}

{% call m.figure("truth_table_A_or_B.PNG", "truth table for A OR B", "no-border responsive-img") %}
**Figure 4** Truth table for A OR B.
{% endcall %}

#### **Example 4** {:.exercise}

Evaluate 0 OR 0.

**Solution**

Since OR only evaluates to 1 when at least one input is 1, 0 OR 0 = 0.

## NOT {:.not}

The **NOT** logic gate takes one input. The output of the NOT gate is
simply the opposite of the input. NOT A, for example, would output 1
if A=0 and output 0 if A=1. For this reason, a NOT gate is often
called an inverter. In Boolean algebra, NOT is represented as an
apostrophe.

{% call m.equation() %}
NOT A = A'
{% endcall %}

{% call m.figure("NOT.PNG", "NOT Logic Gate") %}
**Figure 5** The electronic symbol for the NOT logic gate.
{% endcall %}

{% call m.figure("truth_table_NOT_A.PNG", "truth table for NOT A", "no-border responsive-img") %}
**Figure 6** Truth table for NOT A.
{% endcall %}

#### **Example 5** {:.exercise}

Evaluate NOT 0.

**Solution**

Since NOT flips the input, NOT 0 = 1

# Compound Boolean Expression {:.compound-boolean-expression}


The basic boolean operations can be combined to create more complex and
useful functions. We can analyze the behavior of these compound
expressions using the truth tables introduced previously. For a boolean
expression with $K$ variables, the truth table will consist of $2^K$
rows. For example, the basic logic gates with $K=2$ inputs have
$2^2 = 4$ rows in their truth table. A compound boolean expression with
$K=3$ variables will have $2^3 = 8$ rows in its truth table.

#### **Example 6** {:.exercise}

Write the truth table for A OR A'.

**Solution**

Since we only have one variable – A – we will have $2^1=2$ rows in the
truth table. We will explicitly state the value of A' for the sake
clarity. We recall that the OR function will evaluate to 1 when either
input is 1. Recall that A' indicates NOT A and will be 1 anytime that
A is 0. Therefore, either A or A' will be 1, and the entire expression
will evaluate to 1 for all cases.


{% call m.figure("TT_AorA'.png", "truth table for A OR A'", "no-border") %}
**Figure 7** Truth table for A OR A'.
{% endcall %}

As in traditional algebra, Boolean algebra uses parentheses to indicate
the order of operations.

#### **Example 7** {:.exercise}

Write the truth table for A AND (B AND C).

**Solution**

Since we have three variables, we will have $2^3=8$ rows in the truth
table. For each row in the truth table, we can first evaluate the (B
AND C) term and then use this result to obtain the final output. By
inspection we can see that this expression will evaluate to 1 only
when A, B, and C are 1.

{% call m.figure("TT_AandBandC.png", "truth table for A AND (B AND C)", "no-border restrict responsive-img") %}

**Figure 8** Truth table for A AND (B AND C).  We note that the
only time the output of this circuit is is 1 is for the case when
A=B=C=1.

{% endcall %}

#### **Example 8** {:.exercise}
Write the truth table for A OR (B AND C).

**Solution**
Since we have three variables, we will have $2^3=8$ rows in the truth
table. For each row in the truth table, we can first evaluate the (B
AND C) term and then use this result to obtain the final output.

{% call m.figure("TT_AorBandC.png", "truth table for A OR (B AND C)", "no-border restrict responsive-img") %}
**Figure 9** Truth table for A OR (B AND C).
{% endcall %}

## Circuits to Truth Tables {:.circuits-to-truth-tables}


It is often very easy to calculate the entries of a truth table using
digital logic circuit diagram.  This is because digital circuit
diagrams make it easy to visualize how logic gates operate on boolean
variables and how the function of these gates combine to produce the
final output.  We will illustrate this using the logic circuit that
implements the expression A OR (B AND C) from the previous example.

#### **Example 9** {:.exercise}

Write the truth table for the following circuit.

{% call m.figure("circuit_tt_1_prob_v2.png", "Circuit diagram for A OR (B AND C)", "no-border restrict responsive-img") %}
**Figure 10** Circuit diagram for A OR (B AND C)
{% endcall %}

**Solution**

We can take each row of the truth table and apply their inputs into
the circuit. We can then propagate the results through the circuit to
obtain the final result. As a concrete example, we show how this works
for the case A=1, B=1, and C=0.

{% call m.figure("circuit_tt_1_ans_v2.png", "Realization of the circuit diagram for A OR (B AND C)", "no-border restrict responsive-img") %}
**Figure 11** Realization of the circuit diagram for A OR (B AND C) for A=1, B=1 and C=0.
{% endcall %}

We have labeled the Boolean values in the circuit in red for
convenience.  We first evaluate the output of the AND gate. Since 1
AND 0 = 0, we end up with 0 at the output of the AND gate.  Finally,
we evaluate the output of the OR gate using the 0 output from the AND
gate and with the value of A=1.  This evaluates to 1, which gives the
final result.  Repeating this for all input combinations we can arrive
at the final truth table given in Example 6.

#### **Example 10** {:.exercise}

Write the truth table for the following circuit, which implements the expression
(NOT A) AND (B OR C) = A' $\cdot$ (B + C).

{% call m.figure("circuit_tt_2_prob_v2.png", "Circuit diagram for (NOT A) AND (B OR C)", "no-border restrict responsive-img") %}
**Figure 12** Circuit diagram for (NOT A) AND (B OR C).
{% endcall %}

**Solution**

As with the previous example, we can take each row of the truth table
and apply their inputs into the circuit. Propagating the results
through the circuit will obtain the final result. As a concrete
example, we show how this works for the case A=0, B=1, and C=0.

{% call m.figure("circuit_tt_2_ans_v2.png", "Realization of the circuit (NOT A) AND (B OR C)", "no-border restrict responsive-img") %}
**Figure 13** Realization of the circuit (NOT A) AND (B OR C) when A=0, B=1 and C=0.
{% endcall %}

The NOT gate will invert the value of A = 0 to 1.  The output of the
OR gate for inputs B=1 and C=0 is 1 since at least one input (in this
case, B) is 1.  Finally, we propagate through the AND gate.  Recall
that the output of AND is 1 whenever both inputs are 1 - which is
achieved for the case under consideration.  This, the final result
is 1.  Repeating this for all input combinations we can arrive at the
final truth table given below.

{% call m.figure("truth_table_NOTA_AND_BORC.png", "Truth table for (NOT A) AND (B OR C)", "no-border restrict responsive-img") %}

**Figure 14** Truth table for (NOT A) AND (B OR C).

{% endcall %}


## Truth Tables to Boolean Expressions {:.truth-tables-to-boolean}


Often a digital logic designer will start with a truth table expression
for a given function and then need to convert it to a Boolean expression
and, ultimately, a circuit. This is an important conversion because:

1.  Truth tables are often the first thing that a circuit designer knows
    about a circuit: what the circuit should output given different
    combinations of inputs.

2.  From a Boolean expression, it is very easy to design the final
    circuit.

There are multiple methods of transforming a truth table to a Boolean
expression. However, in this module, we will utilize a very simple and
intuitive method called the **sum-of-products** Boolean expression form:

1.  For each combination of inputs that results in an output of 1, write
    a Boolean expression that ANDs (*product*) the combination of
    inputs.

2.  *Sum* (OR) each Boolean expression obtained in step 1.

This process will be clearer with an example.

#### **Example 11** {:.exercise}

Write a Boolean expression for Z from the truth table below.

{% call m.figure("truth_bool.PNG", "Truth table to be translated to a boolean expression", "no-border restrict responsive-img") %}
**Figure 15** Truth table to be translated to a boolean expression.
{% endcall %}

**Solution**

1.  Write a Boolean expression for each combination of inputs that
    results in Z=1.

    1.  Z = 1 when X is NOT 1 AND Y is 1: Z = 1 = X'Y
    2.  Z = 1 when X is 1 AND Y is NOT 1: Z = 1 = XY'
    3.  Z = 1 when X is 1 AND Y is 1: Z = 1 = XY

2.  Sum the Boolean expressions obtained from step 1.

    Z = X'Y + XY' + XY

# Chapter Summary {:.summary}


-   **Boolean algebra** performs logical operations on binary inputs to
    produce some useful output.

-   **Logic gates** are the theoretical and electronic components that
    perform Boolean operations:

    -   A **AND** B: Evaluates to 1 when A and B are both 1.

    -   A **OR** B: Evaluates to 1 when at least one of the inputs are
        1.

    -   **NOT** A: Flips the value of A.

-   **Truth tables** show the output of a Boolean expression for every
    possible combination of inputs. If there are $K$ inputs, then there
    will be $2^K$ rows in the truth table.

-   A **digital circuit** is an arrangement of logic gates that apply
    Boolean operations to binary inputs to produce one or more outputs.

-   We can obtain a truth table representation of a digital circuit by
    taking every combination of inputs and propagating them through the
    circuit to obtain the final outputs.

-   Use **sum-of-products** representation to convert truth tables into
    Boolean expressions.

{% endmarkdown %}
