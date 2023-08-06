import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    id: deleg
    width: 248
    height: 64

    opacity: device.online ? 1.0 : 0.3

    color: "transparent"

    Image {
        id: deviceImage

        width: 48
        height: 48
        source: Images.get_image(device.obj_type, "Small", device.color, "TAMPER_ALARM", device.subtype)

        anchors {
            top: parent.top
            left: parent.left
        }
    }

    DS3.Text {
        id: deviceName

        anchors {
            top: parent.top
            topMargin: 2
            left: deviceImage.right
            leftMargin: 12
        }

        text: device.name
        style: ui.ds3.text.body.MRegular
    }

    DS3.Text {
        id: deviceIndex

        anchors {
            top: deviceName.bottom
            left: deviceImage.right
            leftMargin: 12
        }

        style: ui.ds3.text.body.SRegular
        text: util.insert(tr.device_index_911, [device.device_index])
        opacity: 0.6
    }

    RowLayout {
        spacing: 0

        anchors {
            left: deviceImage.right
            bottom: parent.bottom
            bottomMargin: 3
        }

    }
}