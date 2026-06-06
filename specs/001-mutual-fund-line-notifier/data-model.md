# Data Model: Mutual Fund LINE Notifier

## Entities

### FundRequest
取得対象の投資信託を指定するための入力データ。

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | string | Yahoo!ファイナンスの銘柄ID | 8文字の英数字 |
| display_name | string | 通知時に表示する銘柄名称 | 必須 |

### FundData
スクレイピングによって取得された銘柄ごとの詳細データ。

| Field | Type | Description |
|-------|------|-------------|
| name | string | 取得した銘柄名 |
| price | integer | 基準価額 (円) |
| change | integer | 前日比 (円) |
| is_success | boolean | 取得に成功したかどうか |
| timestamp | string | 取得日時 (ISO 8601) |

## State Transitions
- **Pending**: Lambda起動直後、未処理の状態。
- **Processing**: スクレイピング実行中。
- **Success**: スクレイピングに成功し、データが取得された状態。
- **Failed**: スクレイピングに失敗したが、「取得なし」として通知対象となる状態。
