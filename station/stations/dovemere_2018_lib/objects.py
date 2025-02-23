from .west_plaza.grounds import make_ground_layouts
from .west_plaza.topiary import make_topiaries
from .west_plaza.components import make_components
from .west_plaza.objects import make_objects
from .west_plaza.templates import make_templates
from .objects_utils import objects, templates, named_layouts

make_ground_layouts()
make_topiaries()
make_components()
make_objects()
make_templates()
