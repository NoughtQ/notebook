# Glossary

>这里只选录了部分词汇和结论，仅供考前快速记忆和方便查阅。中文主要是我自己翻译的，未标注中文或未摘录的(也有可能是我漏掉了)词汇不作为考点。

## Chap 1 The Foundations: Logic and Proofs

+ proposition：命题
+ proposition variable：命题变量
+ truth value：真值
+ $\neg p$, negation：否定
+ logical operators：逻辑运算符
+ compound proposition：复合命题
+ truth table：真值表
+ $p \vee q$, disjunction：析取
+ $p \wedge q$, conjunction：合取
+ $p \oplus q$, exclusive or：异或
+ $p \rightarrow q$：条件语句
+ converse of $p \rightarrow q$：逆命题$q \rightarrow p$
+ contrapositive of $p \rightarrow q$：逆否命题$\neg q \rightarrow \neg p$
+ inverse of $p \rightarrow q$：否命题$\neg p \rightarrow \neg q$
+ $p \leftrightarrow q$, biconditional：双条件语句
+ bit：位
+ Boolean variable：布尔变量
+ bit operation：位运算
+ bit string：位串
+ bitwise operations：按位运算
+ tautology：永真
+ contradiction：永假
+ contingency：(可能为真也可能为假)
+ consistent compound propositions：一致复合命题
+ satisfiable compound propositions：可满足的复合命题
+ logically equivalent compound propositions：逻辑等价复合命题
+ propositional function：命题函数
+ domain of discourse：域
+ $\exists x\ P(x)$, existential quantification：存在量词
+ $\forall x\ P(x)$, universal quantification：全称量词
+ logically equivalence expressions：逻辑等价命题
+ free variable：自由变量
+ bound variable：约束变量
+ scope of a quantifier：量词范围
+ argument：论证
+ argument form：论证形式
+ premise：前提
+ conclusion：结论
+ valid argument form：合法的论证形式
+ valid argument：合法论证
+ rule of inference：推理规则
+ fallacy：谬误
+ circular reasoning or begging the question：循环论证
+ theorem：定理
+ conjecture：猜想
+ proof：证明
+ axiom：公理
+ lemma：引理 
+ corollary：推论
+ vacuous proof：空证明
+ trivial proof：平凡证明
+ direct proof：直接证明
+ proof by contraposition：反证法
+ proof by contradiction：归谬法
+ exhaustive proof：穷举证明
+ proof by cases：分类证明
+ without loss of generality：不失一般性
+ counterexample：反例
+ constructive existence proof：构造存在证明
+ nonconstructive existence proof：非构造存在证明
+ rational number：有理数
+ uniqueness proof：唯一性证明

---
+ 逻辑等值表
+ 量词的德摩根定理
+ 推断规则(命题演算、量词语句)

## Chap 2 Basic Structures: Sets, Functions, Sequences, Sums, and Matrices

