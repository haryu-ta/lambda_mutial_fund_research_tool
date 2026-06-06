# Feature Specification: Mutual Fund LINE Notifier

**Feature Branch**: 001-mutual-fund-line-notifier

**Created**: 2026-05-30

**Status**: Draft

**Input**: User description: "指定した投資信託の基準価額データを定期取得し、投資判断に必要な情報を LINE に通知する。" (Reference: docs/requirements.md)

## User Scenarios & Testing

### User Story 1 - 基準価額の定期通知 (Priority: P1)

投資信託の保有者は、平日の決まった時間に、最新の基準価額と前日比を LINE で受け取り、迅速に投資判断（売買の検討など）を行いたい。

**Why this priority**: 本ツールのコア機能であり、これがなければ投資判断の自動化という目的が達成されないため。

**Independent Test**: 特定の投資信託IDを含むテストイベントを Lambda に送信した際、指定されたフォーマットの LINE 通知が正しく届くことで検証可能。

**Acceptance Scenarios**:

1. **Given** 取得対象の投資信託IDリストが設定されている, **When** 平日午前9時に EventBridge が Lambda を起動する, **Then** 指定された全銘柄の基準価額と前日比が LINE に通知される。
2. **Given** 無効な投資信託IDが混入している, **When** Lambda が実行される, **Then** 該当銘柄について「取得なし」と表示された LINE 通知が届き、CloudWatch Logs に警告が出力される。

---

### User Story 2 - 複数銘柄の一括通知 (Priority: P2)

複数の投資信託を保有しているユーザーは、1回の通知で全保有銘柄の状態を確認し、全体的な資産推移を把握したい。

**Why this priority**: 複数の通知が届く煩わしさを避け、一覧性を高めるため。

**Independent Test**: 複数（例：2件以上）の投資信託情報を含むイベントを処理し、1通の LINE メッセージに全銘柄が含まれていることを確認する。

**Acceptance Scenarios**:

1. **Given** 2件の投資信託が指定されている, **When** Lambda が正常に終了する, **Then** LINE メッセージ1通の中に、2銘柄それぞれの名称・価格・前日比が含まれている。

## Requirements

### Functional Requirements

- **FR-001**: システムは EventBridge から渡された JSON 配列（id, display_name）を解析しなければならない。IDは英数字を含む8文字（例：8931123C）を想定する。
- **FR-002**: システムは Yahoo!ファイナンスから基準価額と前日比をスクレイピングしなければならない。
- **FR-003**: システムは取得した情報を LINE Messaging API (Push Message) を使用して単一ユーザーへ送信しなければならない。送信先の User ID は環境変数から取得する。
- **FR-004**: 通知メッセージは「YYYY/MM/DD 基準値」というヘッダーを含み、各行に「名称 金額円 前日比円」を記載しなければならない。データが取得できない場合は「名称 取得なし」と記載する。
- **FR-005**: スクレイピングまたは API 呼び出しに致命的な失敗（ネットワークエラー等）をした場合、システムは CloudWatch Logs にエラーを出力し、例外をスローしなければならない。個別の銘柄取得失敗は通知内で「取得なし」として扱う。
- **FR-006**: 認証情報（LINEトークン、User ID等）は環境変数から取得し、コード内にハードコードしてはならない。

## Clarifications

### Session 2026-05-31

- Q: データソースのフォールバックについて（Yahoo!ファイナンス失敗時の挙動） → A: Yahoo!ファイナンスのみを対象とし、失敗時はエラーとして通知する。
- Q: 投資信託IDのフォーマットについて → A: 英数字を含む8文字（例：8931123C）。
- Q: データ取得不可（非営業日等）の挙動について → A: その銘柄のみ「取得なし」として通知に含める。
- Q: 通知先（LINE User ID）の指定方法について → A: 環境変数から取得する。
- Q: 「データなし」時の表示形式について → A: 「名称 取得なし」とする。

## Key Entities

- **FundRequest**: 取得対象の投資信託（id, display_name）。IDは8文字の英数字。
- **FundData**: スクレイピング後のデータ（名称, 基準価額, 前日比, タイムスタンプ）。取得失敗時は状態を保持。
- **NotificationMessage**: LINE に送信されるテキスト形式のメッセージ。

## Success Criteria

### Measurable Outcomes

- **SC-001**: Lambda 起動から LINE 通知完了までが 20秒以内（タイムアウト設定内）で完了すること。
- **SC-002**: 通知された基準価額が、ソースサイトの表示内容と 100% 一致すること。
- **SC-003**: 致命的なエラー発生時、例外が確実にスローされ、CloudWatch で ERROR レベルとして検知可能であること。

## Assumptions

- ユーザーは有効な LINE Messaging API の Channel Access Token と User ID を持っている。
- Yahoo!ファイナンスの HTML 構造が（短期的には）大きく変更されない。
- AWS Lambda から外部インターネットへの通信が許可されている（VPC 設定等）。
- 基準価額は整数（円単位）として扱う。
