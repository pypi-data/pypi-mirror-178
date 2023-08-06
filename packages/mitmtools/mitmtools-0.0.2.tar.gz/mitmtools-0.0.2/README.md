# 介绍

mitmtools 是根据 mitmproxy 封装的工具库

具备如下功能

- 替换响应文件
- 修改部分响应内容
- 移除部分响应内容
- hook 注入

# 替换响应文件

- ReplaceFileByUrl: 通过 url 完全匹配，替换响应文件
- ReplaceFileByRegex: 通过正则匹配 url，替换响应文件

```
ReplaceFileByUrl(url='', filepath='', max_times=0)  # 注意 max_time 为可选参数，代表匹配次数
ReplaceFileByRegex(pattern='', filepath='')
```

# 修改部分响应内容

- ReplaceContentByUrl：通过 url 完全匹配，修改响应内容
- ReplaceContentByRegex：通过正则匹配 url，修改响应内容

```
ReplaceContentByUrl(url='', replace_dict={'old':'new'}, max_times=0)  # 注意 max_time 为可选参数，代表匹配次数
ReplaceContentByRegex(pattern='', replace_dict={'old':'new'})
```

# 移除部分响应内容

- RemoveContentByUrl：通过 url 完全匹配，移除响应内容
- RemoveContentByRegex：通过正则匹配 url，移除响应内容

```
RemoveContentByUrl(url='', remove_list=['x'], max_times=0)  # 注意 max_time 为可选参数，代表匹配次数
RemoveContentByRegex(pattern='', remove_list=['x'])
```

# hook 注入

- HookByHtml：通过在 html 的 head 标签插入 script 标签达到效果
- HookByJs：获取 html 的第一个外部 js url，并在其加载时注入
- HookByJsUrl：指定 js url，在其加载时注入

```
HookByHtml(filepath='./static/hookfile.js')
HookByJs(filepath='./static/hookfile.js')
HookByJsUrl(url='', filepath='./static/hookfile.js')
```

## 注意
html 注入属于 xss 攻击，部分会有 csp 防护导致 script 不会执行，从而 hook 失败  

友情提醒：任何注入都可能被检测！

# 查看
如果只是想查看请求过程的话，直接使用 MitmproxyBase
```
MitmproxyBase()
```

# 执行
将需要执行的方法单独放一个 .py 文件，并放在 addons 列表中，如下：
```
addons = [
    MitmproxyBase(),

    # replace
    # ReplaceContentByUrl(replace_dict={'百度一下，你就知道': '百度一下，你也不知道'}, url='https://www.baidu.com/')
    ReplaceContentByRegex(replace_dict={'百度一下，你就知道': '百度一下，你也不知道'},
                          pattern='^https://www.baidu.com.?$')

    # hook
    # HookByHtml(filepath='./static/hookfile.js'),
    # HookByJs(filepath='./static/hookfile.js'),
    # HookByJsUrl(url='', filepath='./static/hookfile.js'),

    # remove
    # RemoveContentByUrl(url='https://www.baidu.com/', remove_list=['百度一下，你就知道'])
]

```
随后调用如下代码，或者自己通过 mitmproxy 命令行命令自行启动
```
from mitmtools.start import execute

execute(filepath='', port=8866)
```
