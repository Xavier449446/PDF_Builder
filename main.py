from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate
from utils.data_operations import get_data
from utils.page_components import (all_components, TOP_MARGIN, BOTTOM_MARGIN, RIGHT_MARGIN,
                                   LEFT_MARGIN, PAGE_WIDTH, PAGE_HEIGHT)
from utils.UI import MyWindow
import sys


class DocBuilder:
    pdf_class = SimpleDocTemplate

    def __init__(self, datafile: str, dest_dir: str, img_loc: str):
        _, self.data_sets = get_data(datafile)
        self.dest_dir = dest_dir
        self.img_loc = img_loc

    def ready(self):
        for number, data in self.data_sets:
            builder = self.__class__.pdf_class(f"{self.dest_dir}//{number}.pdf",
                                               pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
                                               topMargin=TOP_MARGIN,
                                               rightMargin=RIGHT_MARGIN,
                                               leftMargin=LEFT_MARGIN,
                                               bottomMargin=BOTTOM_MARGIN)

            components = all_components(number, data, img_location=self.img_loc)
            builder.build(components)

        print('Generation Completed. Check the location for the documents.')


def start(source, dest, cmd, img):
    doc = DocBuilder(source, dest, img_loc=img)
    if not source.endswith(('xlsx', 'csv', 'xls')):
        raise ValueError('Unaccepted file extension.')
    if source and dest:
        cmd()
        doc.ready()
    sys.exit()


if __name__ == "__main__":
    MyWindow(end_func=start).mainloop()
