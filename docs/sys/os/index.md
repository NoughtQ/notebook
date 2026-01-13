# 操作系统

!!! info "课程信息"

    - 学分：5.0
    - 教师：寿黎但
    - 教材：*Operating System Concepts*, 10th Edition (7th edition is also OK)

!!! abstract "目录"

    - Part 1: Overview
        - [x] [Introduction](1.md)
        - [x] [Operating-System Structures](2.md)
    - Part 2: Process Management
        - [x] [Processes](3.md)
        - [x] [Threads and Concurrency](4.md)
        - [x] [CPU Scheduling](5.md)
    - Part 3: Process Synchronization
        - [x] [Synchronization Tools](6.md)
        - [x] [Synchronization Examples](7.md)
        - [x] [Deadlocks](8.md)
    - Part 4: Memory Management
        - [x] [Main Memory](9.md)
        - [x] [Virtual Memory](10.md)
    - Part 5: Storage Management
        - [x] [Mass-Storage Structure](11.md)
        - [x] [I/O Systems](12.md)
    - Part 6: File System
        - [x] [File-System Interface](13.md)
        - [x] [File-System Implementation](14.md)
        - [x] [File-System Internals](15.md)

    >注：sld 的讲课会先跳过同步部分，等讲完内存部分后再回过头来学同步，这样的编排和 OSTEP 很像。
    
!!! recommend "参考资料"

    超级多资料！

    - 教材
    - 课件
    - [Operating System: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)（笔记中那些不存在于课件和教材的内容大都来自这里）
        - 很可惜的是，随着课业压力增大，我不得不牺牲掉阅读 OSTEP 的时间了，所以大致从第 13 章后我就没再往下阅读了。如果之后重温操作系统的话，这应该是我首选的阅读资料！
    - 前辈们的笔记：
        - [修佬的笔记](https://note.isshikih.top/cour_note/D3QD_Operatingsys/)
        - [咸鱼暄老师的笔记](https://xuan-insr.github.io/%E6%A0%B8%E5%BF%83%E7%9F%A5%E8%AF%86/os/I_overview/1_intro/)
        - [HobbitQia 前辈的笔记](https://note.hobbitqia.cc/OS/)
    - 2025 朋辈辅学
    - 国内外优质课程：
        - [NJU 蒋炎岩老师的 OS 课（2025）](https://jyywiki.cn/OS/2025/)
        - [THU rCore-Tutorial-Guide](https://learningos.cn/rCore-Tutorial-Guide-2025S/index.html)
        - [MIT 6.1810（2024）](https://pdos.csail.mit.edu/6.828/2024/index.html)（大名鼎鼎的 [xv6](https://github.com/mit-pdos/xv6-public) OS 诞生于此，最近从 x86 转向 [risc-v](https://github.com/mit-pdos/xv6-riscv) 版本）
    - 实验文档：
        - [sld 班的实验文档（2025）](https://os-25fall-81d0ad.pages.zjusct.io/)：好像目前照搬了 24 年的实验文档
        - [jjm, whs 班的实验文档（2025）](https://zju-os.github.io/doc/)：写得比笔者班的更好
        - 注意期末考试和实验还是有一些关系的（重点关注 Lab3-5），所以复习时不能遗漏，具体见[实验文档的描述](https://zju-os.github.io/doc/#%E4%B8%8E%E8%80%83%E8%AF%95%E7%9A%84%E8%81%94%E7%B3%BB)（24-25 就考了 Sv39 虚拟内存）
        