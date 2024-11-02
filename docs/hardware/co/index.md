# 计算机组成

!!! info "课程信息"

    - 学分：4.5
    - 教师：赵莎
    - 教材：*Computer Organization and Design*, RISC-V Edition

!!! plan "更新计划"

    - [x] [Chap 1: Computer Abstractions and Technology](1.md)
    - [x] [Chap 2: Language of the Machine](2.md)
    - [x] [Chap 3: Arithmetic for Computer](3.md)
    - [ ] [Chap 4: The Processor](4.md)
    - [ ] [Chap 5: Memory Hierarchy](5.md)
    - [ ] [Appendix: Storage, Networks and Other Peripherals](appendix.md)

!!! success "参考资料"

    - 教材
    - PPT
    - [咸鱼暄前辈的笔记](https://xuan-insr.github.io/computer_organization/)

??? note "在做lab时踩过的坑"

    记录一些硬控我n个小时的坑，兴许对大家有所帮助。

    - 电脑无法连接开发板
        - 电脑里少了对应的驱动，需要手动安装（对应的文件应该还在Vivado里，Google一下看怎么安装，我记得要在管理员下的cmd运行一些命令）
    - 综合失败，且`runme.log`和`.vivado.end.rst`没有任何错误信息
        - 先检查路径、用户名、计算机名是否全是英文字符，如果不是请修改
        - 如果你的（Windows）电脑（曾经）装过conda/anaconda，或者scoop，请检查注册表`计算机\HKEY_CURRENT_USER\Software\Microsoft\Command Processor`路径下的`Autorun`字段值是否存在无效的路径，若是请删除（如果实在不知道怎么删可以全删掉）