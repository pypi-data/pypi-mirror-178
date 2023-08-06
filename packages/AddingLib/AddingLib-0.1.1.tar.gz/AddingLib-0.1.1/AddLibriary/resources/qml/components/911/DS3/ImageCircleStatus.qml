import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: imageCircleStatus

//  Image of the user
    property alias imageSource: image.source

    width: 40
    height: 40

    DS3.Image {
        id: defaultImage

        anchors.fill: image

        source: appUser.company_id ?
            "qrc:/resources/images/Athena/user_rows/ProUserPlaceholderImage-M.svg" :
            "qrc:/resources/images/Athena/user_rows/UserPlaceholderImage-M.svg"
        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
        visible: image.status != Image.Ready
    }

    DS3.Image {
        id: image

        width: 40
        height: 40

        anchors.centerIn: parent

        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
    }

    Rectangle {
        id: circle

        anchors.fill: image

        radius: width / 2
        visible: false
    }

    Item {
        id: statusItemContainer

        width: 16
        height: 16

        anchors{
            bottom: parent.bottom
            bottomMargin: -2
            right: parent.right
            rightMargin: -2
        }

        Rectangle {
            id: statusFrame

            anchors.fill: parent

            radius: width / 2
            color: ui.ds3.bg.highest
        }

        Rectangle {
            height: 12
            width: 12

            anchors.centerIn: parent

            radius: width / 2
            color: app.online ? ui.ds3.figure.interactive : ui.ds3.figure.attention
        }
    }
}
