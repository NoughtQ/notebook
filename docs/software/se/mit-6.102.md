---
counter: true
---

# MIT 6.102: Software Construction

!!! note "课程目标"

    - **Safe from bugs**. Correctness (correct behavior right now) and defensiveness (correct behavior in the future) are required in any software we build.
    - **Easy to understand**. The code has to communicate to future programmers who need to understand it and make changes in it (fixing bugs or adding new features). That future programmer might be you, months or years from now. You’ll be surprised how much you forget if you don’t write it down, and how much it helps your own future self to have a good design.
    - **Ready for change**. Software always changes. Some designs make it easy to make changes; others require throwing away and rewriting a lot of code.

## Static Checking

编程语言的三种类型检查方式：

- **静态检查**(static checking)：在程序运行前就自动检测到 bug，可以发现以下和变量**类型**相关的错误：
    - 语法错误
    - 拼写错误的名称
    - 错误的参数数量和类型
    - 错误的返回类型

- **动态检查**(dynamic checking)：程序执行时自动检测到 bug，可以发现以下错误：
    - 特定的非法参数值（比如除以零）
    - 非法转换
    - 索引越界或缺失的键

- **不检查**(no checking)：语言本身不会检查错误，需要自己仔细检查

显然，静态检查 > 动态检查 > 不检查。

!!! note "静态检查与课程目标的关系"

    - Safe from bug：有助于在运行之前捕获类型错误等错误，从而提高安全性
    - Easy to understand：类型在代码中明确定义
    - Ready for change：通过识别其他需要同时更改的地方，使代码的更改变得更加容易


## Testing

## Code Review

## Specifications

## Designing Specifications

## Abstract Data Types

## Abstraction Functions & Rep Invariants

## Interfaces & Subtyping

## Equality

## Functional Programming

## Recursive Data Types

## Grammars & Parsing

## Debugging

## Concurrency

## Promises

## Mutual Exclusion

## Callbacks & Graphical User Interfaces

## Message-Passing & Networking

## Little Languages