import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
    id: imagePhotoPreview

//  image ratio w/h
    property var ratio: 4/3
//  image source
    property alias source: image.source
//  error text
    property alias errorText: errorText.text

    signal goNext
    signal goPrev
    signal download

    height: image.height

    layer.enabled: true
    layer.samplerName: "maskSource"
    layer.effect: ShaderEffect {
        property var colorSource: roundedMask

        //fragmentShader: util.shaders.round_corners
    }

    Rectangle {
        id: roundedMask

        width: imagePhotoPreview.width
        height: imagePhotoPreview.height

        visible: false
        radius: 12
        layer.enabled: true
    }

    DS3.Image {
        id: image

        width: parent.width
        height: width / ratio
    }

    Column {
        width: 240

        anchors.centerIn: parent

        spacing: 8

        DS3.Spinner {
            id: loadingSpinner

            anchors.horizontalCenter: parent.horizontalCenter

            size: DS3.Spinner.ImageSize.M
            visible: image.status == Image.Loading
        }

        DS3.Icon {
            id: warningIcon

            anchors.horizontalCenter: parent.horizontalCenter

            source: "qrc:/resources/images/Athena/common_icons/WarningFilled-M.svg"
            visible: errorText.visible
        }

        DS3.Text {
            id: errorText

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: !!text
        }
    }

    Item {
        id: buttons

        anchors.fill: parent

        visible: image.status == Image.Ready

        Rectangle {
            width: 48
            height: 48

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 24
            }

            color: ui.ds3.bg.overlay
            radius: 24

            DS3.Icon {
                anchors.centerIn: parent

                source: "qrc:/resources/images/Athena/common_icons/ChevronLeft-M.svg"
                color: ui.ds3.figure.base
            }
        }

        Rectangle {
            width: 48
            height: 48

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 24
            }

            color: ui.ds3.bg.overlay
            radius: 24

            DS3.Icon {
                anchors.centerIn: parent

                source: "qrc:/resources/images/Athena/common_icons/ChevronRight-M.svg"
                color: ui.ds3.figure.base
            }
        }

        DS3.MouseArea {
            width: 96
            height: parent.height

            anchors {
                fill: undefined
                left: parent.left
            }

            onClicked: goPrev()
        }

        DS3.MouseArea {
            width: 96
            height: parent.height

            anchors {
                fill: undefined
                right: parent.right
            }

            onClicked: goNext()
        }

        Rectangle {
            width: 40
            height: 40

            anchors {
                right: parent.right
                top: parent.top
                margins: 24
            }

            color: ui.ds3.bg.overlay
            radius: 20

            DS3.Icon {
                anchors.centerIn: parent

                source: "qrc:/resources/images/Athena/common_icons/Download-S.svg"
                color: ui.ds3.figure.base
            }

            DS3.MouseArea {
                onClicked: download()
            }
        }
    }
}