+ set：集合
+ paradox：悖论
+ element, member of set：集合的元素或成员
+ roster method：枚举法
+ set builder notation
+ multiset：多重集
+ $\emptyset$, empty/null set：空集
+ universal set：全集
+ Veen diagram：维恩图
+ $S = T$：集合等价
+ $S \subseteq T$：S是T的子集
+ $S \subset T$：S是T的真子集
+ finite set：有限集
+ infinite set：无限集
+ $|S|$, the cardinality of S：S的基数
+ $P(S)$：S的幂集
+ $A \cup B$, union：A和B的并集
+ $A \cap B$, intersection：A和B的交集
+ $A - B$, difference：A和B的差集
+ $\overline{A}$, complement：A的补集
+ $A \oplus B$, symmetric difference：A和B的对称差集
+ membership table：成员表
+ function from A to B：A到B的函数
+ domain of f：f的域
+ codomain of f：f的伴域
+ b is the image of a under f, b = f(a)：b是a在f下的象
+ a is a preimage of b under f, f(a) = b：a是b在f下的一个原象
+ range of f：f的范围
+ onto function, surjection：满射函数
+ one-to-one function, injection：单射函数
+ one-to-one correspondence, bijection：双射函数
+ inverse of f：f的反函数
+ $f \circ g$, composition：f和g的复合函数
+ $\lfloor x \rfloor$, floor function：底函数
+ $\lceil x \rceil$, ceiling function：顶函数
+ sequence：序列
+ geometric progression：几何级数(等比数列)
+ arithmetic progression：算术级数(等差数列)
+ string：字符串
+ empty string：空字符串
+ recurrence relation：递推关系
+ cardinality：基数
+ countable set：可数集合
+ uncountable set：不可数集合
+ $\aleph_0$：表示可数集合的基数
+ $c$：实数集的基数
+ Cantor diagonalization argument：康托对角化论证
+ computable function：可计算函数
+ uncomputable function：不可计算函数
+ continuum hypothesis：连续统假设
+ matrix：矩阵
+ matrix addition：矩阵加法
+ matrix multiplication：矩阵乘法
+ $I_n$, identity matrix of order n：n阶单位矩阵
+ $A^t$, transpose of A：A的转置矩阵
+ symmetric matrix：对称矩阵
+ zero-one matrix：零一矩阵
+ $\bm{A} \vee \bm{B}$, join：A和B的并
+ $\bm{A} \wedge \bm{B}$, meet：A和B的交
+ $\bm{A} \odot \bm{A}$, Boolean product：A和B的布尔积

---
+ 集合恒等式
+ 序列和公式
+ 有理数集是可数的
+ 实数集是不可数的


## Chap 3

## Chap 4 Number Theory and Cryptography

+ $a\ |\ b$ (a divides b)：整除
+ a and b are congruent module m: m divides a - b：a与b模m同余
+ prime：质数
+ composite：合数
+ Mersenne prime：梅森质数，$2^p - 1$，p为质数
+ gcd(a, b)：a, b的最大公约数
+ relatively prime integers：互质整数
+ pairwise relatively prime integers：两两互质整数
+ lcm(a, b)：a, b的最小公倍数
+ a mod b：a模除b
+ $a \equiv b(\text{mod } m)$：a与b模m同余
+ $n = (a_ka_{k-1}\dots a_1a_0)_b$：n的b进制表示法
+ binary representation：二进制
+ octal representation：八进制
+ hexadecimal representation：十六进制
+ linear combination of a and b with integer coefficients：带整系数的a, b的线性组合
+ Bezout coefficients of a and b：使Bezout identity sa + tb = gcd(a, b)成立
+ inverse of a modulo m：a模m的逆，满足$a\overline{a} \equiv 1(\text{mod } m)$
+ linear congurence：线性同余，$ax \equiv b(\text{mod } m)$
+ pseudoprime to the base b：基底b的伪质数，合数n满足$b^{n-1} \equiv 1 (\text{mod } n)$
+ Carmichael number：卡迈克尔数
+ primitive root of a prime p
+ discrete logarithm of a to the base r modulo p

---
+ division algorithm：除法算法
+ b进制表达扩展
+ fast modular exponentiation algorithm：快速指数模算法
+ Euclidean algorithm：欧几里得算法
+ Bezout's theorem：裴蜀定理
+ sieve of Eratosthenes：埃氏筛
+ fundamental theorem of arithmetic：算术基本定理
+ Chinese remainder theorem：中国剩余定理
+ Fermat's little theorem：费马小定理

## Chap 5 Induction and Recursion

+ sequence：序列
+ geometric progression：几何级数/等比数列
+ arithmetic progression：算术级数/等差数列
+ the principle of mathematical induction：数学归纳法
+ basis step：基本步骤
+ inductve step：递归步骤
+ strong induction：强归纳法
+ well-ordering property：良序性
+ recursive definition of a function：函数的递归定义
+ recursive definition of a set：集合的递归定义
+ structural induction：结构化归纳
+ recursive algorithm：递归算法
+ merge sort
+ iteration：迭代
+ program correctness
+ loop invariant
+ initial assertion
+ final assertion

## Chap 6 Counting

