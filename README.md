# moocs-downloader
## INIAD Moocs上の講義スライドを自動で一括ダウンロードしてくれるPythonスクリプト
- INIADded拡張機能に依存しているので俺しかつかえません
- 初期化のために使用時はChromeのタスクが全てkillされます
- 現時点では映像が含まれる講義はうまくダウンロードできません(プロ言とか)
- 公開時点でのMoocsのDOMに依存しているためリニューアルされた後は動きません（多分、ほぼ確実に）

## おまけ
- 自動でPDF化するスクリプトもついてます

## 使い方
```powershell
// ダウンロードスクリプト
python main.py {ダウンロードしたい講義の名前（部分一致可） or URL}

// PDF化スクリプト
python make_pdf.py {PDF化したいファイルの絶対パス} {PDFの保存先の絶対パス(default="~/Downloads")}
```
