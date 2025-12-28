# 汇编与接口

!!! info "课程信息"

    - 学分：4.5
    - 教师：蔡铭
    - 教材：Barry B. Brey *INTEL Microprocessors* 8th Edition（~~09 年出版，没有再更新过，可见课程内容相当古老~~）

??? question "为什么要修这门课"

    ~~为了凑模块课的学分（确信）~~

    对大多数开发者而言，汇编语言并不能对他们所从事的工作起到直接的帮助。但是缺少对汇编语言的理解会让我们难以理解程序是如何运行的，以及代码实际上在做什么。

    ??? example "例子"

        === "例1"

            <div style="text-align: center">
                <img src="images/C1/3.png" width=60% />
            </div>

            对于不同的编译优化选项，程序运行结果会变得不一样。这种不一致的输出正是**未指定行为**(unspecified behavior)的体现。

        === "例2"

            <div style="text-align: center">
                <img src="images/C1/4.png" width=70% />
            </div>

            进入上图所示[链接](https://www.godbolt.org/z/xTYPhr14n)（一个在线编译环境）后，尝试用右侧给出的编译器和优化选项进行编译，发现编译得到的汇编语言程序各不相同。

            === "x86-64 gcc -O1"

                ```asm
                Sum1ToN:
                        test    edi, edi
                        jle     .L4
                        mov     eax, 0
                        mov     edx, 0
                .L3:
                        add     edx, eax
                        add     eax, 1
                        cmp     edi, eax
                        jne     .L3
                .L1:
                        mov     eax, edx
                        ret
                .L4:
                        mov     edx, 0
                        jmp     .L1
                ```

            === "x86-64 gcc -O3"

                ```asm
                Sum1ToN:
                        mov     edx, edi
                        test    edi, edi
                        jle     .L7
                        lea     eax, [rdi-1]
                        cmp     eax, 9
                        jbe     .L8
                        mov     ecx, edi
                        movdqa  xmm1, XMMWORD PTR .LC0[rip]
                        xor     eax, eax
                        pxor    xmm0, xmm0
                        movdqa  xmm3, XMMWORD PTR .LC1[rip]
                        shr     ecx, 2
                .L4:
                        movdqa  xmm2, xmm1
                        add     eax, 1
                        paddd   xmm1, xmm3
                        paddd   xmm0, xmm2
                        cmp     eax, ecx
                        jne     .L4
                        movdqa  xmm1, xmm0
                        mov     ecx, edx
                        psrldq  xmm1, 8
                        and     ecx, -4
                        paddd   xmm0, xmm1
                        movdqa  xmm1, xmm0
                        psrldq  xmm1, 4
                        paddd   xmm0, xmm1
                        movd    eax, xmm0
                        test    dl, 3
                        je      .L11
                .L3:
                        lea     esi, [rcx+1]
                        add     eax, ecx
                        cmp     edx, esi
                        jle     .L1
                        add     eax, esi
                        lea     esi, [rcx+2]
                        cmp     edx, esi
                        jle     .L1
                        add     eax, esi
                        lea     esi, [rcx+3]
                        cmp     edx, esi
                        jle     .L1
                        add     eax, esi
                        lea     esi, [rcx+4]
                        cmp     edx, esi
                        jle     .L1
                        add     eax, esi
                        lea     esi, [rcx+5]
                        cmp     edx, esi
                        jle     .L1
                        add     eax, esi
                        lea     esi, [rcx+6]
                        cmp     edx, esi
                        jle     .L1
                        add     eax, esi
                        lea     esi, [rcx+7]
                        cmp     edx, esi
                        jle     .L1
                        add     eax, esi
                        lea     esi, [rcx+8]
                        cmp     edx, esi
                        jle     .L1
                        add     eax, esi
                        add     ecx, 9
                        lea     esi, [rax+rcx]
                        cmp     edx, ecx
                        cmovg   eax, esi
                        ret
                .L7:
                        xor     eax, eax
                .L1:
                        ret
                .L11:
                        ret
                .L8:
                        xor     ecx, ecx
                        xor     eax, eax
                        jmp     .L3
                .LC0:
                        .long   0
                        .long   1
                        .long   2
                        .long   3
                .LC1:
                        .long   4
                        .long   4
                        .long   4
                        .long   4
                ```

            === "x86-64 icc 2021.10.0 -O3"

                ```asm
                Sum1ToN:
                ..B1.1:                         # Preds ..B1.0
                        push      rbx                                           #2.19
                        push      rbp                                           #2.19
                        xor       eax, eax                                      #3.10
                        test      edi, edi                                      #4.22
                        jle       ..B1.22       # Prob 50%                      #4.22
                ..B1.2:                         # Preds ..B1.1
                        mov       ecx, edi                                      #4.2
                        mov       ebx, 1                                        #4.2
                        xor       edx, edx                                      #4.2
                        shr       ecx, 3                                        #4.2
                        je        ..B1.6        # Prob 9%                       #4.2
                ..B1.3:                         # Preds ..B1.2
                        xor       r11d, r11d                                    #5.4
                        xor       r10d, r10d                                    #5.4
                        xor       r9d, r9d                                      #5.4
                        xor       r8d, r8d                                      #5.4
                        xor       esi, esi                                      #5.4
                        xor       ebp, ebp                                      #5.4
                        xor       ebx, ebx                                      #5.4
                ..B1.4:                         # Preds ..B1.4 ..B1.3
                        lea       eax, DWORD PTR [rax+rdx*8]                    #5.4
                        lea       r11d, DWORD PTR [1+r11+rdx*8]                 #5.4
                        lea       r10d, DWORD PTR [2+r10+rdx*8]                 #5.4
                        lea       r9d, DWORD PTR [3+r9+rdx*8]                   #5.4
                        lea       r8d, DWORD PTR [4+r8+rdx*8]                   #5.4
                        lea       esi, DWORD PTR [5+rsi+rdx*8]                  #5.4
                        lea       ebp, DWORD PTR [6+rbp+rdx*8]                  #5.4
                        lea       ebx, DWORD PTR [7+rbx+rdx*8]                  #5.4
                        inc       edx                                           #4.2
                        cmp       edx, ecx                                      #4.2
                        jb        ..B1.4        # Prob 99%                      #4.2
                ..B1.5:                         # Preds ..B1.4
                        add       eax, r11d                                     #5.4
                        add       r10d, r9d                                     #5.4
                        add       r8d, esi                                      #5.4
                        add       ebp, ebx                                      #5.4
                        add       eax, r10d                                     #5.4
                        add       r8d, ebp                                      #5.4
                        add       eax, r8d                                      #5.4
                        lea       ebx, DWORD PTR [1+rdx*8]                      #5.4
                ..B1.6:                         # Preds ..B1.5 ..B1.2
                        cmp       ebx, edi                                      #4.2
                        ja        ..B1.22       # Prob 50%                      #4.2
                ..B1.7:                         # Preds ..B1.6
                        lea       edx, DWORD PTR [-1+rbx]                       #2.5
                        sub       edi, edx                                      #2.5
                        dec       edi                                           #2.5
                        jmp       QWORD PTR [.2.3_2.switchtab.1+rdi*8]          #4.2
                ..1.3_0.TAG.6:
                ..B1.9:                         # Preds ..B1.7
                        lea       eax, DWORD PTR [5+rax+rbx]                    #5.4
                ..1.3_0.TAG.5:
                ..B1.11:                        # Preds ..B1.7 ..B1.9
                        lea       eax, DWORD PTR [4+rax+rbx]                    #5.4
                ..1.3_0.TAG.4:
                ..B1.13:                        # Preds ..B1.7 ..B1.11
                        lea       eax, DWORD PTR [3+rax+rbx]                    #5.4
                ..1.3_0.TAG.3:
                ..B1.15:                        # Preds ..B1.7 ..B1.13
                        lea       eax, DWORD PTR [2+rax+rbx]                    #5.4
                ..1.3_0.TAG.2:
                ..B1.17:                        # Preds ..B1.7 ..B1.15
                        lea       eax, DWORD PTR [1+rax+rbx]                    #5.4
                ..1.3_0.TAG.1:
                ..B1.19:                        # Preds ..B1.7 ..B1.17
                        add       eax, ebx                                      #5.4
                ..1.3_0.TAG.0:
                ..B1.21:                        # Preds ..B1.7 ..B1.19
                        lea       eax, DWORD PTR [-1+rax+rbx]                   #5.4
                ..B1.22:                        # Preds ..B1.21 ..B1.6 ..B1.1
                        pop       rbp                                           #7.9
                        pop       rbx                                           #7.9
                        ret                                                     #7.9
                .2.3_2.switchtab.1:
                        .quad   ..1.3_0.TAG.0
                        .quad   ..1.3_0.TAG.1
                        .quad   ..1.3_0.TAG.2
                        .quad   ..1.3_0.TAG.3
                        .quad   ..1.3_0.TAG.4
                        .quad   ..1.3_0.TAG.5
                        .quad   ..1.3_0.TAG.6
                ```

            === "x86-64 clang 21.1.0 -O3"

                ```asm
                Sum1ToN:
                        test    edi, edi
                        jle     .LBB0_1
                        lea     eax, [rdi - 1]
                        lea     ecx, [rdi - 2]
                        imul    rcx, rax
                        shr     rcx
                        lea     eax, [rdi + rcx]
                        dec     eax
                        ret
                .LBB0_1:
                        xor     eax, eax
                        ret
                ```

    如今汇编语言还用于开发高效且轻量级的应用，比如：

    - [NCNN](https://github.com/Tencent/ncnn)（腾讯）：专为移动平台设计的高性能神经网络推理计算框架，以 ARM NEON 汇编级别的精细优化为特色。
    - [MNN](https://github.com/alibaba/MNN)（阿里）：一个高效轻量的深度学习框架，支持在设备端进行深度学习模型的推理与训练，通过大量手写汇编代码实现核心操作以充分利用 ARM CPU 性能。

??? note "计算机接口及其功能（~~The Missing Semester of Your ZJU CS System Courses~~）"

    <div style="text-align: center">
        <img src="images/C1/6.png" width=60% />
    </div>

    **接口**(interface)或**端口**(port)是连接计算机与外部设备的连接点，使得它们能够协同工作。

    <div style="text-align: center">
        <img src="images/C1/7.png" width=60% />
    </div>

    接口的功能：

    - **通信**：串行(serial)/并行(parallel)通信

        <div style="text-align: center">
            <img src="images/C1/8.png" width=60% />
        </div>

    - **控制**：中断控制器(interrupt controller)，定时器(timer)

        <div style="text-align: center">
            <img src="images/C1/9.png" width=60% />
        </div>

!!! abstract "目录"

    - [x] [Introduction to the Microprocessor and Computer](1.md)
    - [x] [The Microprocessor and its Architecture](2.md)
    - [x] [Addressing Modes](3.md)
    - [x] [Data Movement Instructions](4.md)
    - [x] [Arithmetic and Logic Instructions](5.md)
    - [x] [Program Control Instructions](6.md)
    - [x] [8086/8088 Hardware Specifications](9.md)
    - [x] [Basic I/O Interface](11.md)

!!! recommend "参考资料"

    - 课件（从应试角度看最值得阅读的东西，而且课件里已经讲得很清楚了）

    ??? info "课件列出的参考资料"

        <div style="text-align: center">
            <img src="images/C1/1.png" width=60% />
        </div>

        <div style="text-align: center">
            <img src="images/C1/2.png" width=60% />
        </div>
    
    （由于是选修课，加上大三上来可能学业压力更大了，所以网上很难找到前辈们的笔记（悲））