import argparse
import subprocess


def create_wave(text, path):
    if isinstance(text, bytes):
        text = text.decode('utf-8')

    text = text.strip()
    text = text.replace('\r\n', ' ')
    text = text.replace('\n', ' ')
    text = text.encode('utf-8')

    open_jtalk = ['open_jtalk']
    mech = ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice = ['-m', '/usr/share/hts-voice/mei/mei_normal.htsvoice']
    outwav = ['-ow', path]
    cmd = open_jtalk + mech + htsvoice + outwav

    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(text)
    c.stdin.close()
    c.wait()

    return path

def play(path):
    cmd = ['aplay', path]
    subprocess.call(cmd)

def main(text, path):
    path = create_wave(text, path)
    play(path)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--text', required=True, help='発話させるテキスト')
    ap.add_argument('-p', '--path', default='/tmp/jtalk.wav',
            help='作成する音声ファイルへのパス')
    args = vars(ap.parse_args())

    main(args['text'], args['path'])
