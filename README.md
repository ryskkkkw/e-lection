# はじめに

このプロジェクトはPython,Djangoを独学したアウトプットとして作成した2つ目のポートフォリオです。  
次の項目に沿って、ポートフォリオについて説明します。

1. プロジェクトについて
2. ディレクトリ構成
3. 主なディレクトリの説明

<br>

# 1.　プロジェクトについて

2つ目のポートフォリオとして政党への投票アプリケーションを作成しました。このアプリケーションを作成した理由は、投票率や政治への関心の低さなどの問題に対して、日常的に投票や投票結果を可視化できるサービスがあればと考えたためです。  

あくまでポートフォリオであり、実際に運用をしているわけではありませんが、最初のポートフォリオである[eFarm](https://github.com/ryskkkkw/eFarm/tree/main)同様に、テーマを持って実践的に取り組むことを意識し、プロジェクト名は「e-lection」としました。デプロイもしていますので、実際に[e-lection](https://krkr.pythonanywhere.com/)を確認できます。

機能的にはeFarmよりも小規模ではありますが、データベースをDjangoデフォルトのsqliteではなくmysqlにしたことや、大量のテストデータや効率的な投票結果の作成のために、カスタムコマンドを作ったことがeFarmとは違うところです。  
また、当初は３つ目のポートフォリオである[local_llm_for_cpu](https://github.com/ryskkkkw/local_llm_for_cpu)と組み合わせて、政治関係のドメインに特化した生成AIによるQ&A機能も実装しようと考えていましたが、パフォーマンスの理由から別のプロジェクトとしたことが、このプロジェクトが小規模になった理由です。


<br>

# 2.ディレクトリ構成

プロジェクトディレクトリの主な構成は以下のとおりです。  
アプリケーションはvotesのみです。

    apps
    ├── config
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   └── production.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    ├── requirements.txt
    └── votes
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── management
        │   ├── __init__.py
        │   └── commands
        │       ├── testdata_create.py
        │       └── vote_result.py
        ├── models.py
        ├── static
        │   └── votes
        │       └── style.css
        ├── templates
        │   └── votes
        │       ├── base.html
        │       ├── confirm.html
        │       ├── index.html
        │       ├── result.html
        │       └── select.html
        ├── tests
        │   ├── test_commands.py
        │   └── test_votes.py
        ├── urls.py
        └── views.py
        

<br>

#  3.主なディレクトリの説明


