# 数值分析

!!! info "课程信息"

    - 学分：2.5
    - 教师：黄劲
    - 教材：*Numeric Analysis*, 7th Edition

!!! abstract "目录"

    上课顺序为：1 -> 2 -> 6 -> 7 -> 9 -> 3 -> 8 -> 4 -> 5，建议复习的时候也按这个顺序来。

    - [x] [Chap 1: Mathematical Premiminaries](1.md)
    - [x] [Chap 2: Solutions of Equations in One Variable](2.md)
    - [x] [Chap 3: Interpolation and Polynomial Approximation](3.md)
    - [x] [Chap 4: Numerical Differentiation and Integration](4.md)
    - [x] [Chap 5: Initial-Value Problems for Ordinary Differential Equations](5.md)
    - [x] [Chap 6: Direct Methods for Solving Linear Systems](6.md)
    - [x] [Chap 7: Iterative Techniques in Matrix Algebra](7.md)
    - [x] [Chap 8: Approximation Theory](8.md)
    - [x] [Chap 9: Approximating Eigenvalues](9.md)

    <div class="card file-block" markdown="1">
    <div class="file-icon"><img src="/assets/pdf.svg" style="height: 3em;"></div>
    <div class="file-body">
    <div class="file-title">笔记（打印版）</div>
    <div class="file-meta">27 MB / 105 P / 2025-06-20</div>
    </div>
    <a class="down-button" target="_blank" href="https://courses.noughtq.top/NA-D2CX/note_print_version.pdf" markdown="1">:fontawesome-solid-download: 下载</a>
    </div>

    剩下三章不会介绍，但这里还是列一下标题：

    - Chap 10: Numerical Solutions of Nonlinear Systems for Equations
    - Chap 11: Boundary-Value Problems for Ordinary Differential Equations
    - Chap 12: Numerical Solutions to Partial Differential Equations

??? info "可能有用的东西"

    - 泰勒展开式的一般形式：$f(x) = f(a) + f'(a)(x - a) + \dfrac{f''(a)}{2!}(x - a)^2 + \dfrac{f'''(a)}{3!}(x - a)^3 + \dots$
    - 常用的泰勒展开式：
        - 指数函数：$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots = \sum_{n=0}^{\infty} \frac{x^n}{n!}$（收敛半径：$\infty$）
        - 正弦函数：$\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \dots = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{(2n+1)!}$（收敛半径：$\infty$）
        - 余弦函数：$\cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \dots = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n}}{(2n)!}$（收敛半径：$\infty$）
        - 自然对数函数：$\ln(1+x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \dots = \sum_{n=1}^{\infty} (-1)^{n-1} \frac{x^n}{n}$（收敛区间：$(-1, 1]$）
        - 几何级数（或二项式展开的特例）：$\frac{1}{1-x} = 1 + x + x^2 + x^3 + \dots = \sum_{n=0}^{\infty} x^n$（收敛区间：$(-1, 1)$）
        - 推广的二项式定理：$(1+x)^\alpha = 1 + \alpha x + \frac{\alpha(\alpha-1)}{2!} x^2 + \frac{\alpha(\alpha-1)(\alpha-2)}{3!} x^3 + \dots = \sum_{n=0}^{\infty} \binom{\alpha}{n} x^n$，其中 $\binom{\alpha}{n} = \frac{\alpha(\alpha-1)\dots(\alpha-n+1)}{n!}$（收敛区间：$(-1, 1)$，当 $\alpha$ 为非负整数时，级数是有限项的）



!!! recommend "参考资料"

    - PPT、教材
    - [Jiepeng 学长的笔记](https://note.jiepeng.tech/CS/NA/)
    - [CrazySpottedDove 的笔记](https://crazyspotteddove.github.io/blog/numericalanalysis/)：记录了很多 hj 老师课上提到的一些很有价值的观点（~~但笔者没好好听课，所以就参考这位大佬的笔记了hh~~）
    - [Fundamentals of Numerical Computation](https://fncbook.com/)：MIT 18.330 数值分析课程的教材。实际上我并没有参考这本书（~~发现的时候离期末考只剩2天了（悲）~~），但看起来挺不错的，所以就放在这里了。
    
    <div class="card file-block" markdown="1">
    <div class="file-icon"><img src="/assets/pdf.svg" style="height: 3em;"></div>
    <div class="file-body">
    <div class="file-title">复习提纲 by hj 老师</div>
    <div class="file-meta">243 KB / 2 P / 2025-06-06</div>
    </div>
    <a class="down-button" target="_blank" href="https://courses.noughtq.top/NA-D2CX/outline_hj.pdf" markdown="1">:fontawesome-solid-download: 下载</a>
    </div>
    