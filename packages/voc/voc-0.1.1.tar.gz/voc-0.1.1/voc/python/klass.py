import os

from ..java import (
    Annotation, Class as JavaClass, Code as JavaCode, ConstantElementValue,
    Field as JavaField, Method as JavaMethod, RuntimeVisibleAnnotations,
    SourceFile, opcodes as JavaOpcodes,
)
from .blocks import Block, IgnoreBlock
from .methods import (
    CO_GENERATOR, InitMethod, InstanceMethod
)
from .utils import (
    ALOAD_name, ASTORE_name, free_name
)


class Class(Block):
    def __init__(self, module, name, namespace=None, bases=None, extends=None, implements=None, public=True, final=False, methods=None, fields=None, init=None, verbosity=0):
        super().__init__(module, verbosity=verbosity)
        self.name = name
        if namespace is None:
            self.namespace = '%s.%s' % (self.parent.namespace, self.parent.name)
        else:
            self.namespace = namespace

        self.bases = bases if bases else []
        self.extends = extends

        self.implements = implements if implements else []
        self.public = public
        self.final = final
        self.methods = methods if methods else []
        self.fields = fields if fields else {}
        self.init = init

        self.anonymous_inner_class_count = 0

        # Track constructors when they are added
        self.init_method = None

        # Mark this class as being a VOC generated class.
        self.fields["__VOC__"] = "Lorg/python/Object;"

        # Make sure there is a default constructor
        default_init = InitMethod(self)
        default_init.visitor_setup()
        default_init.visitor_teardown()
        self.methods.append(default_init)

    @property
    def descriptor(self):
        return '/'.join([self.namespace.replace('.', '/'), self.name])

    @property
    def class_name(self):
        return '.'.join(self.namespace.split('.') + [self.name])

    @property
    def class_descriptor(self):
        return '/'.join(self.namespace.split('.') + [self.name])

    @property
    def module(self):
        return self.parent

    def visitor_setup(self):
        if self.extends:
            base_descriptor = self.extends.replace('.', '/')
        else:
            base_descriptor = 'org/python/types/Object'

        self.add_opcodes(
            # JavaOpcodes.LDC_W("STATIC BLOCK OF " + self.klass.descriptor),
            # JavaOpcodes.INVOKESTATIC('org/Python', 'debug', '(Ljava/lang/String;)V'),

            # Force the loading and instantiation of the module
            # that contains the class.
            JavaOpcodes.LDC_W(self.module.full_name),
            JavaOpcodes.ACONST_NULL(),
            JavaOpcodes.ICONST_0(),
            JavaOpcodes.INVOKESTATIC('org/python/ImportLib', '__import__', '(Ljava/lang/String;[Ljava/lang/String;I)Lorg/python/types/Module;'),
            JavaOpcodes.POP(),

            # Set __base__ on the type
            JavaOpcodes.LDC_W(self.descriptor),
            JavaOpcodes.INVOKESTATIC('org/python/types/Type', 'pythonType', '(Ljava/lang/String;)Lorg/python/types/Type;'),

            JavaOpcodes.LDC_W(base_descriptor),
            JavaOpcodes.INVOKESTATIC('org/python/types/Type', 'pythonType', '(Ljava/lang/String;)Lorg/python/types/Type;'),

            # JavaOpcodes.DUP(),
            # JavaOpcodes.LDC_W("__base__ for %s should be %s; is" % (self.klass, base_descriptor)),
            # JavaOpcodes.SWAP(),
            # JavaOpcodes.INVOKESTATIC('org/Python', 'debug', '(Ljava/lang/String;Ljava/lang/Object;)V'),

            JavaOpcodes.PUTFIELD('org/python/types/Type', '__base__', 'Lorg/python/types/Type;'),

            # Set __bases__ on the type
            JavaOpcodes.LDC_W(self.descriptor),
            JavaOpcodes.INVOKESTATIC('org/python/types/Type', 'pythonType', '(Ljava/lang/String;)Lorg/python/types/Type;'),

            JavaOpcodes.NEW('org/python/types/Tuple'),
            JavaOpcodes.DUP(),

            JavaOpcodes.NEW('java/util/ArrayList'),
            JavaOpcodes.DUP(),
            JavaOpcodes.INVOKESPECIAL('java/util/ArrayList', '<init>', '()V'),
        )

        if self.extends:
            self.add_opcodes(
                JavaOpcodes.DUP(),

                JavaOpcodes.NEW('org/python/types/Str'),
                JavaOpcodes.DUP(),
                JavaOpcodes.LDC_W(self.extends.replace('.', '/')),
                JavaOpcodes.INVOKESPECIAL('org/python/types/Str', '<init>', '(Ljava/lang/String;)V'),

                JavaOpcodes.INVOKEVIRTUAL('java/util/ArrayList', 'add', '(Ljava/lang/Object;)Z'),
                JavaOpcodes.POP()
            )

        for base in self.bases:
            base_namespace = self.namespace.replace('.', '/') + '/'
            self.add_opcodes(
                JavaOpcodes.DUP(),

                JavaOpcodes.NEW('org/python/types/Str'),
                JavaOpcodes.DUP(),
                JavaOpcodes.LDC_W(base if base.startswith('org/python/') else base_namespace + base),
                JavaOpcodes.INVOKESPECIAL('org/python/types/Str', '<init>', '(Ljava/lang/String;)V'),

                JavaOpcodes.INVOKEVIRTUAL('java/util/ArrayList', 'add', '(Ljava/lang/Object;)Z'),
                JavaOpcodes.POP()
            )

        self.add_opcodes(
            JavaOpcodes.INVOKESPECIAL('org/python/types/Tuple', '<init>', '(Ljava/util/List;)V'),

            JavaOpcodes.PUTFIELD('org/python/types/Type', '__bases__', 'Lorg/python/types/Tuple;'),
        )

        self.load_name('__name__')
        self.store_name('__module__')

        self.add_opcodes(
            JavaOpcodes.NEW('org/python/types/Str'),
            JavaOpcodes.DUP(),
            JavaOpcodes.LDC_W(self.name),
            JavaOpcodes.INVOKESPECIAL('org/python/types/Str', '<init>', '(Ljava/lang/String;)V')
        )
        self.store_name('__qualname__')

        # self.add_opcodes(
        #     JavaOpcodes.LDC_W("STATIC BLOCK OF " + self.klass.descriptor + " DONE"),
        #     JavaOpcodes.INVOKESTATIC('org/Python', 'debug', '(Ljava/lang/String;)V'),
        # )

    def store_name(self, name):
        self.add_opcodes(
            ASTORE_name(self, '#value'),
            JavaOpcodes.LDC_W(self.descriptor),
            JavaOpcodes.INVOKESTATIC('org/python/types/Type', 'pythonType', '(Ljava/lang/String;)Lorg/python/types/Type;'),

            JavaOpcodes.LDC_W(name),
            ALOAD_name(self, '#value'),

            JavaOpcodes.INVOKEINTERFACE('org/python/Object', '__setattr__', '(Ljava/lang/String;Lorg/python/Object;)V'),
        )
        free_name(self, '#value')

    def store_dynamic(self):
        self.add_opcodes(
            ASTORE_name(self, '#value'),
            JavaOpcodes.LDC_W(self.descriptor),
            JavaOpcodes.INVOKESTATIC('org/python/types/Type', 'pythonType', '(Ljava/lang/String;)Lorg/python/types/Type;'),

            JavaOpcodes.GETFIELD('org/python/types/Type', '__dict__', 'Ljava/util/Map;'),
            ALOAD_name(self, '#value'),

            JavaOpcodes.INVOKEINTERFACE('java/util/Map', 'putAll', '(Ljava/util/Map;)V'),
        )
        free_name(self, '#value')

    def load_name(self, name):
        self.add_opcodes(
            JavaOpcodes.LDC_W(self.descriptor),
            JavaOpcodes.INVOKESTATIC('org/python/types/Type', 'pythonType', '(Ljava/lang/String;)Lorg/python/types/Type;'),
            JavaOpcodes.LDC_W(name),
            JavaOpcodes.INVOKEVIRTUAL('org/python/types/Type', '__getattribute__', '(Ljava/lang/String;)Lorg/python/Object;'),
        )

    def delete_name(self, name):
        self.add_opcodes(
            JavaOpcodes.LDC_W(self.descriptor),
            JavaOpcodes.INVOKESTATIC('org/python/types/Type', 'pythonType', '(Ljava/lang/String;)Lorg/python/types/Type;'),
            JavaOpcodes.LDC_W(name),
            JavaOpcodes.INVOKEVIRTUAL('org/python/types/Type', '__delattr__', '(Ljava/lang/String;)V'),
        )

    def add_method(self, name, code, parameter_signatures, return_signature):
        # parts = name.split('$')[-1].split('.')
        # method_name = parts[-1]
        # class_name = parts[-2]

        # if class_name != self.klass.name:
        #     raise Exception("Method %s being added to %s!" % (class_name, self.klass.name))

        # print (code)
        if False:  # FIXME code.co_flags & CO_GENERATOR:
            raise Exception("Can't handle Generator instance methods (yet)")
        else:
            # return_type = annotations.get('return', 'org/python/Object')
            # if return_type is None:
            #     return_type = 'void'

            method = InstanceMethod(
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

        if method.name == '__init__':
            self.init_method = method

        return method

    def visitor_teardown(self):
        self.add_opcodes(
            JavaOpcodes.RETURN()
        )

    def transpile(self):
        classfile = JavaClass(
            self.descriptor,
            extends=self.extends if self.extends else 'org/python/types/Object',
            implements=self.implements,
            public=self.public,
            final=self.final
        )

        classfile.attributes.append(
            SourceFile(os.path.basename(self.module.sourcefile))
        )

        classfile.attributes.append(
            RuntimeVisibleAnnotations([
                Annotation(
                    'Lorg/python/Method;',
                    {
                        '__doc__': ConstantElementValue("Python Class (insert docs here)")
                    }
                )
            ])
        )

        try:
            # If we have block content, add a static block to the class
            static_init = JavaMethod('<clinit>', '()V', public=False, static=True)
            static_init.attributes.append(super().transpile())
            classfile.methods.append(static_init)
        except IgnoreBlock:
            pass

        # Add any manually defined fields
        classfile.fields.extend([
            JavaField(name, descriptor)
            for name, descriptor in self.fields.items()
        ])

        # Add any methods
        for method in self.methods:
            classfile.methods.extend(method.transpile())

        # Ensure the class has a class protected, no-args init() so that
        # instances can be instantiated.
        if self.extends:
            base_descriptor = self.extends.replace('.', '/')
        else:
            base_descriptor = 'org/python/types/Object'

        classfile.methods.append(
            JavaMethod(
                '<init>',
                '()V',
                public=False,
                static=False,
                attributes=[
                    JavaCode(
                        max_stack=1,
                        max_locals=1,
                        code=[
                            JavaOpcodes.ALOAD_0(),
                            JavaOpcodes.INVOKESPECIAL(base_descriptor, '<init>', '()V'),
                            JavaOpcodes.RETURN(),
                        ]
                    )
                ]
            )
        )

        return self.namespace, self.name, classfile


class InnerClass(Class):
    def __init__(self, parent, name, bases=None, extends=None, implements=None, public=True, final=False, methods=None, init=None, verbosity=0):
        if isinstance(parent, Class):
            module = parent.module
        else:
            module = parent
        super().__init__(
            module=module,
            name=name,
            namespace=parent.namespace,
            bases=bases,
            extends=extends,
            implements=implements,
            public=public,
            final=final,
            methods=methods,
            init=init,
            verbosity=verbosity
        )


class ClosureClass(Class):
    def __init__(self, parent, closure_var_names, name=None, extends=None, bases=None, implements=None, public=True, final=False, methods=None, init=None, verbosity=0):
        self.closure_var_names = closure_var_names
        if isinstance(parent, Class):
            module = parent.module
        else:
            module = parent
        if name is None:
            parent.anonymous_inner_class_count += 1
            name = "%s$%d" % (parent.name, parent.anonymous_inner_class_count)
        super().__init__(
            module=module,
            name=name,
            namespace=parent.namespace,
            bases=bases,
            extends=extends,
            implements=implements,
            public=public,
            final=final,
            methods=methods,
            init=init,
            verbosity=verbosity
        )

    @property
    def klass(self):
        return self.parent
