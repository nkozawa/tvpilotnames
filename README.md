# tvpilotnames 
## Manipulate Tiny View Plues pilot name field for each cameras

***English version (program and readme) will be availabe in the near future***

### V2.0について
V1ではパイロット名を列記したファイルを用意する方法でしたが、大幅な改訂となりますがクリップボードを使用する方法に変えました。表計算ワークシートや文書からパイロット名(複数同時可能)をコピーしてボタンを押せばTinyViewPlusに送ることができます。
またTinyViewPlusの稼働しているPCをIP Addressだけではなくホスト名で指定することも出来るようになりました。

### 目的
このプログラムはTiny View Plus(以下のリンク参照)に対してパイロット名を各カメラに設定するものです。
https://github.com/t-asano/tinyviewplus
Tiny View PlusとはOSCプロトコルを介して通信を行います。

### プログラムの起動
#### Python3環境での実行
1. `pip install python-osc`
2. `pip install pyperclip`
4. python tvpilotnames.py

### 実行ファイルを使用する場合
MacOSおよびWindows環境で直接稼働する実行ファイルを用意しています。実行ファイルについてはReleaseページをご覧ください。

### 使用方法
![main menu](images/tvpilotnames2.png)
1. Tiny View Plus IP/hostname、Tiny View Plusが稼働しているPCのIP Addressもしくはホスト名を指定する。同じPC上で実行する場合は「Local」ボタンを押すとIP Addressに127.0.0.1が設定されます。
2. カメラ[n]の横の入力欄は単なる覚書です。チャネルなどを書いておくと便利です。何も書かなくても構いません。
3. 表計算シートや文書ファイルからパイロット名をクリップボードにコピーします。
4. 「クリップボードから送る」ボタンで対応するカメラ番号にTiny View Plusにパイロット名が送付されます。もし複数のパイロット名がクリップポードに入っている場合は最初のものが使われます。
5. 「クリップボードから全カメラに送る」ボタンを押すとカメラ1からカメラ4まで全てのパイロット名が送付されます。

### 制限事項
パイロット名にスペースを含むことは出来ません。

### tvpilotnames.ini
ユーザーのホームディレクトリーにtvpilotname.iniファイルをプログラムの終了時(ウィンドウのＸボタンで終了する時)に作成します。IP Address/hostname、各カメラのメモが保存され、次の起動時に読み込まれます。
