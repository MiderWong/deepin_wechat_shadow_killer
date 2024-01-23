# WeChat Shadow Killer

## I、原理

  - 我们发现微信窗体的阴影实际上也是一个窗体，它没有名字，但是其`window id`与其主窗体相关，详细可见：[文章连接](https://forum.ubuntu.org.cn/viewtopic.php?t=491709)
  
  - 于是思路就是通过主窗体id来求解阴影窗体的id
  
  - 这里我们通过暴力枚举，因为实际上这两者的id之差一般在20以内，但是在枚窗体id的同时需要判断窗体是否是一个主窗体，于是`window_names`列表起到了排除检查的作用。

  - 当检查的到符合条件的窗体id（正确的shadow_id）时，会通过`xdotool windowunmap <shadow_id>`让阴影窗体不可见，实现去除阴影。

## II、使用

  - 只有一个Python脚本，使用以下命令来运行它：
  ```bash
  vim log.txt     #创建log文件
  vim pid.txt     #创建pid文件
  nohup python ./shadow_killer.py > log.txt &  #使用nohup保证关闭terminal依然运行，并将terminal输出重定向到log文件
  ```
  - 由于该脚本很大程度上依赖于控制台的输出内容，所以请不要漏掉log文件和nohup
  - 也可以考虑将其配置为一个开机启动项，但目前配置为systemctl的服务尚不可行

## III、注意

 - 所有测试均只在我自己的Ubuntu 22.04.3上经过测试，不能保证全平台适配
 - 使用该脚本导致的一切后果作者均不负责