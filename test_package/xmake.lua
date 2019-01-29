
-- add modes: debug and release 
add_rules("mode.debug", "mode.release")

-- add requires
add_requires("CONAN::zlib/1.2.11@conan/stable", {alias = "zlib", --[[debug = true,]] config = {build_requires = "xmake_generator/0.1.0@bincrafters/testing", build = "all"}})
add_requires("CONAN::OpenSSL/1.0.2n@conan/stable", {alias = "openssl", config = {build_requires = "xmake_generator/0.1.0@bincrafters/testing",
                                                                                 options = "OpenSSL:shared=True",
                                                                                 build = "all"}})

-- add target
target("test")

    -- set kind
    set_kind("binary")

    -- add files
    add_files("src/*.c") 

    -- on load
    on_load(function (target)
        print(find_packages("CONAN::OpenSSL/1.0.2n@conan/stable", "CONAN::zlib/1.2.11@conan/stable"))
    end)

    -- add packages
    add_packages("openssl", "zlib")

--
-- FAQ
--
-- You can enter the project directory firstly before building project.
--   
--   $ cd projectdir
-- 
-- 1. How to build project?
--   
--   $ xmake
--
-- 2. How to configure project?
--
--   $ xmake f -p [macosx|linux|iphoneos ..] -a [x86_64|i386|arm64 ..] -m [debug|release]
--
-- 3. Where is the build output directory?
--
--   The default output directory is `./build` and you can configure the output directory.
--
--   $ xmake f -o outputdir
--   $ xmake
--
-- 4. How to run and debug target after building project?
--
--   $ xmake run [targetname]
--   $ xmake run -d [targetname]
--
-- 5. How to install target to the system directory or other output directory?
--
--   $ xmake install 
--   $ xmake install -o installdir
--
-- 6. Add some frequently-used compilation flags in xmake.lua
--
-- @code 
--    -- add macro defination
--    add_defines("NDEBUG", "_GNU_SOURCE=1")
--
--    -- set warning all as error
--    set_warnings("all", "error")
--
--    -- set language: c99, c++11
--    set_languages("c99", "cxx11")
--
--    -- set optimization: none, faster, fastest, smallest 
--    set_optimize("fastest")
--    
--    -- add include search directories
--    add_includedirs("/usr/include", "/usr/local/include")
--
--    -- add link libraries and search directories
--    add_links("tbox", "z", "pthread")
--    add_linkdirs("/usr/local/lib", "/usr/lib")
--
--    -- add compilation and link flags
--    add_cxflags("-stdnolib", "-fno-strict-aliasing")
--    add_ldflags("-L/usr/local/lib", "-lpthread", {force = true})
--
-- @endcode
--
-- 7. If you want to known more usage about xmake, please see http://xmake.io/#/home
--
    
