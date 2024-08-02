# はじめに

このプロジェクトはPython,Djangoを独学したアウトプットとして作成した2つ目のポートフォリオです。  
次の項目に沿って、ポートフォリオについて説明します。

1. プロジェクトについて
2. ディレクトリ構成
3. 主なディレクトリの説明

<br>

# 1.　プロジェクトについて

2つ目のポートフォリオとして政党への投票アプリケーションを作成しました。このアプリケーションを作成した理由は、投票率や政治への関心の低さなどの問題を普段からニュースで目にする中で、日常的に投票や投票結果を可視化できるサービスがあればと考えたためです。  

あくまでポートフォリオであり、実際に運用をしているわけではありませんが、最初のポートフォリオである[eFarm](https://github.com/ryskkkkw/eFarm/tree/main)同様に、テーマを持って実践的に取り組むことを意識し、プロジェクト名は「e-lection」としました。デプロイもしていますので、実際に[e-lection](https://krkr.pythonanywhere.com/)を確認できます。

プロジェクトとしてはeFarmよりも小規模ではありますが、データベースをDjangoデフォルトのsqliteではなくmysqlにしたことや、大量のテストデータや効率的な投票結果の作成のために、カスタムコマンドを作ったことがeFarmとは違うところです。  
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

votesがこのプロジェクトで唯一のアプリケーションなので、その中で主なところを説明します。

- モデルは投票データ用のVoteモデル、投票結果データ用のResultモデルの2つを実装しています。
- Voteモデルは投票する政党や投票者の年代、性別などのフィールドがあり、投票ごとに1つのオブジェクトが作成されます。
- Rusultモデルは投票データを日別で集計します。投票日、政党、投票数のフィールドを持ちます。
- 投票する際は、投票画面に政党名、投票者の年代、性別を選ぶラジオボタンが表示されるので、それを選択して投票を行います。
- 投票を行うとVoteViewで投票データが作成されますが、その時に投票者のIPアドレスを取得してデータに追加します。
- IPアドレスを取得するのは、1日に２回以上の投票を防ぐためです。投票データを作成するときは、その日に同じIPアドレスの投票データがないかを確認して、該当データがある場合は投票を受け付けない仕様になっています。
- 実際のところ、この仕組みでは複数回の投票を防ぐことはできませんが、IPアドレスが固定という前提であれば簡易に実装できることや、最初のポートフォリオであるeFarmではIPアドレス用のモデルフィールドは使わなかったので試してみたかったということが、この仕様にした理由です。
<br>

- 投票結果は日別、月別、月単位推移を確認できます。
- get_svg_daily or monthly or transitionのいずれかの関数で、setPLT_daily or monthly or transitionのいずれかの関数を呼び出し、その際にユーザーが入力した日付や月、期間を関数に渡します。setPLT_関数では渡された値を基に投票結果を集計し、matplotlibを使って投票結果のグラフを表示します。
- 投票結果を集計するときは、個別の投票データであるVoteオブジェクトではなく、日別の投票結果の集計データであるResultオブジェクトから投票結果を抽出しています。
- 最初はVoteオブジェクトから投票結果を集計していましたが、月別や月単位推移で集計する場合はある程度の時間を要するので、Resultオブジェクトをつくり、あらかじめ日別の集計データを作成しておくことで、月別や月単位推移の集計に要する時間を短縮しました。
<br>

- Resultオブジェクトの作成には、votes/management/commands/vote_result.pyにあるカスタムコマンドを使います。
- コマンドライン引数に開始日と終了日を入力して実行すると、入力された日付に作成されたVoteオブジェクトを抽出し、政党ごとに票数を集計してResultオブジェクトを作成します。
- 一度に大量の投票データを作成するために、vote_result.pyと同じディレクトリにあるtestdata_create.pyに投票データ作成用のカスタムコマンドも作成しました。
- このカスタムコマンドも引数に開始日と終了日を入力して実行すると、投票データとして1日あたり1000件のVoteオブジェクトが作成されます。各投票データの政党、年代、性別はPythonのrandom.choice関数に重みを設定したうえで疑似乱数により生成しています。
- 今回のプロジェクトでは、このコマンドで大量の投票データをあらかじめ作成してから、Resultオブジェクトを作成しています。
- 仮に実際に運用するとしたら、日付が変わった深夜帯に前日分の投票データに対して、Resultオブジェクト作成コマンドを定時で自動実行することを想定しています。
<br>

- テストはviewとカスタムコマンドについて行っています。
- viewのテストでは、選択した政党や年代などが正しくVoteオブジェクトとして登録されているか、レスポンスに意図したテンプレートや文言が含まれているか、同日に同じIPアドレスの投票が行われたときはエラーになるかといった基本的な機能の動作をテストしています。
- カスタムコマンドのテストでは、引数に入力した日数分のVoteオブジェクト（1日あたり1000件）が作られているか、Voteオブジェクトとそれを基に作成したResultオブジェクトを比較したときに、特定の政党の得票数は同じになっているかをテストしています。



