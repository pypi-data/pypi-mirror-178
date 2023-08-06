import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


PopupStep {
    id: popupStepExample

    property alias color: child.color
    property alias childHeight: child.height
    property alias topPartVisible: topPart.visible
    property int index: 0

    title: "Popup Step Example"
    sidePadding: 24

    Rectangle {
        id: topPart

        width: parent.width
        height: 700

        Rectangle {
            color: 'blue'
            width: parent.width
            height: 72
        }

        Rectangle {
            width: parent.width
            height: 300

            color: 'green'

            anchors.centerIn: parent
        }
    }

    Rectangle {
        id: child

        width: parent.width
        height: 100

        color: ['red', 'blue', 'green', 'yellow'][index] || 'grey'

        DS3.ButtonContained {
            anchors.centerIn: parent
            onClicked: popupStepExample.setChild(
                "qrc:/resources/qml/components/911/DS3/popups/PopupStepExample.qml",
                {childHeight: 300 * ((Math.random() * 10).toFixed() % 3 + 1), topPartVisible: false,
                index: popupStepExample.index + 1}
            )
        }
        DS3.ButtonContained {
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            onClicked: goBack(2)
        }
    }

    footer: Rectangle {
        color: 'grey'

        width: parent.width
        height: 50
    }
}
