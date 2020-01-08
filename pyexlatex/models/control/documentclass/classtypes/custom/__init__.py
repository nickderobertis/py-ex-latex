from pyexlatex.models.control.documentclass.classtypes.custom.resume import resume_class_type

CUSTOM_CLASS_TYPE_OBJS = [
    resume_class_type
]

CUSTOM_CLASS_TYPES = {class_type.name: class_type for class_type in CUSTOM_CLASS_TYPE_OBJS}
