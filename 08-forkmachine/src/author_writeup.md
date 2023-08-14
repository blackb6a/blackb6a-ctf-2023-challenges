# Bauhinia CTF 2023 / Fork Machine / Author's Writeup
### Author: [cdemirer](https://github.com/cdemirer)

In this writeup, I will explain how the Fork Machine works, then I will show one way to reverse the `prog.bin` file using what we know about the Fork Machine.

## 1. What is a Fork Machine?


### 1.1 Intro

It is a VM where each "instruction" is executed in a different process, spawned using `fork()`s. However, it doesn't just fork a new process to handle the instruction one at a time. Instead it spawns all instruction-processes (that are known to be needed) at the same time, to run simultaneously. *Use your CPU cores to the max efficiency! Also, \*cough\* please ignore the process spawn overhead \*cough\**.

Obviosuly, for this out-of-order processing to not be total chaos, we need some solution to handle inter-instruction dependencies. To simplify the dependency problem, I opted to go with a "computation graph"-like system where a node's dependencies are implicitly the edges, or in other words the node only depends on nodes which it considers to be its inputs. Using a computation graph also means that all values are immutable. A node can process its inputs (when they are done with their own processing), and the generated output will be the definitive value of that node, never to be changed again.

Example computation graph:
```cpp
# id: node(properties...) #out => output_value

0: const_node(2)        #out => 2
1: const_node(3)        #out => 3
2: op_node(add, :0, :1) #out => 5
```

It is clear how all 3 nodes above could be spawned at the same time, wait for dependencies (if any), and produce their results. They could be configured in the following way, and would do basically the same thing:

```cpp
0: op_node(sub, :2, :1) #out => 5
1: const_node(3)        #out => 3
2: const_node(2)        #out => 2
```

However, what if there were complex control flow, like conditionals and loops?


### 1.2 Conditionals

Let's use this pseudo-code as our target program:

```py
n = 10
if n % 2 == 0:
    n = n // 2
else:
    n = 3 * n + 1
result = n
# assume "result" is used in further calculations
```

Now, what should the node that is supposed to have the value of `result` be like? Let's do some [Static Single Assignment](https://en.wikipedia.org/wiki/Static_single-assignment_form) on this code:

```py
n_0 = 10
if n_0 % 2 == 0:
    n_1 = n_0 // 2
else:
    n_2 = 3 * n_0 + 1
result_0 = phi(n_1, n_2)
```

In this case, `result_0` would be a `phi_node`. How would a phi node work? One possible way would be this: We have a requirements list in a node, such that the node only "runs" if all nodes in the requirements list produce a non-zero value. The phi node could then use the first (and hopefully only) node option that managed to run and produce a value. Here's the list of nodes for the above program:

```cpp
0: const_node(0)                    #out => 0
1: const_node(1)                    #out => 1
2: const_node(2)                    #out => 2
3: const_node(3)                    #out => 3
4: const_node(10)                   #out => 10
5: op_node(mod, :4, :2)             #out => 0
6: op_node(equal, :5, :0)           #out => 1
7: op_node(div, :4, :2, req=[:6])   #out => 5
8: op_node(not, :6)                 #out => 0
9: op_node(mul, :3, :4)             #out => 30 // this could also have requirements, but it doesn't matter
10: op_node(add, :9, :1, req=[:8])  #out => (none) // requirements not met
11: phi_node(:7, :10)               #out => 5 // from :7
```

We could just add more nodes to the list of requirements as we go deeper into nested `if/else` blocks.

But, what about loops though?


### 1.3 The Loop Problem

Let's have the following program:

```py
n = 0
i = 1
limit = int(input())
while i <= limit:
    n = n + i
    i = i + 1
result = n
```

Looks simple. Let's try to convert it to a node-based representation. Wait... we can't do that, due to a number of problems:
- It's a computation graph of immutable nodes, you can't have loops, duh.
- Let's say we have enough nodes for all iterations, how will the phi node for `result` know what choices it has?
- Even if you wanted to unroll the loop, you can't in this case because `limit` is runtime-known.
- etc.

