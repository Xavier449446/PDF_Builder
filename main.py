from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate
from data_operations import get_data
from page_components import all_components
from UI import MyWindow
import sys


class DocBuilder:
    pdf_class = SimpleDocTemplate

    def __init__(self, datafile: str, dest_dir: str):
        _, self.data_sets = get_data(datafile)
        self.dest_dir = dest_dir

    def ready(self):
        for number, data in self.data_sets:
            builder = self.__class__.pdf_class(f"{self.dest_dir}//{number}.pdf", pagesize=A4, topMargin=cm / 4,
                                               rightMargin=cm, leftMargin=cm, bottomMargin=cm / 4)
            components = all_components(number, data)
            builder.build(components)
        print('Generation Completed. Check the location for the documents.')


def start(source, dest, cmd):
    doc = DocBuilder(source, dest)
    if not source.endswith(('xlsx', 'csv', 'xls')):
        raise ValueError('Unaccepted file extension.')
    if source and dest:
        cmd()
        doc.ready()
    sys.exit()


if __name__ == "__main__":
    MyWindow(end_func=start).mainloop()
