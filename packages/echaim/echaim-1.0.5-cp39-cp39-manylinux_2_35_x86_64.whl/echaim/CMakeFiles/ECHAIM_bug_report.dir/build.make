# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/lap1dem/dev-python/echaim/src/echaim

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/lap1dem/dev-python/echaim/src/echaim

# Include any dependencies generated for this target.
include CMakeFiles/ECHAIM_bug_report.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/ECHAIM_bug_report.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/ECHAIM_bug_report.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/ECHAIM_bug_report.dir/flags.make

CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o: CMakeFiles/ECHAIM_bug_report.dir/flags.make
CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o: source_c/lib/bug_report.c
CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o: CMakeFiles/ECHAIM_bug_report.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lap1dem/dev-python/echaim/src/echaim/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o -MF CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o.d -o CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o -c /home/lap1dem/dev-python/echaim/src/echaim/source_c/lib/bug_report.c

CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/lap1dem/dev-python/echaim/src/echaim/source_c/lib/bug_report.c > CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.i

CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/lap1dem/dev-python/echaim/src/echaim/source_c/lib/bug_report.c -o CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.s

# Object files for target ECHAIM_bug_report
ECHAIM_bug_report_OBJECTS = \
"CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o"

# External object files for target ECHAIM_bug_report
ECHAIM_bug_report_EXTERNAL_OBJECTS =

ECHAIM_bug_report: CMakeFiles/ECHAIM_bug_report.dir/source_c/lib/bug_report.c.o
ECHAIM_bug_report: CMakeFiles/ECHAIM_bug_report.dir/build.make
ECHAIM_bug_report: libECHAIM.so
ECHAIM_bug_report: CMakeFiles/ECHAIM_bug_report.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/lap1dem/dev-python/echaim/src/echaim/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ECHAIM_bug_report"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ECHAIM_bug_report.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/ECHAIM_bug_report.dir/build: ECHAIM_bug_report
.PHONY : CMakeFiles/ECHAIM_bug_report.dir/build

CMakeFiles/ECHAIM_bug_report.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ECHAIM_bug_report.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ECHAIM_bug_report.dir/clean

CMakeFiles/ECHAIM_bug_report.dir/depend:
	cd /home/lap1dem/dev-python/echaim/src/echaim && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/lap1dem/dev-python/echaim/src/echaim /home/lap1dem/dev-python/echaim/src/echaim /home/lap1dem/dev-python/echaim/src/echaim /home/lap1dem/dev-python/echaim/src/echaim /home/lap1dem/dev-python/echaim/src/echaim/CMakeFiles/ECHAIM_bug_report.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ECHAIM_bug_report.dir/depend