We will come back to the issue of loops. Before that, let's introduce another concept.


### 1.4 Scopes

#### 1.4.1 Scopes Intro

Scopes are collections of nodes that are designed to be spawned together. They are analogous to blocks / suites in regular programming. The Fork Machine uses separate scopes to handle functions and anything that needs to be computed conditionally. A scope contains "node templates" that define how an actual spawned node should look like. A scope is said to be "instantiated" when all its node templates are used to spawn corresponding nodes. *Note that these are all definitions that I made up.*

For the purpose of dynamically instantiating a scope, we now have a `scope_node`. Let's have a short example:

```py
def main():
    return f() + 3

def f():
    return 5
```

```cpp
#scope(id=::0, ret=:2)
0: const_node(3)        #out => 3
1: scope_node(::1)      #out => 5
2: op_node(add, :1, :0) #out => 8

#scope(id=::1, ret=:0)
0: const_node(5)        #out => 5
```

#### 1.4.2 Scope Parameters

The `scope_node` would not be complete without the ability to pass arguments of course. Example:

```py
def main():
    return f(4, 7)

def f(a, b):
    return a * b
```

```cpp
#scope(id=::0, ret=:2)
0: const_node(4)                    #out => 4
1: const_node(7)                    #out => 7
2: scope_node(::1, args=[:0, :1])   #out => 28

#scope(id=::1, ret=:2, num_params=2)
0: phi_node()
1: phi_node()
2: op_node(mul, :0, :1)
```

See what I did there? The `phi_node`s aren't responsible for knowing about their choices anymore, someone else needs to tell them. In this case, the `scope_node` does the telling. We can define that the first `num_params` node templates (which should be `phi_node`s) correspond to the scope's parameters, and `scope_node`s can use this fact to pass arguments by providing those `phi_node`s with the argument nodes.

#### 1.4.3 Non-Function Scopes

Scopes are also useful for `if/else` blocks and `while` loops. In the previous section, we modified `phi_node` to not know about its choices. The `scope_node` is responsible for handling the `phi_node`s that are used as parameters. What about `phi_node`s that are just combining conditional assignments? It would be convenient to have the `phi_node`s know about the choices as we did before (since they are easily knowable, unlike functions which can be called from anywhere). However, we'll use another method, the usefulness of which will be more apparent when we get to `while` loops.

Introducing: the `phi_setter` node. This node simply tells a `phi_node` the node it will get its value from. Let's see an example:

```py
def main():
    x = 1
    if 0:
        x = 2
    return x
```

```cpp
#scope(id=::0, ret=:5)
0: const_node(0)                        #out => 0
1: const_node(1)                        #out => 1
2: scope_node(::1, args=[], req=[:0])   #out => (none) // ::1 doesn't return a value
3: op_node(not, :0)                     #out => 1
4: phi_setter(:5, :1, req=[:3])         #out => (none) // no value
5: phi_node()                           #out => 1 // from ::0:1

#scope(id=::1)
0: const_node(2)
1: phi_setter(::@:5, :0)
```

Above, there are 2 `phi_setter` nodes. One (`::0:4`) that sets the `phi_node` to `x`'s initial value of 1 *if the `if`s condition is false*. Another one (`::1:1`) that sets the `phi_node` *if it ever gets the chance to do so by its scope being instantiated*. Note the `::@:5` form, which refers to the `:5` of the "outer scope" or "current scope's instantiator's scope". This is a placholder value for the template node, which will be "filled in" by the `scope_node` at runtime.

Let's revisit an example from before:

```py
n = 10
if n % 2 == 0:
    n = n // 2
else:
    n = 3 * n + 1
result = n
```

These were the nodes we set up back then:

