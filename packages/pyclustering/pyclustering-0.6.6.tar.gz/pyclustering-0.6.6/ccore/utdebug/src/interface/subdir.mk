################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../src/interface/dbscan_interface.o \
../src/interface/kmedians_interface.o \
../src/interface/pcnn_interface.o \
../src/interface/pyclustering_package.o 

CPP_SRCS += \
../src/interface/dbscan_interface.cpp \
../src/interface/kmedians_interface.cpp \
../src/interface/pcnn_interface.cpp \
../src/interface/pyclustering_package.cpp 

OBJS += \
./src/interface/dbscan_interface.o \
./src/interface/kmedians_interface.o \
./src/interface/pcnn_interface.o \
./src/interface/pyclustering_package.o 

CPP_DEPS += \
./src/interface/dbscan_interface.d \
./src/interface/kmedians_interface.d \
./src/interface/pcnn_interface.d \
./src/interface/pyclustering_package.d 


# Each subdirectory must supply rules for building sources it contributes
src/interface/%.o: ../src/interface/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/src" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


