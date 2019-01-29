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

        # get plat
        plat = str(self.settings.get_safe("os_build"))
        if plat == "Macos":
            plat = "macosx"

        # get mode
        mode = str(self.settings.get_safe("build_type"))
        if mode == "Debug":
            mode = "debug"
        else:
            mode = "release"

        # get arch
        arch = str(self.settings.get_safe("arch_build"))
        
        # make template
        template = ('  {plat}_{arch}_{mode} = \n'
                    '  {{\n'
                    '    includedirs = {{{deps.include_paths}}},\n'
                    '    linkdirs    = {{{deps.lib_paths}}},\n'
                    '    links       = {{{deps.libs}}},\n'
                    '    defines     = {{{deps.defines}}},\n'
                    '    cxxflags    = {{{deps.cppflags}}},\n'
                    '    cflags      = {{{deps.cflags}}},\n'
                    '    shflags     = {{{deps.sharedlinkflags}}},\n'
                    '    ldflags     = {{{deps.exelinkflags}}}\n'
                    '  }}')
        
        # make sections
        sections = []
        sections.append(template.format(plat = plat, arch = arch, mode = mode, deps = deps))

        # make content
        return "{\n" + ",\n".join(sections) + "\n}"

class XmakeDepsFormatter(object):

    def __init__(self, deps_cpp_info):
        self.include_paths   = ",\n".join('"%s"' % p.replace("\\", "/") for p in deps_cpp_info.include_paths)
        self.lib_paths       = ",\n".join('"%s"' % p.replace("\\", "/") for p in deps_cpp_info.lib_paths)
        self.bin_paths       = ",\n".join('"%s"' % p.replace("\\", "/") for p in deps_cpp_info.bin_paths)
        self.libs            = ", ".join('"%s"' % p for p in deps_cpp_info.libs)
        self.defines         = ", ".join('"%s"' % p for p in deps_cpp_info.defines)
        self.cppflags        = ", ".join('"%s"' % p for p in deps_cpp_info.cppflags)
        self.cflags          = ", ".join('"%s"' % p for p in deps_cpp_info.cflags)
        self.sharedlinkflags = ", ".join('"%s"' % p for p in deps_cpp_info.sharedlinkflags)
        self.exelinkflags    = ", ".join('"%s"' % p for p in deps_cpp_info.exelinkflags)
        self.rootpath        = "%s" % deps_cpp_info.rootpath.replace("\\", "/")
