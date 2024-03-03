import os

###############  CHANGE THIS ###############
folder_path = "/home/Jason/.shell/deepin_wechat_shadow_killer"
###############  CHANGE THIS ###############

############### Filtered Window Names ###############
# window_names = ["微信", "图片查看", "聊天文件", "朋友圈", "设置", "ChatContactMenu", "EmotionTipWnd", "DragAttachWnd",
#                 "SessionDragWnd"]
window_names = ["微信"]
############### Filtered Window Names ###############

############### Filtered Window Geometry ###############
window_geometry = ["396x440"]

###############  MAKE SURE ONLY ONE PROCESS IS RUNNING #################
if not os.path.exists("{}/pid.txt".format(folder_path)):
    with open("./pid.txt", "w", encoding="utf-8") as f:
        f.write("not running")
        f.close()

if not os.path.exists("{}/log.txt".format(folder_path)):
    with open("./log.txt", "w", encoding="utf-8") as f:
        f.write("")
        f.close()

new_pid = "not running"

with open("{}/log.txt".format(folder_path), "w", encoding="utf-8") as f:
    f.write("")
    f.close()

with open("{}/pid.txt".format(folder_path), "r", encoding="utf-8") as f:
    pid = f.read()
    if pid != "not running":
        try:
            os.kill(int(pid), 9)
        except:
            pass

    f.close()

new_pid = os.getpid()
print("launched shadow_killer.py with pid : {}".format(new_pid))

with open("{}/pid.txt".format(folder_path), "w", encoding="utf-8") as f:
    f.write(str(new_pid))
    f.close()

###################  MAKE SURE ONLY ONE PROCESS IS RUNNING #################


################### LOOP TO KILL SHADOWS #################
wx_win_id = os.popen(
    "wmctrl -l -G -p -x |grep wechat.exe.com.qq.weixin.deepin |awk '{print $1,$10}'"
).readlines()

old_window_num = len(wx_win_id)
new_window_num = old_window_num

while True:
    # 如果没有微信窗体，就不用检查了
    if wx_win_id == []:
        wx_win_id = os.popen(
            "wmctrl -l -G -p -x |grep wechat.exe.com.qq.weixin.deepin |awk '{print $1,$10}'"
        ).readlines()

        new_window_num = len(wx_win_id)

        continue

    # 如果微信窗体数量发生了变化或者只有一个窗体，就要检查一下
    if new_window_num != old_window_num or new_window_num == old_window_num == 1:

        print("|||||" * 25,
              "\nchange happened, new_window_num : {}, old_window_num : {}".format(new_window_num, old_window_num))
        old_window_num = new_window_num

        # 循环检查每一个微信窗体
        for id_name_pair in wx_win_id:

            # 获取窗体 id 和名字
            w_id = int(id_name_pair.split(" ")[0], 16)
            w_name = id_name_pair.split(" ")[1][:-1] if id_name_pair.split(" ")[1][:-1] != "" else "has no name"

            print("=====" * 25, "\n", "w_id : {}, w_name : {}".format(hex(w_id), w_name))

            if w_name == "has no name":
                continue

            # 初始化 shadow_id
            shadow_id = w_id + 1
            print("\n\nshadow_id : {}".format(hex(shadow_id)))

            # 通过 xwininfo 查询 shadow_id 的信息
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

            # 说明这是一个有名字的窗体，保存名字，后面检查防止关掉了相关的主窗体
            if len(split_test) == 3:
                test_win_name = split_test[1]
            else:
                test_win_name = "has no name"

            print("test_win_name : {}".format(test_win_name))

            # 获取 mapped_state
            mapped_state = cli_return[19].split(":")[1][1:-1] if len(cli_return) == 24 else "IsUnMapped"
            print("mapped_state : {}".format(mapped_state))

            # 获取 geometry
            test_win_geometry_unprocessed = cli_return[22].split(" ")[3][0:-1] if len(cli_return) == 24 else "0x0+0+0"
            plus_num = test_win_geometry_unprocessed.count("+")
            if plus_num == 2:
                test_win_geometry = test_win_geometry_unprocessed.split("+")[0]
            elif plus_num == 1:
                index_of_plus = test_win_geometry_unprocessed.index("+")
                index_of_minus = test_win_geometry_unprocessed.index("-")

                if index_of_plus < index_of_minus:
                    test_win_geometry = test_win_geometry_unprocessed.split("+")[0]
                else:
                    test_win_geometry = test_win_geometry_unprocessed.split("-")[0]
            else:
                test_win_geometry = test_win_geometry_unprocessed.split("-")[0]

            print("geometry : {}".format(test_win_geometry))

            print("-----" * 25)

            # 循环直到找到一个正确的shadow，或者shadow id 超过了自己的 id + 20
            while (
                    len(cli_return) != 24 or
                    test_win_name in window_names or
                    test_win_geometry in window_geometry or
                    mapped_state != "IsViewable"
            ) and shadow_id - w_id < 20:

                shadow_id += 1
                print("\n\nshadow_id : {}".format(hex(shadow_id)))
                cli_return = os.popen(
                    "xwininfo -id {}".format(hex(shadow_id))
                ).readlines()
                print("\ncli_return : {}\n".format(cli_return))
                split_test = cli_return[1].split("\"") if len(cli_return) == 24 else []

                # 说明这是一个有名字的窗体，保存名字，后面检查防止关掉了相关的主窗体
                if len(split_test) == 3:
                    test_win_name = split_test[1]
                else:
                    test_win_name = "has no name"

                print("test_win_name : {}".format(test_win_name))

                mapped_state = cli_return[19].split(":")[1][1:-1] if len(cli_return) == 24 else "IsUnMapped"
                print("mapped_state : {}".format(mapped_state))

                test_win_geometry_unprocessed = cli_return[22].split(" ")[3][0:-1] if len(
                    cli_return) == 24 else "0x0+0+0"
                plus_num = test_win_geometry_unprocessed.count("+")
                if plus_num == 2:
                    test_win_geometry = test_win_geometry_unprocessed.split("+")[0]
                elif plus_num == 1:
                    index_of_plus = test_win_geometry_unprocessed.index("+")
                    index_of_minus = test_win_geometry_unprocessed.index("-")

                    if index_of_plus < index_of_minus:
                        test_win_geometry = test_win_geometry_unprocessed.split("+")[0]
                    else:
                        test_win_geometry = test_win_geometry_unprocessed.split("-")[0]
                else:
                    test_win_geometry = test_win_geometry_unprocessed.split("-")[0]
                print("geometry : {}".format(test_win_geometry))

                print("-----" * 25)

            if shadow_id - w_id < 20 and test_win_name not in ["图片查看"]:
                os.system("xdotool windowunmap {}".format(hex(shadow_id)))
                print("kill shadow win_name: {}".format(test_win_name))
                print("kill shadow shadow_id: {}".format(hex(shadow_id)))

            shadow_id = 0

    wx_win_id = os.popen(
        "wmctrl -l -G -p -x |grep wechat.exe.com.qq.weixin.deepin |awk '{print $1,$10}'"
    ).readlines()

    with open("{}/log.txt".format(folder_path), "w", encoding="utf-8") as f:
        f.write("")
        f.close()

    new_window_num = len(wx_win_id)

################### LOOP TO KILL SHADOWS #################


with open("{}/log.txt".format(folder_path), "w", encoding="utf-8") as f:
    f.write("not running")
