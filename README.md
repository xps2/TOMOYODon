# TOMOYODon
ディレクトリを監視してファイルをアップロードし、トートする

## 準備

### トークン
* token.ini.sampleを、token.iniにリネームする。
* token.iniを自分が使用しているインスタンスに合わせて変更する。
* `python tomoyodon.py --token`を実行する。
* client_id, access_tokenで指定したファイルが作成されていることを確認する。
* token.iniは不要なので削除する。

### tomoyodon.ini
* tomoyodon.ini.sampleをtomoyodon.iniにリネームする。

#### [API]
* api_base_url=自分が使用しているインスタンス
* client_id, access_tokenはtoken.iniで指定したものとあわせる

#### [Path]
* target=監視対象のパス

#### [TOOT]
* toot_str=アップロードする画像と一緒に表示するtoot内容を記述
* visibility=(private, unlisted or public)
* sensitive=(true or false)
* visibilityとsensitiveについてはMastodon.pyのドキュメントを参照

## 実行方法
* `python tomoyodon.py`

## 動作確認環境
* Windows + Python 2.7
* Windows + Python 3.6
* 他環境は確認してませんが、依存ライブラリのwatchdogが対応しているOSであれば動くかもしれません。

## 依存ライブラリ
* [Mastodon.py](https://github.com/halcy/Mastodon.py)
* [retry](https://github.com/invl/retry)
* [watchdog](https://github.com/gorakhargosh/watchdog)
