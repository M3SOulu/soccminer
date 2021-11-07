
class Comment:
    def __init__(self):
        self.comment_text = None
        self.comment_line_no = None
        self.file_name = None

    def set_comment_file_name(self, file_name):
        self.file_name = file_name

    def set_comment_text(self, comment_text):
        self.comment_text = comment_text

    def set_comment_line_no(self, line_no):
        self.comment_line_no = line_no

    def get_comment_file_name(self):
        return self.file_name

    def get_comment_text(self):
        if self.comment_text is not None:
            return self.comment_text
        else:
            return "Warning! Unavailable/Undefined comment"

    def get_comment_line_no(self):
        if self.comment_line_no is not None:
            return self.comment_line_no
        else:
            return "Warning! Unavailable/Undefined comment line number"


class CommentInfo(Comment):
    def __init__(self):
        self.comment_level = None                # ----- can be package_level or class_level or interface_level
        self.comment_sub_level = None            # ----- can be method_level or static_block_level (applicable for either class or interface_level)
        self.comment_type = None                 # ----- can be line comment or block comment
        self.comment_category = None             # ----- can be header or nonheader (by default package level can be header)
        self.comment_sub_category = None         # ---- can be block_level or non_block_level (applicable only for non_header)
                                                 # ---- block_level inside control/exception
                                                 # ---- non_block_level preceding or succeeding control/exception/declaration/expression/others
        self.comment_sub_catg_type = None        # ---- type of block level (i.e., control/exception/construct, etc.,)
        self.comment_assoc_block_ele = None      # ---- sub_catg ele that contain the comment/other element in focus
        self.succeeding_code = None
        self.preceding_code = None
        self.succeeding_element = None           # ---- To hold the succeeding element (xml element), serves as input for succeeding cocde
        self.preceding_element = None            # ---- To hold the preceding element (xml element), serves as input for preceding code
        self.succeeding_node = None              # ---- To hold the succeeding node (tag from succeeding xml element)
        self.preceding_node = None               # ---- To hold the preceding node (tag from preceding xml element)
        self.last_element_in = None              # ---- comment located in the last line of the element
        self.first_element_in = None             # ---- comment located in the first line of the element
        self.comment_meta = None                 # ---- comment text, filename, lineno
        self.comment_preceding_parents = []
        self.comment_element = None
        self.comment_parent_identifier = None
        #self.comment_succeeding_child = []
        self.comment_trace = None

        super().__init__()

    def set_comment_parent_identifier(self, id):
        self.comment_parent_identifier = id

    def set_comment_trace(self, trace):
        self.comment_trace = trace

    def get_comment_trace(self):
        return self.comment_trace

    def get_comment_parent_identifier(self):
        return self.comment_parent_identifier

    def set_comment_element(self, comment_ele):
        self.comment_element = comment_ele

    def get_comment_element(self):
        return self.comment_element

    def append_preceding_parents(self, node):
        if type(node) == list:
            self.comment_preceding_parents.extend(node)
        else:
            self.comment_preceding_parents.append(node)

    def get_preceding_parents(self):
        return self.comment_preceding_parents

    def set_succeeding_code(self, src_cd):
        self.succeeding_code = src_cd

    def set_preceding_code(self, src_cd):
        self.preceding_code = src_cd

    def set_succeeding_node(self, node):
        self.succeeding_node = node

    def set_preceding_node(self, node):
        self.preceding_node = node

    def set_succeeding_element(self, element):
        self.succeeding_element = element

    def set_preceding_element(self, element):
        self.preceding_element = element

    def get_succeeding_code(self):
        return self.succeeding_code

    def get_preceding_code(self):
        return self.preceding_code

    def get_succeeding_element(self):
        return self.succeeding_element

    def get_preceding_element(self):
        return self.preceding_element

    def get_succeeding_node(self):
        return self.succeeding_node

    def get_preceding_node(self):
        return self.preceding_node

    def set_last_element_in(self, element):
        self.last_element_in = element

    def set_first_element_in(self, element):
        self.first_element_in = element

    def get_last_element_in(self):
        return self.last_element_in

    def get_first_element_in(self):
        return self.first_element_in

    def get_comment_sub_catg_type(self):
        return self.comment_sub_catg_type if self.comment_sub_catg_type is not None else "Warning! Unavailable/Undefined comment sub category"

    def get_comment_assoc_block_ele(self):
        return self.comment_assoc_block_ele if self.comment_assoc_block_ele is not None else "Warning! Unavailable/Undefined comment assoc block element"

    def get_comment_level(self):
        if self.comment_level is not None:
            return self.comment_level
        else:
            return "Warning! Unavailable/Undefined comment level"

    def get_comment_sub_level(self):
        if self.comment_sub_level is not None:
            return self.comment_sub_level
        else:
            return "Warning! Unavailable/Undefined comment sub level"

    def get_comment_type(self):
        if self.comment_type is not None:
            return self.comment_type
        else:
            return "Warning! Unavailable/Undefined comment type"

    def get_comment_category(self):
        if self.comment_category is not None:
            return self.comment_category
        else:
            return "Warning! Unavailable/Undefined comment category"

    def get_comment_sub_category(self):
        if self.comment_sub_category is not None:
            return self.comment_sub_category
        else:
            return "Warning! Unavailable/Undefined comment sub-category"

    #def set_preceding_comment_ele(self, comment_ele):
    #    self.preceding = comment_ele

    #def set_succeeding_comment_ele(self, comment_ele):
    #    self.succeeding = comment_ele

    def set_comment_level(self, comment_level):
        self.comment_level = comment_level

    def set_comment_sub_category_type(self, cmnt_sub_catg_type):
        self.comment_sub_catg_type = cmnt_sub_catg_type

    def set_comment_assoc_block_ele(self, cmnt_assoc_block_ele):
        self.comment_assoc_block_ele = cmnt_assoc_block_ele

    def set_comment_sub_level(self, comment_sub_level):
        self.comment_sub_level = comment_sub_level

    def set_comment_type(self, comment_type):
        self.comment_type = comment_type

    def set_comment_category(self, comment_category):
        self.comment_category = comment_category

    def set_comment_sub_category(self, comment_sub_category):
        self.comment_sub_category = comment_sub_category

    def get_comment_meta(self):
        self.comment_meta = Comment()
        self.comment_meta.set_comment_file_name(self.get_comment_file_name())
        self.comment_meta.set_comment_line_no(self.get_comment_line_no())
        self.comment_meta.set_comment_text(self.get_comment_text())
        return self.comment_meta

