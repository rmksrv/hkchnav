import os
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
        print('Att. {c}{link}'.format(
            c=cr.Fore.CYAN,
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
        print('{s}{f}--------------------------------------------------------------------------------'.format(
            s=cr.Style.BRIGHT,
            f=cr.Fore.BLACK,
        ))
        print('{b}{sub} - {name} {date} {num}'.format(
            sub=self.subject,
            name=self.name,
            date=self.date,
            num=self.num,
            b=cr.Back.GREEN,
        ))
        print(self.comment)
        if self.files:
            print('{s}{f}________________________________________________________________________________'.format(
                s=cr.Style.BRIGHT,
                f=cr.Fore.BLACK,
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
        print('{f}{b}/{code}/ - {board}'.format(
            code=jsn['Board'],
            board=jsn['BoardName'],
            f=cr.Fore.BLACK,
            b=cr.Back.YELLOW,
        ))
        print('{f}{s}{descr}'.format(
            descr=jsn['BoardInfoOuter'],
            f=cr.Fore.YELLOW,
            s=cr.Style.BRIGHT,
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
        print('{f}{b}/{code}/ - {board}'.format(
            code=jsn['Board'],
            board=jsn['BoardName'],
            f=cr.Fore.BLACK,
            b=cr.Back.YELLOW,
        ))
        print('{f}{s}{descr}'.format(
            descr=jsn['BoardInfoOuter'],
            f=cr.Fore.YELLOW,
            s=cr.Style.BRIGHT,
        ))
        for jsn_thread in jsn['threads']:
            print('{b_num}{f_num}{num}{b_sub}{f_sub}\t- {sub} - {f_descr}{descr}... {f_date}{s_date}-- {date}'.format(
                num=jsn_thread['posts'][0]['num'],
                sub=jsn_thread['posts'][0]['subject'],
                date=jsn_thread['posts'][0]['date'],
                descr=jsn_thread['posts'][0]['comment'][:60],
                f_num=cr.Fore.BLACK,
                b_num=cr.Back.CYAN,
                f_sub=cr.Fore.CYAN,
                b_sub=cr.Back.RESET,
                f_date=cr.Fore.BLACK,
                s_date=cr.Style.BRIGHT,
                f_descr=cr.Fore.RESET,
            ))


class MainPage(Gist):
    def __init__(self):
        super().__init__()
        self.request_url_template = self.request_url = 'https://2ch.hk/makaba/mobile.fcgi?task=get_boards'

    def cout(self):
        jsn = self.get()
        print('{b}{f}Двач'.format(
            b=cr.Back.YELLOW,
            f=cr.Fore.BLACK,
        ))
        print('{s}{f}--------------------------------------------------------------------------------'.format(
            s=cr.Style.BRIGHT,
            f=cr.Fore.BLACK,
        ))
        for category in jsn:
            print('{s}{cat}'.format(
                cat=category,
                s=cr.Style.BRIGHT,
            ))
            for board in jsn[category]:
                #print(board)
                print('\t{f}{id} - {name}'.format(
                    id=board['id'],
                    name=board['name'],
                    f=cr.Fore.CYAN,
                ))


# TODO
#class Navigator:
#    def __init__(self):
#        self.current_pos =


if __name__ == '__main__':
    cr.init(autoreset=True)
    #sample_board = Board('electrach')
    #sample_board.cout()
    s = input('Select (1 - Main Page; 2 - Sample board; 3 - Sample Thread): ')
    print(s)
    if s == '1':
        sample_main_page = MainPage()
        sample_main_page.cout()
    elif s == '2':
        sample_board = Board('electrach')
        sample_board.cout()
    elif s == '3':
        sample_thread = Thread('electrach', '18140')
        sample_thread.cout()
    else:
        print('fuck ', s)

