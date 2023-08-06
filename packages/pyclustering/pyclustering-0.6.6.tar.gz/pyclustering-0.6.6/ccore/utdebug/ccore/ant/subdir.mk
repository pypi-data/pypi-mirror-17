################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../ccore/ant/ant_colony.o \
../ccore/ant/distance_matrix.o 

CPP_SRCS += \
../ccore/ant/ant_colony.cpp \
../ccore/ant/distance_matrix.cpp 

OBJS += \
./ccore/ant/ant_colony.o \
./ccore/ant/distance_matrix.o 

CPP_DEPS += \
./ccore/ant/ant_colony.d \
./ccore/ant/distance_matrix.d 


# Each subdirectory must supply rules for building sources it contributes
ccore/ant/%.o: ../ccore/ant/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


