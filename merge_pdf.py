import pypdf
import os
import sys
import glob
from natsort import natsorted

if len(sys.argv) < 2:
    print("引数が足りません")
    sys.exit()
# FIXME 相対パスだとバグる？
SRC_DIR = str(sys.argv[1])
if not os.path.exists(SRC_DIR):
    print("フォルダが存在しません")
    sys.exit()
if len(sys.argv) == 3:
    DST_DIR = str(sys.argv[2])
else:
    DST_DIR = SRC_DIR
print("src: " + SRC_DIR)
print("dst: " + DST_DIR)

merger = pypdf.PdfMerger()

# ファイルかフォルダかを判定
if os.path.isfile(SRC_DIR):
    file_list = [SRC_DIR]
    print("hoge")
else:
    file_list = glob.glob(SRC_DIR + "/*.pdf")
file_list = natsorted(file_list)
print(file_list)

for file in file_list:
    print(file)
    merger.append(file)
merger.write(DST_DIR + "/merged.pdf")
merger.close()
print("終了")
