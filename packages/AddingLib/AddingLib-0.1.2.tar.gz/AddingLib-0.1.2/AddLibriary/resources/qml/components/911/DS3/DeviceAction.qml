import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/images.js" as Images


Rectangle {
//  Component atomTitle
    property alias atomTitle: atomTitle
//  On start mini button clicked
    property alias buttonMiniControl : buttonMiniControl
//  When spinner is visible
    property alias spinnerVisibility : spinner.visible
// Image source
    property alias imageSource : deviceImage.source

    width: parent.width
    height: 104

    color: ui.ds3.bg.highest
    opacity: enabled ? 1 : 0.3

    Item {
        id: mainBody

        width: parent.width
        height: 104

        anchors {
            top: parent.top
            left: parent.left
        }
    }

    DS3.Image {
        id: deviceImage

        width: 96
        height: 96

        anchors {
            verticalCenter: mainBody.verticalCenter
            left: parent.left
            leftMargin: 4
        }
    }

    DS3.AtomTitle {
        id: atomTitle

        width: 215
        height: 44

        anchors {
            top: mainBody.top
            topMargin: 30
            left: parent.left
            leftMargin: 112
        }

        isBold: true
    }

    DS3.ButtonMini {
        id: buttonMiniControl

        anchors {
            verticalCenter: mainBody.verticalCenter
            right: parent.right
            rightMargin: 16
        }
    }

    DS3.Spinner {
        id: spinner

        anchors {
            verticalCenter: mainBody.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        visible: false
    }
}