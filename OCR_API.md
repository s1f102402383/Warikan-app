# API リファレンス
開発環境:https://ocr-bridge-dev.inv.sorimachi.biz
## POST /recognize

画像ファイルをOCR解析するAPIです。

### リクエストヘッダー (Request Headers)

| Key | Value | Example |
| :--- | :--- | :--- |
| Accept | 利用したいOCRエンジン指定 | `application/ocrv3+json`|
| Authorization | 発行されたシークレットキー | - |
| Content-Type | `multipart/form-data` | - |

### リクエストボディ (Request Body)

| Key | Type | Spec | Value | Note |
| :--- | :--- | :--- | :--- | :--- |
| evidence_type | string | 指定の証憑種別 | "receipt" | - |
| file | binary | 画像ファイル | - | サイズ: 20MBまで<br>拡張子:<br>・OCRV3: PDF, PNG, JPEGをサポート|

## レスポンス (Response)

OCRエンジンのレスポンスが返却されます。
※中間サーバー ↔ エンジン間のタイムアウト: 24秒

- `result` (Object) : 読み取り結果オブジェクト
    - `ocrInfo` (Object) : Google Vision APIのOCR結果オブジェクト
        - `fullText` (Object) : OCR全文結果
            - `text` (String) : 読み取り結果 **※インターンで使用する値**
    - `senderInfo` (Object) : 店舗情報オブジェクト
        - `regNo` (Object) : 登録番号
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。 1が最も高い信頼度を表します。
        - `name` (Object) : 店名
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。 1が最も高い信頼度を表します。
        - `branch` (Object) : 支店名
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。 1が最も高い信頼度を表します。
        - `nameByRegNo` (Object) : 登録番号に基づいて政府APIからの店名
            - `text` (String) : 政府APIからの取得結果
    - `recipientInfo` (Object) : 発行先情報オブジェクト
        - `name` (Object) : 発行先会社名
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。1が最も高い信頼度を表します。
    - `totalPrice` (Object) : 合計情報オブジェクト
        - `price` (Object) : 合計金額
            - `formatted` (Object) : フォーマット済みの読み取り結果
                - `value` (String) : 数値書式にフォーマット済みの読み取り結果
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。 1が最も高い信頼度を表します。
        - `tax` (Object) : 消費税
            - `formatted` (Object) : フォーマット済みの読み取り結果
                - `value` (String) : 数値書式にフォーマット済みの読み取り結果
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。1が最も高い信頼度を表します。
    - `subTotal` (Object) : 小計情報オブジェクト
        - `price10` (Object) : 10%対象合計額
            - `formatted` (Object) : フォーマット済みの読み取り結果
                - `value` (String) : 数値書式にフォーマット済みの読み取り結果
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。1が最も高い信頼度を表します。
        - `price8` (Object) : 8%対象合計額
            - `formatted` (Object) : フォーマット済みの読み取り結果
                - `value` (String) : 数値書式にフォーマット済みの読み取り結果
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。1が最も高い信頼度を表します。
        - `tax10` (Object) : 税額10%
            - `formatted` (Object) : フォーマット済みの読み取り結果
                - `value` (String) : 数値書式にフォーマット済みの読み取り結果
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。1が最も高い信頼度を表します。
        - `tax8` (Object) : 税額8%
            - `formatted` (Object) : フォーマット済みの読み取り結果
                - `value` (String) : 数値書式にフォーマット済みの読み取り結果
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。1が最も高い信頼度を表します。
    - `paymentInfo` (Object) : 支払情報オブジェクト
        - `date` (Object) : 支払日(取引日付)
            - `formatted` (Object) : フォーマット済みの読み取り結果
                - `day` (String) : 日 2桁
                - `month` (String) : 月 2桁
                - `year` (String) : 年 4桁
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。 1が最も高い信頼度を表します。
        - `reason` (Object) : 件名
            - `text` (String) : 読み取り結果
            - `confidenceScore` (Float) : OCR信頼度。 1が最も高い信頼度を表します。

### エラー (Errors)
| Key | Type | Note |
| :--- | :--- | :--- |
| error_code | number | 10進数表記のエラーコード |
| type | string | エラータイプ |
| message | string | エラー内容 |

#### error_code一覧
| エラーコード | HTTPステータス | 内容 | 備考 |
| :--- | :--- | :--- | :--- |
| 0x20200002 | 400 | パラメータエラー | |
| 0x20200003 | 400 | パラメータエラー | |
| 0x20200304 | 400 | パラメータエラー | |
| 0x29900001 | 500 | システム障害 | |
| 0x29900101 | 500 | システムロジックエラー | |
| 0x29900201 | 500 | DBレコード挿入エラー | |
| 0x29900301 | 500 | DBレコード選択エラー | |
| 0x29900302 | 500 | DBレコード選択エラー | |
| 0x29900502 | 500 | OCR処理エラー | |

#### メッセージ一覧 (Message List)

| メッセージ | 内容 | 対応エラーコード |
| :--- | :--- | :--- |
| api_key_nameパラメータを指定して再実行してください。 | 中間サーバ設定ミス（OCR担当者へ連絡が必要） | 0x29900501, 0x29900601 |
| サーバーエラー。メッセージ=「1」 | サーバーエラー（リクエスト不備の可能性あり） | 0x29900501, 0x29900601 |
| OCRプロセスがタイムアウトしました。 | Google Vision APIからのタイムアウト | 0x29900502, 0x29900602 |
| OCRプロセスが失敗しました。コード={0}, メッセージ={1} | Google Vision APIからの失敗<br/>詳細エラー情報も返されます。リクエスト内容に不備がないがご確認後に再実行してください。<br/>{0}:エラーコード、{1}:エラー内容 | 0x29900502, 0x29900602 |
| invalid secret key: {0} | シークレットキー不正 | 0x20200002 |
| invalid  evidence type: {0} | パラメータ不正 | 0x20200003 |
| invalid accept header: {0} | Content-Type不正 | 0x20200004 |
| ただいまシステムが大変混み合っております、申し訳ありませんがしばらく時間を置いてからご利用ください。 | システムエラー系 | 0x20000001, 0x20100001, 0x29900001, 0x29900101, 0x29900201, 0x29900301, 0x29900302 |