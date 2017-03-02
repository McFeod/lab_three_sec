import os

from gost94.keygen import Gost94Keygen
from gost94.eds import Gost94Prover, Gost94Verifier

from gost2001.keygen import Gost2001Keygen
from gost2001.eds import Gost2001Prover, Gost2001Verifier

from rsa.keygen import RsaKeygen
from rsa.eds import RsaProver, RsaVerifier

from demo import make_demo
from report.jinja_settings import render_template


OUT_DIR = 'out'
TEMP_FILE = 'report.tex'
OUT_FILE = 'report.pdf'


def show_report(template, context, out_dir=OUT_DIR, tex_file=TEMP_FILE, pdf_file=OUT_FILE):
    tex = render_template(template, context)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    os.chdir(out_dir)
    with open(tex_file, 'w+') as f:
        f.write(tex)
    os.system('pdflatex {}'.format(tex_file))
    os.system('evince {}'.format(pdf_file))


if __name__ == '__main__':

    context = {
        'func': {
            'str': str
        },
        'rsa': make_demo(RsaKeygen, RsaProver, RsaVerifier),
        'gost94': make_demo(Gost94Keygen, Gost94Prover, Gost94Verifier),
        'gost2001': make_demo(Gost2001Keygen, Gost2001Prover, Gost2001Verifier)
    }
    show_report('templates/main.tex', context)
