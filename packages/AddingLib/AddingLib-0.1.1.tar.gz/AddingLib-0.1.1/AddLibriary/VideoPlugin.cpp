#include "VideoPlugin.h"

#include <QtQml/QtQml>
#include <VideoPlayer.h>
#include <PlaybackController.h>

#include <iostream>

void VideoPlugin::registerTypes(const char* uri) {
    qmlRegisterModule(uri, 1, 0);
    qmlRegisterType<VideoPlayer>(uri, 1, 0, "VideoPlayerWindow");
}
