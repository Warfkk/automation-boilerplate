import os
import os.path


class GenUnitFunc:
    """Multiple functions to interact with worbook and sub-classes in obj_lib,
    and ui.
    """

    def __init__(self, gen_main):
        self.s = gen_main.s

    def _replace_keywords(self, line, obj):
        """Take in a line and convert all the identifiers to obj data"""

        offset = self.s.OFFSET_IDENTIFIER
        offset_end = self.s.OFFSET_END_IDENTIFIER

        # Replace the keywords that always exists
        line = line.replace(self.s.ID_REPLACE, obj["id"])
        line = line.replace(self.s.TYPE_REPLACE, obj["type"])

        if obj["parent"] is not None:
            line = line.replace("@PARENT", obj["parent"])

        if obj["plc"] is not None:
            line = line.replace(self.s.PLC_REPLACE, obj["plc"])

        if obj["hmi_group"] is not None:
            line = line.replace(self.s.ALARM_GROUP_REPLACE, obj["hmi_group"])

        return line

    def _replace_offset(self, line, obj):
        offset = self.s.OFFSET_IDENTIFIER
        offset_end = self.s.OFFSET_END_IDENTIFIER

        if offset and offset_end in line:
            start_char_index = line.find(offset)  # find char offset
        else:
            print(
                f"WARNING replace offset fault identifier {offset} or {offset_end} was not found"
            )
            return line  # if not found just return line unchanged

        not_found_whole_string = True
        temp_str = line[start_char_index]
        i = start_char_index
        while not_found_whole_string:
            i += 1
            temp_str += line[i]  # add char to string

            if offset_end in temp_str:
                not_found_whole_string = False

        str_to_replace_in_line = temp_str
        temp_str = temp_str.replace(offset, "")
        temp_str = temp_str.replace(offset_end, "")
        temp_offset = int(temp_str)
        temp_offset += obj["db_offset"]

        line = line.replace(str_to_replace_in_line, str(temp_offset))

        return line

    @staticmethod
    def single(config_file, list_result, ref_txt):
        """Read a text file and copy the data inside notifiers to memory"""
        with open(config_file, "r", encoding="cp1252") as config:
            exists_in_config = False
            section_found = False
            inst_data = ""
            begin = "<" + ref_txt + ">"
            end = "</" + ref_txt + ">"

            for line in config:
                if end in str(line):
                    section_found = False
                if section_found:
                    inst_data += line
                if begin in str(line):
                    exists_in_config = True
                    section_found = True
        if not exists_in_config:
            result_ok = False
            result_msg = f"'{ref_txt}' not found in config file"
        else:
            result_ok = True
            result_msg = None

        # Return a dictionary with the result
        result = {
            "ref_txt": ref_txt,
            "type": None,
            "result_ok": result_ok,
            "bad_result_msg": result_msg,
        }

        list_result.append(result)
        return inst_data

    def single_obj(self, config_file, list_result, obj, ref_txt):
        """Read each line in a text file and replace any strings that match the ones
        states in _replace keywords"""
        with open(config_file, "r", encoding="cp1252") as config:
            exists_in_config = False
            section_found = False
            inst_data = ""
            begin = "<" + ref_txt + ">"
            end = "</" + ref_txt + ">"

            for line in config:
                if end in str(line):
                    section_found = False
                if section_found:
                    line = self._replace_keywords(line, obj)
                    inst_data += line
                if begin in str(line):
                    exists_in_config = True
                    section_found = True

        if not exists_in_config:
            result_ok = False
            result_msg = f"'{ref_txt}' not found in config file"
        else:
            result_ok = True
            result_msg = None

        if obj["parent"] is None:
            help_msg = obj["id"]
        else:
            help_msg = f"{obj['parent']}_{obj['id']}"

        result_ref_txt = f"{help_msg} ({ref_txt})"
        # Return a dictionary with the result
        result = {
            "ref_txt": result_ref_txt,
            "type": None,
            "result_ok": result_ok,
            "bad_result_msg": result_msg,
        }

        list_result.append(result)
        return inst_data

    def append_bad_result(self, bad_result_msg, list_result):
        # Return a dictionary with the result
        if self.s.debug_level > 0:
            print("\n", bad_result_msg)

        result = {
            "ref_txt": "",
            "type": None,
            "result_ok": False,
            "bad_result_msg": bad_result_msg,
        }

        list_result.append(result)

    @staticmethod
    def result(list_with_dicts, type="undefined"):
        """Check all result dicts and sum them, then print info to user"""
        result_ok_cnt = 0
        result_bad_cnt = 0
        print("\n")
        print(type)

        good_results = []  # Empty list
        bad_results = []  # Empty list

        for dict in list_with_dicts:
            if dict["result_ok"]:
                good_results.append(dict["ref_txt"])
                result_ok_cnt += 1
            else:
                msg = f"\t ERROR: {dict['bad_result_msg']}"
                bad_results.append(msg)
                result_bad_cnt += 1
        if result_ok_cnt > 0:
            tmp_text = "Succesfully processed"
            print(f"\t {tmp_text} {result_ok_cnt} objects: {good_results}")

        if result_bad_cnt > 0:
            print("\n")
            print(f"\t {result_bad_cnt} resulted with error:")
            for r in bad_results:
                print("\t", r)

        if result_ok_cnt == 0 and result_bad_cnt == 0:
            print("\t Nothing processed")
