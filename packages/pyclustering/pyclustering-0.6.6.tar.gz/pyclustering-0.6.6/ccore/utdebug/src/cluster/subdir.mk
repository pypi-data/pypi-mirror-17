################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../src/cluster/agglomerative.o \
../src/cluster/cluster_algorithm.o \
../src/cluster/cluster_data.o \
../src/cluster/cure.o \
../src/cluster/dbscan.o \
../src/cluster/dbscan_data.o \
../src/cluster/hierarchical.o \
../src/cluster/hsyncnet.o \
../src/cluster/kmeans.o \
../src/cluster/kmedians.o \
../src/cluster/kmedians_data.o \
../src/cluster/kmedoids.o \
../src/cluster/kmedoids_data.o \
../src/cluster/rock.o \
../src/cluster/syncnet.o \
../src/cluster/xmeans.o 

CPP_SRCS += \
../src/cluster/agglomerative.cpp \
../src/cluster/cluster_algorithm.cpp \
../src/cluster/cluster_data.cpp \
../src/cluster/cure.cpp \
../src/cluster/dbscan.cpp \
../src/cluster/dbscan_data.cpp \
../src/cluster/hierarchical.cpp \
../src/cluster/hsyncnet.cpp \
../src/cluster/kmeans.cpp \
../src/cluster/kmedians.cpp \
../src/cluster/kmedians_data.cpp \
../src/cluster/kmedoids.cpp \
../src/cluster/kmedoids_data.cpp \
../src/cluster/rock.cpp \
../src/cluster/syncnet.cpp \
../src/cluster/xmeans.cpp 

OBJS += \
./src/cluster/agglomerative.o \
./src/cluster/cluster_algorithm.o \
./src/cluster/cluster_data.o \
./src/cluster/cure.o \
./src/cluster/dbscan.o \
./src/cluster/dbscan_data.o \
./src/cluster/hierarchical.o \
./src/cluster/hsyncnet.o \
./src/cluster/kmeans.o \
./src/cluster/kmedians.o \
./src/cluster/kmedians_data.o \
./src/cluster/kmedoids.o \
./src/cluster/kmedoids_data.o \
./src/cluster/rock.o \
./src/cluster/syncnet.o \
./src/cluster/xmeans.o 

CPP_DEPS += \
./src/cluster/agglomerative.d \
./src/cluster/cluster_algorithm.d \
./src/cluster/cluster_data.d \
./src/cluster/cure.d \
./src/cluster/dbscan.d \
./src/cluster/dbscan_data.d \
./src/cluster/hierarchical.d \
./src/cluster/hsyncnet.d \
./src/cluster/kmeans.d \
./src/cluster/kmedians.d \
./src/cluster/kmedians_data.d \
./src/cluster/kmedoids.d \
./src/cluster/kmedoids_data.d \
./src/cluster/rock.d \
./src/cluster/syncnet.d \
./src/cluster/xmeans.d 


# Each subdirectory must supply rules for building sources it contributes
src/cluster/%.o: ../src/cluster/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/src" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


