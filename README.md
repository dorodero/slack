
# slack

Serverless Slash Commands with Python

https://api.slack.com/tutorials/tags/slash-commands

を参考に実施

# Installation
pyenv
```bash
pip install pyenv-win --target %USERPROFILE%/.pyenv
```
python
```bash
pyenv 3.6.4
pyenv local 3.6.4
```
requirements
```bash
pip install -r requirements.txt
```

# Development
ローカル環境での試し方

事前にslackのslash commandを作成しておく

必要な環境変数をExportをし、Flasｋでアプリを実行
```bash
export SLACK_VERIFICATION_TOKEN=your-verification-token
export SLACK_TEAM_ID=your-team-id
export FLASK_APP=hello-there.py
flask run
```
ngrokを使用してローカル上で起動しているネットワークサービスを外部に公開する。

https://ngrok.com/
```bash
ngrok　http 5000
```
HTTPS転送URLをコピーしslack apiのRequet apiに設定。エンドポイントは/hello-thereとしておく
# Deployment
AWS credentials fileを作成しておく

Zappaを使用してAWS Lambda に公開

https://github.com/Miserlou/Zappa

```bash
pip install zappa
```

zappa_settings.jsonを作成し必要な情報を記載しデプロイ
```bash
zappa deploy prod
zappa update prod
```
API Gateway URLをslack apiのrequest urlに設定