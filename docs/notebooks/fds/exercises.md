# 作业错题整理

>注：仅供自己看，怕传上去要出事。还需要整理排版！

## Chap 2

> 2.3 The recurrent equations for the time complexities of programs P1 and P2 are:
>
> - $P1$: $T(1)=1,T(N)=T(N/3)+1$
> - $P2$: $T(1)=1,T(N)=3T(N/3)+1$
>
> Then the correct conclusion about their time complexities is:

+ $P1$：$O(logN)$，相当于解决一个规模为$N$的问题时，只取其中的三分之一，类似二分法
+ $P2$：$O(N)$，我的理解是相当于把问题分成三份，但都要做，而且还要额外做一个任务，所以是线性增长度。

> 补充：对于$T(N) = kT(N/k) + C$
>
> + 如果$C$为常数，时间复杂度为$O(N)$
> + 如果$C = N$，时间复杂度为$O(NlogN)$

---

> 2.4 For the following piece of code
>
``` c
 if ( A > B ){     
   for ( i=0; i<N*2; i++ )         
     for ( j=N*N; j>i; j-- )             
       C += A; 
 }
 else {     
   for ( i=0; i<N*N/100; i++ )         
     for ( j=N; j>i; j-- ) 
       for ( k=0; k<N*3; k++)
         C += B; 
 } 
```
>
> the lowest upper bound of the time complexity is $O(N^3)$.

这是对的。如果分析有误的话，应该没有理解第3行的trick，尤其是`j > i`那部分。不难发现时间复杂度的最小上界为$O(N^3)$(执行第一个`if`条件)

---

**7-1 Balloon Popping**

Balloon popping is a fun game for kids. Now n balloons are positioned in a line. The goal of the game is very simple: to pop as many balloons as possible. Here we add a special rule to this game -- that is, you can only make ONE jump. Assume that a smart baby covers his/her body by thorns（刺）, jumps to some position and lies down (as shown by the figures below), so that the balloons will be popped as soon as they are touched by any part of the baby's body. Now it is your job to tell the baby at which position he/she must jump to pop the most number of balloons.

**Input Specification:**

Each input file contains one test case. For each case, two positive integers are given in the first line: n (≤105), the number of balloons in a line, and h (≤103), the height of the baby with his/her arms stretched up. Then n integers are given in the next line, each corresponds to the coordinate of a balloon on the axis of the line. It is guaranteed that the coordinates are given in ascending order, and are all in the range [−106,106].

**Output Specification:**

Output in a line the coordinate at which the baby shall jump, so that if the baby jumps at this position and then lie down, the maximum number of the balloons can be popped beneath his/her body. Then also print the maximum number of balloons that can be popped. If the coordinate is not unique, output the smallest one.

The numbers must be separated by 1 space, and there must be no extra space at the beginning or the end of the line.

**Sample Input:**

```in
11 120
-120 -40 0 80 122 140 160 220 240 260 300
```

**Sample Output:**

```out
120 5
```

**Note:** jumping at any position from 120 to 140, or from 240 to 260 can pop 5 balloons, hence 120 is printed as the smallest one.

my code:
``` c
#include <stdio.h>
#define SIZE 100001
int main()
{
    int n, h;                  // 坐标个数，小孩高度
    int coordinates[SIZE];     // 坐标
    int pos, far;              // 最佳位置，最远位置
    int cnt, max = 0;          // 当前个数，最大个数
    int i, j, k;         
    // 输入
    scanf("%d%d", &n, &h);
    for (int k = 0; k < n; k++)
        scanf("%d", &coordinates[k]);
    // 找最佳位置
    for (i = 0; i < n - max; i++)  // n - max 可以减少不必要的查找
    {
        cnt = 1;
        // 按一个个具体坐标找更加高效
        for (j = i + 1; coordinates[j] - coordinates[i] <= h; j++)
        {
            cnt++;
        }
        // 找到当前最佳位置，记录下来
        if (cnt > max)
        {
            max = cnt;
            far = coordinates[j - 1];
            // printf("%d %d\n", temp_pos, max);
        }  
    }

    pos = far - h;  // 求出最佳位置

    printf("%d %d", pos, max);

    return 0;
}
```

