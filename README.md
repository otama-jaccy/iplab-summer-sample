# iplab-summer-sample
研究室合宿のサンプルコード

## 環境構築
### python
python3.6以上をインストールしてください．

macの場合は，[これ](https://qiita.com/okhrn/items/935cf187aec5cf144558)を参考にするか，次のコマンドを実行．
```bash
brew install python3
```
windows10はpowershellを起動して，
```bash
choco install python
```

後は以下の必要なpythonライブラリをインストールしてください．環境によってはpip3とかにしてください．
```bash
pip install opencv-python opencv-contrib-python kivy
```

## 動作確認
### opencvが動くか
```bash
python opencv-test.py
```

### kivyとopencvが動くか
```bash
python main.py
```