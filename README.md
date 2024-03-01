# Deepin WeChat Shadow Killer

## I、原理

  - 我们发现微信窗体的阴影实际上也是一个窗体，它没有名字，但是其`window id`与其主窗体相关，详细可见：[文章连接](https://forum.ubuntu.org.cn/viewtopic.php?t=491709)
  
  - 于是思路就是通过主窗体id来求解阴影窗体的id
  
  - 这里我们通过暴力枚举，因为实际上这两者的id之差一般在20以内，但是在枚窗体id的同时需要判断窗体是否是一个主窗体，于是`window_names`列表起到了排除检查的作用。

  - 当检查的到符合条件的窗体id（正确的shadow_id）时，会通过`xdotool windowunmap <shadow_id>`让阴影窗体不可见，实现去除阴影。

## II、使用

  - 1、项目运行环境
    1) 确保系统已经安装了`python3`
    2) 确保系统已经安装了`xdotool`和`wmctrl`
  - 2、修改运行配置
    1) 修改`deepin_wechat_shadow_killer.py`中`folder_path`的值
    2) 修改`deepin_wechat_shadow_killer.sh`中`PYTHON_PATH`和`PROJECT_FOLDER`的值
  - 3、为脚本添加执行权限
    ```shell
    chmod +x deepin_wechat_shadow_killer.sh
    ```
  - 4、运行项目:
    ```shell
    bash ./deepin_wechat_shadow_killer.sh
    ```
  - 5、设置脚本登陆启动
  ```markdown
    # 此处仅针对`ArchLinux`做说明，其余系统请自行研究
    在`开机与关机`——>`自动启动`——>`添加`——>`添加登陆脚本`——>选择`deepin_wechat_shadow_killer.sh`文件
  ```

## III、注意
 - 脚本在`Ubuntu 22.04.3`上测试通过
 - 脚本在`ArchLinux 2024.1`上测试通过
 - 使用该脚本导致的一切后果作者均不负责