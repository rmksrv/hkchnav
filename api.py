import os
import re
import colorama as cr
from requests import get


class Gist:
    def __init__(self):
        self.request_url_template = None
        self.request_url = None

    def get(self):
        return get(self.request_url).json()

    def cout(self):
        print('Gist from \'{}\''.format(self.request_url))

    def parse_html(self, src):
        res = src
        res = re.sub('\<\/a\>', cr.Fore.RESET, res)
        #res = re.sub(r'\<a .*\S\>', cr.Fore.CYAN + '<aga>' , res)
        res = re.sub('<br>', '\n' , res)
        return res


class Attachment(Gist):
    def __init__(self, path):
        super().__init__()
        self.request_url_template = 'https://2ch.hk{}'
        self.request_url = self.request_url_template.format(path)

    def get(self):
        if get(self.request_url):
            return self.request_url
        else:
            return None

    def cout(self):
        print('Att. {co}{link}{cc}'.format(
            co=cr.Fore.CYAN,
            cc=cr.Fore.RESET,
            link=self.get(),
        ))


class Post(Gist):
    def __init__(self, num, date, name, op, subject, comment, files):
        super().__init__()
        self.num = num
        self.date = date
        self.name = name
        self.op = op
        self.subject = subject
        self.comment = comment
        self.files = files

    def cout(self):
        print('{so}{fo}--------------------------------------------------------------------------------{sc}{fc}'.format(
            so=cr.Style.BRIGHT,
            fo=cr.Fore.BLACK,
            sc=cr.Style.RESET_ALL,
            fc=cr.Fore.RESET,
        ))
        print('{bo}{sub} - {name} {date} {num}{bc}'.format(
            sub=self.subject,
            name=self.name,
            date=self.date,
            num=self.num,
            bo=cr.Back.GREEN,
            bc=cr.Back.RESET,
        ))
        print(self.parse_html(self.comment))
        if self.files:
            print('{so}{fo}________________________________________________________________________________{sc}{fc}'.format(
                so=cr.Style.BRIGHT,
                fo=cr.Fore.BLACK,
                sc=cr.Style.RESET_ALL,
                fc=cr.Fore.RESET,
            ))
            for f in self.files:
                f.cout()


class Thread(Gist):
    def __init__(self, board, initial_post):
        super().__init__()
        self.request_url_template = 'https://2ch.hk/{b}/res/{ip}.json'
        self.request_url = self.request_url_template.format(
            b=board,
            ip=initial_post,
        )

    def cout(self):
        jsn = self.get()
        print('{fo}{bo}/{code}/ - {board}{fc}{bc}'.format(
            code=jsn['Board'],
            board=jsn['BoardName'],
            fo=cr.Fore.BLACK,
            bo=cr.Back.YELLOW,
            fc=cr.Fore.RESET,
            bc=cr.Back.RESET,
        ))
        print('{fo}{so}{descr}{fc}{sc}'.format(
            descr=jsn['BoardInfoOuter'],
            fo=cr.Fore.YELLOW,
            so=cr.Style.BRIGHT,
            fc=cr.Fore.RESET,
            sc=cr.Style.RESET_ALL,
        ))
        for jsn_post in jsn['threads'][0]['posts']:
            post = Post(
                num=jsn_post['num'],
                date=jsn_post['date'],
                name=jsn_post['name'],
                op=jsn_post['op'],
                subject=jsn_post['subject'],
                comment=jsn_post['comment'],
                files=[Attachment(f['path']) for f in jsn_post['files']]
            )
            post.cout()


