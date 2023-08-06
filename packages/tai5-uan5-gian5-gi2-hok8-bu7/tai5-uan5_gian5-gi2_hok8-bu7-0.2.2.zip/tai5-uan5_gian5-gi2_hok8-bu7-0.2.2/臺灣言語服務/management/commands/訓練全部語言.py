from django.core.management.base import BaseCommand
from 臺灣言語服務.模型訓練 import 模型訓練
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾


class Command(BaseCommand):
    help = '訓練全部語言的模型'

    def handle(self, *args, **參數):
        模型訓練.輸出全部語料(翻譯語料資料夾)
        模型訓練.訓練一个摩西翻譯模型(翻譯語料資料夾, 翻譯模型資料夾)
