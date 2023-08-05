
class DockerArg(object):
    def __init__(self, name, val):
        self.name = name
        self.value = val

    def is_null(self):
        if self.value:
            return False
        return True

    def __str__(self):
        return self.value

class DockerOpt(object):
    def __init__(self, opt, val):
        self.opt = opt
        self.value = val

    def is_null(self):
        if self.value:
            return False
        return True

    def __str__(self):
        return '%s %s' % (self.opt, self.value)

class BoolOpt(DockerOpt):
    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    def __str__(self):
        return self.opt

class ByteValueOpt(DockerOpt):
    """ Option with one or more user-defined values """
    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    @staticmethod
    def format_bytes(x):
        KB = 1024
        MB = KB*1024
        GB = MB*1024
        x = float(x)
        if x < 1024:
            return '%sb' % round(x)
        elif 1024 <= x < MB:
            return '%sk' % round(x/KB)
        elif KB <= x < GB:
            return '%sm' % round(x/MB)
        elif GB <= x:
            return '%sg' % round(x/GB)

    def __str__(self):
        try:
            return '%s %s' % (self.opt, self.format_bytes(self.value))
        except ValueError:
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.opt, self.value))

class ValueOpt(DockerOpt):
    """ Option with one or more user-defined values """

    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    def __str__(self):
        if type(self.value) == list:
            return ' '.join([ '%s %s' % (self.opt, v) for v in self.value ])
        try:
            return '%s %s' % (self.opt, self.value)
        except ValueError:
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.opt, self.value))

class MapOpt(DockerOpt):
    """ Option with one or more user-defined mappings """
    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    def __str__(self):
        if not isinstance(self.value, dict):
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.opt, self.value))
        kvlist = [ '%s=%s' % (k,v) for k,v in self.value.items() ]
        return ' '.join([ '%s %s' % (self.opt, i) for i in kvlist ])
