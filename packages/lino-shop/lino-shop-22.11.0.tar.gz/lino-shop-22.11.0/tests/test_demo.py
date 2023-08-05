# how to run a single test:
# $ python -m unittest tests.test_demo.Main.test_shop1

from lino.utils.pythontest import TestCase


class Main(TestCase):

    demo_projects_root = "lino_shop/projects"

    def test_shop1(self):
        self.do_test_demo_project('shop1')
