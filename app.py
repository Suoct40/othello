#!/usr/bin/env python3.10

"""
Created on Wed Dit 15 14:30 2021

@author: shinji3
"""

import tkinter

class OthelloArgolthm:
    """オセロなクラス"""
    def __init__(self) -> None:
        # othero
        self.game_state: str  = 'run'     #start' 'run', 'end'
        self.game_mode : str  = 'joke'  # 'normal', 'easy', 'joke'
        count_turn: int  = 0            # if count_turn % 2 == 0: black put turn
        board     : list = [            # 1 = black, 2 = white, 0 = speace
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,2,0,0,0,
            0,0,0,2,1,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0]
        self.game_save: list = [(board, count_turn)]
        self.redo_save: list = [([], -1)]
        
    def _put_stones(self, coordinates: list, put: int= 3) -> list:
        """指定された座標群に指定されたデータを挿入"""
        self.redo_save = [([], -1)]
        count_turn = self.game_save[-1][1]
        board      = self.game_save[-1][0][:]
        for coordinate in coordinates: board[coordinate] = 1 + count_turn % 2 if put > 2 else put
        if coordinates: self.game_save.append((board, count_turn + 1))
        return coordinates

    def _put_stone_check(self, choice_point: int, other_turn: int = 0) -> list:
        """マスの座標を入力されたら改変できる石を返す"""
        board, count_turn = self.game_save[-1]
        if other_turn: count_turn = other_turn

        if not(-1 <= choice_point <= 64): return []#範囲外の引数を受け取ったら弾く分岐
        if not board[choice_point] == 0 : return []#空きマス以外を受け取ったら弾く分岐
        """確認すべきマスを全て取り出す"""
        wide = choice_point %  8
        high = choice_point // 8
        angel_45 : list = [i +  wide + high for i in range(0,len(board),7) if i / 7 < 8   ] #選択した数を基準とて１時半の角度の線分
        angel_135: list = [i +  wide - high for i in range(0,len(board),9) if i / 9 < 8   ] #選択した数を基準とて４時半の角度の線分
        angel_0  : list = [i +  wide        for i in range(0,len(board),8)                ] #選択した数を基準とて１２時の角度の線分
        angel_90 : list = [i                for i in range(high * 8, high * 8 + 8)]         #選択した数を基準とて　３時の角度の線分
        angel_45 : list = angel_45 [:1 + wide + high] if  wide + high < 8 else angel_45 [wide + high - 7:]  #有効な数値を抽出
        angel_135: list = angel_135[:8 - wide + high] if  wide > high     else angel_135[high - wide    :]  #有効な数値を抽出

        coordinates = [angel_0, angel_45, angel_90, angel_135]
        """確認すべきマスから駒を反転できるか確認する"""
        replace_order: list = []
        strong       : int  = 1 + count_turn % 2
        weak         : int  = 2 - count_turn % 2 

        for coordinat in coordinates:    #4回に分けて指定された8方向の座標群をゲームの条件に従って選別する繰返し文
            zone_A: list = coordinat[coordinat.index(choice_point)::-1][1::]#choice_pointからchoice_pointを除く左辺を逆順にした座標群 [choice_point, ->, 外][1:]
            zone_B: list = coordinat[coordinat.index(choice_point):][1::]   #choice_pointからchoice_pointを除く右辺の座標群　　　　　 [choice_point, ->, 外][1:]
            tmp   : list = []
            active: bool = True
            for pos in zone_A:  # 劣勢な駒->優勢な駒 の場合のみ反転予定リストに加わる
                if   board[pos] == 0 or not(active): active                = False
                elif board[pos] == strong          : replace_order, active = replace_order+tmp, False
                elif board[pos] == weak            : tmp.append(pos)
            tmp    = []
            active = True
            for pos in zone_B:  # 劣勢な駒->優勢な駒 の場合のみ反転予定リストに加わる
                if   board[pos] == 0 or not(active): active                = False
                elif board[pos] == strong          : replace_order, active = replace_order+tmp, False
                elif board[pos] == weak            : tmp.append(pos)

        if replace_order: replace_order.append(choice_point) #返す石がなかった場合石を置けない座標なのでchoice_pointも除外する

        return replace_order

    def _attack_check(self, other_turn: int = 0)-> list:
        """総当りで盤面にどちらかの石が設置できる位置を返す"""
        replacement_chances:list = []
        for pos in range(64):
            if self._put_stone_check(pos, other_turn): replacement_chances.append(pos)
        return replacement_chances

    def _pass_check(self): # game_state change
        """パスとゲームセットを検知して反映する"""
        count_turn = self.game_save[-1][1]
        board      = self.game_save[-1][0][:]
        now_turn  = self._attack_check()
        next_turn = self._attack_check(other_turn= count_turn+1)
        # True -> next check, else -> None
        if not now_turn:
            # True -> Game set, else -> pass turn
            if not next_turn: self.game_state = 'end'
            else            : self.game_save.append([board, count_turn+1])

    def othello_put_stone(self, point: int or str, function: object= lambda: None) -> None:
        """オセロのルールに則って石を反転させる"""
        if self._put_stones(self._put_stone_check(int(point))):
            self._pass_check()
            function()

    def othello_del_stone(self, point: int or str, function: object= lambda: None) -> None:
        """選択したマスに石がある場合それを削除する"""
        if self.game_save[-1][0][int(point)] != 0:
            self._put_stones([int(point)], put= 0)
            self._pass_check()
            function()

    def othello_undo(self, function: object= lambda: None) ->None:
        """一回前の手に戻る"""
        if  len(self.game_save) > 1:
            _ga_sv = self.game_save.pop()
            self.redo_save.append(_ga_sv)
            function()

    def othello_redo(self, function: object= lambda: None) -> None:
        """直前にundoした場合その変更を１回元に戻す"""
        if  self.redo_save and self.redo_save[-1][1] > self.game_save[-1][1]:
            _re_sv = self.redo_save.pop()
            self.game_save.append(_re_sv)
            function()

    def __del__(self)-> None:
        print("deleted othello argolithm")

