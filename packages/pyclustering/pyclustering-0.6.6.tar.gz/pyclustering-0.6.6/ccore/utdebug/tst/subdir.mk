################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../tst/main.o \
../tst/samples.o \
../tst/utest-cluster.o 

CPP_SRCS += \
../tst/main.cpp \
../tst/samples.cpp \
../tst/utest-cluster.cpp 

OBJS += \
./tst/main.o \
./tst/samples.o \
./tst/utest-cluster.o 

CPP_DEPS += \
./tst/main.d \
./tst/samples.d \
./tst/utest-cluster.d 


# Each subdirectory must supply rules for building sources it contributes
tst/%.o: ../tst/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/src" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


