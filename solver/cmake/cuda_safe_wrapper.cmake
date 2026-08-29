function(make_cuda_safe_wrapper wrapper target)
    add_library(${wrapper} INTERFACE)

    # Передаём target только в link-контексте.
    target_link_libraries(${wrapper}
        INTERFACE
            "$<LINK_ONLY:${target}>"
    )

    # Переносим основные compile usage requirements.
    foreach(property IN ITEMS
        INTERFACE_INCLUDE_DIRECTORIES
        INTERFACE_SYSTEM_INCLUDE_DIRECTORIES
        INTERFACE_COMPILE_DEFINITIONS
        INTERFACE_COMPILE_FEATURES
    )
        get_target_property(value ${target} ${property})

        if (value AND NOT value STREQUAL "value-NOTFOUND")
            if (property STREQUAL "INTERFACE_INCLUDE_DIRECTORIES")
                target_include_directories(${wrapper}
                    INTERFACE ${value}
                )
            elseif (property STREQUAL "INTERFACE_SYSTEM_INCLUDE_DIRECTORIES")
                target_include_directories(${wrapper}
                    SYSTEM INTERFACE ${value}
                )
            elseif (property STREQUAL "INTERFACE_COMPILE_DEFINITIONS")
                target_compile_definitions(${wrapper}
                    INTERFACE ${value}
                )
            elseif (property STREQUAL "INTERFACE_COMPILE_FEATURES")
                target_compile_features(${wrapper}
                    INTERFACE ${value}
                )
            endif()
        endif()
    endforeach()

    get_target_property(options
        ${target}
        INTERFACE_COMPILE_OPTIONS
    )

    if (NOT options OR options STREQUAL "options-NOTFOUND")
        return()
    endif()

    set(cxx_options)
    set(cuda_options)
    set(other_options)

    foreach(option IN LISTS options)
        # Простая обработка MSVC-style host options.
        if (option MATCHES "^/")
            list(APPEND cxx_options
                "$<$<COMPILE_LANGUAGE:CXX>:${option}>"
            )

            list(APPEND cuda_options
                "$<$<COMPILE_LANG_AND_ID:CUDA,NVIDIA>:-Xcompiler=${option}>"
            )
        else()
            # Нестандартные или CUDA-neutral options.
            # Их следует проверить отдельно.
            list(APPEND other_options
                "$<$<NOT:$<COMPILE_LANGUAGE:CUDA>>:${option}>"
            )
        endif()
    endforeach()

    target_compile_options(${wrapper}
        INTERFACE
            ${cxx_options}
            ${cuda_options}
            ${other_options}
    )
endfunction()