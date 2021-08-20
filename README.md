# vj_spider

## 使用须知

### 变量说明

``driver_path``是指你自己本地的浏览器驱动，需要自己下载，``path/chromedriver.exe``是你自己本地的浏览器驱动的地址。

``csv_file_path``是用于用于保存爬取结果的本地csv文件，``path/rank.csv``是你自己本地该.csv文件的地址。

```python
driver_path = r'path/chromedriver.exe'
csv_file_path = r'path/rank.csv'
```

在以下两个变量中，使用你自己的vj账户名和密码。

```python
username = r'username'
password = r'password'
```

### 其他文件

``contents.txt``里面保存的是比赛的ID和密码，若无密码也请随便写一个。

运行``rank.py``前，请确保你的``contents.txt``里面有数据。
