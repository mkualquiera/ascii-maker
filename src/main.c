#if INTERFACE
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include "stb_image.h"
#include "stb_image_resize.h"
#include <argp.h>
#include "ascii.h"
#include "util.h"
#endif 

#include "main.h"

const char *argp_program_version = "asciimaker C";
const char *argp_program_bug_address = "ozjuanpa@gmail.com";

static char doc[] = "Ascii maker -- A tool that converts image to ascii art";

static struct argp_option options[] = {
  {"output", 'o', "FILE", OPTION_ARG_OPTIONAL, "Output to FILE instead of standard output"},
  {"input", 'i', "FILE", 0, "Input image FILE"},
  {"color", 'c', 0, OPTION_ARG_OPTIONAL, "Use colors"},
  {"grasycale", 'g', 0, OPTION_ARG_OPTIONAL, "Use grayscale"},
  {"background", 'b', 0, OPTION_ARG_OPTIONAL, "Also change background of the text"},
  {"width", 'w', "WIDTH", 0, "Change the width in characters of the final image"},
  {"defaults", 'd', 0, OPTION_ARG_OPTIONAL, "Treat black and white as the default background and foreground colors"},
  { 0 }
};

/* Used by main to communicate with parse_opt. */
struct arguments
{
  char *args[2];                /* arg1 & arg2 */
  char verbose;
  char set_output;
  char set_input;
  char use_color;
  char use_grayscale;
  char use_background; 
  int width;
  char set_width;
  char explicit;
  char *output_file;
  char *input_file;
};

static error_t parse_opt (int key, char *arg, struct argp_state *state)
{
  /* Get the input argument from argp_parse, which we
     know is a pointer to our arguments structure. */
  struct arguments *arguments = state->input;

  switch (key)
    {
    case 'o':
      arguments->set_input = 1;
      arguments->output_file = arg;
      break;
    case 'i':
      if( access( arg, R_OK ) != -1 ) {
        arguments->set_input =1;
        arguments->input_file = arg;
      } else {
        argp_usage(state);
      }
      break;
    case 'w':
      arguments->set_width = 1;
      str2int_errno err = str2int(&arguments->width,arg,10);
      if (err != STR2INT_SUCCESS)
        argp_usage(state);
      break;
    case 'b':
      arguments->use_background = 1;
      break;
    case 'c':
      arguments->use_color = 1;
      break;
    case 'g':
      arguments->use_grayscale = 1;
      break;
    case 'd':
      arguments->explicit = 1;
      break;

    case ARGP_KEY_ARG:
      //if (state->arg_num >= 2)
        /* Too many arguments. */
        //argp_usage (state);

      arguments->args[state->arg_num] = arg;

      break;

    case ARGP_KEY_END:
      if (arguments->set_input == 0)
        /* Not enough arguments. */
        argp_usage (state);
      break;

    default:
      return ARGP_ERR_UNKNOWN;
    }
  return 0;
}

static struct argp argp = { options, parse_opt, 0, doc };

int main(int argc, char *argv[]) {

  struct arguments arguments;

  /* Default values. */
  arguments.output_file = "-";
  arguments.input_file = "-";
  arguments.set_input = 0;
  arguments.set_output = 0;
  arguments.use_color = 0;
  arguments.use_background = 0;
  arguments.width = 0;
  arguments.set_width = 0;
  arguments.explicit = 0;
  arguments.use_grayscale = 0;

  argp_parse (&argp, argc, argv, 0, 0, &arguments);

  int fd = arguments.set_output ? open(arguments.output_file, O_RDONLY) : STDOUT_FILENO;

  ascii_convert(fd, arguments.use_color, arguments.use_background,
    arguments.set_width, arguments.width, arguments.explicit,
    arguments.input_file, arguments.use_grayscale);

  exit(0);
}