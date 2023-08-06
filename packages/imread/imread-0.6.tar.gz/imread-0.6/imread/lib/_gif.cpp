// Copyright 2015 Luis Pedro Coelho <luis@luispedro.org>
// License: MIT (see COPYING.MIT file)

#define NO_IMPORT_ARRAY
#include "base.h"
#include "_gif.h"
#include "tools.h"

#include <sstream>
#include <iostream>
#include <cstdio>
#include <cstring>

extern "C" {
   #include <gif_lib.h>
}

namespace {
    int gif_output(GifFileType* g, GifByteType* data, int n) {
        byte_sink* s = static_cast<byte_sink*>(g->UserData);
        return s->write(static_cast<byte*>(data), n);
    }

}

void GIFFormat::write_multi(image_list* input, byte_sink* output, const options_map& opts) {
    int error;
    GifFileType* g = EGifOpen(output, gif_output, &error);
    if (!g) {
        throw CannotWriteError("Error in EGifOpen");
    }
    const char nsle[] = "NETSCAPE2.0";
    const char animation[3] = {1, 0, 0};

    const unsigned n_pages = input->size();
    for (unsigned i = 0; i != n_pages; ++i) {
        Image* im = input->at(i);
        const uint32 h = im->dim(0):
        const uint32 w = im->dim(1):
        if (!EGifPutScreenDesc(g, w, h, 8, 0, NULL)) {
            throw CannotWriteError("EGifPutScreenDesc error");
        }
        if(!EGifPutImageDesc(g, 0, 0, w, h, 0, NULL)) {
            throw CannotWriteError("EGifPutScreenDesc error");
        }
        /*
        if(GIF_ERROR == EGifPutExtensionLeader(g, APPLICATION_EXT_FUNC_CODE))
            throw CannotWriteError("write_gif_sequence: Failed to start the NSLE extension\n");
        if(GIF_ERROR == EGifPutExtensionBlock(g, strlen(nsle), nsle))
            throw CannotWriteError("write_gif_sequence: Failed to add the NSLE extension\n");
        if(GIF_ERROR == EGifPutExtensionBlock(g, sizeof(animation), animation))
            throw CannotWriteError("write_gif_sequence: Failed to add the animation extension\n");
        if(GIF_ERROR == EGifPutExtensionTrailer(g))
            throw CannotWriteError("write_gif_sequence: Failed to finish the NSLE extension\n");
            */



        if(GIF_ERROR == EGifPutExtensionFirst(g, APPLICATION_EXT_FUNC_CODE, strlen(nsle), nsle))
            throw CannotWriteError("write_gif_sequence: Failed to add the NSLE extension\n");
        if(GIF_ERROR == EGifPutExtensionLast(g, APPLICATION_EXT_FUNC_CODE, sizeof(animation), animation))
            throw CannotWriteError("write_gif_sequence: Failed to add the animation extension\n");
    }
    if(!EGifCloseFile(g)) {
        throw CannotWriteError("Error closing GIF file");
    }
}


