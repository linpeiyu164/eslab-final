#include "mbed.h"
#include "stm32l475e_iot01_gyro.h"
#include "stm32l475e_iot01_accelero.h"
#include <string>
#include "HTTPClient.cpp"
using namespace std;

InterruptIn button(BUTTON1);
Thread T2;
Timer t;

static BufferedSerial serial_port(USBTX, USBRX);
FileHandle *mbed::mbed_override_console(int fd){
    return &serial_port; 
}

void send_direction_message(string& car, string& cam, HTTPClient * client){
    const char * car_direction = car.c_str();
    const char * cam_direction = cam.c_str();
    char msg[50];
    sprintf(msg, "{\"direction\": \"%s\",\"camera\": \"%s\"}", car_direction, cam_direction);
    client -> send_message((const char *)msg);
}

void car_motion(string& car, string& cam, HTTPClient * client){
    BSP_ACCELERO_Init();
    uint32_t i = 0;
    uint32_t index = 0;
    int limit = 300;
    const int amount = 30;
    /* Initialize input and output buffer pointers */
    int16_t Acc[3] = {0};
    float sumax = 0,sumay = 0,sumaz = 0;
    float tempx[amount]={0};
    float tempy[amount]={0};
    float tempz[amount]={0};
    int state = 0;
    int prestate = 0;
    int count = 0;
    printf("Start sensing\n");
    while(true){
        sumax = 0;
        sumay = 0;
        sumaz = 0;
        BSP_ACCELERO_AccGetXYZ(Acc);
        int temp;
        temp = index % amount;
        tempx[temp] = (float)Acc[0];
        tempy[temp] = (float)Acc[1];
        tempz[temp] = (float)Acc[2];
        for(int i=0;i<amount;i++){
            sumax += tempx[i];
            sumay += tempy[i];
            sumaz += tempz[i];
        }
        sumax = sumax/amount;
        sumay = sumay/amount;
        sumaz = sumaz/amount;
        if(sumax<-limit && sumax<sumay){
            state = 1;
            car = "right";
            if(state != prestate){
                printf("car right\n");
            }
        }
        else if(sumax>limit && sumax>sumay){
            state = 2;
            car = "left";
            if(state != prestate){
                printf("car left\n");
            }
        }
        else if(sumay<-limit && sumax>=sumay){
            state = 3;
            car = "forward";
            if(state != prestate){
                printf("car forward\n");
            }
        }
        else if(sumay>limit && sumax<=sumay){
            state = 4;
            car = "backward";
            if(state != prestate){
                printf("car backward\n");
            }
        }
        else if(sumaz<0){
            state = 0;
            car = "upsidedown";
            if(state != prestate){
                printf("upsidedown\n");
            }
        }
        else{
            state = 0;
            car = "stable";
            if(state != prestate){
                printf("stable or unknown\n");
            }
        }         
        if(count == 10){
            send_direction_message(car, cam, client);
            count = 0;
        }
        prestate = state;
        index++;
        count++;
    }
};

void motion_detection(HTTPClient * client, string& car_msg, string& camera_msg){
    while(true){
        car_motion(car_msg, camera_msg, client);
    }
}

int main()
{
    #ifdef MBED_CONF_MBED_TRACE_ENABLE
    mbed_trace_init();
    #endif
    HTTPClient *client = new HTTPClient();
    MBED_ASSERT(client);
    char addr1[] = "192.168.0.156";
    int port = 3000;

    client -> setAddress(addr1, port);
    client -> connect_wifi();
    client -> connect_port();

    BSP_ACCELERO_Init();
    string car_msg = "";
    string camera_msg = "";
    motion_detection(client, car_msg, camera_msg);
    delete client;
}