int sendIconToVMU(const unsigned char *icon) {
    uint8 lcd_data[48 * 32 / 8];
    maple_device_t *vmu;
    int i, j;
    
    //Convert image data to vmu format
    for (i = 0; i < 32; i++) {
        for (j = 0; j < 48 / 8; j++) {
            lcd_data[i * (48 / 8) + j] = icon[(31 - i) * (48 / 8) + j];
        }
    }
    
    // Look for VMU in port A1
    vmu = maple_enum_dev(0, 1);
    if (!vmu) {
        fprintf(stderr, "Couldn't find the VMU in port A1.\n");
        return -1;
    }
    
    // Send data to the vmu using vmu_draw_lcd
    if (vmu_draw_lcd(vmu, lcd_data) < 0) {
        fprintf(stderr, "Error when sending icon to the VMU.\n");
        return -1;
    }
    return 0;
    }
