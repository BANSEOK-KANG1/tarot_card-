# tools/pick_files_easygui.py
import os
import subprocess
from pathlib import Path
import easygui

def main():
    deck_dir = easygui.diropenbox(msg="덱 폴더(deck)를 선택하세요 (images/, metadata.xlsx 포함)", title="Tarot Deck Folder")
    if not deck_dir:
        return
    deck_dir = Path(deck_dir)

    meta = deck_dir / "metadata.xlsx"
    if not meta.exists():
        meta = deck_dir / "metadata.csv"
    if not meta.exists():
        easygui.msgbox("metadata.xlsx 또는 metadata.csv가 없습니다. 템플릿을 먼저 만드세요.", title="오류")
        return

    os.chdir(deck_dir.parent)  # app.py가 있는 루트로 이동
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()
