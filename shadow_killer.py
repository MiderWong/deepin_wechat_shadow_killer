import os

if not os.path.exists("./pid.txt"):
    with open("./pid.txt", "w", encoding="utf-8") as f:
        f.write("not running")
        f.close()
        
if not os.path.exists("./log.txt"):
    with open("./log.txt", "w", encoding="utf-8") as f:
        f.write("")
        f.close()

new_pid = "not running"

with open("/home/lildino/wechat_shadow_killer/log.txt", "w", encoding="utf-8") as f:
    f.write("")
    f.close()
    
with open("/home/lildino/wechat_shadow_killer/pid.txt", "r", encoding="utf-8") as f:
    pid = f.read()
    if pid != "not running":
        try:
            os.kill(int(pid), 9)
        except:
            pass
        
    f.close()

new_pid = os.getpid()
print("launched shadow_killer.py with pid : {}".format(new_pid))
    
with open("/home/lildino/wechat_shadow_killer/pid.txt", "w", encoding="utf-8") as f:
    f.write(str(new_pid))
    f.close()
    
window_names = ["微信", "图片查看", "聊天文件", "朋友圈", "设置", "ChatContactMenu", "EmotionTipWnd"]

wx_win_id = os.popen(
                "wmctrl -l -G -p -x |grep wechat.exe.com.qq.weixin.deepin |awk '{print $1,$10}'"
            ).readlines()
    
old_window_num = len(wx_win_id)    
new_window_num = old_window_num

while True:
    if wx_win_id == []:
        wx_win_id = os.popen(
                        "wmctrl -l -G -p -x |grep wechat.exe.com.qq.weixin.deepin |awk '{print $1,$10}'"
                    ).readlines()
        
        new_window_num = len(wx_win_id)
        
        continue
    
    #print("wx_win_id : {}".format(wx_win_id))
    
    if new_window_num != old_window_num or new_window_num == old_window_num == 1:
        
        print("change happened, new_window_num : {}, old_window_num : {}".format(new_window_num, old_window_num))
        old_window_num = new_window_num

        for id_name_pair in wx_win_id:

            w_id = int(id_name_pair.split(" ")[0], 16)
            w_name = id_name_pair.split(" ")[1][:-1]
            
            print("-"*50,"\n","w_id : {}, w_name : {}".format(w_id, w_name))
            
            shadow_id = 0

            shadow_id = w_id + 1
            print("\n\nshadow_id : {}".format(hex(shadow_id)))
            cli_return = os.popen(
                "xwininfo -id {}".format(hex(shadow_id))
            ).readlines()
            
            print("\ncli_return : {}\n".format(cli_return))
            
            # 一个正确的查询会返回这样的第二行：
            # xwininfo: Window id: 0x3000021 "微信"\n
            # 使用双引号分割后，会产生三个元素
            # 但是如果是一个shadow窗体，是没有名字的
            # 于是会返回这样的第二行：
            # xwininfo: Window id: 0x3000021 (has no name)\n
            # 使用双引号分割后，无法产生三个元素，split_test 就会只有一个元素
            
            # 这一切的前提是作出查询的窗口 id 是正确的，可以通过是否返回了 24 行来判断
            split_test = cli_return[1].split("\"") if len(cli_return) == 24 else []
            print("split_test : {}".format(split_test))
            
            mapped_state = cli_return[19].split(":")[1][1:-1] if len(cli_return) == 24 else "IsUnMapped"
            
            # 说明这是一个有名字的窗体，保存名字，后面检查防止关掉了相关的主窗体
            if len(split_test) == 3:
                test_win_name = split_test[1]         
            else:
                test_win_name = "no name"                  
                
            print("test_win_name : {}".format(test_win_name))                                                                 

            # 循环直到找到一个正确的shadow，或者shadow id 超过了自己的 id + 20
            while (len(cli_return) != 24 or test_win_name in window_names or mapped_state != "IsViewable") and shadow_id - w_id < 20:
                shadow_id += 1
                print("\n\nshadow_id : {}".format(hex(shadow_id)))
                cli_return = os.popen(
                    "xwininfo -id {}".format(hex(shadow_id))
                ).readlines()
                print("\ncli_return : {}\n".format(cli_return))
                split_test = cli_return[1].split("\"") if len(cli_return) == 24 else []
                
                mapped_state = cli_return[19].split(":")[1][1:-1] if len(cli_return) == 24 else "IsUnMapped"
                print("mapped_state : {}".format(mapped_state))
            
                # 说明这是一个有名字的窗体，保存名字，后面检查防止关掉了相关的主窗体
                if len(split_test) == 3:
                    test_win_name = split_test[1]         
                else:
                    test_win_name = "no name"
                    
                print("test_win_name : {}".format(test_win_name))

            os.system("xdotool windowunmap {}".format(hex(shadow_id)))
        
    wx_win_id = os.popen(
        "wmctrl -l -G -p -x |grep wechat.exe.com.qq.weixin.deepin |awk '{print $1,$10}'"
    ).readlines()
    
    with open("/home/lildino/wechat_shadow_killer/log.txt", "w", encoding="utf-8") as f:
        f.write("")
        f.close()
    
    new_window_num = len(wx_win_id)


with open("./log.txt", "w", encoding="utf-8") as f:
    f.write("not running")