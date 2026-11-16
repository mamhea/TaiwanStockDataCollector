# **Taiwan Stock Data Collector — 專案路徑規劃**

> **版本：** 1.0\
> **狀態：** 規劃中\
> **開發語言：** Python\
> **版本控制：** Git + GitHub（Public Repository）
> **開發環境：** 
```
Windows 11
├── WSL2
│   └── Ubuntu
│       ├── Python 3.14.4
│       ├── Virtual Environment
│       └── VS Code Remote - WSL
```

## **1. 專案完整資料夾結構**

```
TaiwanStockDataCollector/
│
├── .github/
│   └── workflows/
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── database/
│   │   └── .gitkeep
│   └── exports/
│       └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── scripts/
│   ├── __init__.py
│   └── run_collector.py
│
├── src/
│   └── stock_collector/
│       ├── __init__.py
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── twse_client.py
│       │   └── tpex_client.py
│       │
│       ├── collector/
│       │   ├── __init__.py
│       │   └── market_collector.py
│       │
│       ├── database/
│       │   ├── __init__.py
│       │   ├── connection.py
│       │   ├── models.py
│       │   └── repository.py
│       │
│       ├── processors/
│       │   ├── __init__.py
│       │   ├── parser.py
│       │   └── validator.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   ├── export_service.py
│       │   └── notification.py
│       │
│       └── utils/
│           ├── __init__.py
│           └── logger.py
│
├── dashboard/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── pages/
│   │   ├── 1_Stock_Search.py
│   │   ├── 2_Stock_Rankings.py
│   │   ├── 3_Stock_Analysis.py
│   │   ├── 4_Market_Analysis.py
│   │   ├── 5_Data_Management.py
│   │   └── 6_Settings.py
│   │
│   └── components/
│       ├── __init__.py
│       ├── charts.py
│       └── theme.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api_clients.py
│   ├── test_processors.py
│   └── test_database.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── main.py
```

## **2. 資料夾用途**

| 資料夾                  | 用途                |
| ----------------------- | ------------------- |
| `.github/`              | GitHub 相關設定     |
| `config/`               | 系統設定及環境變數  |
| `data/database/`        | SQLite 資料庫       |
| `data/exports/`         | CSV、Excel 匯出檔案 |
| `logs/`                 | 系統及爬蟲執行紀錄  |
| `scripts/`              | 手動執行及維護腳本  |
| `src/`                  | 核心程式碼          |
| `src/.../api/`          | TWSE、TPEx API 串接 |
| `src/.../collector/`    | 股票資料蒐集        |
| `src/.../database/`     | 資料庫操作          |
| `src/.../processors/`   | 資料解析及驗證      |
| `src/.../services/`     | 匯出、通知等服務    |
| `src/.../utils/`        | 共用工具            |
| `dashboard/`            | Streamlit 網站      |
| `dashboard/pages/`      | 網站各功能頁面      |
| `dashboard/components/` | 共用介面元件        |
| `tests/`                | 自動化測試          |

## **3. 核心檔案職責**

| 檔案                  | 職責                             |
| --------------------- | -------------------------------- |
| `main.py`             | 專案主要執行入口                 |
| `settings.py`         | 集中管理系統設定                 |
| `twse_client.py`      | 取得上市股票資料                 |
| `tpex_client.py`      | 取得上櫃股票資料                 |
| `market_collector.py` | 統一管理市場資料蒐集             |
| `connection.py`       | 管理 SQLite 連線                 |
| `models.py`           | 定義資料模型                     |
| `repository.py`       | 負責資料庫 CRUD                  |
| `parser.py`           | 解析官方 API 回傳資料            |
| `validator.py`        | 驗證及清理行情資料               |
| `export_service.py`   | 匯出 CSV、Excel                  |
| `notification.py`     | 發送電子郵件通知                 |
| `logger.py`           | 設定系統日誌                     |
| `app.py`              | Streamlit 網站入口               |
| `run_collector.py`    | Windows 工作排程器呼叫的爬蟲入口 |

## **4. Git 忽略設定**

`.gitignore`：

```
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual Environment
.venv/
venv/

# Environment Variables
.env

# Database
data/database/
*.db
*.sqlite
*.sqlite3

# Exported Files
data/exports/

# Logs
logs/
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/

# Operating System
.DS_Store
Thumbs.db
```

## **5. 環境變數範例**

`.env.example`：

```
# Application
APP_NAME=Taiwan Stock Data Collector
APP_ENV=development

# Database
DATABASE_PATH=data/database/stocks.db

# Email Notification
SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
EMAIL_SENDER=
EMAIL_RECEIVER=
```

`.env.example` 可以公開上傳 GitHub，但真正的 `.env` 必須排除。

## **6. 網站頁面規劃**

採用混合式架構：

| 頁面            | 功能                 |
| --------------- | -------------------- |
| Dashboard       | 台灣股市總覽         |
| Stock Search    | 個股查詢             |
| Stock Rankings  | 股票排行榜           |
| Stock Analysis  | 個股統計分析         |
| Market Analysis | 大盤分析             |
| Data Management | 資料蒐集及資料庫管理 |
| Settings        | 主題及系統設定       |

## **7. 技術架構**

```
                    使用者裝置
                         │
                    區域網路 LAN
                         │
                         ▼
               Streamlit 網站介面
                         │
                         ▼
                 Python 分析服務
                         │
                ┌────────┴────────┐
                ▼                 ▼
           Pandas             Plotly
          資料分析           圖表呈現
                │
                ▼
             SQLite
                ▲
                │
         Python 資料蒐集程式
                │
          ┌─────┴─────┐
          ▼           ▼
       TWSE API    TPEx API
          │           │
          ▼           ▼
        上市資料     上櫃資料
```

## **8. 開發注意事項**

1. 不需要一次建立所有資料夾，按照開發階段逐步建立。
2. 核心資料蒐集程式與 Streamlit 網站分離。
3. SQLite 資料庫不提交至公開 GitHub。
4. Email 密碼及其他敏感憑證不得寫入原始碼。
5. 歷史資料回補範圍為最近五年，實際取決於官方 API 可取得資料。
6. 每日預計於 18:00 透過 Windows 工作排程器執行。
7. 官方 API 必須加入錯誤處理、適當請求間隔及重試機制。
8. 網站需測試桌面、平板及手機的響應式使用體驗。

**文件狀態：初步架構已規劃，尚未開始建立實際檔案。**
