from conans import ConanFile, CMake, tools
import os


class GlfwConan(ConanFile):
    name = "glfw"
    version = "latest"
    license = "Zlib"
    url = "https://github.com/thoughton/conan-glfw"
    description = "A multi-platform library for OpenGL, OpenGL ES, Vulkan, window and input."

    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/glfw/glfw")
        self.run("cd glfw")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("glfw/CMakeLists.txt", "project(GLFW C)", '''project(GLFW C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        self.run('cmake glfw %s' % (cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="glfw/include")
        self.copy("*glfw3.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["glfw3"]
        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework CoreFoundation")
            self.cpp_info.exelinkflags.append("-framework CoreGraphics")
            self.cpp_info.exelinkflags.append("-framework CoreVideo")
            self.cpp_info.exelinkflags.append("-framework Cocoa")
            self.cpp_info.exelinkflags.append("-framework OpenGL")
            self.cpp_info.exelinkflags.append("-framework IOKit")
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append("dl")
            self.cpp_info.libs.append("X11")
            self.cpp_info.libs.append("Xrandr")
            self.cpp_info.libs.append("Xi")
            self.cpp_info.libs.append("Xcursor")
            self.cpp_info.libs.append("Xinerama")
            self.cpp_info.libs.append("pthread")
        self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags

