#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "xmake"
    requires = ("zlib/1.2.11@conan/stable")

    def build(self):
        self.run("xmake -P test_package")
        
    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            self.run(os.path.join("bin", "test_package"))
