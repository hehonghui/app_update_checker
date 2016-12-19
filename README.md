# app_update_checker

1. 要测试的apk放到 apks_dir 目录中,并且以 NewsDog_v版本号.apk 样式命名, 例如 NewsDog_v1.6.apk.
使用方式为: 

1. 在终端切换到update_checker.py所在的目录下;
2. 然后执行: `monkeyrunner  update_checker.py` 脚本
3. 然后monkeyrunner就会依次读取 apks_dir 目录下的 apk, 然后挨个安装测试.
