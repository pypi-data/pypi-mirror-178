import QtQuick 2.13
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
// Image alias for external access
    property alias imageRect: imageRect
//  Size of the image
    property int size: 136

    width: size
    height: size

    DS3.Image {
        id: defaultImage

        anchors.fill: parent

        source: "qrc:/resources/images/Athena/user_settings/UserImage-BG.svg"
        layer.enabled: true
        visible: imageRect.status != Image.Ready
    }

    DS3.Image {
        id: imageRect

        // Image data
        property var imageData: null

        anchors.fill: parent

        cache: false
        layer.enabled: true
        layer.effect: OpacityMask {
            maskSource: Rectangle {
                width: imageRect.width
                height: imageRect.height

                radius: height / 2
            }
        }

        onSourceChanged: {
            if (source.toString().endsWith("WRONG")) source = ""
        }

        onImageDataChanged: {
            if (imageData) {
                app.process_image(imageData, "user")
            }
        }
    }
}
