---

# 🔍 NCR.py — NIK Checker CLI

![NCR Banner](assets/NCR.jpg)

**NCR.py** is a Python CLI tool for checking and validating Indonesian National ID Numbers (**NIK**) completely **offline**.  
It reads regional data directly from `ncr.min.js` and displays detailed information with **colored and animated terminal output**.

---

# 👁️ Features
- Automatically detects **Province, City/District, Subdistrict, and Postal Code**
- Parses and validates NIK structure (gender, birth date, unique code)
- Automatically calculates:
  - Age
  - Zodiac sign
  - Javanese “Pasaran” day
  - Upcoming birthday countdown

---

## ⚙️ Usage
git clone https://github.com/ruiixvolthacked/NCR-NIK-CHECKER.git

cd NCR.py

pip install -r requirements.txt

python3 NCR.py

When prompted, enter your NIK
Example:

----------------------------------------
🔍 NCR NIK-CHECKER
----------------------------------------
// ENTER YOUR NIK \\
INPUT NIK : 3xxxx10609xxxx01

✅ STATUS: SUCCESS !

NIK: 3xxxx10609xxxx01
GENDER: Male

BIRTHDATE: 06/09/1997

PROVINCE: West Java

CITY/DISTRICT: Bandung Regency

SUBDISTRICT: Katapang

UNIQCODE: 0001

POSTAL CODE: 40921

PASARAN: Saturday Pahing, 6 September 1997

AGE: 28 Years 1 Month 17 Days

NEXT BIRTHDAY: In 10 Months 8 Days

ZODIAC: Virgo


---

## 📦 Dependencies

Python 3.8+

colorama


Install dependencies:

pip install -r requirements.txt


---

## 👤 Developer

Author: Ruiix_.volt

Project Name: NCR.py

Version: 1.0

License: MIT



---

## 📜 License

MIT License © 2025 Ruiix_.volt

---