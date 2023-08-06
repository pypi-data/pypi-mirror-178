/*
* This file was automatically generated using Avlos.
* https://github.com/tinymovr/avlos
*
* Any changes to this file will be overwritten when
* content is regenerated.
*/
#include <test.h>


uint8_t (*avlos_endpoints[3])(uint8_t * buffer, uint8_t * buffer_len, Avlos_Command cmd) = {&avlos_toaster_sn, &avlos_toaster_heater_temperature, &avlos_toaster_relay_relay_state };
uint32_t avlos_proto_hash = 2748144804;

uint32_t _avlos_get_proto_hash(void)
{
    return avlos_proto_hash;
}

uint8_t avlos_toaster_sn(uint8_t * buffer, uint8_t * buffer_len, Avlos_Command cmd)
{
    if (AVLOS_CMD_READ == cmd) {
        uint32_t v;
        v = toaster_get_sn();
        *buffer_len = sizeof(v);
        memcpy(buffer, &v, sizeof(v));
        return AVLOS_RET_READ;
    }
    return AVLOS_RET_NOACTION;
}

uint8_t avlos_toaster_heater_temperature(uint8_t * buffer, uint8_t * buffer_len, Avlos_Command cmd)
{
    if (AVLOS_CMD_READ == cmd) {
        float v;
        v = toaster_get_heater_temp();
        *buffer_len = sizeof(v);
        memcpy(buffer, &v, sizeof(v));
        return AVLOS_RET_READ;
    }
    return AVLOS_RET_NOACTION;
}

uint8_t avlos_toaster_relay_relay_state(uint8_t * buffer, uint8_t * buffer_len, Avlos_Command cmd)
{
    if (AVLOS_CMD_READ == cmd) {
        bool v;
        v = toaster_get_relay_state();
        *buffer_len = sizeof(v);
        memcpy(buffer, &v, sizeof(v));
        return AVLOS_RET_READ;
    }
    else if (AVLOS_CMD_WRITE == cmd) {
        bool v;
        memcpy(&v, buffer, sizeof(v));
        toaster_set_relay_state(v);
        return AVLOS_RET_WRITE;
    }
    return AVLOS_RET_NOACTION;
}
