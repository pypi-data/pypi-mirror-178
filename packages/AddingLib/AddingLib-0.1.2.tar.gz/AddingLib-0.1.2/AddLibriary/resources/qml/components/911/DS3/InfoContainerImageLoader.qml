import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

Item {
//  Alias for Image component
    property alias imageComponent: imageComponent
//  Alias for Title component
    property alias titleComponent: titleComponent
//  Alias for Description component
    property alias descComponent: descComponent

    width: parent.width
    height: content.height

    Column {
        id: content

        width: parent.width

        DS3.PlugImageLoader {
            id: imageComponent

            anchors.horizontalCenter: parent.horizontalCenter
        }

        DS3.Spacing {
            height: 24

            visible: imageComponent.visible
        }

        DS3.TitleUniversal {
            id: titleComponent

            width: parent.width - 32

            anchors.horizontalCenter: parent.horizontalCenter
        }

        DS3.Spacing {
            height: 8

            visible: titleComponent.visible && descComponent.visible
        }

        DS3.Text {
            id: descComponent

            width: parent.width - 32

            anchors.horizontalCenter: parent.horizontalCenter

            horizontalAlignment: Text.AlignHCenter
            style: ui.ds3.text.body.LRegular
            color: ui.ds3.figure.secondary
        }
    }
}
