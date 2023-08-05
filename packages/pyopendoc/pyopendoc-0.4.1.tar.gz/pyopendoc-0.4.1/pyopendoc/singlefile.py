#!/usr/bin/env python3
from xml.etree import ElementTree as ET
import tempfile
import imghdr

#
# Component Files
#

class SingleFileFactory():
    def load_file(self, filename, filebytes):
        if filename.endswith(".xml"):
            return SingleXMLFile(filename, filebytes)
        if imghdr.what(file=None, h=filebytes):
            return SingleImageFile(filename, filebytes)
        return SingleUnknownFile(filename, filebytes)


class SingleFile(object):
    @property
    def filetype():
        raise NotImplementedError

    def to_bytes(self):
        raise NotImplementedError


class SingleXMLFile(SingleFile):

    xmlns_str = "xmlns"

    def _parse(self, filebytes):
        tf = tempfile.TemporaryFile()
        tf.write(filebytes)
        tf.seek(0)

        events = "start", "start-ns"
        root = None
        ns_map = []

        for event, elem in ET.iterparse(tf, events):
            if event == "start-ns":
                ns_map.append(elem)
            elif event == "start":
                if root is None:
                    root = elem
                for prefix, uri in ns_map:
                    elem.set("{}:{}".format(self.xmlns_str, prefix), uri)
                ns_map = []

        tf.close()
        return ET.ElementTree(root)

    def __init__(self, filename, filebytes):
        self.filename = filename
        self.root = ET.fromstring(filebytes)

    @property
    def filetype(self):
        return "XML"

    def to_bytes(self):
        return bytes(ET.tostring(self.root))

    def new_element(self, name="new", attributes={}):
        return ET.Element(name, attributes)


class SingleImageFile(SingleFile):
    def __init__(self, filename, filebytes):
        self.filename = filename
        self.filebytes = filebytes

    @property
    def filetype(self):
        return "Image"

    def to_bytes(self):
        return self.filebytes


class SingleUnknownFile(SingleFile):
    def __init__(self, filename, filebytes):
        self.filename = filename
        self.filebytes = filebytes

    @property
    def filetype(self):
        return "Unknown"

    def to_bytes(self):
        return self.filebytes
