#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans.model.conan_generator import Generator
from conans import ConanFile, tools, load


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
        deps = prepare_xmake_deps(self.deps_build_info)
        
        # TODO:    This generator spits out valid lua, but it's copied from 
        #                the conan premake generator, and not xmake. 
        #                I have started with this to demonstrate to xmake
        #                maintainer so he can understand how the generator works
        #                and see the output, and then make suggestions/corrections
        #                via PR or email.  
        
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

        for dep_name, dep_cpp_info in self.deps_build_info.dependencies:
            deps = PremakeDeps(dep_cpp_info)
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

def prepare_xmake_deps(deps_cpp_info):

        deps = {}

        deps.include_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                        for p in deps_cpp_info.include_paths)
        deps.lib_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                    for p in deps_cpp_info.lib_paths)
        deps.bin_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                    for p in deps_cpp_info.bin_paths)
        deps.libs = ", ".join('"%s"' % p for p in deps_cpp_info.libs)
        deps.defines = ", ".join('"%s"' % p for p in deps_cpp_info.defines)
        deps.cppflags = ", ".join('"%s"' % p for p in deps_cpp_info.cppflags)
        deps.cflags = ", ".join('"%s"' % p for p in deps_cpp_info.cflags)
        deps.sharedlinkflags = ", ".join('"%s"' % p for p in deps_cpp_info.sharedlinkflags)
        deps.exelinkflags = ", ".join('"%s"' % p for p in deps_cpp_info.exelinkflags)

        deps.rootpath = "%s" % deps_cpp_info.rootpath.replace("\\", "/")
        
        return deps