set(Namespace_SRCS
        freecad/gridfinity_plus_workbench/init_gui.py
        freecad/gridfinity_plus_workbench/__init__.py
        freecad/gridfinity_plus_workbench/my_numpy_function.py
        freecad/gridfinity_plus_workbench/version.py
        freecad/gridfinity_plus_workbench/resources/cool.svg
        freecad/gridfinity_plus_workbench/resources/translations/gridfinity_plus_workbench_es-ES.qm
        freecad/gridfinity_plus_workbench/resources/translations/gridfinity_plus_workbench_es-ES.ts
)

SOURCE_GROUP("" FILES ${Namespace_SRCS})

ADD_CUSTOM_TARGET(SEARCHBAR ALL
        SOURCES ${Namespace_SRCS}
)

fc_copy_sources(SEARCHBAR "${CMAKE_BINARY_DIR}/Mod/GridifintyPlusWorkbench" ${Namespace_SRCS})

INSTALL(
    FILES
        ${Namespace_SRCS}
    DESTINATION
        Mod/SearchBar
)
