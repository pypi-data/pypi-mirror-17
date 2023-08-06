################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../ccore/adjacency_bit_matrix.cpp \
../ccore/adjacency_factory.cpp \
../ccore/adjacency_list.cpp \
../ccore/adjacency_matrix.cpp \
../ccore/adjacency_weight_list.cpp \
../ccore/agglomerative.cpp \
../ccore/ccore.cpp \
../ccore/cure.cpp \
../ccore/dbscan.cpp \
../ccore/hierarchical.cpp \
../ccore/hsyncnet.cpp \
../ccore/kdtree.cpp \
../ccore/kmeans.cpp \
../ccore/kmedians.cpp \
../ccore/legion.cpp \
../ccore/network.cpp \
../ccore/pcnn.cpp \
../ccore/rock.cpp \
../ccore/som.cpp \
../ccore/support.cpp \
../ccore/sync.cpp \
../ccore/syncnet.cpp \
../ccore/syncpr.cpp \
../ccore/xmeans.cpp 

OBJS += \
./ccore/adjacency_bit_matrix.o \
./ccore/adjacency_factory.o \
./ccore/adjacency_list.o \
./ccore/adjacency_matrix.o \
./ccore/adjacency_weight_list.o \
./ccore/agglomerative.o \
./ccore/ccore.o \
./ccore/cure.o \
./ccore/dbscan.o \
./ccore/hierarchical.o \
./ccore/hsyncnet.o \
./ccore/kdtree.o \
./ccore/kmeans.o \
./ccore/kmedians.o \
./ccore/legion.o \
./ccore/network.o \
./ccore/pcnn.o \
./ccore/rock.o \
./ccore/som.o \
./ccore/support.o \
./ccore/sync.o \
./ccore/syncnet.o \
./ccore/syncpr.o \
./ccore/xmeans.o 

CPP_DEPS += \
./ccore/adjacency_bit_matrix.d \
./ccore/adjacency_factory.d \
./ccore/adjacency_list.d \
./ccore/adjacency_matrix.d \
./ccore/adjacency_weight_list.d \
./ccore/agglomerative.d \
./ccore/ccore.d \
./ccore/cure.d \
./ccore/dbscan.d \
./ccore/hierarchical.d \
./ccore/hsyncnet.d \
./ccore/kdtree.d \
./ccore/kmeans.d \
./ccore/kmedians.d \
./ccore/legion.d \
./ccore/network.d \
./ccore/pcnn.d \
./ccore/rock.d \
./ccore/som.d \
./ccore/support.d \
./ccore/sync.d \
./ccore/syncnet.d \
./ccore/syncpr.d \
./ccore/xmeans.d 


# Each subdirectory must supply rules for building sources it contributes
ccore/%.o: ../ccore/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++0x -fPIC -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


