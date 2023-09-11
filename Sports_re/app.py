from re import S, T
from flask import Flask
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from PIL import ImageTk, Image
from functools import partial
import time
import datetime as dt
app = Flask(__name__)

class Application(tk.Frame):
    def __init__(self, master=None): #masterにはNoneをデフォルト値を設定する。
        super().__init__(master) #引数のウィンドウを作成する。
        
        master.title('アプリメイン画面')
        master.geometry('400x600')
        
        self.elapse = 0
        self.after_id = 0
        
        self.sports = ('陸上', 'サッカー', '野球')
        self.gender = ('男', '女', 'その他')
        self.d_hand = ('右', '左', '両')
     
###スポーツに関する変数の設定----------------------------------------------------------------------------------------------------------
        self.sports_index = 0
        
#陸上の競技に関する変数-------------------------------------------------------------------------------------------------
        
        self.tandf = ('短距離', 
                      '中距離',
                      '長距離',
                      'ハードル',
                      '跳躍',
                      '投擲',
                      '競歩')
        
        self.tandf_cat = (('100m', '200m', '400m'), #短距離 
                         ('800m', '1000m', '1500m', '1マイル', '2km', '3km'), #中距離 
                         ('5km', '10km', 'ハーフ', 'フル', '100km'), #長距離
                         ('100mハードル', '110mハードル', '400mハードル'), #ハードル 
                         ('走り幅跳び', '走り高跳び', '棒高跳び', '三段跳び'), #跳躍
                         ('砲丸投', '円盤投', 'ハンマー投', 'やり投'), #投擲
                         ('10km競歩', '20km競歩', '30km競歩', '50km競歩') #競歩
                         )
        self.tandf_l = (3, #短距離
                        6, #中距離
                        5, #長距離
                        3, #ハードル
                        4, #跳躍
                        4, #投擲
                        4  #競歩
                        )
        self.tandf_index = 0
#-----------------------------------------------------------------------------------------------------------------------

#サッカーのポジションに関する変数---------------------------------------------------------------------------------------

        self.soccer = ('FW',
                       'MF',
                       'DF',
                       'GK')
        
        self.soccer_pos = (('CF', 'ST', 'CF'), #FW
                          ('OMF', 'SMF', 'CMF', 'WB', 'DMF'), #MF
                          ('CB', 'SB', 'SW'), #DF
                          ('GK') #GK
                          )
        self.soccer_l = (3, #FW
                         5, #MF
                         3, #DF
                         1  #GK
                         )
        
        self.soccer_index = 0
#------------------------------------------------------------------------------------------------------------------------
        
#野球のポジションに関する変数--------------------------------------------------------------------------------------------
        
        self.bball = ('pitching', 
                      'batting')
   
        self.bball_pandb = (('ファスト', 'スピン', 'チェンジアップ', 'その他'),
                            ('右', '左'))
        
        self.bball_l = (4, #pitching
                        2  #batting
                        )
        
        self.bball_pitch = (('フォーシーム', 'ツーシーム', 'カット',  'スプリット'), #ファスト
                            ('スライダー', 'カーブ', 'シュート', 'シンカー'), #スピン
                            ('チェンジアップ', 'フォーク', 'パーム'), #チェンジアップ
                            ('ナックル', 'スロー', 'ジャイロ') #その他
                            )
        
        self.bball_pitch_l = (4, #ファスト
                              4, #スピン
                              3, #チェンジアップ
                              3  #その他
                              )
        
        self.bball_bat = ('ミート', 'パワー', 'スピード', 'バランス', 'ディフェンス')
        
        self.bball_bat_l = 5
        
        self.bball_pitch_index = 0
        self.bball_bat_index = 0
        self.bball_index = 0
#------------------------------------------------------------------------------------------------------------------------
###------------------------------------------------------------------------------------------------------------------------------------

#プロフィールに関する変数------------------------------------------------------------------------------------------------
        #名前, スポーツ, 性別, 年齢(歳, 月), 身長, 体重, 利き手(足)
        self.profile = ('佐藤太一', '陸上', '男', 19, 7, 173, 67, '右')
        #生年月日
        self.birth = '20040202'
        #フォロー, フォロワー
        self.follow = (161, 132)
        
        self.nm, self.sp, self.gd, self.agy, self.agm, self.ht, self.wt, self.dh = self.profile
        self.fw, self.fwr = self.follow