```cpp
0: const_node(0)                    #out => 0
1: const_node(1)                    #out => 1
2: const_node(2)                    #out => 2
3: const_node(3)                    #out => 3
4: const_node(10)                   #out => 10
5: op_node(mod, :4, :2)             #out => 0
6: op_node(equal, :5, :0)           #out => 1
7: op_node(div, :4, :2, req=[:6])   #out => 5
8: op_node(not, :6)                 #out => 0
9: op_node(mul, :3, :4)             #out => 30 // this could also have requirements, but it doesn't matter
10: op_node(add, :9, :1, req=[:8])  #out => (none) // requirements not met
11: phi_node(:7, :10)               #out => 5 // from :7
```

Adjusting it to use our current node scheme, we have this:

```py
def collatz(n)
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    return n
```
```cpp
#scope(id=::0, ret=:11, num_params=1)
0: phi_node()
1: const_node(0)
2: const_node(2)
3: op_node(mod, :0, :2)
4: op_node(equal, :3, :1)
5: scope_node(::1, args=[0], req=[:4])
6: op_node(not, :4)
7: phi_setter(:8, :0, req=[:6])
8: phi_node()
9: scope_node(::2, args=[8], req=[:6])  // both args=[0] and args=[8] can make sense here and are equivalent
10: phi_setter(:11, :8, req=[:4])
11: phi_node()

#scope(id=::1, ret=None, num_params=1)
0: phi_node()
1: const_node(2)
2: op_node(div, :0, :1)
3: phi_setter(::@:8, :2)

#scope(id=::2, ret=None, num_params=1)
0: phi_node()
1: const_node(3)
2: const_node(1)
3: op_node(mul, :1, :0)
4: op_node(add, :3, :2)
5: phi_setter(::@:11, :4)
```

Ok, the number of nodes almost doubled and it's much more complex now. Why did we do this again?!

Because of this:

```py
def triangle(n)
    s = 0
    i = 1
    while i <= n:
        s = s + i
        i = i + 1
    return s
```
```cpp
#scope(id=::0, ret=:9, num_params=1)
0: phi_node()
1: const_node(0)
2: const_node(1)
3: op_node(lte, :2, :0)
4: scope_node(::1, args=[:2, :0, :1], req=[:3])
5: op_node(not, :3)
6: phi_setter(:8, :2, req=[:5])
7: phi_setter(:9, :1, req=[:5])
8: phi_node() // final i
9: phi_node() // final s

#scope(id=::1, ret=None, num_params=3)
0: phi_node() // i
1: phi_node() // n
2: phi_node() // s
3: const_node(1)
4: op_node(add, :2, :0) // next s
5: op_node(add, :0, :3) // next i
6: op_node(lte, :5, :1)
7: scope_node(::1, args=[:5, :1, :4], req=[:6])
8: op_node(not, :6)
9: phi_setter(::@:8, :5, req=[:8])
10: phi_setter(::@:9, :4, req=[:8])
```

Nice, isn't it? Note that here `::@` refers not to the immediate outer scope (which may be the previous iteration of the loop), but to the outer scope of the "root" scope of this loop. In this case it refers to `::0`.


### 1.5 Vectors

Finally, we have the vector value type. They are like arrays/lists but they are immutable, so a copy is made when they are modified. A vector contains values of any type (i.e. int or vector). A `vector_node` is used to create a vector value from a list of input nodes.

## 2. Reversing `prog.bin`

When you play the challenge, you don't have access to the design notes above, but you have access to the source code of the Fork Machine. The following can be known / deduced from the source:
- Various kinds of nodes and what they do
- Value types (`int`, `vector`)
- Compute ops (`add`, `sub`, etc.)
- Something called `scope`, that it can have parameters and optionally a return `id`
- How nodes have `id`s and how they refer to each other within a scope
- The way parameters are passed when instantiating a scope
- How nodes and scopes are serialized into a program file such as `prog.bin`
- That the first scope corresponds to the `main` function.
- etc.

In `prog.bin`, there are many scopes to deal with. In order to classify them, we can use the following knowledge:
- Scopes that do have a `ret_id` are likely to be functions.
- Scopes that have a `scope_node` that instantiates the same scope are likely loops.
- Other scopes are likely `if/else` suites.

