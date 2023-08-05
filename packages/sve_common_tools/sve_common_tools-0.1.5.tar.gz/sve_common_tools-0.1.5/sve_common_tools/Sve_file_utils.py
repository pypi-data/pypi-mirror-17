# VERSION 1.0.1

class FileUtils:
    @staticmethod
    def command_to_str_array(command_output):
        outr = ''
        for out_row in command_output.splitlines():
            outr += out_row.rstrip() + '\n'
        return outr;

    @staticmethod
    def remove_before_header_string(str, header_str):
        """
            msg = \"""text text
            H1 H2 H3
            a  b  c
            d  e  f
            FOOTER xxxxx
            yyyyyyyy
            \"""
            print ">" + (x._remove_before_header_string(msg, "H1 H2 H3")) + "<"

            RISULTATO
            >a  b  c
            d  e  f
            FOOTER xxxxx
            yyyyyyyy
            <

        :param str:
        :param header_str:
        :return:
        """
        return str[str.find(header_str + '\n') + len(header_str + '\n'):]

    @staticmethod
    def remove_after_footer_string(str, footer_str):
        """
            msg = \"""text text
            H1 H2 H3
            a  b  c
            d  e  f
            FOOTER xxxxx
            yyyyyyyy
            \"""
            print ">" + (x._remove_after_footer_string(msg, "\nFOOTER")) + "<"

            RISULTATO
            >text text
            H1 H2 H3
            a  b  c
            d  e  f<

        :param str:
        :param footer_str:
        :return:
        """
        return str[:str.find(footer_str)]

    @staticmethod
    def remove_skip_rows(str, skip_str_starting_array, skip_empty_lines):
        """
            Remove lines
            msg = \"""text text
            xxxxxxxxx
            yyyyyyyyy
            zzzzzzzzz
            aaaaaaaaa

            bbbbbbbbb
            \"""
            print ">" + (x._remove_skip_rows(msg, ["xxxx", "zzzzz"], True)) + "<"

            RISULTATO
            >text text
            yyyyyyyyy
            aaaaaaaaa

            bbbbbbbbb
            <
        """
        outr = ''
        for out_row in str.splitlines():
            found = 0
            for s in skip_str_starting_array:
                if s in out_row:
                    found = 1
            if found == 0 and \
                    (not skip_empty_lines or (skip_empty_lines and out_row.rstrip() != "")):
                outr += out_row.rstrip() + '\n'
        return outr;

    @staticmethod
    def extract_block(str, starting_row, ending_row, add_ending_row):
        copy = False
        outr = ''
        for line in str.splitlines():
            line = line.rstrip()
            if line == starting_row:
                copy = True
            elif line == ending_row:
                if add_ending_row:
                    outr += line + '\n'
                copy = False

            if copy:
                outr += line + '\n'
        return outr

    @staticmethod
    def add_char_to_every_row_if_not_exist(str, character):
        str2 = ''
        for out_row in str.splitlines():
            str2 += out_row + (character if character not in out_row else '') + '\n'
        return str2

    @staticmethod
    def parse_extact_table(str, header_column_position):
        result = []
        for out_result_row in str.splitlines():
            arr = []
            for i in range(0, len(header_column_position)):
                start_pos = header_column_position[i][0]
                if header_column_position[i][1] is None:
                    if i < len(header_column_position) - 1:
                        end_pos = header_column_position[i + 1][0] - 1
                    else:
                        end_pos = len(out_result_row)
                else:
                    end_pos = header_column_position[i][1] - 1
                d = out_result_row[start_pos:end_pos].strip()
                arr.append(d)
            result.append(arr)

        if len(result) == 0:
            raise Exception('TI_Utilis', 'No param list (' + str + ')')
        return result

    @staticmethod
    def create_htmltable(command_output_array_table, html_header):
        """
           Add to output windows an HTML table with the command
        :param context:
        :param command_output:
        """
        str = '<table style="color:black" border="1" cellpadding="5">'
        str += '<thead>'
        for th in html_header:
            str += '<th>' + th + '</th>'
        str += '</thead>'
        str += '<tbody>'
        for row in command_output_array_table:
            str += '<tr>'

            for val in row:
                str += '<td>' + val + '</td>'
            str += '</tr>'
        str += '</tbody></table>'
        return str;