#-------------------------------------------------------------------------------------------------------------------------

        self.pack()
        

###初期画面の部品---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #大元のフレーム
        self.mainFrame = tk.Frame(self.master, width=400, height=600, bg='#FFFF00')
        self.mainFrame.place(x=0, y=0)
        #プロフィール欄用のフレーム
        self.pFrame = tk.Frame(self.master, width=400, height=600, bg='#FFFF00')
        self.canvas_bg = tk.Canvas(self.pFrame, width=400, height=600, bg='#FFFF00')
        self.canvas_bg.place(x=0, y=0)
        
        #プロフィール画面に飛ぶプロフィール画像アイコン
        self.profile_btn_image = Image.open('profile_icon.png') #画像ファイルを選択する時、拡張子を付けるのを忘れずに。tk.PhotoImageは限定的な拡張子でしかできないので２行使うがこの方法の方が良い。
        self.pf_b_img = ImageTk.PhotoImage(self.profile_btn_image, master=self.master)
        self.profile_btn = tk.Button(self.mainFrame, image=self.pf_b_img, command=self.m1_btn_clicked)
        self.profile_btn.place(x=0, y=0)
        #self.canvas_bg.create_image(10, 10, anchor=tk.NW, image=self.pf_b_img, tag='pf_btn_img', state=tk.HIDDEN)
        #self.canvas_bg.tag_bind('pf_btn_img', '<Button-1>', self.m1_btn_clicked) #tag名を指定する時、間違ってオブジェクト名を指定しない用に注意しよう。
        
        #公式/フォロワーの情報⇔練習メニュー⇔試合・解説動画⇔選手一覧ページを切り替えるためのボタン
        self.practice_btn = tk.Button(self.mainFrame, width=6, height=1, text='練習', bg='#FF00FF', fg='#FFFF00')
       
        #練習検索ページ
        self.practice_page = tk.Frame(self.mainFrame, width=300, height=500, bg='#696969')
        
        #練習検索ページを開いてスポーツを選択するためのボタン
        self.sports_btn = [tk.Button(self.practice_page, width=6, height=1, bg='#FFFF00', fg='#FF00FF', text=s_text, command=partial(self.sports_btn_clicked, i)) for i, s_text in enumerate(self.sports)]#commandでの関数に引数を渡す場合、partialを使ったほうが良い。
        [self.sports_btn[i].place(x=0, y=i*40) for i in range(len(self.sports))]
        
        #競技orポジションを選択する画面。内包表記で複数のフレームを同時に作成する。
        self.cbtn_frame = [tk.Frame(self.practice_page, width=230, height=500, bg='#c0c0c0', relief=tk.RIDGE) for x in self.sports]
          
#陸上----------------------------------------------------------------------------------------------------------------------------------------------------------------
        #陸上の競技を選ぶチェックボタン
        self.tandf_cat_chbtn = [[] for i in range(len(self.tandf))]
        for i, c in enumerate(self.tandf_cat):
            for j, cat_t in enumerate(c):
                self.tandf_cat_chbtn[i].append(tk.Checkbutton(self.cbtn_frame[0], text=cat_t))
            
        #陸上の競技の種類を選ぶボタン
        self.tandf_btn = [tk.Button(self.cbtn_frame[0], width=6, height=1, bg='#FFFF00', fg='#FF00FF', text=c_text, command=partial(self.tandf_btn_clicked, i)) for i, c_text in enumerate(self.tandf)]
        [self.tandf_btn[i].place(x=0, y=i*40) for i in range(len(self.tandf))]
            
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#サッカー------------------------------------------------------------------------------------------------------------------------------------------------------------
        #サッカーのポジションを選ぶチェックボタン
        self.soccer_pos_chbtn = [[] for i in range(len(self.soccer))]
        for i, p in enumerate(self.soccer_pos):
            for j, pos_t in enumerate(p):
                self.soccer_pos_chbtn[i].append(tk.Checkbutton(self.cbtn_frame[1], text=pos_t))
            
        #サッカーのポジションの種類を選ぶボタン
        self.soccer_btn = [tk.Button(self.cbtn_frame[1], width=6, height=1, bg='#FFFF00', fg='#FF00FF', text=p_text, command=partial(self.soccer_btn_clicked, i)) for i, p_text in enumerate(self.soccer)]
        [self.soccer_btn[i].place(x=0, y=i*40) for i in range(len(self.soccer))]
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#野球-----------------------------------------------------------------------------------------------------------------------------------------------------------------
        #球種を細かく分割したものを選ぶボタン
        self.bball_pitch_chbtn = [[] for i in range(self.bball_l[0])]
        for i, p in enumerate(self.bball_pitch):
            for pitch_t in p:
                self.bball_pitch_chbtn[i].append(tk.Checkbutton(self.cbtn_frame[2], text=pitch_t))
                
        #打ち方を細かく分割したものを選ぶボタン
        self.bball_bat_chbtn = [[] for i in range(self.bball_l[1])]
        for i in range(self.bball_l[1]):
            for type_t in self.bball_bat:
                self.bball_bat_chbtn[i].append(tk.Checkbutton(self.cbtn_frame[2], text=self.bball_pandb[1][i]+'・'+type_t))
        
        #野球の球種・打ち方を選ぶチェックボタン
        self.bball_pandb_btn = [[] for i in range(len(self.bball))]
        for i, p in enumerate(self.bball_pandb):
            for j, pandb_t in enumerate(p):
                self.bball_pandb_btn[i].append(tk.Button(self.cbtn_frame[2], text=pandb_t, bg='#FFFF00', fg='#FF00FF', command=partial(self.bball_pitch_btn_clicked, i, j)))

        #野球の投打を選ぶ画面
        self.bball_btn = [tk.Button(self.cbtn_frame[2], width=6, height=1, bg='#FFFF00', fg='#FF00FF', text=p_text, command=partial(self.bball_btn_clicked, i)) for i, p_text in enumerate(self.bball)]
        [self.bball_btn[i].place(x=0, y=i*40) for i in range(len(self.bball))]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.create_widget()