class OthelloGUI(tkinter.Frame):
    """オセロをGUIで操作するクラス"""
    def __init__(self, root=None) -> None:
        # Othello frame
        self.OA = OthelloArgolthm()
        # tkinter frame
        super().__init__(root, bg='#222222')
        self.place(x=0, y=0, height=610, width=450)
        self.root = root
        self.widgets: dict = {'names':[], 'widgets':[]}
        self.create_widgets()
        self.player_input()


    def create_widgets(self) -> None:
        """ゲームの状態に合わせてウィジェットを作成する"""
        board, count_turn = self.OA.game_save[-1]
        def _del_widget() -> None:
            for i in self.widgets['widgets']:i.destroy()
            self.widgets = {'names':[], 'widgets':[]}

        def _put_widget(name: str, widget: object, x: int, y: int, row: int, col: int)-> None:
            self.widgets['names'  ].append(name)
            self.widgets['widgets'].append(widget)
            self.widgets['widgets'][self.widgets['names'].index(name)].place(x=x, y=y, width=row, height=col)

        def _widget_run() -> None:
            # button update
            def _st_btn_conf(place, color, text=""):
                _put_widget(
                    name= f"btn stone {place}", x= place %  8 * 50 + 25, y = place // 8 * 50 + 100, row= 50, col= 50,
                    widget=tkinter.Button(self,
                        name= f"btn stone {place}", activeforeground= color   , fg= color   , bg= "#114411",
                        text= text                , font= ("MS","25", "bold") , activebackground= "#336633"))
            _chance = self.OA._attack_check() if self.OA.game_mode != 'normal' else [] 
            [_st_btn_conf(btn, "#001100", "●") if board[btn] == 1 else # black
             _st_btn_conf(btn, "#ffddff", "●") if board[btn] == 2 else # white
             _st_btn_conf(btn, "#330000", "・") if btn in _chance  else # installation point
             _st_btn_conf(btn, "#225522","")    for btn in range(64)]

            # labels update
            # Label count stone in board
            _put_widget(
                name= "label count field stone", x= 25, y= 35, row= 400, col=50,
                widget= tkinter.Label(self,
                    text= f"Black:{board.count(1)} White:{board.count(2)} Last:{board.count(0)}",
                    font= ("MS","15", "bold"), name= "label count field stone"))

            # Label count turn and segment turn
            _put_widget(
                name="label count turn", x=25, y=510, row=400, col=50,
                widget=tkinter.Label(self,
                    text= "count:%d turn:%s"%(count_turn, "black" if count_turn % 2 == 0 else "white"),
                    name= "label count turn"  , fg  = "black" if count_turn % 2 == 1 else "white",
                    font= ("MS", "15", "bold"), bg  = "black" if count_turn % 2 == 0 else "white"))

        def _widget_end() -> None:
            """ゲームが終了したときの画面"""
            _del_widget()
            judge = "Black" if board.count(1) > board.count(2) else "White" if board.count(1) != board.count(2) else "Draw"

            # print end statas label
            _put_widget(
                name= "label judeg winer",x= 25, y= 35, row= 400, col= 540,
                widget= tkinter.Label(self,
                    name= "label judge winer", fg= "#ffffff" if judge == "Black" else "#000000",
                    font= ("MS","15", "bold"), bg= "#222222" if judge == "Black" else "#cccccc",
                    text= "GAME SET !\n\n%s\n%s\n%s"%(judge if judge == 'Draw' else f'wins {judge}', f"Sum tuen {count_turn}", f"Black:{board.count(1)} White:{board.count(2)} Last:{board.count(0)}")))
            
            # mini board viewer label
            def _st_label_conf(place, st_color, text=""):
                _put_widget(
                    name= f"label stone {place}", x= place %  8 * 10 + 335, y= place // 8 * 10 + 480, row= 10, col= 10,
                    widget= tkinter.Label(self,
                        name= f"label stone {place}", text= text,
                        font= ("MS", "6"), fg= st_color, bg= "#114411"))
            
            [_st_label_conf(pos, "#001100", "●") if board[pos] == 1 else _st_label_conf(pos, "#ffddff", "●") if board[pos] == 2 else _st_label_conf(pos, "#225522") for pos in range(64)]

            # restart game button
            _put_widget(
                name= "replay game" ,x= 30, y=400, row=80, col=20,
                widget=tkinter.Button(self,
                    name= "replay game", # command= lambda : Othello(root = self.root),
                    bg="#222222", fg="#ffffff",  text="restart" ))

        if   self.OA.game_state == 'start': None            # 未実装。Usr選択,追加 Game_Mode指定 Save_Data選択,読み込み 等実装予定
        elif self.OA.game_state == 'run'  : _widget_run()
        elif self.OA.game_state == 'end'  : _widget_end()

    def player_input(self):
        """ Player の入力を選別しメソッド等を実行する"""

        def push(key):
            """tkinter.bind(push key)を受け取ったら条件に従って関数を実行する"""
            if self.OA.game_state == 'run' :
                if   key.char == 'c' and self.OA.game_mode != 'normal': self.OA.othello_undo(self.create_widgets)
                elif key.char == 'v' and self.OA.game_mode != 'normal': self.OA.othello_redo(self.create_widgets)
            if self.OA.game_state:
                if   key.char == 'q' and self.OA.game_mode != ''      : exit(self)

        def click(btn):
            '''Bindから名前を取得したら条件に従って関数を実行する'''
            try:
                #| game state
                    #| key str                                | click btn      | game mode                 | execute commands
                if self.OA.game_state == 'start':
                    if   "run game"    in btn.widget._name and btn.num == 1                                : None
                if self.OA.game_state == 'run'  :
                    if   "btn stone"   in btn.widget._name and btn.num == 1                                : self.OA.othello_put_stone(btn.widget._name.split(" ")[-1], self.create_widgets)
                    elif "btn stone"   in btn.widget._name and btn.num == 3 and self.OA.game_mode == 'joke': self.OA.othello_del_stone(btn.widget._name.split(" ")[-1], self.create_widgets)
                    elif "label count" in btn.widget._name and btn.num == 3 and self.OA.game_mode == 'joke': None
                if self.OA.game_state == 'end'  :
                    if   "replay game" in btn.widget._name and btn.num == 1                                : self.destroy(), OthelloGUI(root= self.root)
            except AttributeError as a: print(f"That object is has not name states\n{a}")


        self.root.bind("<ButtonPress>", click)
        self.root.bind("<KeyPress>"   , push )
    def __del__(self)-> None:
        del self.OA

def main() -> None:
    # make window
    root = tkinter.Tk()
    root.configure(bg='#555555')
    root.title('othello')
    root.geometry("450x610")

    app  = OthelloGUI(root=root)
    app.mainloop()

if __name__ == "__main__":
    main()