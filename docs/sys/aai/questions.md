---
counter: true
---

# Question Set

>收集部分历年卷真题。


## 24-25

!!! question "问题 1"

    >大题第 2 道第一小问。

    === "题目"

        ```asm
        TEST EDX, EDX
        JG .L1
        MOV EAX, EDX
        SHR EAX, 31
        ADD EAX, EDX
        SAR EAX, 1
        TEST EDX, EDX
        MOV EDX, 20
        CMOVE EAX, EDX
        RET

        .L1:
        NEG EDX
        LEA EAX, [EDX+EDX]
        RET
        ```

        `EDX` 分别等于 0、10、-21 时，`EAX` 最终的值

    === "解答"

        |`EDX`|`EAX`|
        |:-:|:-:|
        |0|20|
        |10|-20|
        |-21|-10|

        ??? code "代码解读"

            ```asm
            ; EDX 为正数时跳转到 L1 标签
            TEST EDX, EDX
            JG .L1

            MOV EAX, EDX
            SHR EAX, 31       ; 逻辑右移 31 位，仅在最低位保留了原来的最高位
            ADD EAX, EDX
            SAR EAX, 1        ; 算术右移（除以 2，正负数均成立）
            TEST EDX, EDX     ; 用于后面的 CMOVE 指令
            MOV EDX, 20
            CMOVE EAX, EDX    ; ZF=0 时 MOV
            RET

            .L1:
            NEG EDX               ; 取相反数
            LEA EAX, [EDX+EDX]    ; EAX <- 2*EDX
            RET
            ```

!!! question "问题 2"

    >大题第 2 道第二小问。

    === "题目"

        ```asm
        XOR EDX, EDX
        TEST EAX, EAX
        JLE .L1

        .L2
        TEST AL, 3
        JNE .L3

        .L4
        SUB EAX, 1
        ADD EDX, 2
        TEST AL, 3
        JE .L4

        .L3
        ADD EDX, 1
        SUB EAX, 1
        JNE .L2

        .L1
        MOV EAX, EDX
        RET
        ```

        `EAX` 分别等于 5、20 时，`EDX` 最终的值

    === "解答"

        |`EAX`|`EDX`|
        |:-:|:-:|
        |5|6|
        |20|30|

        `EAX=5` 是让我们搞清楚这段指令序列在干什么，不然 `EAX=20` 时计算量太大了。
        
        不难发现，这段指令序列的功能是：遍历 [1, `EAX`] 整数，遇到 4 的倍数时 `EDX+3`，其余情况 `EDX+1`（`EDX` 初始为 0）。 
