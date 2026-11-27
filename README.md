# Taiwan Stock Data Collector

台灣股票市場資料蒐集與分析系統。

本專案使用 Python 開發，目標是蒐集臺灣證券交易所（TWSE）及證券櫃檯買賣中心（TPEx）的公開市場行情資料，並建立資料儲存、查詢、統計分析及視覺化功能。

目前專案處於資料來源 API Client 開發階段，已完成 TWSE 每日行情 API Client、資料型別定義、回應資料驗證及 Logger。

---

## Project Overview

Taiwan Stock Data Collector 是一個開源的台灣股票市場資料蒐集與分析專案。

### Data Sources

- [TWSE — 臺灣證券交易所](https://www.twse.com.tw/)
- [TPEx — 證券櫃檯買賣中心](https://www.tpex.org.tw/)

本專案預計透過官方公開資料來源取得市場行情，並逐步建立統一的資料處理流程。

## Features

### Implemented

- [x] BaseAPIClient：共用 HTTP API Client
- [x] HTTP 請求與錯誤處理
- [x] Retry 機制
- [x] TWSE 每日行情 API Client
- [x] DailyMarketData 資料型別定義
- [x] TWSE API 回應資料驗證
- [x] TypeGuard 靜態型別輔助
- [x] TWSE 專屬 Logger
- [x] pytest 單元測試與資料品質測試

### Planned

- [ ] TPEx 每日行情 API Client
- [ ] 統一 TWSE 與 TPEx 資料格式
- [ ] 歷史行情資料回補（最近五年）
- [ ] SQLite 資料庫管理
- [ ] 每日自動資料蒐集
- [ ] 個股歷史行情查詢
- [ ] 股票排行榜
- [ ] 股價與成交量圖表
- [ ] 市場統計分析
- [ ] CSV / Excel 資料匯出
- [ ] Streamlit 網頁儀表板
- [ ] 電子郵件錯誤通知

## Technology Stack

### Currently Used

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python 3.14+ | Main programming language |
| Requests     | HTTP API requests         |
| pytest       | Automated testing         |
| Ruff         | Linting and code quality  |
| Black        | Code formatting           |
| pre-commit   | Git hooks and code checks |
| SQLite       | Planned database          |

### Planned

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Pandas     | Data processing and analysis |
| Streamlit  | Web dashboard                |
| Plotly     | Interactive charts           |
| OpenPyXL   | Excel export                 |

## Project Structure

```text
TaiwanStockDataCollector/
│
├── src/
│   └── stock_collector/
│       ├── api/
│       │   ├── base_client.py
│       │   └── twse_client.py
│       │
│       ├── collector/
│       ├── database/
│       ├── processors/
│       ├── services/
│       └── utils/
│           └── logger.py
│
├── tests/
│
├── config/
│   └── settings.py
│
├── pyproject.toml
├── .pre-commit-config.yaml
├── LICENSE
└── README.md
```

## Requirements

- Python 3.14 or later
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mamhea/TaiwanStockDataCollector.git

cd TaiwanStockDataCollector
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Linux / WSL:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install the project

```bash
python -m pip install --upgrade pip

python -m pip install -e ".[dev]"
```

## Development

### Run tests

```bash
pytest -v
```

### Run Ruff

```bash
ruff check .
```

### Check code formatting

```bash
black --check .
```

### Run pre-commit

```bash
pre-commit run --all-files
```

## Project Status

**Current Stage: API Client Development**

目前已完成共用 API Client 與 TWSE 每日行情資料擷取功能，並加入資料結構驗證、日誌紀錄及自動化測試。

接下來的開發重點：

1. 實作 TPEx API Client。
2. 統一 TWSE 與 TPEx 的行情資料格式。
3. 建立資料處理與 SQLite 儲存模組。
4. 開發歷史資料回補功能。
5. 建立 Streamlit 網頁儀表板。

本專案仍在持續開發中，功能及專案架構可能隨開發進度調整。

## Data Sources and Usage

本專案使用 TWSE 與 TPEx 提供的公開市場資料。

- 資料來源及其使用規範以各官方機構公告為準。
- 本專案的 MIT License 僅適用於本專案中由作者擁有權利的原始程式碼。
- 官方市場資料、第三方套件及其他外部資源不會因本專案採用 MIT License 而自動取得相同授權。

## License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) 2026 柏翰
