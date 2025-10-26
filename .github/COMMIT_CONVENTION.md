# コミットメッセージ規約

本プロジェクトでは [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) に準拠した形式を採用します。履歴の可読性向上、CHANGELOG自動生成、レビュー効率化が目的です。

##　前提
日本語で書きましょう

## 基本フォーマット

```
<type>(<scope>)<!>: <日本語のsubject>

<日本語のbody>

<footer>
```

- subject: 50文字以内を推奨。**日本語で記述**。文末の句点（。）は付けない
- body: 72桁目で改行を推奨。**日本語で記述**。何を/なぜ/影響範囲を簡潔に記述
- footer: Issue連携や破壊的変更の宣言を記述

## type 一覧

- feat: 新機能
- fix: バグ修正
- docs: ドキュメントのみ
- style: コードスタイル（機能変更なし）
- refactor: リファクタリング（バグ修正/新機能なし）
- perf: パフォーマンス改善
- test: テスト追加/修正
- build: ビルド/依存関係の変更（requirements.txt 等）
- ci: CI設定やスクリプトの変更
- chore: その他の雑務（ツール設定、スクリプト等）
- revert: 取り消し

## scope 例（任意）

- api, views, services, models, static, templates, db, docs, config

## 破壊的変更

- 互換性を失う変更には `!` を付与し、footer に `BREAKING CHANGE:` を必ず記載

```
feat(api)!: 予報APIのレスポンス形式を変更

BREAKING CHANGE: /api/weather/forecast のフィールド名を変更
```

## 本プロジェクトでの例

- feat(services): 明日の最高/最低の計算をtemp_max/minから集計
- fix(api): /api/locations/search が空文字で500になる不具合を修正
- docs: READMEにセットアップ手順を追記
- refactor(models): WeatherForecast のインデックスを追加
- test(views): エクスポートAPIのCSV出力を検証
- chore: .gitignore を追加し機密ファイルを除外

## フッターの書き方

- Closes: #123 でIssueをクローズ
- Refs: #456 で関連参照
- BREAKING CHANGE: 破壊的変更の詳細

## コミットテンプレート（任意）

ルートに `.gitmessage` を用意しています。利用する場合は以下を実行してください：

```powershell
# 一度だけ設定
git config commit.template .gitmessage

# グローバルに設定したい場合
# git config --global commit.template "C:/path/to/.gitmessage"
```

これで `git commit` 実行時にテンプレートが開きます。
