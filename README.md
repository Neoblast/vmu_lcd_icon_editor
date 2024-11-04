VMU Icon Editor (48x32) - Version 0.1

Author: Neoblast

Description:
This python application provides a VERY simple LCD editor to create monochrome 48x32 pixel LCD images for the Sega Dreamcast's VMU (Visual Memory Unit) to use in homebrew projects with KOS.
Users can draw on the canvas, save the icon as a C array, and clear the canvas.

Usage: 
Left click on a pixel to paint it.
Right click on a pixel to erase it.

Drag the left click over the canvas to paint the selected pixels.
Drag the right click over the canvas to erase the selected pixels.

Press on any of the buttons to copy the C array to the clipboard or as a header file to use in projects.

Features:
- Draw and erase pixels on a 48x32 grid
- Save the current icon as a C array that can be used in projects
- Clear the entire canvas


Example C function to draw the icon to the VMU

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
