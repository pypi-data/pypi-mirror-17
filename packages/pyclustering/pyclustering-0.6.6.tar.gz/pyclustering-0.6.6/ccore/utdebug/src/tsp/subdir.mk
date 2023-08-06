################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../src/tsp/ant_colony.o \
../src/tsp/distance_matrix.o 

CPP_SRCS += \
../src/tsp/ant_clustering_mean.cpp \
../src/tsp/ant_colony.cpp \
../src/tsp/distance_matrix.cpp 

OBJS += \
./src/tsp/ant_clustering_mean.o \
./src/tsp/ant_colony.o \
./src/tsp/distance_matrix.o 

CPP_DEPS += \
./src/tsp/ant_clustering_mean.d \
./src/tsp/ant_colony.d \
./src/tsp/distance_matrix.d 


# Each subdirectory must supply rules for building sources it contributes
src/tsp/%.o: ../src/tsp/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/src" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


