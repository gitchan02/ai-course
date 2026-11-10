---
name: contact-csv
description: 이름, 학번, 전화번호, 이메일이 섞인 연락처 명단을 정리해 CSV 파일로 만들 때 쓴다. 중복 제거, 전화번호 형식 통일, 정렬을 포함한다. 점수가 있는 성적표나 워드 문서에는 쓰지 않는다.
---

# 연락처 명단 csv 만들기

## 규칙

- 파일 이름은 `contacts_YYYYMMDD.csv` (오늘 날짜). 날짜는 기억으로 쓰지 말고 코드로 구한다.
- 인코딩은 `utf-8-sig`다. 엑셀에서 열었을 때 한글이 깨지지 않게 하려면 BOM이 있어야 한다.
- 열 순서는 학번, 이름, 전화, 이메일. 첫 줄은 머리글.
- 전화번호는 숫자만 뽑아 `010-1234-5678` 꼴로 통일한다.
- 이메일은 소문자로 바꾼다.
- 학번이 같은 사람이 여러 번 나오면 처음 나온 줄만 남긴다.
- 학번 오름차순으로 정렬한다.
- 받은 사람만 쓴다. 없는 사람이나 빈 칸을 지어내지 않는다.

## 코드

아래 코드에서 `raw` 목록만 받은 명단으로 바꿔 그대로 실행한다. 함수 정의 없이 위에서 아래로 실행되는 코드다.

```python
import csv, re, datetime

raw = [
    ("20231234", "홍길동", "010 1234 5678", "Hong@Example.com"),
]

fname = "contacts_" + datetime.date.today().strftime("%Y%m%d") + ".csv"
seen = {}
for sid, name, phone, email in raw:
    if sid in seen:
        continue
    d = re.sub(r"\D", "", phone)
    seen[sid] = (sid, name.strip(), f"{d[:3]}-{d[3:7]}-{d[7:]}", email.strip().lower())
rows = sorted(seen.values())
with open(fname, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["학번", "이름", "전화", "이메일"])
    w.writerows(rows)
print("saved", fname, len(rows), "명")
```
