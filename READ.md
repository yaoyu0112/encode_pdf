# PDF Unlocker Tool

一個使用 **PyQt6 + pypdf** 開發的桌面工具，用於**移除 PDF 密碼保護**，支援拖拉操作、進度條顯示與成功動畫提示，並可打包成 Windows 可執行檔（exe）。

---

## ✨ 功能特色

- ✅ 拖拉 PDF 檔案快速載入
- ✅ 密碼錯誤提示與重新輸入
- ✅ 即時解鎖進度條顯示
- ✅ 解鎖成功動畫提示
- ✅ 支援另存解鎖後 PDF
- ✅ 可打包為單一 exe 檔案
- ✅ 不需安裝 Python 即可執行（打包後）

---

## 🧰 使用技術

| 元件 | 用途 |
------|------
PyQt6 | 圖形化介面 (GUI)
pypdf | PDF 讀取與解鎖
pyinstaller | 封裝成 exe

---

## 📦 安裝環境需求

- Python 3.9 以上（建議）
- Windows 10+

---

## 📥 套件安裝

```bash
pip install PyQt6 pypdf pyinstaller
```

## 啟動程式

```bash
python main.py
```