## Chap 3

>2.2  If the most commonly used operations are to visit a random position and to insert and delete the last element in a linear list, then which of the following data structures is the most efficient?
> A. doubly linked list
> B. singly linked circular list
> C. doubly linked circular list with a dummy head node
> D. sequential list

**D**，看清题目，它说的是随机访问+在最后进行插入和删除操作，那么显然是数组啦。
这么简单都错，该打🖐️

---
**7-1 Pop Sequence**

Given a stack which can keep M numbers at most. Push N numbers in the order of 1, 2, 3, ..., N and pop randomly. You are supposed to tell if a given sequence of numbers is a possible pop sequence of the stack. For example, if M is 5 and N is 7, we can obtain 1, 2, 3, 4, 5, 6, 7 from the stack, but not 3, 2, 1, 7, 5, 6, 4.

**Input Specification:**

Each input file contains one test case. For each case, the first line contains 3 numbers (all no more than 1000): M (the maximum capacity of the stack), N (the length of push sequence), and K (the number of pop sequences to be checked). Then K lines follow, each contains a pop sequence of N numbers. All the numbers in a line are separated by a space.

**Output Specification:**

For each pop sequence, print in one line "YES" if it is indeed a possible pop sequence of the stack, or "NO" if not.

**Sample Input:**

```in
5 7 5
1 2 3 4 5 6 7
3 2 1 7 5 6 4
7 6 5 4 3 2 1
5 6 4 3 7 2 1
1 7 6 5 4 3 2
```

**Sample Output:**

```out
YES
NO
NO
YES
NO
```

my code:
``` c
#include <stdio.h>
#define SIZE 1000

int main()
{
    int m, n, k;
    int i, j, t;
    int a[SIZE];
    // int stack[SIZE];
    int top, pt;
    int flag, cnt;
    int temp;

    scanf("%d%d%d", &m, &n, &k);
    for (i = 0; i < k; i++)
    {
        
        for (j = 0; j < n; j++)
            scanf("%d", &a[j]);
        
        for (j = 0; j < n - 1; j++)
        {
            flag = 0;
            cnt = 1;
            temp = 0;
            for (t = j + 1; t < n && cnt <= m; t++)
            {
                if (a[t] < a[j])
                {
                    if (!temp || a[t] < temp)
                    {
                        temp = a[t];
                        cnt++;
                    }
                    else
                    {
                        flag = 1;
                        break;
                    }
                }
            }
            if (flag || cnt > m)
            {
                printf("NO\n");
                break;
            }
        }
        if (!flag && cnt <= m)
            printf("YES\n");
    }
    return 0;
}
```

## Chap 4

> 1-2. In a binary search tree which contains several integer keys including 4, 5, and 6, if 4 and 6 are on the same level, then 5 must be their parent.

**F**
5不一定是4, 6的直接父节点，它可能是4, 6的祖先，比如5和4中间放个3，5和6中间放个7，此时4, 6还是处在同一层，但它们的父节点不是5

---
>2-2. If a general tree T is converted into a binary tree BT, then which of the following BT traversals gives the same sequence as that of the post-order traversal of T?
>A. Pre-order traversal
>B. In-order traversal
>C. Post-order traversal
>D. Level-order traversal

**B**
这个光想我也想不好，要画一下图才知道。但为了解题速度，这个可以先死记。

>补充：普通树的前序 = 转化成二叉树的前序
>普通树没有中序……

---
>quiz3-R1-1. The worst cast time complexity of Binary Search is always O(logn) where n is the number of sorted integers.

**F**
==要考虑存储方式==：假设我用**链表**存储二分查找树，那么查找的时间复杂度就不可能是$O(\log n)$了


---
**6-1 Isomorphic**

Two trees, `T1` and `T2`, are **isomorphic** if `T1` can be transformed into `T2` by swapping left and right children of (some of the) nodes in `T1`. For instance, the two trees in Figure 1 are isomorphic because they are the same if the children of A, B, and G, but not the other nodes, are swapped. Give a polynomial time algorithm to decide if two trees are isomorphic.

