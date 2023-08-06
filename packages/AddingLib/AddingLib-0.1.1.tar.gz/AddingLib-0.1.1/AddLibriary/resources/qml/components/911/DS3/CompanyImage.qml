import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


// Image that automatically resizes image
Rectangle {
    id: mask

//  Name of the company. With this name the letter alias will be generated automatically
    property string name: "A"
//  Source of the company image. If it does not exist, the generated image will be shown
    property alias source: image.source

    width: 40
    height: visible ? 40 : 0

    radius: 4
    color: ui.ds3.figure.transparent

    Rectangle {
        id: defaultImage

        anchors.fill: parent

        visible: image.status != Image.Ready
        color: ui.ds3.bg.high
        radius: parent.radius

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
            visible: !loadingSpinner.visible
        }

        DS3.Spinner {
            id: loadingSpinner

            anchors.centerIn: parent

            visible: image.status == Image.Loading
        }
    }

    DS3.Image {
        id: image

        anchors.fill: parent

        fillMode: Image.PreserveAspectCrop
        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
    }

    Rectangle {
        id: circle

        anchors.fill: image

        radius: 4
        visible: false
    }
}
