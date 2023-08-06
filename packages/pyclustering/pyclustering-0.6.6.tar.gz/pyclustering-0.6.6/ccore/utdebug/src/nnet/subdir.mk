################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../src/nnet/legion.o \
../src/nnet/pcnn.o \
../src/nnet/som.o \
../src/nnet/sync.o \
../src/nnet/syncpr.o 

CPP_SRCS += \
../src/nnet/legion.cpp \
../src/nnet/pcnn.cpp \
../src/nnet/som.cpp \
../src/nnet/sync.cpp \
../src/nnet/syncpr.cpp 

OBJS += \
./src/nnet/legion.o \
./src/nnet/pcnn.o \
./src/nnet/som.o \
./src/nnet/sync.o \
./src/nnet/syncpr.o 

CPP_DEPS += \
./src/nnet/legion.d \
./src/nnet/pcnn.d \
./src/nnet/som.d \
./src/nnet/sync.d \
./src/nnet/syncpr.d 


# Each subdirectory must supply rules for building sources it contributes
src/nnet/%.o: ../src/nnet/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/src" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


