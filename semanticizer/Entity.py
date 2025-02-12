# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 11:51:48 2017

@author: erich
@modified by: ricardo
"""


class Entity:

    def __init__(self, text, tag, pos, start=None, end=None, type=None):
        self.text = text
        self.start = start
        self.end = end
        self.tag = tag
        self.pos = pos
        self.type = type

    def __str__(self):
        return 'text: {}, start: {}, end: {}, tag: {}, pos: {}, type: {}'.format(self.text, self.start,
                                                                                 self.end, self.tag,
                                                                                 self.pos, self.type)

    def __repr__(self):
        return self.__str__()


def exists_overlap(entity1, entity2):

    if entity1.start is not None and entity1.end is not None\
            and entity2.start is not None and entity2.end is not None:
        if entity1.start >= entity2.start and entity1.start <= entity2.end:
            return True
        elif entity1.end >= entity2.start and entity1.end <= entity2.end:
            return True
        elif entity2.start >= entity1.start and entity2.start <= entity1.end:
            return True
        elif entity2.end >= entity1.start and entity2.end <= entity1.end:
            return True
        else:
            return False
    return False


def find_new_location(entity, text):

    relative_start = entity.text.find(text)
    if relative_start != -1:
        new_start = entity.start + relative_start
        new_end = new_start + len(text)
        return new_start, new_end
    return None, None