![](https://images.ptausercontent.com/37)  
Figure 1

Format of functions:

```c++
int Isomorphic( Tree T1, Tree T2 );
```

where `Tree` is defined as the following:

```c++
typedef struct TreeNode *Tree;
struct TreeNode {
    ElementType Element;
    Tree  Left;
    Tree  Right;
};
```

The function is supposed to return 1 if `T1` and `T2` are indeed isomorphic, or 0 if not.

**Sample program of judge:**

```c++
#include <stdio.h>
#include <stdlib.h>

typedef char ElementType;

typedef struct TreeNode *Tree;
struct TreeNode {
    ElementType Element;
    Tree  Left;
    Tree  Right;
};

Tree BuildTree(); /* details omitted */

int Isomorphic( Tree T1, Tree T2 );

int main()
{
    Tree T1, T2;
    T1 = BuildTree();
    T2 = BuildTree();
    printf(“%d\n”, Isomorphic(T1, T2));
    return 0;
}

/* Your function will be put here */
```

**Sample Output 1 (for the trees shown in Figure 1):**

```out
1
```

**Sample Output 2 (for the trees shown in Figure 2):**

```
0
```

![](https://images.ptausercontent.com/38)  
Figure2

my code
``` c
int Isomorphic( Tree T1, Tree T2 )
{
    int cnt[4];

    if (T1 == NULL && T2 == NULL)
        return 1;
    else if (T1 == NULL || T2 == NULL)
        return 0;
    else if (T1->Element == T2->Element)
    {
        cnt[0] = Isomorphic(T1->Left, T2->Left);
        cnt[1] = Isomorphic(T1->Right, T2->Right);
        cnt[2] = Isomorphic(T1->Left, T2->Right);
        cnt[3] = Isomorphic(T1->Right, T2->Left);
        if (cnt[0] && cnt[1] || cnt[2] && cnt[3])
            return 1;
    }
        
    return 0;
}
```

---
**7-1 ZigZagging on a Tree**

Suppose that all the keys in a binary tree are distinct positive integers. A unique binary tree can be determined by a given pair of postorder and inorder traversal sequences. And it is a simple standard routine to print the numbers in level-order. However, if you think the problem is too simple, then you are too naive. This time you are supposed to print the numbers in "zigzagging order" -- that is, starting from the root, print the numbers level-by-level, alternating between left to right and right to left. For example, for the following tree you must output: 1 11 5 8 17 12 20 15.

![zigzag.jpg](https://images.ptausercontent.com/337cbfb0-a7b2-4500-9664-318e9ffc870e.jpg)

Input Specification:

Each input file contains one test case. For each case, the first line gives a positive integer N (≤30), the total number of nodes in the binary tree. The second line gives the inorder sequence and the third line gives the postorder sequence. All the numbers in a line are separated by a space.

Output Specification:

For each test case, print the zigzagging sequence of the tree in a line. All the numbers in a line must be separated by exactly one space, and there must be no extra space at the end of the line.

Sample Input:

```in
8
12 11 20 17 1 15 8 5
12 20 17 11 15 8 5 1
```

Sample Output:

```out
1 11 5 8 17 12 20 15
```

my code(revised)
``` c
#include <stdio.h>
#include <stdlib.h>

#define SIZE 31

typedef struct node * PtrToNode;
typedef PtrToNode tree;
struct node
{
    int data;
    PtrToNode left;
    PtrToNode right;
};

int inorder[SIZE], postorder[SIZE];

tree CreateTree(int in[], int post[], int n);
void Traversal(tree t);

int main()
{
    int n;
    int i, j;
    tree tree;

    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%d", &inorder[i]);
    for (i = 0; i < n; i++)
        scanf("%d", &postorder[i]);
        
    tree = CreateTree(0, n - 1, n - 1);
    Traversal(tree);

    return 0;
}

// 知道中序和后序遍历构造一棵树
tree CreateTree(int in[], int post[], int n)
{
    PtrToNode node;
    int root;
    int i;

	if (!n)
		return NULL;

	root = post[n - 1];
	for (i = 0; i < n && in[i] != root; i++);

	node = (PtrToNode)malloc(sizeof(struct node));
	node->data = root;
	node->left = CreateTree(in, post, i);
	node->right = CreateTree(in + i + 1, post + i, n - i - 1);
	

    return node;
}

// 思路：使用两个堆栈(堆栈可以改变顺序)，一个存从右往左遍历的那层节点(stack1)，另一个存从左往右遍历的那层节点(stack2)，交替进行，直到两个堆栈均为空结束
void Traversal(tree t)
{
    PtrToNode stack1[SIZE], stack2[SIZE];
    int cnt = 0, flag = 1;
    int top1, top2;

    top1 = top2 = -1;
    stack1[++top1] = (PtrToNode)malloc(sizeof(struct node));
    stack1[top1] = t;
    while (top1 != -1 || top2 != -1)
    {   
        if (cnt % 2 == 0)
        {
            while (top1 != -1)
            {
                if (flag)
                {
                    printf("%d", stack1[top1]->data);
                    flag = 0;
                }
                else
                    printf(" %d", stack1[top1]->data);
                if (stack1[top1]->right != NULL)
                {
                    stack2[++top2] = (PtrToNode)malloc(sizeof(struct node));
                    stack2[top2] = stack1[top1]->right;
                }
                if (stack1[top1]->left != NULL)
                {
                    stack2[++top2] = (PtrToNode)malloc(sizeof(struct node));       
                    stack2[top2] = stack1[top1]->left;
                }
                free(stack1[top1--]);
            }
        }
        else
        {
            while (top2 != -1)
            {
                printf(" %d", stack2[top2]->data);
                if (stack2[top2]->left != NULL)
                {
                    stack1[++top1] = (PtrToNode)malloc(sizeof(struct node));
                    stack1[top1] = stack2[top2]->left;
                }

                if (stack2[top2]->right != NULL)
                {
                    stack1[++top1] = (PtrToNode)malloc(sizeof(struct node));                    
                    stack1[top1] = stack2[top2]->right;
                }
                free(stack2[top2--]);
            }
        }
        cnt++;
    }
    printf("\n");
}
```
>我感觉好像没有必要在`Traversal()`函数里使用`malloc()`，因为我已经开了大小确定的数组了🤔

## Chap 5

## Chap 6

### 6-1 Percolate Up and Down

Write the routines to do a "percolate up" and a "percolate down" in a binary min-heap.

**Format of functions:**

```c++
void PercolateUp( int p, PriorityQueue H );
void PercolateDown( int p, PriorityQueue H );
```

where `int p` is the position of the element, and `PriorityQueue` is defined as the following:

```c++
typedef struct HeapStruct *PriorityQueue;
struct HeapStruct {
    ElementType  *Elements;
    int Capacity;
    int Size;
};
```

**Sample program of judge:**

```c++
#include <stdio.h>
#include <stdlib.h>

typedef int ElementType;
#define MinData -1

typedef struct HeapStruct *PriorityQueue;
struct HeapStruct {
    ElementType  *Elements;
    int Capacity;
    int Size;
};

PriorityQueue Initialize( int MaxElements ); /* details omitted */

void PercolateUp( int p, PriorityQueue H );
void PercolateDown( int p, PriorityQueue H );

void Insert( ElementType X, PriorityQueue H ) 
{
    int p = ++H->Size;
    H->Elements[p] = X;
    PercolateUp( p, H );
}

ElementType DeleteMin( PriorityQueue H ) 
{ 
    ElementType MinElement; 
    MinElement = H->Elements[1];
    H->Elements[1] = H->Elements[H->Size--];
    PercolateDown( 1, H );
    return MinElement; 
}

int main()
{
    int n, i, op, X;
    PriorityQueue H;

    scanf("%d", &n);
    H = Initialize(n);
    for ( i=0; i<n; i++ ) {
        scanf("%d", &op);
        switch( op ) {
        case 1:
            scanf("%d", &X);
            Insert(X, H);
            break;
        case 0:
            printf("%d ", DeleteMin(H));
            break;
        }
    }
    printf("\nInside H:");
    for ( i=1; i<=H->Size; i++ )
        printf(" %d", H->Elements[i]);
    return 0;
}

/* Your function will be put here */
```

**Sample Input:**

```in
9
1 10
1 5
1 2
0
1 9
1 1
1 4
0
0
```

**Sample Output:**

```out
2 1 4 
Inside H: 5 10 9
```

my code
``` c
void PercolateUp( int p, PriorityQueue H )
{
    int i;
    ElementType x = H->Elements[p];
    
    for (i = p; H->Elements[i / 2] > x; i /= 2)
        H->Elements[i] = H->Elements[i / 2];

    H->Elements[i] = x;
}

void PercolateDown( int p, PriorityQueue H )
{
    int i, child;
    ElementType last = H->Elements[p];
    
    for (i = p; i * 2 <= H->Size; i = child)
    {
        child = i * 2;
        if (child != H->Size && H->Elements[child + 1] < H->Elements[child])
            child++;
        if  (last > H->Elements[child])
            H->Elements[i] = H->Elements[child];
        else 
            break;
    }
    H->Elements[i] = last;
}
```
>注：这题可以作为模版记忆

---
### 7-1 Complete Binary Search Tree

A Binary Search Tree (BST) is recursively defined as a binary tree which has the following properties:

- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than or equal to the node's key.
- Both the left and right subtrees must also be binary search trees.

A Complete Binary Tree (CBT) is a tree that is completely filled, with the possible exception of the bottom level, which is filled from left to right.

Now given a sequence of distinct non-negative integer keys, a unique BST can be constructed if it is required that the tree must also be a CBT. You are supposed to output the level order traversal sequence of this BST.

**Input Specification:**

Each input file contains one test case. For each case, the first line contains a positive integer N (≤1000). Then N distinct non-negative integer keys are given in the next line. All the numbers in a line are separated by a space and are no greater than 2000.

**Output Specification:**

For each test case, print in one line the level order traversal sequence of the corresponding complete binary search tree. All the numbers in a line must be separated by a space, and there must be no extra space at the end of the line.

**Sample Input:**

```in
10
1 2 3 4 5 6 7 8 9 0
```

**Sample Output:**

```out
6 3 8 1 5 7 9 0 2 4
```

my code
``` c
#include <stdio.h>
#include <stdlib.h>
#define SIZE 1001

void cbst(int root, int * src, int * dst);
int cmp(const void * a, const void * b);
int n, cnt = 1;

int main()
{

    int nodes[SIZE];
    int * results;
    int i;

    scanf("%d", &n);
    for (i = 1; i <= n; i++)
        scanf("%d", &nodes[i]);
    nodes[0] = -1;
    qsort(nodes, n + 1, sizeof(nodes[0]), cmp);
    results = (int *)malloc(sizeof(int) * (n + 1));
    
    cbst(1, nodes, results);
    printf("%d", results[1]);
    for (i = 2; i <= n; i++)
        printf(" %d", results[i]);

    return 0;
}

int cmp(const void * a, const void * b)
{
    return *((int *)a) - *((int *)b); 
}

void cbst(int root, int * src, int * dst)
{
    if (root > n)
        return;

    int l, r;
    l = root * 2;
    r = root * 2 + 1;

    cbst(l, src, dst);
    dst[root] = src[cnt++];
    cbst(r, src, dst);
}
```

## Chap 7

## Chap 8

>2-1. The array representation of a disjoint set containing numbers 0 to 8 is given by { 1, -4, 1, 1, -3, 4, 4, 8, -2 }. Then to union the two sets which contain 6 and 8 (with union-by-size), the index of the resulting root and the value stored at the root are:
>A. 1 and -6
>B. 4 and -5
>C. 8 and -5
>D. 8 and -6

**B**
这题很简单，只要画一下图就ok了~~（当时脑子没长）~~

---
**7-1 File Transfer**

We have a network of computers and a list of bi-directional connections. Each of these connections allows a file transfer from one computer to another. Is it possible to send a file from any computer on the network to any other?

**Input Specification:**

Each input file contains one test case. For each test case, the first line contains N (2≤N≤104), the total number of computers in a network. Each computer in the network is then represented by a positive integer between 1 and N. Then in the following lines, the input is given in the format:

```
I c1 c2  
```

where `I` stands for inputting a connection between `c1` and `c2`; or

```
C c1 c2    
```

where `C` stands for checking if it is possible to transfer files between `c1` and `c2`; or

```
S
```

where `S` stands for stopping this case.

**Output Specification:**

For each `C` case, print in one line the word "yes" or "no" if it is possible or impossible to transfer files between `c1` and `c2`, respectively. At the end of each case, print in one line "The network is connected." if there is a path between any pair of computers; or "There are `k` components." where `k` is the number of connected components in this network.

**Sample Input 1:**

```in
5
C 3 2
I 3 2
C 1 5
I 4 5
I 2 4
C 3 5
S
```

**Sample Output 1:**

```out
no
no
yes
There are 2 components.
```

**Sample Input 2:**

```in
5
C 3 2
I 3 2
C 1 5
I 4 5
I 2 4
C 3 5
I 1 3
C 1 5
S
```

**Sample Output 2:**

```out
no
no
yes
yes
The network is connected.
```

my code
``` c
#include <stdio.h>
#include <math.h>
#define SIZE 100001

int s[SIZE];

void Init(int n);
int Find(int x);
void Union(int n1, int n2);
void CheckCnt(int n1, int n2);
void JoinCnt(int n1, int n2);
void CheckAll(int n);

int main()
{
    int n, i;
    char opt;
    int num1, num2;

    scanf("%d", &n);
    getchar();
    Init(n);
    opt = getchar();
    while (opt != 'S')
    {
        scanf("%d%d", &num1, &num2);
        getchar();
        if (opt == 'C')      
            CheckCnt(num1, num2);            
        else if (opt == 'I')
            JoinCnt(num1, num2);
        opt = getchar();
    }

    CheckAll(n);
    
    return 0;
}

void Init(int n)
{
    int i;
    for (i = 1; i <= n; i++)
        s[i] = -1;
}

int Find(int x)
{
    if (s[x] <= 0)
        return x;
    else 
        return s[x] = Find(s[x]);
}

void Union(int n1, int n2)
{
    if (n1 == n2)
        return;
    if (s[n2] < s[n1])
    {
        s[n2] += s[n1];
        s[n1] = n2;
    }
    else
    {
        s[n1] += s[n2];
        s[n2] = n1;
    }
}

void CheckCnt(int n1, int n2)
{
    if (Find(n1) == Find(n2))
        printf("yes\n");
    else
        printf("no\n");
}

void JoinCnt(int n1, int n2)
{
    Union(Find(n1), Find(n2)); // Important!
}

void CheckAll(int n)
{
    int i;
    int cnt = 0;

    for (i = 1; i <= n; i++)
    {
        if (s[i] <= 0)
            cnt++;       
    }
    if (cnt == 1)
        printf("The network is connected.\n");
    else if (cnt > 1)
        printf("There are %d components.\n", cnt);
}
```

## Chap 9

>2-1. If graph G is NOT connected and has 35 edges, then it must have at least ___ vertices.
>A. 7
>B. 8
>C. 9
>D. 10

**D**

$C(8, 2) = 28, C(9, 2) = 36$，因此9个顶点35条边也能构成连通图，所以需要10个顶点

---
>2-2. A graph with 90 vertices and 20 edges must have *at least* __ connected component(s).
>A. 69
>B. 70
>C. 84
>D. 85

**B**

20条边至多可以将21个顶点连接起来，形成一个连通分量。那么剩余69个顶点各自形成连通分量，所以最小的总的连通分量个数为1 + 69 = 70

---
>2-4. Given an undirected graph G with 16 edges, where 3 vertices are of degree 4, 4 vertices are of degree 3, and all the other vertices are of degrees less than 3. Then G must have at least __ vertices.
>A. 10
>B. 11
>C. 13
>D. 15

**B**

对于无向图，16条边就有32个度，已知3 * 4 + 4 * 3 = 24个度，因此剩下12个度。又因为其余顶点的度少于3个，因此就让它们的度均为2，因此就有 8 / 2 = 4个顶点。所以至少有3 + 4 + 4 = 11个顶点

---
>Midterm-R2-9. A graph with 100 vertices and 12 edges must have *at most* ___ connected component(s).
>A.95
>B.88
>C.94
>D.87

**A**

12条边至少使6个顶点连通，因为$\dfrac{5(5-1)}{2} < 12 \le \dfrac{6(6-1)}{2}$。所以至多有94 + 1 = 95个连通分量

>注：将2-2和Midterm-R2-9对照起来看，注意题目问的是什么

---

>The minimum spanning tree of any weighted graph 
>A. must be unique
>B. must not be unique
>C. exists but may not be unique
>D. may not exist

**D**

最小生成树存在的充要条件是图是 ==连通的==

---
### 6-1 Is Topological Order
Write a program to test if a give sequence `Seq` is a topological order of a given graph `Graph`.

**Format of functions**:

```c++
bool IsTopSeq( LGraph Graph, Vertex Seq[] );
```

where `LGraph` is defined as the following:

```c++
typedef struct AdjVNode *PtrToAdjVNode; 
struct AdjVNode{
    Vertex AdjV;
    PtrToAdjVNode Next;
};

typedef struct Vnode{
    PtrToAdjVNode FirstEdge;
} AdjList[MaxVertexNum];

typedef struct GNode *PtrToGNode;
struct GNode{  
    int Nv;
    int Ne;
    AdjList G;
};
typedef PtrToGNode LGraph;
```

The function `IsTopSeq` must return `true` if `Seq` does correspond to a topological order; otherwise return `false`.

**Note:** Although the vertices are numbered from 1 to MaxVertexNum, they are **indexed from 0** in the LGraph structure.

**Sample program of judge**:

```c++
#include <stdio.h>
#include <stdlib.h>

typedef enum {false, true} bool;
#define MaxVertexNum 10  /* maximum number of vertices */
typedef int Vertex;      /* vertices are numbered from 1 to MaxVertexNum */

typedef struct AdjVNode *PtrToAdjVNode; 
struct AdjVNode{
    Vertex AdjV;
    PtrToAdjVNode Next;
};

typedef struct Vnode{
    PtrToAdjVNode FirstEdge;
} AdjList[MaxVertexNum];

typedef struct GNode *PtrToGNode;
struct GNode{  
    int Nv;
    int Ne;
    AdjList G;
};
typedef PtrToGNode LGraph;

LGraph ReadG(); /* details omitted */

bool IsTopSeq( LGraph Graph, Vertex Seq[] );

int main()
{
    int i, j, N;
    Vertex Seq[MaxVertexNum];
    LGraph G = ReadG();
    scanf("%d", &N);
    for (i=0; i<N; i++) {
        for (j=0; j<G->Nv; j++)
            scanf("%d", &Seq[j]);
        if ( IsTopSeq(G, Seq)==true ) printf("yes\n");
        else printf("no\n");
    }

    return 0;
}

/* Your function will be put here */
```

**Sample Input (for the graph shown in the figure):**

![topord.JPG](https://images.ptausercontent.com/5373e878-196d-45dd-a82f-555b1fea6929.JPG)

```in
6 8
1 2
1 3
5 2
5 4
2 3
2 6
3 4
6 4
5
1 5 2 3 6 4
5 1 2 6 3 4
5 1 2 3 6 4
5 2 1 6 3 4
1 2 3 4 5 6
```

**Sample Output:**

```out
yes
yes
yes
no
no
```

My code:

``` c
bool IsTopSeq( LGraph Graph, Vertex Seq[] )
{
    int indegree[MaxVertexNum];
    int i;
    int flag = 1;
    PtrToAdjVNode cur;

    for (i = 0; i < Graph->Nv; i++)
    {
        indegree[i] = 0;
    }

    for (i = 0; i < Graph->Nv; i++)
    {
        cur = Graph->G[i].FirstEdge;
        while (cur != NULL)
        {
            indegree[cur->AdjV]++;
            cur = cur->Next;
        }
    }

    for (i = 0; i < Graph->Nv; i++)
    {
        if (indegree[Seq[i] - 1] != 0)
        {
            flag = 0;
            break;
        }

        indegree[Seq[i] - 1] = -1;

        cur = Graph->G[Seq[i] - 1].FirstEdge;
        while (cur != NULL)
        {
            indegree[cur->AdjV]--;
            cur = cur->Next;
        }
    }

    if (flag)
        return true;
    else
        return false;
}
```

---
### 7-1 Hamiltonian Cycle

^3b293b

The "Hamilton cycle problem" is to find a simple cycle that contains every vertex in a graph. Such a cycle is called a "Hamiltonian cycle".

In this problem, you are supposed to tell if a given cycle is a Hamiltonian cycle.

**Input Specification:**

Each input file contains one test case. For each case, the first line contains 2 positive integers N (2<N≤200), the number of vertices, and M, the number of edges in an undirected graph. Then M lines follow, each describes an edge in the format `Vertex1 Vertex2`, where the vertices are numbered from 1 to N. The next line gives a positive integer K which is the number of queries, followed by K lines of queries, each in the format:

n V1​ V2​ ... Vn​

where n is the number of vertices in the list, and Vi​'s are the vertices on a path.

**Output Specification:**

For each query, print in a line `YES` if the path does form a Hamiltonian cycle, or `NO` if not.

**Sample Input:**

```in
6 10
6 2
3 4
1 5
2 5
3 1
4 1
1 6
6 3
1 2
4 5
6
7 5 1 4 3 6 2 5
6 5 1 4 3 6 2
9 6 2 1 6 3 4 5 2 6
4 1 2 5 1
7 6 1 3 4 5 2 6
7 6 1 2 5 4 3 1
```

**Sample Output:**

```out
YES
NO
NO
NO
YES
NO
```

My code:

``` c
#include <stdio.h>
#include <stdlib.h>

#define SIZE 201
#define PSIZE 2001

typedef struct AdjVNode *PtrToAdjVNode; 
struct AdjVNode{
    int AdjV;
    PtrToAdjVNode Next;
};

typedef struct Vnode{
    PtrToAdjVNode FirstEdge;
} AdjList[SIZE];

typedef struct GNode *PtrToGNode;
struct GNode{  
    int Nv;
    int Ne;
    AdjList G;
};
typedef PtrToGNode LGraph;

void HCycle(LGraph g, int p[ ]);

int main()
{
    int n, m, k, q;
    int i, j;
    int v1, v2;
    int path[PSIZE];
    LGraph Graph;
    PtrToAdjVNode cur1, cur2;

    Graph = (PtrToGNode)malloc(sizeof(struct GNode));
    scanf("%d%d", &n, &m);
    Graph->Nv = n;
    Graph->Ne = m;
    for (i = 0; i < n; i++)
    {
        Graph->G[i].FirstEdge = NULL;
    }

    for (i = 0; i < m; i++)
    {
        scanf("%d%d", &v1, &v2);
        cur1 = (PtrToAdjVNode)malloc(sizeof(struct AdjVNode));
        cur1->AdjV = v2;
        cur1->Next = Graph->G[v1 - 1].FirstEdge;
        Graph->G[v1 - 1].FirstEdge = cur1;
        cur2 = (PtrToAdjVNode)malloc(sizeof(struct AdjVNode));
        cur2->AdjV = v1;
        cur2->Next = Graph->G[v2 - 1].FirstEdge;
        Graph->G[v2 - 1].FirstEdge = cur2;
    }

    scanf("%d", &k);
    for (i = 0; i < k; i++)
    {
        scanf("%d", &q);
        for (j = 0; j < q; j++)
            scanf("%d", &path[j]);
        if (q != Graph->Nv + 1)
            printf("NO\n");
        else
            HCycle(Graph, path);
    }

    return 0;

}

void HCycle(LGraph g, int p[ ])
{
    int i;
    int flag[SIZE];
    PtrToAdjVNode cur;

    if (p[0] != p[g->Nv])
    {
        printf("NO\n");
    }
    else
    {
        for (i = 0; i < g->Nv; i++)
            flag[i] = 0;
        for (i = 1; i < g->Nv + 1; i++)
        {
            if (flag[p[i - 1] - 1] == 1)
            {
                printf("NO\n");
                return;
            }
            cur = g->G[p[i - 1] - 1].FirstEdge;
            while (cur != NULL && cur->AdjV != p[i])
                cur = cur->Next;
            if (cur == NULL)
            {
                printf("NO\n");
                return;
            }
            flag[p[i - 1] - 1] = 1;
        }
        printf("YES\n");
    }
}
```