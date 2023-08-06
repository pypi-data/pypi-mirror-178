class StringSort:

    def __init__(self, string):
        self.string = string

    def delete(self, delete):
        self.delete = delete
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if list1[i] == str(self.delete):
                list1[i] = ''
        return ''.join(list1)

    def delete_2_symbols(self, sign1, sign2):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)):
                list1[i] = ''
        return ''.join(list1)

    def delete_3_symbols(self, sign1, sign2, sign3):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)):
                list1[i] = ''
        return ''.join(list1)

    def delete_4_symbols(self, sign1, sign2, sign3, sign4):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)):
                list1[i] = ''
        return ''.join(list1)

    def delete_5_symbols(self, sign1, sign2, sign3, sign4, sign5):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)):
                list1[i] = ''
        return ''.join(list1)

    def delete_6_symbols(self, sign1, sign2, sign3, sign4, sign5, sign6):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)):
                list1[i] = ''
        return ''.join(list1)

    def delete_7_symbols(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)):
                list1[i] = ''
        return ''.join(list1)

    def delete_8_symbols(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)):
                list1[i] = ''
        return ''.join(list1)

    def delete_9_symbols(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8, sign9):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)) | (list1[i] == str(sign9)):
                list1[i] = ''
        return ''.join(list1)

    def delete_10_symbols(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8, sign9, sign10):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)) | (list1[i] == str(sign9)) | (list1[i] == str(sign10)):
                list1[i] = ''
        return ''.join(list1)

    def alphabetical_order(self):
        list1 = []
        list1.extend(self.string)
        list1.sort()
        return ''.join(list1)

    def delete_with_space(self, delete):
        self.delete = delete
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if list1[i] == str(self.delete):
                list1[i] = ' '
        return ''.join(list1)

    def delete_2_symbols_with_space(self, sign1, sign2):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)):
                list1[i] = ' '
        return ''.join(list1)

    def delete_3_symbols_with_space(self, sign1, sign2, sign3):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)):
                list1[i] = ' '
        return ''.join(list1)

    def delete_4_symbols_with_space(self, sign1, sign2, sign3, sign4):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)):
                list1[i] = ' '
        return ''.join(list1)

    def delete_5_symbols_with_space(self, sign1, sign2, sign3, sign4, sign5):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)):
                list1[i] = ' '
        return ''.join(list1)

    def delete_6_symbols_with_space(self, sign1, sign2, sign3, sign4, sign5, sign6):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)):
                list1[i] = ' '
        return ''.join(list1)

    def delete_7_symbols_with_space(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)):
                list1[i] = ' '
        return ''.join(list1)

    def delete_8_symbols_with_space(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)):
                list1[i] = ' '
        return ''.join(list1)

    def delete_9_symbols_with_space(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8, sign9):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)) | (list1[i] == str(sign9)):
                list1[i] = ' '
        return ''.join(list1)

    def delete_10_symbols_with_space(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8, sign9, sign10):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)) | (list1[i] == str(sign9)) | (list1[i] == str(sign10)):
                list1[i] = ' '
        return ''.join(list1)

    def which_one_delete(self, sing, number):
        self.sign = sing
        self.number = number
        list1 = []
        list1.extend(str(self.string))

        num = 0

        for i in range(len(list1)):
            if list1[i] == str(self.sign):
                num += 1
                if list1.count(self.sign) >= self.number:
                    if num == int(self.number):
                        list1[i] = ''
                else:
                    raise SyntaxError(f"your string '{self.string}' don't have {self.number} of '{self.sign}'")

        return ''.join(list1)

    def which_one_delete_with_space(self, sing, number):
        self.sign = sing
        self.number = number
        list1 = []
        list1.extend(str(self.string))

        num = 0

        for i in range(len(list1)):
            if list1[i] == str(self.sign):
                num += 1
                if list1.count(self.sign) >= self.number:
                    if num == int(self.number):
                        list1[i] = ' '
                else:
                    raise SyntaxError(f"your string '{self.string}' don't have {self.number} of '{self.sign}'")

        return ''.join(list1)

    def same_signs(self, search_string):
        list1 = []

        list2 = []

        list1.extend(self.string)

        list2.extend(search_string)

        list3 = []

        if len(list1) <= len(list2):
            for i in range(len(list2)):
                if list2[i] != ' ':
                    for j in list1:
                        if list2[i] == j:
                            list3.append(j)
                            list1.remove(j)
        else:
            raise SyntaxError(f"string '{list1}' is bigger than '{list2}'")

        return ', '.join(list3)