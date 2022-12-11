from flask import escape


class TextCleaner:
    @staticmethod
    def clean(text):
        return escape(text)


class TitleCleaner:
    @staticmethod
    def clean(text):
        return escape(" ".join(text.split()))
