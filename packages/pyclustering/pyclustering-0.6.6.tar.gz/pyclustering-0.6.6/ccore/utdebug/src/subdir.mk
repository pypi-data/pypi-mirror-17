################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../src/ccore.o \
../src/utils.o 

CPP_SRCS += \
../src/ccore.cpp \
../src/utils.cpp 

OBJS += \
./src/ccore.o \
./src/utils.o 

CPP_DEPS += \
./src/ccore.d \
./src/utils.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/src" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


