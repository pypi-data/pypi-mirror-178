# -*- coding: utf-8 -*-
from atelier.sphinxconf import configure ; configure(globals())
from lino.sphinxcontrib import configure
configure(globals(), 'lino_welfare.projects.gerd.settings.doctests')
project = "Lino Welfare"
import datetime
copyright = '2012-{} Rumma & Ko Ltd'.format(datetime.date.today().year)
extensions += ['lino.sphinxcontrib.logo']
# autodoc_default_options = {'members': None}
html_title = "Lino Welfare"
# html_context.update(public_url='https://welfare.lino-framework.org')

from rstgen.sphinxconf import interproject
interproject.configure(
    globals(), 'lino_welfare getlino',
    # cg=('https://community.lino-framework.org/', None),
    # hg=('https://hosting.lino-framework.org/', None),
    # ug=('https://using.lino-framework.org/', None),
    django=('https://docs.djangoproject.com/en/4.1/', 'https://docs.djangoproject.com/en/dev/_objects/'),
    sphinx=('https://www.sphinx-doc.org/en/master/', None))

extensions += ['lino.sphinxcontrib.help_texts_extractor']
help_texts_builder_targets = {
    # 'lino.': 'lino.modlib.lino_startup',
    'lino_welfare.': 'lino_welfare.modlib.welfare',
    'lino_welcht.': 'lino_welcht',
    'lino_weleup.': 'lino_weleup',
}
