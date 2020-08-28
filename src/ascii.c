#if INTERFACE

#include <dirent.h>
#include <stdio.h>
#include "util.h"
#include <stdlib.h>
#define cell_w 10
#define cell_h 20

#endif

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include "stb_image_resize.h"
#include "stamps.h"

#include "ascii.h"

char fg_colors[16][20] = {
  "\033[30m",
  "\033[31m",
  "\033[32m",
  "\033[33m",
  "\033[34m",
  "\033[35m",
  "\033[36m",
  "\033[37m",
  "\033[90m",
  "\033[91m",
  "\033[92m",
  "\033[93m",
  "\033[94m",
  "\033[95m",
  "\033[96m",
  "\033[97m",
};

char bg_colors[16][20] = {
  "\033[40m",
  "\033[41m",
  "\033[42m",
  "\033[43m",
  "\033[44m",
  "\033[45m",
  "\033[46m",
  "\033[47m",
  "\033[100m",
  "\033[101m",
  "\033[102m",
  "\033[103m",
  "\033[104m",
  "\033[105m",
  "\033[106m",
  "\033[107m",
};

char *reset = "\033[0m";

void ascii_convert(unsigned int fd, unsigned char use_color,
  unsigned char use_background, unsigned char use_width,
  unsigned int cwidth, unsigned char explicit, char *infile,
  char use_grayscale) {
  
  // Load initial image 
  int x,y,n;
  unsigned char *initial_image = stbi_load(infile, &x, &y, &n, 3);

  if (initial_image == NULL) {
    return;
  }

  int final_cwidth = 0;

  if (use_width) {
    final_cwidth = cwidth;
  } else {
    final_cwidth = x/cell_w;
  }

  int final_iwidth = final_cwidth*cell_w;
  double rel = (double)final_iwidth/(double)x;
  int final_iheight = (double)y*rel;
  int final_cheight = final_iheight/cell_h;

  //printf("%u %u %u %u %u %u\n", x, y, final_iwidth, final_iheight, final_cwidth, final_cheight);


  unsigned char *resized_image = malloc(sizeof(char) * 3 * final_iwidth * final_iheight); 
  stbir_resize_uint8(initial_image, x, y, 0, resized_image, final_iwidth, final_iheight, 0, 3);

  unsigned char *stamps_data = stamps;
  //char *stamps_data = malloc(sizeof(unsigned char) * cell_w * cell_h * 3 * 16 * 16 * 95);
  long s_char_selector = sizeof(unsigned char) * cell_w * cell_h * 3 * 16 * 16;
  long s_bg_selector = sizeof(unsigned char) * cell_w * cell_h * 3 * 16;
  long s_fg_selector = sizeof(unsigned char) * cell_w * cell_h * 3;
  long s_row_selector = sizeof(unsigned char) * cell_w * 3;
  long s_col_selector = sizeof(unsigned char) * 3;

  //printf("Loading stamps...\n");
  /*DIR *d;
  struct dirent *dir;
  d = opendir("./stamps");
  if (d) {
    while ((dir = readdir(d)) != NULL) {
      if (strlen(dir->d_name) > 5) {
        char char_id[4];
        char bg_id[3];
        char fg_id[3];
        for (int i = 0; i < 3; i++) {
          char_id[i] = dir->d_name[i];
        }
        char_id[3] = '\0';
        for (int i = 0; i < 2; i++) {
          bg_id[i] = dir->d_name[i+4];
        }
        bg_id[2] = '\0';
        for (int i = 0; i < 2; i++) {
          fg_id[i] = dir->d_name[i+7];
        }
        fg_id[2] = '\0';

        int char_id_num;
        int bg_id_num;
        int fg_id_num;
        str2int(&char_id_num, char_id, 10);
        str2int(&bg_id_num, bg_id, 10);
        str2int(&fg_id_num, fg_id, 10);
        char_id_num-=32;
        int w, h, _;
        char fname[100];
        strcpy(fname, "./stamps/");
        strcat(fname,dir->d_name);
        unsigned char *stamp_image = stbi_load(fname, &w, &h, &_, 3);
        memcpy(stamps_data+s_char_selector*char_id_num+s_bg_selector*bg_id_num+s_fg_selector*fg_id_num,stamp_image,cell_h*cell_w*3);
      }
    }
    closedir(d);
  }*/
  //printf("Done loading stamps...\n");
  /*for (unsigned long long i = 0; i < sizeof(unsigned char) * cell_w * cell_h * 3 * 16 * 16 * 95; i += sizeof(char)) {
    printf("%u,",(unsigned char)(stamps_data[i]));
  }
  printf("\n");
  return;*/

  for (unsigned int fy = 0; fy < final_cheight; fy++) {
    for (unsigned int fx = 0; fx < final_cwidth; fx++) {
      unsigned long long lowest_error = LONG_MAX; 
      unsigned int best_char = 0;
      unsigned int best_fg = 0;
      unsigned int best_bg = 0;
      for (unsigned int char_id = 0; char_id < 95; char_id++) {
        for (unsigned int bg_id = 0; bg_id < 16; bg_id++) {
          for (unsigned int fg_id = 0; fg_id < 16; fg_id++) {
            if((bg_id == fg_id) & (char_id != 0)) {
              continue;
            }
            if((0 != fg_id) & (char_id == 0)) {
              continue;
            } 
            if (!use_background) {
              if (bg_id != 0) {
                continue;
              }
            }
            if ((!use_color) & (!use_grayscale)) {
              if (((bg_id != 0) & (bg_id != 15)) | ((fg_id != 0) &
                  (fg_id != 15))) {
                continue;
              } 
            }
            if ((!use_color) & use_grayscale) {
              if (((bg_id != 0) & (bg_id != 15)& (bg_id != 7)& (bg_id != 8)) | ((fg_id != 0) &
                  (fg_id != 15)& (fg_id != 7)& (fg_id != 8))) {
                continue;
              } 
            }
            unsigned long long error = 0;
            for (unsigned int ix = 0; ix < cell_w; ix++) {
              for (unsigned int iy = 0; iy < cell_h; iy++) {
                unsigned char *a = stamps_data+s_char_selector*char_id+s_bg_selector*bg_id+s_fg_selector*fg_id+iy*s_row_selector+ix*s_col_selector;
                int internal_x = fx * cell_w + ix;
                int internal_y = fy * cell_h + iy;
                unsigned char *b = resized_image+final_iwidth*3*sizeof(char)*internal_y+3*sizeof(char)*internal_x;
                //printf("%u\n", ((int)a[0]-(int)b[0])*((int)a[0]-(int)b[0]));
                long long ar = a[0];
                long long ag = a[1];
                long long ab = a[2];
                long long br = b[0];
                long long bg = b[1];
                long long bb = b[2];
                error += (ar-br)*(ar-br);
                error += (ag-bg)*(ag-bg);
                error += (ab-bb)*(ab-bb);
              }
            }
            if (error < lowest_error) {
              //printf("new best");
              lowest_error = error;
              best_bg = bg_id;
              best_fg = fg_id;
              best_char = char_id;
            }
          }
        }
      }
      best_char += 32;
      //printf("%u\n", best_bg);
      if (explicit) {
        if (best_bg != 0) {
          write(fd, &bg_colors[best_bg],best_bg<=7?5:6);
        } 
        if (best_fg != 7) {
          write(fd, &fg_colors[best_fg],best_fg<=7?5:5);
        }
      } else {
        write(fd, &bg_colors[best_bg],best_bg<=7?5:6);
        write(fd, &fg_colors[best_fg],best_fg<=7?5:5);
      }
      write(fd, &best_char, 1);
      write(fd, reset,4);
    }
    char nl = '\n';
    write(fd, &nl, 1);
  }

}