+ combinatorics：组合学
+ enumeration：枚举
+ tree diagram：树形图
+ r-permutation：r排列，P(n, r)
+ r-combination：r组合，C(n, r)
+ binomial coefficient$\left(\begin{array}{a} n \\ r\end{array}\right)$：二项式系数
+ combinatorial proof：组合证明
+ Pascal's triangle：帕斯卡三角形
+ S(n, j)：(第二类)斯特林数

---
+ product rule for counting(sets)：计数(或集合)的乘积法则
+ sum rule for counting(sets)：计数(或集合)的和法则
+ subtraction rule or inclusion-exclusion for counting(sets)：计数(或集合)的减法法则，或者容斥原理
+ division rule for counting(sets)：计数(或集合)的除法法则
+ the pigeonhole principle：鸽巢原理
+ the generalized pigeonhole principle：广义鸽巢原理
+ Pascal's identity：帕斯卡恒等式
+ the binomial theorem：二项式定理

## Chap 8 Advanced Counting Techniques

+ recurrence relation：递推关系
+ initial conditions for a recurrence relation：递推关系的首条件
+ dynamic programming
+ linear homogenous recurrence relation with constant coefficients：常系数线性齐次递推关系
+ characteristic roots of a linear homogenous recurrence relation with constant efficients：常系数线性齐次递推关系的特征根
+ linear nonhomogenous recurrence relation with constant coefficients：常系数线性非齐次递推关系
+ divide-and-conquer algorithm
+ generating funcition of a sequence：序列的生成函数
+ sieve of Eratosthenes：埃氏筛(又出现了一遍)
+ derangement：错排

---
+ the principle of inclusion-exclusion：容斥原理
+ 满射函数的个数
+ 错排的个数

## Chap 9 Relation

+ binary relation from A to B：A到B的二元关系
+ relation on A：在A上的关系
+ $S \circ R$：R和S的复合关系
+ $R^{-1}$：R的逆关系
+ $R^n$：R的n次幂
+ reflexive：自反性
+ symmetric：对称性
+ antisymmetric：反对称性
+ transitive：传递性
+ n-ary relation on $A_1, A_2, \dots, A_n$：n元关系
+ directed graph / digraph：有向图
+ loop：环
+ closure of a relation R with respect to a property P：R上关于性质P的闭包
+ path in a digraph：有向图上的路径
+ circuit(or cycle) in a digraph：有向图上的环
+ $R^*$, connectivity relation：连通关系
+ equivalence relation：等价关系
+ equivalent：等价
+ $[a]_R$, equivalence class：关于R的a的等价类
+ $[a]_m$, congruence class modulo m：模m的同余类
+ partition of a set S：集合S的分区
+ partial ordering：偏序
+ poset(S, R)：偏序集
+ comparable：可比的
+ incomparable：不可比的
+ total (or linear) ordering：全序
+ totally (or linearly) ordering set：全序集
+ well-ordered set：良序集
+ lexicographic order：词典序
+ Hasse diagram：哈斯图
+ maximal element：极大元素
+ minimal element：极小元素
+ greatest element：最大元素
+ least element：最小元素
+ upper bound of a set：集合的上限
+ lower bound of a set：集合的下限
+ least upper bound of a set：集合的最小上界
+ greatest lower bound of a set：集合的最大下界
+ lattice：格
+ compatible total ordering for a partial ordering：对某个偏序兼容的全序
+ topological sort：拓扑排序

---
+ reflexive closure：自反闭包
+ symmetric closure：对称闭包
+ transitive closure：传递闭包
+ Warshall's algorithm
+ 关于等价关系的3条等价语句
+ 等价类&分区
+ the principle of well-ordered induction：良序归纳法
+ 拓扑排序算法

## Chap 10 Graphs

