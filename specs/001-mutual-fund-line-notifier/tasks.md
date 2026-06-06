# Tasks: Mutual Fund LINE Notifier

**Feature Branch**: `001-mutual-fund-line-notifier`

## Phase 1: Environment & Scaffolding

- [x] **Task 1.1: Project Setup**
  - [x] `requirements.txt` の作成 (beautifulsoup4, line-bot-sdk, pytest)
  - [x] ディレクトリ構造の作成 (`src/`, `tests/unit/`, `tests/integration/`)
  - [x] `.env.example` の作成 (認証情報テンプレート)

- [x] **Task 1.2: Base Data Models**
  - [x] `src/models.py` に `FundRequest` および `FundData` クラスを実装

## Phase 2: Core Logic Implementation

- [x] **Task 2.1: Yahoo! Finance Scraper**
  - [x] `src/scraper.py` にスクレイピングロジックを実装
  - [x] 8文字ID（英数字）を使用したURL生成ロジックの実装
  - [x] `BeautifulSoup4` による基準価額・前日比の抽出
  - [x] 取得失敗時の「取得なし」状態のハンドリング

- [x] **Task 2.2: LINE Notifier**
  - [x] `src/notifier.py` に `line-bot-sdk` を使用した通知ロジックを実装
  - [x] 指定されたフォーマット（ヘッダー + 各銘柄の行）のメッセージ生成ロジック
  - [x] 環境変数からの `LINE_CHANNEL_ACCESS_TOKEN` および `LINE_USER_ID` の読み込み

- [x] **Task 2.3: Lambda Entry Point**
  - [x] `src/lambda_function.py` にメインハンドラーを実装
  - [x] EventBridge からの入力 JSON 解析 (FR-001)
  - [x] Scraper と Notifier の統合

## Phase 3: Testing & Validation

- [x] **Task 3.1: Unit Tests**
  - [x] `tests/unit/test_scraper.py`: 様々なHTMLパターン（正常、取得不可）のテスト
  - [x] `tests/unit/test_notifier.py`: メッセージ生成ロジックのテスト

- [x] **Task 3.2: Integration Tests**
  - [x] `tests/integration/test_lambda.py`: モックを使用した全体フローのテスト

## Phase 4: Finalization

- [x] **Task 4.1: Documentation Update**
  - [x] `quickstart.md` の動作確認と更新
  - [x] Lambda デプロイパッケージ作成手順の確認