class Board(Gist):
    def __init__(self, code):
        super().__init__()
        self.request_url_template = 'https://2ch.hk/{c}/{{}}.json'.format(c=code)

    def get(self, page='0'):
        page_url = 'index' if page == '0' else page
        self.request_url = self.request_url_template.format(page_url)
        return super().get()

    def cout(self, page='0'):
        jsn = self.get(page)
        print('{fo}{bo}/{code}/ - {board}{fc}{bc}'.format(
            code=jsn['Board'],
            board=jsn['BoardName'],
            fo=cr.Fore.BLACK,
            bo=cr.Back.YELLOW,
            fc=cr.Fore.RESET,
            bc=cr.Back.RESET,
        ))
        print('{fo}{so}{descr}{fc}{sc}'.format(
            descr=jsn['BoardInfoOuter'],
            fo=cr.Fore.YELLOW,
            so=cr.Style.BRIGHT,
            fc=cr.Fore.RESET,
            sc=cr.Style.RESET_ALL,
        ))
        for jsn_thread in jsn['threads']:
            print('{bo_num}{fo_num}{num}{bo_sub}{fo_sub}\t- {sub} - {fo_descr}{descr}... {fo_date}{so_date}-- {date}{sc}{fc}{bc}'.format(
                num=jsn_thread['posts'][0]['num'],
                sub=jsn_thread['posts'][0]['subject'],
                date=jsn_thread['posts'][0]['date'],
                descr=jsn_thread['posts'][0]['comment'][:60],
                fo_num=cr.Fore.BLACK,
                bo_num=cr.Back.CYAN,
                fo_sub=cr.Fore.CYAN,
                bo_sub=cr.Back.RESET,
                fo_date=cr.Fore.BLACK,
                so_date=cr.Style.BRIGHT,
                fo_descr=cr.Fore.RESET,
                fc=cr.Fore.RESET,
                sc=cr.Style.RESET_ALL,
                bc=cr.Back.RESET,
            ))


class MainPage(Gist):
    def __init__(self):
        super().__init__()
        self.request_url_template = self.request_url = 'https://2ch.hk/makaba/mobile.fcgi?task=get_boards'

    def cout(self):
        jsn = self.get()
        print('{bo}{fo}Двач{bc}{fc}'.format(
            bo=cr.Back.YELLOW,
            fo=cr.Fore.BLACK,
            fc=cr.Fore.RESET,
            bc=cr.Style.RESET_ALL,
        ))
        print('{so}{fo}--------------------------------------------------------------------------------{sc}{fc}'.format(
            so=cr.Style.BRIGHT,
            fo=cr.Fore.BLACK,
            fc=cr.Fore.RESET,
            sc=cr.Style.RESET_ALL,
        ))
        for category in jsn:
            print('{so}{cat}{sc}'.format(
                cat=category,
                so=cr.Style.BRIGHT,
                sc=cr.Style.RESET_ALL,
            ))
            for board in jsn[category]:
                #print(board)
                print('\t{fo}{id} - {name}{fc}'.format(
                    id=board['id'],
                    name=board['name'],
                    fo=cr.Fore.CYAN,
                    fc=cr.Fore.RESET,
                ))


class Navigator:
    def __init__(self):
        self.current_pos = '/'

    def goto(self, dst='/'):
        board, page, thread = self.parse_dest(dst)
        print(board, page, thread)
        if dst == 'q':
            return 0
        else:
            if board:
                if thread:
                    th = Thread(board, thread)
                    th.cout()
                else:
                    bd = Board(board)
                    bd.cout(page)
            else:
                mp = MainPage()
                mp.cout()
            return 1

    def parse_dest(self, dst):
        board = page = thread = None
        splitted_dst = list(filter(lambda a: a != '', dst.split('/')))
        if len(splitted_dst) != 0:
            foo = splitted_dst[0].split('-')
            board = foo[0]
            page = foo[1] if len(foo) > 1 else '0'
            if len(splitted_dst) == 2:
                thread = splitted_dst[1]
        return board, page, thread

    def run_nav(self):
        dst = '/'
        while self.goto(dst) != 0:
            dst = input('> ')


if __name__ == '__main__':
    cr.init()
    my_nav = Navigator()
    my_nav.run_nav()
