import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/"

Item {

    property var settingText: ""
    property var loaderSource: ""

    width: parent.width
    height: 34

    Rectangle {
        width: parent.width - 96
        height: 32
        color: "transparent"
        anchors{
            top: parent.top
            horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: settingText
            color: ui.colors.light1
            leftPadding: 5

            font.family: roboto.name
            font.pixelSize: 14

            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }
        }


        Image {
            id: arrowVerificationMode
            source: "qrc:/resources/images/desktop/icons/ic-arrow.png"
            visible: false

            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }
        }

        ColorOverlay {
            anchors.fill: arrowVerificationMode
            source: arrowVerificationMode
            color: ui.colors.light1
            opacity: 0.3
        }

        Rectangle {
            width: parent.width
            height: 1

            color: "#504e4e"
            anchors.bottom: parent.bottom
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/" + loaderSource)
            }
        }
    }
}
