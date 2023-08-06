import QtQuick 2.13
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
// Image alias for external access
    property alias imageRect: imageRect
//  Name of the company. With this name the letter alias will be generated automatically
    property string name: "Company"
//  Size of the image
    property int size: 128

    width: size
    height: size

    Rectangle {
        id: defaultImage

        anchors.fill: parent

        visible: imageRect.status != Image.Ready

        color: ui.ds3.bg.high
        radius: 8

        DS3.Text {
            width: undefined

            anchors.centerIn: parent

            style: {
                "height": parent.height / 2,
                "size": parent.height / 2,
                "weight": 75
            }
            text: name.trim().toUpperCase().split(/\s+/).splice(0, 2).reduce((value, token) => value + token.slice(0, 1), '')
            color: ui.ds3.figure.nonessential
        }
    }

    DS3.Image {
        id: imageRect

        // Image data
        property var imageData: null

        visible: !defaultImage.visible && source != "qrc:/resources/qml/screens/home/pages/company/info/WRONG"

        anchors.fill: parent

        cache: false
        layer.enabled: true
        layer.effect: OpacityMask {
            maskSource: Rectangle {
                width: imageRect.width
                height: imageRect.height

                radius: 8
            }
        }

        onImageDataChanged: {
            if (imageData) {
                app.process_image(imageData, "companyLogo")
            }
        }
    }
}
