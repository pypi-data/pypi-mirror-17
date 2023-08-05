from html import escape

from html_processor import Processor as BaseProcessor


class Processor(BaseProcessor):

    def result(self, result):
        return '<pre>' + escape(result) + '</pre>'

    def text(self, text):
        return text
