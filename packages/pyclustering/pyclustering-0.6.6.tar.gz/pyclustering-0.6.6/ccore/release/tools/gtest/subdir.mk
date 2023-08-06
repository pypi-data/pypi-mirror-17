################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../tools/gtest/gtest-all.cpp 

OBJS += \
./tools/gtest/gtest-all.o 

CPP_DEPS += \
./tools/gtest/gtest-all.d 


# Each subdirectory must supply rules for building sources it contributes
tools/gtest/%.o: ../tools/gtest/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++0x -fPIC -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


