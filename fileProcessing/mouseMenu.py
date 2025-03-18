import winreg


def createCompressionKey():
    key1_name = "哆啦A梦 压缩"
    key1_value = r"python D:\\Blog\\toolsbyaosai\\src\\fileProcessing\\qucikComp1.py"
    key2_name = "哆啦A梦 帮我压缩到……"
    key3_name = "大雄 解压"
    key4_name = "大雄 帮我解压到……"

    key_root = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'*\\shell')
    winreg.SetValue(key_root, "AOSAI-Tools", winreg.REG_SZ, "AOSAI-Tools")
    sub_key = winreg.OpenKey(key_root, "AOSAI-Tools")
    winreg.SetValue(sub_key, key1_name, winreg.REG_SZ, key1_value + "%1")

    winreg.CloseKey(sub_key)
    winreg.CloseKey(key)


def deleteCompressionKey():
    pass

createCompressionKey()
