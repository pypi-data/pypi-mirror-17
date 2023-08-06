import os

from ..java import (
    Class as JavaClass, Code as JavaCode, Method as JavaMethod, SourceFile,
    opcodes as JavaOpcodes
)
from .blocks import Block
from .methods import (
    CO_GENERATOR, GeneratorMethod, Method,
)
from .utils import ALOAD_name, ASTORE_name, free_name


class Module(Block):
    def __init__(self, namespace, sourcefile, verbosity=0):
        super().__init__(verbosity=verbosity)
        self.sourcefile = sourcefile

        parts = os.path.splitext(sourcefile)[0].split(os.path.sep)
        if parts[-1] == '__init__':
            parts.pop()

        # If the sourcefile started with a /, the first part will
        # be an empty string; replace that with the namespace.
        # Otherwise, prepend the namespace to the parts.
        if parts[0] == '':
            parts[0] = namespace
        else:
            parts = [namespace] + parts
        self.namespace = '.'.join(parts[:-1])
        self.name = parts[-1]

        self.methods = []
        self.classes = []
        self.anonymous_inner_class_count = 0

        # Preallocate space for self when
        # the module static block is invoked
        self.parameters = [None]
        self.local_vars['self'] = 0

    @property
    def module(self):
        return self

    @property
    def full_name(self):
        return '.'.join(self.namespace.split('.')[1:] + [self.name])

    @property
    def descriptor(self):
        return '/'.join(self.namespace.split('.') + [self.name])

    @property
    def class_name(self):
        return '.'.join(self.namespace.split('.') + [self.name, '__init__'])

    @property
    def class_descriptor(self):
        return '/'.join(self.namespace.split('.') + [self.name, '__init__'])

    # def visitor_setup(self):
    #     self.add_opcodes(
    #         JavaOpcodes.LDC_W("STATIC BLOCK OF " + self.class_name),
    #         JavaOpcodes.INVOKESTATIC('org/Python', 'debug', '(Ljava/lang/String;)V'),
    #     )

    def store_name(self, name):
        self.add_opcodes(
            ASTORE_name(self, '#value'),
            JavaOpcodes.GETSTATIC('python/sys/__init__', 'modules', 'Lorg/python/types/Dict;'),

            JavaOpcodes.NEW('org/python/types/Str'),
            JavaOpcodes.DUP(),
            JavaOpcodes.LDC_W(self.full_name),
            JavaOpcodes.INVOKESPECIAL('org/python/types/Str', '<init>', '(Ljava/lang/String;)V'),

            JavaOpcodes.INVOKEINTERFACE('org/python/Object', '__getitem__', '(Lorg/python/Object;)Lorg/python/Object;'),
            JavaOpcodes.CHECKCAST('org/python/types/Module'),

            JavaOpcodes.LDC_W(name),
            ALOAD_name(self, '#value'),

            JavaOpcodes.INVOKEINTERFACE('org/python/Object', '__setattr__', '(Ljava/lang/String;Lorg/python/Object;)V'),
        )
        free_name(self, '#value')

    def store_dynamic(self):
        self.add_opcodes(
            ASTORE_name(self, '#value'),
            JavaOpcodes.GETSTATIC('python/sys/__init__', 'modules', 'Lorg/python/types/Dict;'),

            JavaOpcodes.NEW('org/python/types/Str'),
            JavaOpcodes.DUP(),
            JavaOpcodes.LDC_W(self.full_name),
            JavaOpcodes.INVOKESPECIAL('org/python/types/Str', '<init>', '(Ljava/lang/String;)V'),

            JavaOpcodes.INVOKEINTERFACE('org/python/Object', '__getitem__', '(Lorg/python/Object;)Lorg/python/Object;'),
            JavaOpcodes.CHECKCAST('org/python/types/Module'),

            JavaOpcodes.GETFIELD('org/python/types/Module', '__dict__', 'Ljava/util/Map;'),

            ALOAD_name(self, '#value'),
            JavaOpcodes.INVOKEINTERFACE('java/util/Map', 'putAll', '(Ljava/util/Map;)V'),
        )
        free_name(self, '#value')

    def load_name(self, name):
        self.add_opcodes(
            JavaOpcodes.GETSTATIC('python/sys/__init__', 'modules', 'Lorg/python/types/Dict;'),

            JavaOpcodes.NEW('org/python/types/Str'),
            JavaOpcodes.DUP(),
            JavaOpcodes.LDC_W(self.full_name),
            JavaOpcodes.INVOKESPECIAL('org/python/types/Str', '<init>', '(Ljava/lang/String;)V'),

            JavaOpcodes.INVOKEINTERFACE('org/python/Object', '__getitem__', '(Lorg/python/Object;)Lorg/python/Object;'),
            JavaOpcodes.CHECKCAST('org/python/types/Module'),
            JavaOpcodes.LDC_W(name),
            JavaOpcodes.INVOKEINTERFACE('org/python/Object', '__getattribute__', '(Ljava/lang/String;)Lorg/python/Object;'),
        )

    def delete_name(self, name):
        self.add_opcodes(
            JavaOpcodes.GETSTATIC('python/sys/__init__', 'modules', 'Lorg/python/types/Dict;'),

            JavaOpcodes.NEW('org/python/types/Str'),
            JavaOpcodes.DUP(),
            JavaOpcodes.LDC_W(self.full_name),
            JavaOpcodes.INVOKESPECIAL('org/python/types/Str', '<init>', '(Ljava/lang/String;)V'),

            JavaOpcodes.INVOKEINTERFACE('org/python/Object', '__getitem__', '(Lorg/python/Object;)Lorg/python/Object;'),
            JavaOpcodes.CHECKCAST('org/python/types/Module'),
            JavaOpcodes.LDC_W(name),
            JavaOpcodes.INVOKEVIRTUAL('org/python/types/Module', '__delattr__', '(Ljava/lang/String;)V'),
        )

    def add_method(self, name, code, parameter_signatures, return_signature):
        if code.co_flags & CO_GENERATOR:
            # Generator method.
            method = GeneratorMethod(
                self,
                name=name,
                code=code,
                generator=code.co_name,
                parameters=parameter_signatures,
                returns=return_signature,
                static=True
            )
        else:
            # Normal method.
            method = Method(
                self,
                name=name,
                code=code,
                parameters=parameter_signatures,
                returns=return_signature,
                static=True,
            )

        # Add the method to the list that need to be
        # transpiled into Java methods
        self.methods.append(method)

        # Add a definition of the callable object
        self.add_callable(method)

        # Store the callable object as an accessible symbol.
        self.store_name(method.name)

        return method

    def add_class(self, class_name, bases, extends, implements):
        from .klass import Class

        klass = Class(
            self,
            name=class_name,
            bases=bases,
            extends=extends,
            implements=implements,
        )

        self.classes.append(klass)

        self.add_opcodes(
            # JavaOpcodes.LDC_W("FORCE LOAD OF CLASS %s AT DEFINITION" % self.klass.descriptor),
            # JavaOpcodes.INVOKESTATIC('org/Python', 'debug', '(Ljava/lang/String;)V'),

            JavaOpcodes.LDC_W(klass.descriptor.replace('/', '.')),
            JavaOpcodes.INVOKESTATIC('java/lang/Class', 'forName', '(Ljava/lang/String;)Ljava/lang/Class;'),

            JavaOpcodes.INVOKESTATIC('org/python/types/Type', 'pythonType', '(Ljava/lang/Class;)Lorg/python/types/Type;'),
        )

        self.store_name(klass.name)

        return klass

    def visitor_teardown(self):
        self.add_opcodes(
            JavaOpcodes.RETURN(),
        )

    def transpile(self):
        """Convert a materialized Python code definition into a list of Java
        Classfile definitions.

        Returns a list of triples:
            (namespace, class_name, javaclassfile)

        The list contains the classfile for the module, plus and classes
        defined in the module.
        """
        # If there is any static content, generate a classfile
        # for this module
        classfile = JavaClass(self.class_descriptor, extends='org/python/types/Module')
        classfile.attributes.append(SourceFile(os.path.basename(self.sourcefile)))

        # Add a static method to the module, populated with the
        # body content of the module.
        static_init = JavaMethod('module$import', '()V', public=False)
        static_init.attributes.append(self.transpile_code())
        classfile.methods.append(static_init)

        # Add a dummy init method.
        classfile.methods.append(
            JavaMethod(
                '<init>',
                '()V',
                attributes=[
                    JavaCode(
                        max_stack=2,
                        max_locals=1,
                        code=[
                            JavaOpcodes.ALOAD_0(),
                            JavaOpcodes.DUP(),
                            JavaOpcodes.INVOKESPECIAL('org/python/types/Module', '<init>', '()V'),
                            JavaOpcodes.RETURN(),
                        ],
                    ),
                ]
            )
        )

        # Add any static methods defined in the module
        for method in self.methods:
            classfile.methods.extend(method.transpile())

        # The list of classfiles that will be returned will contain
        # at least one entry - the class for the module itself.
        classfiles = [(
            self.namespace,
            '%s/__init__' % self.name,
            classfile
        )]
        # Also output any classes defined in this module.
        for klass in self.classes:
            classfiles.append(klass.transpile())

        return classfiles
