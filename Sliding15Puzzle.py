import PySimpleGUI as sg
import random

class Sliding15Puzzle():
    def __init__(self):
        self.images = ['images/space.png',
              'images/01.png',
              'images/02.png',
              'images/03.png',
              'images/04.png',
              'images/05.png',
              'images/06.png',
              'images/07.png',
              'images/08.png',
              'images/09.png',
              'images/10.png',
              'images/11.png',
              'images/12.png',
              'images/13.png',
              'images/14.png',
              'images/15.png' ]

        # 0 - 15 をシャッフル
        self.board = [(no+1) for no in range(15)]
        self.board.append(0)
        self.shuffle()

        # 数字ボタンを作成し、二次元配列（4行 x 4列）に保持
        self.no_buttons = []
        for row in range(4):
            row_btns = []
            for col in range(4):
                # ボタンの数字を取得（シャッフルした board の値を取り出す）
                no = self.board[row * 4 + col]

                # 数字ボタンを作成。キーはタプル(行,列)
                no_button = sg.Button(image_filename = self.image_fname(no), key=(row, col))

                # 作成したボタンを1行用のリストに追加
                row_btns.append(no_button)

            # 1行の数字ボタン(4つ)を、二次元配列(4 x 4)に追加
            self.no_buttons.append(row_btns)

        # フレーム（数字ボタン（4 x 4））と「終了」ボタンでレイアウト作成
        self.layout = [ [sg.Frame('', self.no_buttons)] ] + [ [sg.Button('終了', expand_x=True)] ]

        # ウィンドウ作成
        self.window = sg.Window('スライディングパズル', self.layout)

    # メインループ
    def main_loop(self):
        while True: # Event Loop
            event, values = self.window.read()
            if event in (None, '終了'):
                # 「終了」ボタンが押下されたらループを抜ける
                break

            # イベントがタプルであれば数字ボタンが押下されたと判断する
            if type(event) is tuple:
                self.touch(event)

        # アプリ終了
        self.window.close()

    # 数字に対応する画像ファイル名を取得
    def image_fname(self, no):
        try:
            ifname = self.images[no]
        except:
            ifname = self.images[0]
        return ifname

    # 数字（0～15）をシャッフル
    # 単純にシャッフルすると、解けない配置になることがあるため
    # 「スペース」を上下左右にランダムに動かしてシャッフルする
    def shuffle(self):
        random.seed()

        # 0=スペースのidxを取得
        sp_idx = -1
        for idx in range(len(self.board)):
            if self.board[idx] == 0:
                sp_idx = idx
                break
        if sp_idx == -1:
            return

        # 「スペース」ボタンの（行, 列）
        sp_row, sp_col = divmod(sp_idx, 4)

        # 200～3000回動かす
        n_loops = random.randrange(200, 300)
        for n in range(n_loops):
            target_idx = -1
            while target_idx == -1:
                # 上下左右をランダムに決める
                direction = random.randrange(0, 99) % 4
                target_row = sp_row
                target_col = sp_col

                if direction == 0:      # 上
                    if sp_row >= 1:
                        target_row = sp_row - 1
                        target_idx = target_row * 4 + target_col

                elif direction == 1:    # 下
                    if sp_row < 3:
                        target_row = sp_row + 1
                        target_idx = target_row * 4 + target_col

                elif direction == 2:    # 左
                    if sp_col >= 1:
                        target_col = sp_col - 1
                        target_idx = target_row * 4 + target_col

                elif direction == 3:    # 右
                    if sp_col < 3:
                        target_col = sp_col + 1
                        target_idx = target_row * 4 + target_col

                if target_idx != -1:
                    # 決定した方向（上下左右）に「スペース」ボタン動かすことが可能なら動かす
                    self.board[sp_idx] = self.board[target_idx]
                    self.board[target_idx] = 0
                    sp_row = target_row
                    sp_col = target_col
                    sp_idx = sp_row * 4 + sp_col

    # 指定した位置（行, 列）を 0～15のインデックスに変換
    def pos2idx(self, pos):
        idx = pos[0] * 4 + pos[1]
        return idx

    # 指定した位置（行, 列）の数字を取得
    def pos2no(self, pos):
        return self.board[self.pos2idx(pos)]

    # 完成？
    def is_complete(self):
        ret = True
        for idx in range(len(self.board) - 1):
            if self.board[idx] != (idx + 1):
                ret = False
                break
        return ret

    # 「スペース」と「スペースに隣接する数字ボタン」を入れ替え
    def swap(self, my_pos, target_pos):
        ret = False
        sp_no = self.pos2no(target_pos)
        if sp_no == 0:
            sp_idx = self.pos2idx(target_pos)
            my_idx = self.pos2idx(my_pos)

            self.board[sp_idx] = self.board[my_idx]
            self.board[my_idx] = 0

            if self.window != None:
                self.window[my_pos].Update(image_filename = self.image_fname(0))
                self.window[target_pos].Update(image_filename = self.image_fname(self.board[sp_idx]))

            ret = True

        return ret

    # クリックした数字ボタンの上に「スペース」があれば入れ替え
    def up_swap(self, pos):
        ret = False
        (row, col) = pos
        if row >= 1:
            ret = self.swap(pos, (row - 1, col))
        return ret

    # クリックした数字ボタンの下に「スペース」があれば入れ替え
    def down_swap(self, pos):
        ret = False
        (row, col) = pos
        if row < 3:
            ret = self.swap(pos, (row + 1, col))
        return ret

    # クリックした数字ボタンの左に「スペース」があれば入れ替え
    def left_swap(self, pos):
        ret = False
        (row, col) = pos
        if col >= 1:
            ret = self.swap(pos, (row, col - 1))
        return ret

    # クリックした数字ボタンの右に「スペース」があれば入れ替え
    def right_swap(self, pos):
        ret = False
        (row, col) = pos
        if col < 3:
            ret = self.swap(pos, (row, col + 1))
        return ret

    # クリックした数字ボタンに隣接する「スペース」があれば入れ替え
    def touch(self, pos):
        no = self.pos2no(pos)
        if no == 0:
            # 「スペース」ボタン押下
            return

        if self.up_swap(pos):
            # タッチした数字ボタンの「上」がスペース
            pass
        elif self.down_swap(pos):
            # タッチした数字ボタンの「下」がスペース
            pass
        elif self.left_swap(pos):
            # タッチした数字ボタンの「左」がスペース
            pass
        elif self.right_swap(pos):
            # タッチした数字ボタンの「右」がスペース
            pass

        if self.is_complete():
            sg.popup('完成！')

# スライディングパズル作成
sp = Sliding15Puzzle()

# メインループ
sp.main_loop()

