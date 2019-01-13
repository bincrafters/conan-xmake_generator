#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans.model.conan_generator import Generator
from conans import ConanFile


class XmakeGenerator(ConanFile):
    name = "xmake_generator"
    version = "0.1.0"
    url = "https://github.com/solvingj/conan-xmake_generator"
    description = "Conan build generator for xmake build system"
    topics = ("conan", "generator", "xmake", "tboox")
    homepage = "https://github.com/tboox/xmake"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]


class xmake(Generator):

    @property
    def filename(self):
        return "conanbuildinfo.xmake.lua"

    @property
    def content(self):
        deps = XmakeDepsFormatter(self.deps_build_info)
        
        # TODO:    This generator spits out valid lua, but it's copied from 
        # TODO:    the conan premake generator, and not xmake. 
        # TODO:    I have started with this to demonstrate to xmake
        # TODO:    maintainer so he can understand how the generator works
        # TODO:    and see the output, and then make suggestions/corrections
        # TODO:    via PR or email.  
        
        template = ('conan_includedirs{dep} = {{{deps.include_paths}}}\n'
                          'conan_libdirs{dep} = {{{deps.lib_paths}}}\n'
                          'conan_bindirs{dep} = {{{deps.bin_paths}}}\n'
                          'conan_libs{dep} = {{{deps.libs}}}\n'
                          'conan_cppdefines{dep} = {{{deps.defines}}}\n'
                          'conan_cppflags{dep} = {{{deps.cppflags}}}\n'
                          'conan_cflags{dep} = {{{deps.cflags}}}\n'
                          'conan_sharedlinkflags{dep} = {{{deps.sharedlinkflags}}}\n'
                          'conan_exelinkflags{dep} = {{{deps.exelinkflags}}}\n')

        sections = ["#!lua"]
        
        sections.extend(['conan_build_type = "{0}"'.format(str(self.settings.get_safe("build_type"))),
                                 'conan_arch = "{0}"'.format(str(self.settings.get_safe("arch"))),
                                 ""])

        all_flags = template.format(dep="", deps=deps)
        sections.append(all_flags)
        template_deps = template + 'conan_rootpath{dep} = "{deps.rootpath}"\n'

        for dep_name, _ in self.deps_build_info.dependencies:
            dep_name = dep_name.replace("-", "_")
            dep_flags = template_deps.format(dep="_" + dep_name, deps=deps)
            sections.append(dep_flags)

        sections.append(
            "function conan_basic_setup()\n"
            "    configurations{conan_build_type}\n"
            "    architecture(conan_arch)\n"
            "    includedirs{conan_includedirs}\n"
            "    libdirs{conan_libdirs}\n"
            "    links{conan_libs}\n"
            "    defines{conan_cppdefines}\n"
            "    bindirs{conan_bindirs}\n"
            "end\n")

        return "\n".join(sections)

class XmakeDepsFormatter(object):

    def __init__(self, deps_cpp_info):
        self.include_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                        for p in deps_cpp_info.include_paths)
        self.lib_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                    for p in deps_cpp_info.lib_paths)
        self.bin_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                    for p in deps_cpp_info.bin_paths)
        self.libs = ", ".join('"%s"' % p for p in deps_cpp_info.libs)
        self.defines = ", ".join('"%s"' % p for p in deps_cpp_info.defines)
        self.cppflags = ", ".join('"%s"' % p for p in deps_cpp_info.cppflags)
        self.cflags = ", ".join('"%s"' % p for p in deps_cpp_info.cflags)
        self.sharedlinkflags = ", ".join('"%s"' % p for p in deps_cpp_info.sharedlinkflags)
        self.exelinkflags = ", ".join('"%s"' % p for p in deps_cpp_info.exelinkflags)

        self.rootpath = "%s" % deps_cpp_info.rootpath.replace("\\", "/")