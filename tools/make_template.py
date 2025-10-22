# tools/make_template.py
from openpyxl import Workbook
from pathlib import Path

COLUMNS = [
    "id","name","arcana","suit","number","image_file",
    "upright_general","reversed_general",
    "love_hint","career_hint","health_hint","study_hint"
]

def main():
    out = Path("deck/metadata.xlsx")
    out.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "cards"
    ws.append(COLUMNS)
    # 한 줄 샘플
    ws.append([0,"The Fool","Major","",0,"00_the_fool.jpg","새로운 시작, 자유","충동, 경솔","사랑에서의 모험","초심과 도전","가벼운 운동 시작","호기심 학습"])
    wb.save(out)
    print(f"템플릿 생성 완료: {out.resolve()}")

if __name__ == "__main__":
    main()