####------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#プロフィール画面の部品----------------------------------------------------------------------------------------------------------------------------------------------------------
        #プロフィール画面の土台となる画面の作成
        self.canvas_bg.create_rectangle(0, 0, 400, 600, fill='#000000', stipple='gray50', tag='darksheet', state=tk.HIDDEN)
        self.canvas_bg.create_rectangle(-200, 0, 0, 600, fill='#FFFF00', tag='profile', state=tk.DISABLED)
        
        #戻るボタンの作成
        self.back_btn_image = Image.open('back.png').resize((20, 20))
        self.back_b_img = ImageTk.PhotoImage(self.back_btn_image, master=self.master)
        self.canvas_bg.create_image(0, 0, anchor=tk.NW, image=self.back_b_img, tag='back_btn_img', state=tk.HIDDEN)
        self.canvas_bg.tag_bind('back_btn_img', '<Button-1>', self.back_btn_clicked)
        
        #editボタンの作成
        self.edit_btn_image = Image.open('edit_icon.png').resize((20, 20))
        self.ed_b_img = ImageTk.PhotoImage(self.edit_btn_image, master=self.master)
        self.canvas_bg.create_image(140, 10, anchor=tk.NW, image=self.ed_b_img, tag='ed_btn_img', state=tk.HIDDEN)
        self.canvas_bg.tag_bind('ed_btn_img', '<Button-1>', self.ed_btn_clicked)
        
        #プロフィール写真を載せる場所の作成
        self.canvas_bg.create_image(100, 50, image=self.pf_b_img, tag='pf_icon', state=tk.HIDDEN)
        
        #スペック及びフォロー数の表示の作成
        self.canvas_bg.create_text(100, 90, anchor=tk.N, text= f'{self.nm}', justify='center', tag='nm_t', state=tk.HIDDEN)
        self.canvas_bg.create_text(100, 110, anchor=tk.N, text= f'{self.fw} フォロー    {self.fwr} フォロワー', justify='center', tag='fw_t', state=tk.HIDDEN)
        self.canvas_bg.create_text(100, 200,  anchor=tk.N, text=f'スポーツ: {self.sp}', font=('', 15), tag='sp_t',state=tk.HIDDEN)
        self.canvas_bg.create_text(100, 240, anchor=tk.N, text=f'性別: {self.gd}\n\n年齢: {self.agy} 歳 {self.agm} ヶ月\n\n身長: {self.ht} cm\n\n体重: {self.wt} kg\n\n利き手: {self.dh}', tag='spec_t', state=tk.HIDDEN)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#エディット画面の作成-------------------------------------------------------------------------------------------------------------------------------------------------------------
        #エディット画面の土台となる画面の作成
        self.canvas_bg.create_rectangle(0, 0, 200, 600, fill='#FFFF00', tag='ed_profile', state=tk.HIDDEN)
        
        #一番上に表示するエラー文の作成
        self.errorLabel = tk.Label(self.canvas_bg, text='不正な入力があります！', fg='#FF0000')
        
        #決定ボタンの作成
        self.enterBtn = tk.Button(self.canvas_bg, width=6, height=1, text='決定', state='disabled', command=self.enter_btn_clicked)
        
        #プロフィール画像を編集する場所の作成
        self.canvas_bg.create_image(100, 50, anchor=tk.N, image=self.pf_b_img, tag='pf_ed_icon', state=tk.HIDDEN)
        self.canvas_bg.tag_bind('pf_ed_icon', '<Button-1>', self.profile_img_clicked)
        
        #名前を入力するテキストボックス
        self.nm_label = tk.Label(self.canvas_bg, text='名前')
        self.nm_tbox = tk.Entry(self.canvas_bg, width=10)
        self.nm_tbox.insert(0, self.nm)
        
        #スポーツを選択するコンボボックス
        self.sp_label = tk.Label(self.canvas_bg, text='スポーツ')
        self.sp_cbox = ttk.Combobox(self.canvas_bg, width=10, state='readonly', values=self.sports)
        self.sp_cbox.set(self.sp)
        
        #性別を選択するコンボボックス
        self.gd_label = tk.Label(self.canvas_bg, text='性別')
        self.gd_cbox = ttk.Combobox(self.canvas_bg, width=5, state='readonly', values=self.gender)
        self.gd_cbox.set(self.gd)
        
        #生年月日を選択するテキストボックス
        tcl_bEV = self.register(self.birthEntryValidate)
        self.bd_label = tk.Label(self.canvas_bg, text='生年月日')
        self.bd_tbox = tk.Entry(self.canvas_bg, width=14, validate='key', validatecommand=(tcl_bEV, '%P'))
        self.bd_tbox.insert(0, self.birth)
        
        #身長を入力するテキストボックス
        tcl_hEV = self.register(self.heightEntryValidate)
        self.ht_label = tk.Label(self.canvas_bg, text='身長 (cm)')
        self.ht_tbox = tk.Entry(self.canvas_bg, width = 4, validate='key', validatecommand=(tcl_hEV, '%P'))
        self.ht_tbox.insert(0, self.ht)
        
        #体重を入力するテキストボックス
        tcl_wEV = self.register(self.weightEntryValidate)
        self.wt_label = tk.Label(self.canvas_bg, text='体重 (kg)')
        self.wt_tbox = tk.Entry(self.canvas_bg, width = 4, validate='key', validatecommand=(tcl_wEV, '%P'))
        self.wt_tbox.insert(0, self.wt)
        
        #利き手を選択するコンボボックス
        self.dh_label = tk.Label(self.canvas_bg, text='利き手')
        self.dh_cbox = ttk.Combobox(self.canvas_bg, width=3, state='readonly', values=self.d_hand)
        self.dh_cbox.set(self.dh)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_widget(self):
        
        self.mainFrame.place(x=0, y=0)
        
        self.practice_page.place(x=100, y=100)
        
        self.practice_btn.place(x=100, y=100, anchor=tk.SW)
        
        self.canvas_bg.itemconfigure('pf_btn_img', state='normal')
        
    def m1_btn_clicked(self): 
        self.pFrame.place(x=0, y=0)
        #プロフィール画面の土台の表示
        self.canvas_bg.itemconfigure('darksheet', state='normal')
        self.canvas_bg.itemconfigure('profile', state='normal')
        
        #戻るボタンの表示
        self.canvas_bg.itemconfigure('back_btn_img', state='normal')
        
        #プロフィール画面の出現処理を行う。
        self.canvas_bg.after(3, self.move, 5)
        
        #editボタンを表示
        self.canvas_bg.itemconfigure('ed_btn_img', state='normal')
        
        #プロフィール写真を載せる場所の表示
        self.canvas_bg.itemconfigure('pf_icon', state='normal')
        
        #スペック及びフォロー数の文の表示
        self.canvas_bg.itemconfigure('nm_t', state='normal')
        self.canvas_bg.itemconfigure('fw_t', state='normal')
        self.canvas_bg.itemconfigure('sp_t', state='normal')
        self.canvas_bg.itemconfigure('spec_t', state='normal')
    
    #スポーツを選択した時の処理
    def sports_btn_clicked(self, i):
        self.sports_btn[self.sports_index].configure(bg='#FFFF00', fg='#FF00FF')
        self.cbtn_frame[self.sports_index].place_forget()
        self.cbtn_frame[i].place(x=70, y=0)
        self.sports_btn[i].configure(bg='#FF00FF', fg='#FFFF00')
        self.sports_index = i
        
    #陸上の競技の種類を選んだ時の処理
    def tandf_btn_clicked(self, i):
        self.tandf_btn[self.tandf_index].configure(bg='#FFFF00', fg='#FF00FF')
        [self.tandf_cat_chbtn[self.tandf_index][cat].place_forget() for cat in range(self.tandf_l[self.tandf_index])]
        [self.tandf_cat_chbtn[i][cat].place(x=60, y=cat*40) for cat in range(self.tandf_l[i])]
        self.tandf_btn[i].configure(bg='#FF00FF', fg='#FFFF00')
        self.tandf_index = i
    
    #サッカーのポジションの種類を選んだ時の処理
    def soccer_btn_clicked(self, i):
        self.soccer_btn[self.soccer_index].configure(bg='#FFFF00', fg='#FF00FF')
        [self.soccer_pos_chbtn[self.soccer_index][pos].place_forget() for pos in range(self.soccer_l[self.soccer_index])]
        [self.soccer_pos_chbtn[i][pos].place(x=60, y=pos*40) for pos in range(self.soccer_l[i])]
        self.soccer_btn[i].configure(bg='#FF00FF', fg='#FFFF00')
        self.soccer_index = i
        
    #野球の投打を選んだ時の処理
    def bball_btn_clicked(self, i):
        self.bball_btn[self.bball_index].configure(bg='#FFFF00', fg='#FF00FF')
        
        #投のチェックボックスを表示するとき、打で選択したボタンの色を元に戻すと共に、チェックボックスを非表示にする。
        self.bball_pandb_btn[self.bball_index][self.bball_pitch_index].configure(bg='#FFFF00', fg='#FF00FF')
        [self.bball_bat_chbtn[self.bball_bat_index][bat].place_forget() for bat in range(self.bball_bat_l)] 
        
        #打のチェックボックスを表示するとき、投で選択したボタンの色を元に戻すと共に、投のチェックボックスを非表示にする。
        [self.bball_pitch_chbtn[self.bball_pitch_index][pitch].place_forget() for pitch in range(self.bball_pitch_l[self.bball_pitch_index])] 
        
        [self.bball_pandb_btn[self.bball_index][pandb].place_forget() for pandb in range(self.bball_l[self.bball_index])]
        [self.bball_pandb_btn[i][pandb].place(x=60, y=pandb*40) for pandb in range(self.bball_l[i])]
        self.bball_btn[i].configure(bg='#FF00FF', fg='#FFFF00')
        self.bball_index = i
        
    #野球の大まかな球種or利き手を選んだ時の処理
    def bball_pitch_btn_clicked(self, i, j):
        if i == 0:
            self.bball_pandb_btn[self.bball_index][self.bball_pitch_index].configure(bg='#FFFF00', fg='#FF00FF')
            [self.bball_pitch_chbtn[self.bball_pitch_index][pitch].place_forget() for pitch in range(self.bball_pitch_l[self.bball_pitch_index])]
            [self.bball_pitch_chbtn[j][pitch].place(x=140, y=pitch*40) for pitch in range(self.bball_pitch_l[j])]
            self.bball_pandb_btn[self.bball_index][j].configure(bg='#FF00FF', fg='#FFFF00')
            self.bball_pitch_index = j
        elif i == 1:
            self.bball_pandb_btn[self.bball_index][self.bball_bat_index].configure(bg='#FFFF00', fg='#FF00FF')
            [self.bball_bat_chbtn[self.bball_bat_index][bat].place_forget() for bat in range(self.bball_bat_l)]
            [self.bball_bat_chbtn[j][bat].place(x=100, y=bat*40) for bat in range(self.bball_bat_l)]
            self.bball_pandb_btn[self.bball_index][j].configure(bg='#FF00FF', fg='#FFFF00')
            self.bball_bat_index = j
            
        
    #プロフィール画面にある戻るボタンを押したときの処理
    def back_btn_clicked(self, event):
        
        #プロフィール画面を閉じる処理を行う。
        self.canvas_bg.after(3, self.move, -5)
        
        #editボタンを非表示
        self.canvas_bg.itemconfigure('ed_btn_img', state='hidden')
        
        #プロフィール写真を載せる場所を非表示
        self.canvas_bg.itemconfigure('pf_icon', state='hidden')
        
        #スペック及びフォロー数の文を非表示
        self.canvas_bg.itemconfigure('nm_t', state='hidden')
        self.canvas_bg.itemconfigure('fw_t', state='hidden')
        self.canvas_bg.itemconfigure('sp_t', state='hidden')
        self.canvas_bg.itemconfigure('spec_t', state='hidden')
        
        #プロフィール画面の土台を非表示
        self.canvas_bg.itemconfigure('darksheet', state='hidden')
        self.canvas_bg.itemconfigure('profile', state='disabled')
        
        #戻るボタンを非表示
        self.canvas_bg.itemconfigure('back_btn_img', state='hidden')
        
        self.pFrame.place_forget()
    def ed_btn_clicked(self, event):
        
        #戻るボタンを非表示
        self.canvas_bg.itemconfigure('back_btn_img', state='hidden')
        
        #エディット画面の表示
        self.canvas_bg.itemconfigure('ed_profile', state='normal')
        
        #決定ボタンの表示
        self.enterBtn.place(x=100, y=500, anchor=tk.N)
        
        #プロフィール画像を編集する場所の表示
        self.canvas_bg.itemconfigure('pf_ed_icon', state='normal')
        
        #名前の入力欄の表示
        self.nm_label.place(x=100, y=120, anchor=tk.N)
        self.nm_tbox.place(x=100, y=140, anchor=tk.N)
        
        #スポーツを選ぶコンボボックスの表示
        self.sp_label.place(x=100, y=170, anchor=tk.N)
        self.sp_cbox.place(x=100, y=190, anchor=tk.N)
        
        #性別を選ぶコンボボックスの表示
        self.gd_label.place(x=100, y=220, anchor=tk.N)
        self.gd_cbox.place(x=100, y=240, anchor=tk.N)
        
        #生年月日の入力欄の表示
        self.bd_label.place(x=100, y=270, anchor=tk.N)
        self.bd_tbox.place(x=100, y=290, anchor=tk.N)
        
        #身長の入力欄の表示
        self.ht_label.place(x=100, y=320, anchor=tk.N)
        self.ht_tbox.place(x=100, y=340, anchor=tk.N)
        
        #体重の入力欄の表示
        self.wt_label.place(x=100, y=370, anchor=tk.N)
        self.wt_tbox.place(x=100, y=390, anchor=tk.N)       

        #利き手を選ぶコンボボックスの表示
        self.dh_label.place(x=100, y=420, anchor=tk.N)
        self.dh_cbox.place(x=100, y=440, anchor=tk.N)
        
    def birthEntryValidate(self, P):
        if len(P) == 8 and P.isdecimal():
            self.enterBtn['state'] = 'normal'
            self.bd_label['text'] = '生年月日'
            self.bd_label['fg'] = '#000000'
        else:
            self.enterBtn['state'] = 'disabled'
            self.bd_label['text'] = '生年月日の入力値はyyyymmddです。'
            self.bd_label['fg'] = '#FF0000'
        return True
    
    def heightEntryValidate(self, P):
        if 2 <= len(P) < 4 and P.isdecimal():
            self.enterBtn['state'] = 'normal'
            self.ht_label['text'] = '身長 (cm)'
            self.ht_label['fg'] = '#000000'
        else:
            self.enterBtn['state'] = 'disabled'
            self.ht_label['text'] = 'あり得ない身長が入力されてます。'
            self.ht_label['fg'] = '#FF0000'
        return True
    
    def weightEntryValidate(self, P):
        if 0 < len(P) < 4 and P.isdecimal():
            self.enterBtn['state'] = 'normal'          
            self.wt_label['text'] = '体重 (kg)'
            self.wt_label['fg'] = '#000000'
        else:
            self.enterBtn['state'] = 'disabled'
            self.wt_label['text'] = 'あり得ない体重が入力されてます。'
            self.wt_label['fg'] = '#FF0000'
        return True        
    
    #プロフィール画像を変更するための関数
    def profile_img_clicked(self, event): 
        
        #ファイルのパスを得る。
        file_path = fd.askopenfilename() 
        
        if len(file_path) != 0:
            self.profile_btn_image = Image.open(file_path).resize((60, 60)) #画像ファイルを選択する時、拡張子を付けるのを忘れずに。tk.PhotoImageは限定的な拡張子でしかできないので２行使うがこの方法の方が良い。
            self.pf_b_img = ImageTk.PhotoImage(self.profile_btn_image, master=self.master)
            [self.canvas_bg.itemconfigure(t, image=self.pf_b_img) for t in ('pf_btn_img', 'pf_icon', 'pf_ed_icon')]
    
    def enter_btn_clicked(self):
        ymd = self.bd_tbox.get()
        try:
            y, m, d = int(ymd[0:4]), int(ymd[4:6]), int(ymd[6:8])
            #生年月日に入力した文字列が正当な時間を示すかを調べる。
            dt.datetime(y, m, d)
            #現在のローカル時間を取得する。
            dt_now = dt.datetime.now()
      
            #年齢を取得する。
            self.agm = dt_now.month - m
            self.agy = dt_now.year - y
            
            if dt_now.day - d < 0:
                self.agm -= 1
            if self.agm < 0:
                self.agm = 12 + self.agm
                self.agy -= 1
            if self.agy < 0:
                self.bd_label['text'] = '生年月日が現在の時刻以降です。'
                self.bd_label['fg'] = '#FF0000'
                raise Exception()
            
            #値を取得する
            self.get_profile()
            
            #プロフィール画面の編集
            self.edit_profile()
            
            #エディット画面を非表示
            self.erase_edit()
            
            #戻るボタンの有効化
            self.canvas_bg.itemconfigure('back_btn_img', state='normal')
            
        except:
            self.errorLabel.place(x=100, y=60, anchor=tk.N)
        
    def edit_profile(self):
        self.canvas_bg.itemconfigure('nm_t', text=f'{self.nm}')
        self.canvas_bg.itemconfigure('sp_t', text=f'スポーツ: {self.sp}')
        self.canvas_bg.itemconfigure('spec_t', text=f'性別: {self.gd}\n\n年齢: {self.agy} 歳 {self.agm} ヶ月\n\n身長: {self.ht} cm\n\n体重: {self.wt} kg\n\n利き手: {self.dh}')
        
    def get_profile(self):
        self.nm = self.nm_tbox.get()
        self.sp = self.sp_cbox.get()
        self.gd = self.gd_cbox.get()
        self.ht = int(self.ht_tbox.get())
        self.wt = int(self.wt_tbox.get())
        self.dh = self.dh_cbox.get()
        
    def erase_edit(self):
        #エディット画面を非表示
        self.canvas_bg.itemconfigure('ed_profile', state='hidden')
        
        #一番上にあるエラー文の消去
        self.errorLabel.place_forget()
            
        #決定ボタンを非表示
        self.enterBtn.place_forget()
        
        #プロフィール画像を編集する場所を非表示
        self.canvas_bg.itemconfigure('pf_ed_icon', state='hidden')
        
        #名前の入力欄を非表示
        self.nm_label.place_forget()
        self.nm_tbox.place_forget()
        
        #スポーツを選ぶコンボボックスを非表示
        self.sp_label.place_forget()
        self.sp_cbox.place_forget()
        
        #性別を選ぶコンボボックスを非表示
        self.gd_label.place_forget()
        self.gd_cbox.place_forget()
        
        #生年月日の入力欄を非表示
        self.bd_label.place_forget()
        self.bd_tbox.place_forget()
        
        #身長の入力欄を非表示
        self.ht_label.place_forget()
        self.ht_tbox.place_forget()
        
        #体重の入力欄を非表示
        self.wt_label.place_forget()
        self.wt_tbox.place_forget()     

        #利き手を選ぶコンボボックスを非表示
        self.dh_label.place_forget()
        self.dh_cbox.place_forget()
        
    def move(self, velocity): #afterで少し待ってから画像を動かしていくことであたかも画面を動かしているように見せられる。
        self.elapse += 1
        self.canvas_bg.move('profile', velocity, 0)
        self.canvas_bg.move('back_btn_img', velocity, 0)
        self.after_id = self.canvas_bg.after(3, self.move, velocity)
        if self.elapse == 40:
            self.elapse = 0
            self.canvas_bg.after_cancel(self.after_id)

@app.route('/')
def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    return "Hello World!"

if __name__ == '__main__':
    app.run()
