import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
    id: settingsContainerItem

    property bool isFirst: false
    property bool isLast: false
    property alias color: background.color

    Rectangle {
        id: background

        anchors.fill: parent

        color: ui.ds3.bg.highest

        layer.enabled: true
        layer.effect: OpacityMask {
            maskSource: Item {
                width: settingsContainerItem.width
                height: settingsContainerItem.height

                Rectangle {
                    anchors {
                        fill: parent
                        topMargin: isFirst ? 0 : -8
                        bottomMargin: isLast ? 0 : -8
                    }

                    radius: 12
                }
            }
        }
    }
}