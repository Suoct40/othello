
### othello
 my create othello

## ゲームモードの変更
 othello/app.py 16行目
~~~py
         self.game_mode : str  = 'joke'  # 'normal', 'easy', 'joke'
~~~
 の　__self.game_mode__ を以下の文字列に置換 'normal', 'easy', 'joke'

## 操作方法

# 駒を配置する
 全てのゲームモードで利用が可能だが、_nomal_ の場合置ける場所に目印がつかない
 click __left__ button
https://user-images.githubusercontent.com/103062031/163702783-40a45a2b-3eee-4a97-a04c-8df6f4e984df.mp4

# 一手前に戻る
 ゲームモードが _easy_ 若しくは _joke_ の場合のみ利用可能
 push __c__ key
https://user-images.githubusercontent.com/103062031/163702866-d766ed42-60e3-4694-be00-91c0c57ad912.mp4

# 一手前に進む
 ゲームモードが _easy_ 若しくは _joke_ の場合のみ利用可能
 push __v__ key
https://user-images.githubusercontent.com/103062031/163702847-ff510981-a0dd-4fea-9347-5fd78a333d91.mp4

# 駒を削除
 ゲームモードが _joke_ の場合のみ利用可能
 click __right__ button
https://user-images.githubusercontent.com/103062031/163703453-7a0a3a73-ce72-44e6-a037-8be4b5258252.mp4

# continue
 ゲームが終了した際に実行可能
https://user-images.githubusercontent.com/103062031/163703503-6ad23e0a-53c1-42e8-a64c-23a201e11aac.mp4