We can also look at the hierarchy of non-function scopes within a function scope. For example, here's the scope hierarchy for `prog.bin`:

```text
Scope Hierarchy
::0 (fn)
    ::1 (if)
        ::2 (if)
            ::3 (if)
            ::4 (if)
::5 (fn)
    ::6 (loop)
    ::7 (loop)
        ::8 (if)
        ::9 (if)
    ::10 (loop)
::11 (fn)
    ::12 (loop)
```

We can print the scopes in a format similar to the one used in the previous section. Using the scope hierarchy as our guide, we can figure out what each scope is doing. This isn't a very structured process, everyone would have their own way of doing it. It might be possible to write something like a decompiler to make it easier, but I haven't written one.

Here's the source code of `prog.bin` for your reference:

```py
# Note: This is not exactly Python.

def main(input):
    ret = 'Definitely not the flag.'
    t = -1
    if len(input) >= 9:
        if (input[0] == 'b'[0]) & (input[1] == '6'[0]) & (input[2] == 'a'[0]):
            t = transform(input)
            if t == [19, 105, 105, 56, 48, 124, 17, 25, 23, 77, 23, 13, 53, 49, 93, 125, 66, 111, 12, 14, 77, 60, 21, 112, 83, 96, 42, 71, 2, 4, 48, 61, 88, 112, 21, 8, 86, 12, 123, 16, 61, 50, 24, 32, 32, 92, 58, 39, 75, 4, 3, 107, 125, 81, 33, 74, 9, 14]:
                ret = 'Yes, that\'s the flag!'
            else:
                ret = 'Sorry, that\'s not the flag'
    return ret

def transform(input):
    h = hash(input) % 127
    xs = input
    i = 1
    while i < len(xs):
        xs[i] = xs[i] ^ xs[i-1]
        i += 1
    i = 0
    while i < len(xs):
        if i % 2 == 0:
            xs[i] = xs[i] * 69 % 127
        else:
            xs[i] = xs[i] * 420 % 127
        i += 1
    i = 0
    while i < len(xs):
        xs[i] = xs[i] ^ h
        i += 1
    return xs

def hash(arr):
    ret = 0
    base = 31
    base_p = 1
    i = 0
    while i < len(arr):
        ret = (ret + arr[i] * base_p) % 1000000007
        base_p = base_p * base % 1000000007
        i += 1
    return ret
```

It's easy to write a solver for this algo:

```py
def hash(arr):
    ret = 0
    base = 31
    base_p = 1
    i = 0
    while i < len(arr):
        ret = (ret + arr[i] * base_p) % 1000000007
        base_p = base_p * base % 1000000007
        i += 1
    return ret

def undo_transform(transformed):
    solutions = []
    for h in range(127):
        xs = transformed[:]
        for i in range(len(xs)):
            xs[i] ^= h
            if i % 2 == 0:
                xs[i] = xs[i] * 81 % 127
            else:
                xs[i] = xs[i] * 114 % 127
        for i in reversed(range(1, len(xs))):
            xs[i] ^= xs[i-1]
        if hash(xs) % 127 != h:
            continue
        solutions.append(''.join(chr(x) for x in xs))
    solutions = [x for x in solutions if x.startswith('b6actf{')]
    if len(solutions) != 1:
        print(f'{solutions=}')
        exit()
    else:
        return solutions[0]
```

And we get the flag:

```py
>>> undo_transform([19, 105, 105, 56, 48, 124, 17, 25, 23, 77, 23, 13, 53, 49, 93, 125, 66, 111, 12, 14, 77, 60, 21, 112, 83, 96, 42, 71, 2, 4, 48, 61, 88, 112, 21, 8, 86, 12, 123, 16, 61, 50, 24, 32, 32, 92, 58, 39, 75, 4, 3, 107, 125, 81, 33, 74, 9, 14])
'b6actf{Sp00n_M4ch1ne_1s_l3f7_a5_4n_3x3rc1s3_7o_th3_r34d3r}'
```

I hope it was fun solving it / attempting to solve it!
