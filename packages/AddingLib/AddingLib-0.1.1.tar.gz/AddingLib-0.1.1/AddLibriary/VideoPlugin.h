#ifndef __VIDEO_PLUGIN_H__
#define __VIDEO_PLUGIN_H__

#include <QQmlExtensionPlugin>

class VideoPlugin: public QQmlExtensionPlugin {
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "ajax.plugin.video/1.0")
public:
    void registerTypes(const char* uri) override;
};

#endif // MYPLUGIN_H