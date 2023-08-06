from ._pdf import PdfFile
from ._csv import CsvFile
from ._docx import DocxFile


class FileGenerator:
	@staticmethod
	def generate_pdf() -> PdfFile:
		return PdfFile()

	@staticmethod
	def generate_csv() -> CsvFile:
		return CsvFile()

	@staticmethod
	def generate_docx() -> DocxFile:
		return DocxFile()
