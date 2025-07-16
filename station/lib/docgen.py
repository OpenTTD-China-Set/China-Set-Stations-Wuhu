import os
from agrf.strings import get_translation, remove_control_letters
from agrf.graphics.palette import CompanyColour
from .utils import get_1cc_remap, class_label_printable
from station.lib.idmap import station_idmap


def gen_docs(string_manager, metastations):
    prefix = "docs/"
    for i, metastation in enumerate(metastations):
        metastation_label = metastation.class_label_plain
        translation = get_translation(string_manager[f"STR_METASTATION_CLASS_{metastation_label}"], 0x7F)
        for kind in ["layouts", "stations", "waypoints", "road_stops", "objects"]:
            os.makedirs(os.path.join(prefix, "img", metastation_label, kind), exist_ok=True)

        toc = []

        for kind in ["waypoints", "stations", "road_stops", "objects"]:
            if kind == "road_stops":
                pool = [x for x in metastation.road_stops if not x.is_waypoint]
            elif kind == "objects":
                pool = metastation.objects
            else:
                pool = metastation.stations

            if metastation.categories is None:
                subsections = {
                    None: [
                        x
                        for x in pool
                        if (("waypoint" not in x.doc_layout.notes) ^ (kind == "waypoints"))
                        and "noshow" not in x.doc_layout.notes
                    ]
                }
            else:
                subsections = {k: [] for k in metastation.categories}
                for layout in pool:
                    if (
                        ("waypoint" not in layout.doc_layout.notes) ^ (kind == "waypoints")
                    ) and "noshow" not in layout.doc_layout.notes:
                        subsections[layout.doc_layout.category].append(layout)

            if all(len(v) == 0 for v in subsections.values()):
                continue

            tocentry = f"{metastation_label}_{kind}"
            toc.append(tocentry)
            with open(os.path.join(prefix, f"{tocentry}.rst"), "w") as f:
                title, nav_order = {
                    "stations": ("Building Blocks", 0),
                    "waypoints": ("Waypoints", 1),
                    "road_stops": ("Road Stops", 2),
                    "objects": ("Objects", 4),
                }[kind]
                print(f"================\n{title}\n================\n", file=f)

                for sub in subsections:
                    if sub is not None and len(subsections[sub]) > 0:
                        cat_name = get_translation(
                            string_manager[f"STR_STATION_CLASS_{class_label_printable(sub)}"], 0x7F
                        )
                        if "-" in cat_name:
                            cat_name = cat_name.split("-")[-1].strip()
                        cat_name = remove_control_letters(cat_name)
                        if cat_name.startswith("|> "):
                            cat_name = cat_name[3:]
                        print(f"----------------\n{cat_name}\n----------------", file=f)
                    for layout in sorted(subsections[sub], key=lambda x: x.id):
                        img = (
                            layout.doc_layout.graphics(4, 32, remap=get_1cc_remap(CompanyColour.BLUE))
                            .crop()
                            .to_pil_image()
                        )
                        idstr = f"{layout.id:04X}"
                        idpath = idstr
                        if kind in ["waypoints", "stations"] and layout.id in station_idmap:
                            idstr += f" ({station_idmap[layout.id]:04X})"
                        img.save(os.path.join(prefix, "img", f"{metastation_label}/{kind}/{idpath}.png"))
                        print(
                            f"""
.. figure:: img/{metastation_label}/{kind}/{idpath}.png
  :width: 64
  :figclass: inline-figure

  {idstr}
""",
                            file=f,
                        )

        for demoi, (title, demov) in enumerate(metastation.demos.items()):
            demok = title.replace(" ", "_").lower()
            os.makedirs(os.path.join(prefix, "img", metastation_label, "layouts", demok), exist_ok=True)
            tocentry = f"{metastation_label}_{demok}"
            toc.append(tocentry)
            with open(os.path.join(prefix, f"{tocentry}.rst"), "w") as f:
                print(f"================\n{title}\n================\n", file=f)
                for i, demo in enumerate(demov):
                    img = demo.graphics(4, 32).crop().resize(1920, 1080).to_pil_image()
                    img.save(os.path.join(prefix, "img", f"{metastation_label}/layouts/{demok}/{i:04X}.png"))
                    print(
                        f"""
----------------
{demo.title}
----------------

.. image:: img/{metastation_label}/layouts/{demok}/{i:04X}.png
""",
                        file=f,
                    )

        with open(os.path.join(prefix, f"{metastation_label}.md"), "w") as f:
            print(
                f"""# {translation}

```{{toctree}}
:maxdepth: 2""",
                file=f,
            )
            for item in toc:
                print(item, file=f)
            print(f"```\n", file=f)
