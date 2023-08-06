################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../src/container/adjacency_bit_matrix.o \
../src/container/adjacency_connector.o \
../src/container/adjacency_list.o \
../src/container/adjacency_matrix.o \
../src/container/adjacency_weight_list.o \
../src/container/kdtree.o 

CPP_SRCS += \
../src/container/adjacency_bit_matrix.cpp \
../src/container/adjacency_connector.cpp \
../src/container/adjacency_factory.cpp \
../src/container/adjacency_list.cpp \
../src/container/adjacency_matrix.cpp \
../src/container/adjacency_weight_list.cpp \
../src/container/kdtree.cpp 

OBJS += \
./src/container/adjacency_bit_matrix.o \
./src/container/adjacency_connector.o \
./src/container/adjacency_factory.o \
./src/container/adjacency_list.o \
./src/container/adjacency_matrix.o \
./src/container/adjacency_weight_list.o \
./src/container/kdtree.o 

CPP_DEPS += \
./src/container/adjacency_bit_matrix.d \
./src/container/adjacency_connector.d \
./src/container/adjacency_factory.d \
./src/container/adjacency_list.d \
./src/container/adjacency_matrix.d \
./src/container/adjacency_weight_list.d \
./src/container/kdtree.d 


# Each subdirectory must supply rules for building sources it contributes
src/container/%.o: ../src/container/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/src" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


