# 补充部分

!!! info "注"

    这里补充一些知识点：
    
    - 教材上没有涉及，但上课讲到过的
    - 不方便归类的

- 16位汇编和32位汇编之间的区别
    - 宽度
        - 16位汇编：DOS环境下的汇编语言，只能使用16位地址
        - 32位汇编：Windows或Linux环境下的汇编语言，只能使用32位地址
        - 但两者均可以使用8位、1
    - 调用操作系统函数（以输出为例）
        - 16位汇编：要调用`int 21h`的9号功能
        - 32位汇编：调用`MessageBoxA`弹窗输出