+ undirected edge：无向边
+ directed edge：有向边
+ multiple edges：重边
+ multiple directed edges：有向重边
+ loop：环
+ undirected graph：无向图
+ simple graph：简单图
+ multigraph：多重图
+ pseudograph：伪图
+ directed graph：有向图
+ directed multigraph：有向多重图
+ simple directed graph：简单有向图
+ adjacent：相邻的(2顶点间)
+ incident：关联的(边和顶点)
+ $\mathrm{deg}\ v$：顶点v的度
+ $\mathrm{deg}^-\ v$：顶点v的入度
+ $\mathrm{deg}^+\ v$：顶点v的出度
+ underlying undirected graph of a graph with directed edges：(有向图的)潜在无向图
+ $K_n$(complete graph on $n$ vertices)：完全图
+ bipartite graph：二分图
+ $K_{m, n}$(complete bipartite graph)：完全二分图
+ $C_n$(cycle of size $n(\ge 3)$)：环
+ $W_n$(wheel of size $n(\ge 3)$)：轮
+ $Q_n$($n$-cube)：n立方
+ matching in a graph $G$：匹配
+ complete matching $M$ from $V_1$ to $V_2$：完全匹配
+ maximum matching：最大匹配
+ isolated vertex：孤立顶点(度为0)
+ pendant vertex：下悬顶点(度为1)
+ regular graph：正则图(每个顶点的度相同)
+ subgraph of a graph $G = (V, E)$：子图
+ $G_1 \cup G_2$(union of $G_1$ and $G_2$)：交集
+ adjacency matrix：邻接矩阵
+ indidence matrix：关联矩阵
+ isomorphic simple graphs：同构简单图
+ invariant for graph isomorphism：图同构的不变量
+ path from $u$ to $v$ in a graph with undirected/directed edges：路径
+ simple path：简单路径
+ circuit：回路/环
+ connected graph：连通图
+ cut vertex of $G$：割点
+ cut edge of $G$：割边
+ nonseparable graph：不可分割集
+ vertex cut of G：点割集
+ $\kappa(G)$(the vertex connectivity of $G$)：点连通度
+ $k$-connected graph：k连通度
+ edge cut of $G$：边割集
+ $\lambda(G)$(the edge connectivity of $G$)：边连通度
+ connected component of a graph $G$：连通分量
+ strongly connected directed graph：强连通有向图
+ strongly connected component of a directed graph $G$：有向图的强连通分量
+ Euler path：欧拉路
+ Euler circuit：欧拉环(回路)
+ Hamilton path：哈密顿路
+ Hamilton circuit：哈密顿环(回路) 
+ weighted graph：带权图
+ shortest-path problem：最短路问题
+ traveling salesperson problem：旅行商问题
+ planar graph：平面图
+ regions of a representation of a planar graph：平面图表示法的区域
+ elementary subdivision：初等细分
+ homeomorphic：同胚的
+ graph coloring：图着色
+ chromatic number：着色数

---
+ the handshaking theorem：握手定理 
+ Hall's marriage theorem：霍尔婚配定理
+ 欧拉环和欧拉路存在的充要条件
+ Dijkstra's algorithm
+ Euler's formula
+ Kuratowski's theorem
+ the four color theorem：四色定理

## Chap 11 Trees

+ tree：树
+ forest：森林
+ rooted tree：有根树
+ subtree：子树
+ parent of $v$ in a rooted tree：父节点
+ child of $v$ in a rooted tree：孩子节点
+ sibling of $v$ in a rooted tree：兄弟节点
+ ancestor of $v$ in a rooted tree：祖先
+ descendant of $v$ in a rooted tree：后代
+ internal vertex：内部节点
+ leaf：叶子节点
+ level of a vertex：层级
+ height of a tree：高度
+ $m$-ary tree：$m$叉树
+ full $m$-ary tree：满$m$叉树
+ binary tree：二叉树
+ ordered tree：有序树
+ balanced tree：平衡树
+ binary search tree：二叉搜索树
+ decision tree：决策树
+ game tree：博弈树
+ prefix code：前缀码
+ minmax strategy：极小极大策略
+ tree traversal：树的遍历
+ preorder traversal：前序遍历
+ inorder traversal：中序遍历
+ postorder traversal：后序遍历
+ infix notation：中缀表示法
+ prefix/Polish notation：前缀/波兰表示法
+ postfix/reverse Polish notation：后缀/逆波兰表示法
+ spanning tree：生成树
+ minimum spanning tree：最小生成树

---
+ Huffman coding：哈夫曼编码
+ depth-first search/backtraking：深度优先搜索/回溯
+ breadth-first search：宽度优先搜索
+ Prim's algorithm
+ Kruskal's algorithm