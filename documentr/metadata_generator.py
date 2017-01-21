import os
import fnmatch
import hashlib

from parser import ParserFactory
from document import Document
from writer import Writer


class MetadataGenerator(object):
    def __init__(self, input_path, output_path):
        self.output_path = output_path
        self.input_path = input_path

    def generate(self, engine):
        engine_parser = ParserFactory.create_parser(engine)
        file_list = self.__load_files(self.input_path)

        for file_ in file_list:
            documentr = Document(engine_parser)

            with open(file_) as buffer_:
                sql_content = buffer_.read()
                table_data = documentr.create(sql_content)

                if table_data:
                    documentr.write(Writer(self.output_path))
                    print "File [{}] {} parsed".format(
                        hashlib.md5(sql_content).hexdigest(), file_
                    )

            buffer_.close()

    def __load_files(self, input_path):
        file_list = []

        for root, dirnames, filenames in os.walk(input_path):
            for filename in fnmatch.filter(filenames, '*.sql'):
                file_list.append(os.path.join(root, filename))

        return file_list
