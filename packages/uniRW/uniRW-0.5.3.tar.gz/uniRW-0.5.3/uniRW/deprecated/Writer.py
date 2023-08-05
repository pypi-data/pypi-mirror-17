from __future__ import absolute_import
from __future__ import print_function

from uniRW.Value import GeneralValue
from uniRW.deprecated.Key import GeneralKey


class Writer:

    def __init__(self, KeyValues):
        self.KeyValues = KeyValues

    def write(self, out_file, key_val_dict, mode='w', sort_by=None, reverse=False):
        output = open(out_file.file_name, mode)
        header_line = out_file.line.get_line(out_file.header)
        for foreword_line in out_file.foreword:
            print(foreword_line, file=output)
        print(header_line, file=output, end='')

        if sort_by==None:
            sorted_items = sorted(key_val_dict.items(), reverse=reverse)
        elif sort_by=='key':
            sorted_items = sorted(key_val_dict.items(), key= lambda kv: kv[0], reverse=reverse)
        else:
            sorted_items = sorted(key_val_dict.items(), key= lambda kv: kv[1][sort_by], reverse=reverse)

        for key, val_dict in sorted_items:

            values = []

            for var in self.KeyValues:
                if isinstance(var, GeneralKey):
                    values.append(var.to_string(key))
                elif isinstance(var, GeneralValue):
                    values.append(var.to_string(val_dict[var.name]))

            print(out_file.line.get_line(values), file=output, end='')

        for epilogue_line in out_file.epilogue:
            print(epilogue_line, file=output)

        output.close()
