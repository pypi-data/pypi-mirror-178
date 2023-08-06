import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/images.js" as Images

Item {
    width: parent.width
    height: 208

    property string imageSource: ""
    property alias deviceImage: deviceImage


    Image {
        id: deviceImage
        width: 192
        height: 192
        source: imageSource || Images.get_image(device.obj_type, "Large", device.color, "0", device.subtype)

        anchors {
            top: parent.top
            horizontalCenter: parent.horizontalCenter
        }
    }
}